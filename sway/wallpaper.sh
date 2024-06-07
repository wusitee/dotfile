#!/usr/bin/env sh

wallpaper_path = ~/Pictures/wallpaper/$(ls ~/Pictures/wallpaper/ | wofi)

swww img $wallpaper_path
