#!/bin/sh

case "${1:-}" in
    lid)
        service="inhibit-lid-sleep.service"
        title="Toggled Lid Sleep Inhibition"
        enabled="$service started. The lid will no longer cause sleep."
        disabled="$service stopped. The lid will now cause sleep."
        ;;
    idle)
        service="inhibit-idle.service"
        title="Toggled Idle Inhibition"
        enabled="$service started. Automatic locking, screen-off and idle suspend are now inhibited."
        disabled="$service stopped. Automatic locking, screen-off and idle suspend are now enabled."
        ;;
    *)
        echo "Usage: $0 lid|idle" >&2
        exit 1
        ;;
esac

# Serialize repeated shortcut presses for each hold.
exec 9>"${XDG_RUNTIME_DIR:?}/dotfile-inhibit-$1.lock"
flock 9 || exit 1

if systemctl --user is-active --quiet "$service"; then
    action="stop"
    message="$disabled"
else
    action="start"
    message="$enabled"
fi

if ! systemctl --user "$action" "$service"; then
    notify-send -u critical "$title" "Could not $action the hold. Check: journalctl --user -u $service" || true
    exit 1
fi

notify-send "$title" "$message" || true
