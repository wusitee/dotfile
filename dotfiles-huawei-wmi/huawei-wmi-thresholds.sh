#!/bin/bash
# Restore Huawei battery thresholds after suspend/resume
# This script should be installed to /usr/lib/systemd/system-sleep/

PERSIST_FILE="/etc/default/huawei-wmi/charge_control_thresholds"
PLATFORM_SYSFS="/sys/devices/platform/huawei-wmi/charge_control_thresholds"

case $1 in
    pre)
        # Nothing to do before sleep
        ;;
    post)
        # Restore battery thresholds after resume
        # Wait for EC to be ready
        sleep 2

        if [ -f "$PERSIST_FILE" ]; then
            read -r start end < "$PERSIST_FILE"
            # Try multiple times with delays
            for i in 1 2 3; do
                if echo "$start $end" > "$PLATFORM_SYSFS" 2>/dev/null; then
                    logger "Huawei-WMI: Restored battery thresholds to $start $end (attempt $i)"
                    exit 0
                fi
                sleep 1
            done
            logger "Huawei-WMI: Failed to restore thresholds after 3 attempts"
        fi
        ;;
esac
