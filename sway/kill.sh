#!/usr/bin/env sh

PID=$(swaymsg -t get_tree | jq -r '..|try select(.focused == true).pid')
kill -9 $PID
