#!/bin/bash
set -e

if ! pgrep clash-verge >/dev/null; then echo "Launching clash-verge..." && swaymsg "exec /usr/bin/firefox"; fi
if ! pgrep firefox >/dev/null; then echo "Launching firefox..." swaymsg "exec /usr/bin/firefox"; fi
# if ! pgrep joplin >/dev/null; then echo "Launching joplin..." && swaymsg "exec $HOME/.local/scripts/xjoplin"; fi
# if ! pgrep btm >/dev/null; then echo "Launching bottom..." && swaymsg 'exec alacritty -t "Bottom" -e "/usr/bin/btm"'; fi
# if ! pgrep bandwhich >/dev/null; then echo "Launching bandwhich..." && swaymsg 'exec alacritty -t "Bandwhich" -e "/usr/bin/bandwhich"'; fi
# if [[ ! $(ps aux | grep io.elementary.music >/dev/null) ]]; then echo "Launching music player..." && swaymsg "exec io.elementary.music"; fi
