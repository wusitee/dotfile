"""Exercise the resume hook without touching hardware or the system journal."""

from pathlib import Path
import os
import shlex
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "huawei-wmi-thresholds.sh"
TMP = Path(__file__).resolve().parents[2] / "tmp"


class ThresholdHookTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix="threshold-test-", dir=TMP)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.saved = self.root / "saved"
        self.control = self.root / "control"
        self.saved.write_text("70 90\n")
        self.control.write_text("0 100\n")
        self.script = SCRIPT.read_text().replace(
            "/etc/default/huawei-wmi/charge_control_thresholds", str(self.saved)
        ).replace(
            "/sys/devices/platform/huawei-wmi/charge_control_thresholds", str(self.control)
        )

    def run_hook(self, action="post", delay_action=""):
        # Override only timing and logging. Writes and reads use temporary files.
        wrapper = '''
            ticks=0
            sleep() {
                ticks=$((ticks + 1))
                %s
                :
            }
            logger() { printf '%%s\\n' "$*"; }
        ''' % delay_action
        return subprocess.run(
            ["bash", "-c", wrapper + self.script, "threshold-test", action],
            capture_output=True, text=True, timeout=5,
        )

    def test_restores_and_verifies(self):
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Verified battery thresholds 70 90 (attempt 1)", result.stdout)
        self.assertEqual(self.control.read_text(), "70 90\n")

    def test_accepts_missing_final_newline_and_normalizes_numbers(self):
        self.saved.write_text("070\t090")
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.control.read_text(), "70 90\n")

    def test_retries_when_firmware_resets_after_write(self):
        result = self.run_hook(delay_action='''
            if [ "$ticks" -eq 2 ]; then
                printf '0 100\\n' > "$PLATFORM_SYSFS"
            fi
        ''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("attempt 2", result.stdout)

    def test_fails_when_readback_never_matches(self):
        result = self.run_hook(delay_action='''
            printf '0 100\\n' > "$PLATFORM_SYSFS"
        ''')
        self.assertEqual(result.returncode, 1)
        self.assertIn("after 5 attempts (last read: 0 100)", result.stdout)
        self.assertNotIn("Verified", result.stdout)

    def test_retries_when_interface_appears_late(self):
        self.control.unlink()
        result = self.run_hook(delay_action='''
            if [ "$ticks" -eq 2 ]; then
                printf '0 100\\n' > "$PLATFORM_SYSFS"
            fi
        ''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("attempt 2", result.stdout)

    def test_failed_writes_return_failure(self):
        self.control.unlink()
        self.control.mkdir()
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Failed to restore", result.stdout)
        self.assertNotIn("Verified", result.stdout)

    def test_missing_saved_file_is_reported(self):
        self.saved.unlink()
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Cannot read saved thresholds", result.stdout)
        self.assertEqual(self.control.read_text(), "0 100\n")

    def test_invalid_settings_never_write(self):
        for saved in ("", "70", "70 90 extra", "-1 90", "90 70", "70 101", "x 90", "70 90\n0 100"):
            with self.subTest(saved=saved):
                self.saved.write_text(saved)
                result = self.run_hook()
                self.assertEqual(result.returncode, 1)
                self.assertIn("Invalid", result.stdout)
                self.assertEqual(self.control.read_text(), "0 100\n")

    def test_pre_does_not_change_thresholds(self):
        self.saved.unlink()
        result = self.run_hook(action="pre")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.control.read_text(), "0 100\n")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix="threshold-install-test-", dir=TMP)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.hook = self.root / "system-sleep" / "huawei-wmi-thresholds"
        self.hook.parent.mkdir()
        self.dropin = self.root / "tlp.d" / "99-huawei-wmi.conf"
        self.config = self.root / "effective-config"
        self.config.write_text('NATACPI_ENABLE="0"\nTLP_ENABLE="1"\n')
        self.reloaded = self.root / "reloaded"
        # Keep all destinations local and bypass only the root identity check.
        installer = (SCRIPT.parent / "install.sh").read_text().replace(
            '[ "$EUID" -ne 0 ]', 'false'
        ).replace(
            '/usr/lib/systemd/system-sleep/${SCRIPT_NAME}', str(self.hook)
        ).replace('/etc/tlp.d/99-huawei-wmi.conf', str(self.dropin))
        self.installer = self.root / "install.sh"
        self.installer.write_text(installer)
        for name in ("huawei-wmi-thresholds.sh", "99-huawei-wmi.conf"):
            (self.root / name).write_text((SCRIPT.parent / name).read_text())
        self.write_tool("tlp-stat", f"cat {shlex.quote(str(self.config))}")
        self.write_tool("tlp", f"touch {shlex.quote(str(self.reloaded))}")

    def write_tool(self, name, command):
        tool = self.bin / name
        tool.write_text("#!/bin/sh\n" + command + "\n")
        tool.chmod(0o755)

    def run_installer(self):
        return subprocess.run(
            ["bash", str(self.installer)], capture_output=True, text=True, timeout=5,
            env=dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}"),
        )

    def test_installs_hook_and_reloads_enabled_tlp(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.hook.read_text(), SCRIPT.read_text())
        self.assertTrue(self.hook.stat().st_mode & 0o111)
        self.assertEqual(self.dropin.read_text(), (SCRIPT.parent / "99-huawei-wmi.conf").read_text())
        self.assertTrue(self.reloaded.exists())

    def test_disabled_tlp_does_not_block_hook_installation(self):
        self.config.write_text('NATACPI_ENABLE="0"\nTLP_ENABLE="0"\n')
        self.write_tool("tlp", "exit 1")
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.hook.exists())

    def test_preserves_conflicting_dropin(self):
        self.dropin.parent.mkdir()
        self.dropin.write_text("# independent configuration\n")
        result = self.run_installer()
        self.assertEqual(result.returncode, 1)
        self.assertIn("different contents", result.stdout)
        self.assertEqual(self.dropin.read_text(), "# independent configuration\n")
        self.assertFalse(self.reloaded.exists())

    def test_rejects_effective_tlp_override(self):
        self.config.write_text('NATACPI_ENABLE="1"\nTLP_ENABLE="1"\n')
        result = self.run_installer()
        self.assertEqual(result.returncode, 1)
        self.assertIn("TLP overrides", result.stdout)
        self.assertFalse(self.hook.exists())
        self.assertFalse(self.reloaded.exists())


if __name__ == "__main__":
    unittest.main()
