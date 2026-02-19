#!/bin/bash
# Install Huawei-WMI threshold restore fix

set -e

SCRIPT_NAME="huawei-wmi-thresholds"
SOURCE="$(dirname "$0")/${SCRIPT_NAME}.sh"
DEST="/usr/lib/systemd/system-sleep/${SCRIPT_NAME}"

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
