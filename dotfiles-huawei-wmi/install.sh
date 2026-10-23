#!/bin/bash
# Install Huawei-WMI threshold restore fix

set -e

SCRIPT_NAME="huawei-wmi-thresholds"
SOURCE="$(dirname "$0")/${SCRIPT_NAME}.sh"
DEST="/usr/lib/systemd/system-sleep/${SCRIPT_NAME}"
TLP_SOURCE="$(dirname "$0")/99-huawei-wmi.conf"
TLP_DEST="/etc/tlp.d/99-huawei-wmi.conf"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo"
    exit 1
fi

# Check if source exists
if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found"
    exit 1
fi

# Prevent TLP's parallel resume hook from overwriting the applet's thresholds.
if command -v tlp >/dev/null 2>&1; then
    if [ -e "$TLP_DEST" ] && ! cmp -s "$TLP_SOURCE" "$TLP_DEST"; then
        echo "Error: $TLP_DEST already exists with different contents; compare it first."
        exit 1
    fi
    install -Dm644 "$TLP_SOURCE" "$TLP_DEST"
    tlp_config=$(tlp-stat -c)
    if ! grep -q 'NATACPI_ENABLE="0"' <<< "$tlp_config"; then
        echo "Error: TLP overrides NATACPI_ENABLE=0; check /etc/tlp.conf and /etc/tlp.d/."
        exit 1
    fi
    if grep -q 'TLP_ENABLE="1"' <<< "$tlp_config"; then
        tlp start
    fi
fi

# Install the script
echo "Installing $SCRIPT_NAME to $DEST..."
cp "$SOURCE" "$DEST"
chmod +x "$DEST"

echo "Installed successfully!"
echo ""
echo "To test: suspend and resume your laptop, then check:"
echo "  cat /sys/class/power_supply/BAT0/charge_control_start_threshold"
echo "  cat /sys/class/power_supply/BAT0/charge_control_end_threshold"
echo ""
echo "To verify it's working:"
echo "  journalctl -b | grep Huawei-WMI"
