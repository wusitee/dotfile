#!/usr/bin/env bash

i3lock

sleep 10

if ! pgrep -x "Xorg" > /dev/null; then
    systemctl suspend
fi
