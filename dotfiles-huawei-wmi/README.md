# Huawei-WMI Battery Threshold Fix

Restores battery charge thresholds after suspend/resume on Huawei laptops.

## Problem

On some Huawei laptops (including MateBook X Pro 2021), the battery charge
thresholds reset to 0-100 after suspend/resume. This script automatically
restores your saved thresholds after resume.

## Installation

```bash
sudo ./install.sh
```

## Requirements

- huawei-wmi kernel driver installed
- matebook-applet or manual threshold configuration
- `/etc/default/huawei-wmi/charge_control_thresholds` should exist with your
  saved values

## How It Works

The script is installed as a systemd-sleep hook that runs after resume:
1. Waits 2 seconds for the EC to be ready
2. Reads saved thresholds from `/etc/default/huawei-wmi/charge_control_thresholds`
3. Restores them with retry logic (up to 3 attempts)
4. Logs success/failure to syslog

## Verification

After suspend/resume, check if thresholds were restored:

```bash
cat /sys/class/power_supply/BAT0/charge_control_start_threshold
cat /sys/class/power_supply/BAT0/charge_control_end_threshold

# Check logs
journalctl -b | grep Huawei-WMI
```

## Uninstall

```bash
sudo rm /usr/lib/systemd/system-sleep/huawei-wmi-thresholds
```
