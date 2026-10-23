# Huawei-WMI Battery Threshold Fix

Restores battery charge thresholds after suspend/resume on Huawei laptops.

## Problem

On some Huawei laptops (including MateBook X Pro 2021), the battery charge
thresholds reset to 0-100 after suspend/resume. This script automatically
restores your saved thresholds after resume.

## Installation

```bash
sudo ./dotfiles-huawei-wmi/install.sh
```

Run this from the repository root. The installer copies the resume hook and,
when TLP is installed, installs `99-huawei-wmi.conf` into `/etc/tlp.d/` and runs
`tlp start` to reload it if TLP is enabled. This disables TLP's native battery control while
retaining its power-saving settings. The Huawei applet's saved thresholds
remain authoritative, including after resume and AC power changes.

The installer stops if the TLP drop-in already has different contents or if
another TLP configuration overrides `NATACPI_ENABLE=0`. Compare the conflicting
configuration before replacing it. `/etc/tlp.conf` overrides all drop-ins.

## Requirements

- huawei-wmi kernel driver installed
- matebook-applet or manual threshold configuration
- `/etc/default/huawei-wmi/charge_control_thresholds` should exist with your
  saved values: two integers from 0 to 100, with start no greater than end

## How It Works

The script is installed as a systemd-sleep hook that runs after resume:
1. Reads and validates `/etc/default/huawei-wmi/charge_control_thresholds`
2. Waits 2 seconds for the EC to be ready
3. Writes the saved values, waits 1 second, and reads them back
4. Retries failed writes or mismatched read-back, up to 5 attempts
5. Logs verified success or an error, and exits nonzero on failure

The hook does not change the saved setting. It runs only on resume; use
matebook-applet to change and save thresholds during normal use. Read-back
confirms the driver reports the requested values, but cannot guarantee that
firmware enforces them or that another controller does not change them later.

## Verification

After suspend/resume, check if thresholds were restored:

```bash
cat /etc/default/huawei-wmi/charge_control_thresholds
cat /sys/class/power_supply/BAT0/charge_control_start_threshold
cat /sys/class/power_supply/BAT0/charge_control_end_threshold

# Check logs
journalctl -b | grep Huawei-WMI

# When TLP is installed: expect NATACPI_ENABLE="0" and native control disabled
sudo tlp-stat -c | grep NATACPI_ENABLE
sudo tlp-stat -b
```

Compare the reported thresholds with the saved pair after resume and after
unplugging/reconnecting AC. A `Verified battery thresholds` message records
read-back at that time. A charge level already above the stop threshold need
not fall immediately: the limit prevents charging, rather than forcing discharge.

## Regression checks

From the repository root:

```bash
bash -n dotfiles-huawei-wmi/huawei-wmi-thresholds.sh dotfiles-huawei-wmi/install.sh
shellcheck dotfiles-huawei-wmi/*.sh
python -m unittest discover -s dotfiles-huawei-wmi/tests
```

The tests use temporary files and mocked delays/logging; they do not change
hardware settings or suspend the machine.

## Uninstall

```bash
sudo rm /usr/lib/systemd/system-sleep/huawei-wmi-thresholds
```

To return threshold management to TLP, also remove
`/etc/tlp.d/99-huawei-wmi.conf` and run `sudo tlp start`. This reapplies TLP's
configured thresholds, which may differ from the applet's saved pair.
