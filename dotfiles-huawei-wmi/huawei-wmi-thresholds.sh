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
        if ! saved=$(cat "$PERSIST_FILE" 2>/dev/null); then
            logger -p user.err "Huawei-WMI: Cannot read saved thresholds from $PERSIST_FILE"
            exit 1
        fi
        if [[ ! $saved =~ ^([0-9]{1,3})[[:blank:]]+([0-9]{1,3})[[:blank:]]*$ ]]; then
            logger -p user.err "Huawei-WMI: Invalid saved thresholds in $PERSIST_FILE"
            exit 1
        fi
        start=$((10#${BASH_REMATCH[1]}))
        end=$((10#${BASH_REMATCH[2]}))
        if (( start > end || end > 100 )); then
            logger -p user.err "Huawei-WMI: Invalid threshold range: $start $end"
            exit 1
        fi

        # Wait for the EC, then allow delayed resets to settle before read-back.
        sleep 2
        actual="unavailable"
        for i in 1 2 3 4 5; do
            if ! { [ -e "$PLATFORM_SYSFS" ] && printf '%s %s\n' "$start" "$end" > "$PLATFORM_SYSFS"; } 2>/dev/null; then
                sleep 1
                continue
            fi
            sleep 1
            if actual=$(cat "$PLATFORM_SYSFS" 2>/dev/null) && [[ $actual == "$start $end" ]]; then
                logger "Huawei-WMI: Verified battery thresholds $start $end (attempt $i)"
                exit 0
            fi
        done
        logger -p user.err "Huawei-WMI: Failed to restore thresholds $start $end after 5 attempts (last read: $actual)"
        exit 1
        ;;
esac
