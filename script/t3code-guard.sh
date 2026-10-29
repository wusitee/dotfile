#!/bin/sh
if ! /home/wste/dotfile/script/clash-network-check.fish; then
    if command -v notify-send >/dev/null 2>&1; then
        notify-send -u critical 'T3 Code blocked' 'Enable Clash TUN, Global mode and select a Taiwan node.'
    fi
    exit 1
fi
exec /usr/bin/t3code --password-store=gnome-libsecret "$@"
