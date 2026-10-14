#!/bin/sh

# Rofi window switcher that focuses through Hyprland's focus dispatcher.
# `rofi -show window` activates via foreign-toplevel, which the scrolling
# layout treats as a soft focus on other workspaces and does not scroll to.

# Earlier directories win, so user overrides beat system entries.
app_dirs="$HOME/.local/share/applications /usr/share/applications /var/lib/flatpak/exports/share/applications"
cache="${XDG_CACHE_HOME:-$HOME/.cache}/hypr-window-switcher-icons.json"

# Rebuild the class -> icon map only when an applications dir changed.
stale=
[ -f "$cache" ] || stale=1
for dir in $app_dirs; do
    [ -d "$dir" ] && [ "$dir" -nt "$cache" ] && stale=1
done

if [ -n "$stale" ]; then
    set --
    for dir in $app_dirs; do
        for file in "$dir"/*.desktop; do
            # Unmatched globs stay literal; awk aborts on missing files.
            [ -f "$file" ] && set -- "$@" "$file"
        done
    done
    mkdir -p "$(dirname "$cache")"
    # Map both the desktop id and StartupWMClass (lowercased) to Icon=.
    awk '
        function save() {
            if (icon == "") return
            if (!(tolower(id) in icons)) icons[tolower(id)] = icon
            if (wm != "" && !(tolower(wm) in icons)) icons[tolower(wm)] = icon
        }
        FNR == 1 {
            if (id != "") save()
            id = FILENAME; sub(/.*\//, "", id); sub(/\.desktop$/, "", id)
            wm = ""; icon = ""; entry = 0
        }
        /^\[/ { if (entry) nextfile; entry = ($0 == "[Desktop Entry]"); next }
        entry && /^Icon=/ && icon == "" { icon = substr($0, 6) }
        entry && /^StartupWMClass=/ && wm == "" { wm = substr($0, 16) }
        END { if (id != "") save(); for (k in icons) print k "\t" icons[k] }
    ' "$@" |
        jq -Rn '[inputs | split("\t") | {(.[0]): .[1]}] | add // {}' >"$cache.tmp" &&
        mv "$cache.tmp" "$cache"
fi

selection=$(
    hyprctl clients -j |
        jq -r --slurpfile icons "$cache" '
            ($icons[0] // {}) as $map
            | sort_by(.focusHistoryID) | .[]
            | select(.mapped and .address != "")
            | (.class | ascii_downcase) as $key
            | "\(.address)\t[\(.workspace.name)] \(.class)  \(.title)\u0000icon\u001f\($map[$key] // $key)"' |
        rofi -dmenu -i -show-icons -p window -display-columns 2 -display-column-separator '\t'
) || exit 0

address=$(printf '%s' "$selection" | cut -f1)
case "$address" in
0x*) ;;
*) exit 1 ;;
esac

hyprctl dispatch "hl.dsp.focus({ window = \"address:$address\" })" >/dev/null
