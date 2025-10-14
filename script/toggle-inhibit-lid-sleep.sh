#!/bin/sh

# This script toggles the inhibit-lid-sleep.service on and off.

SERVICE_NAME="inhibit-lid-sleep.service"

if systemctl --user is-active --quiet ${SERVICE_NAME}; then
    # If the service is active, stop it
    systemctl --user stop ${SERVICE_NAME}
    notify-send "Toggled Lid Sleep Inhibition" "${SERVICE_NAME} stopped. The lid will now cause sleep."
else
    # If the service is inactive, start it
    systemctl --user start ${SERVICE_NAME}
    notify-send "Toggled Lid Sleep Inhibition" "${SERVICE_NAME} started. The lid will no longer cause sleep."
fi
