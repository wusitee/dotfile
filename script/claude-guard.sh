#!/bin/sh
/home/wste/dotfile/script/clash-network-check.fish || exit 1
exec /home/wste/.local/bin/claude "$@"
