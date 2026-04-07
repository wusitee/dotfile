# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal dotfiles repository for Arch Linux with Hyprland (Wayland compositor). It contains configuration files for the user's daily computing environment on a Huawei MateBook X Pro 2021.

## Key Technologies

- **Window Manager**: Hyprland (primary), with fallback configs for Sway and i3
- **Terminal**: Ghostty (primary), Alacritty (secondary)
- **Editors**: Doom Emacs (primary), Neovim (secondary)
- **Shell**: Fish (primary), with Nushell and PowerShell configs
- **Status Bar**: Waybar
- **Launcher**: Rofi
- **File Manager**: Yazi (terminal), with shell integration
- **Notification Center**: Swaync

## Configuration Reload Commands

Since this is a dotfiles repo, there are no build/test commands. Instead, use these to apply changes:

- **Hyprland**: `hyprctl reload` (or the config auto-reloads on save)
- **Doom Emacs**: `doom sync` (after modifying `init.el` or `packages.el`)
- **Fish**: `source config.fish`
- **Waybar**: `killall waybar && waybar` (restarts the bar)

## Directory Structure

```
├── hypr/              # Hyprland WM configuration
│   ├── hyprland.conf  # Main config (defines $terminal, $fileManager, $menu)
│   ├── hypridle.conf  # Idle management (lock/suspend)
│   └── hyprlock.conf  # Screen lock config
├── doom/              # Doom Emacs configuration
│   ├── config.org     # Main config in org-mode (literate programming style)
│   ├── init.el        # Doom module selection
│   └── packages.el    # Custom packages
├── nvim/              # Neovim configuration (lazy.nvim based)
├── fish/              # Fish shell configuration
├── ghostty/           # Ghostty terminal config
├── waybar/            # Status bar configuration
├── rofi/              # Application launcher config
├── yazi/              # Terminal file manager config
├── starship/          # Cross-shell prompt config
├── fcitx5/            # Input method (Chinese/Japanese) with Rime
├── swaync/            # Notification center config
└── computer.org       # Main system documentation (system setup, packages)
```

## Important Configuration Details

### Hyprland
- Monitor scale is set to 2 (high DPI)
- Autostart programs defined in `hyprland.conf`: waybar, nm-applet, matebook-applet, fcitx5, copyq, awww-daemon, hypridle, swaync, gammastep, onedrive
- Environment variables for Qt theming and fcitx input method

### Doom Emacs
- Configuration is in `config.org` using literate programming (org-babel)
- Theme: `doom-horizon`
- Font: Maple Mono Normal NF CN (size 15)
- Transparency: 90% alpha background
- AI integration via gptel with Gemini 2.5 Pro
- Org-mode from Tecosaur's dev branch

### Fish Shell
- Uses zoxide for autojumping (`z` command)
- Starship prompt
- Yazi integration via `y` function (changes cwd after exiting yazi)
- Fastfetch alias (`ff`)

## Hardware-Specific Configuration

This setup is tailored for a **Huawei MateBook X Pro 2021**:
- Battery threshold restoration after suspend (see `dotfiles-huawei-wmi/`)
- Sound firmware fixes documented in `computer.org`
- Uses `matebook-applet` for battery threshold control

## System Documentation

The `computer.org` file contains the main system documentation including:
- Package installation commands (Arch Linux / AUR)
- System setup (firewall, input method, sound fixes)
- Application-specific configuration notes
- Firefox CSS for hiding horizontal tabs

## Creating Commits

Follow the conventional commit format used in this repo:

```
<type>(<scope>): <description>

- Details about what changed
- Why it changed

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** `feat` (new feature), `fix` (bug fix), `docs` (documentation)
**Scopes:** `doom`, `hyprland`, `fish`, `ghostty`, `yazi`, etc.

**Example workflow:**
```bash
# Check what changed
git status
git diff

# Stage related files together
git add fish/config.fish fish/functions/

# Commit with proper message
git commit -m "fix(fish): move ff function to proper location

- Move ff function from config.fish to fish/functions/ff.fish
- Fix fastfetch config path to use absolute path

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**GPG Signing:**
This repository requires GPG-signed commits. If GPG signing times out with "gpg: signing failed: Timeout", **ask the user to set up their password manager or GPG agent** instead of using `--no-gpg-sign`. Do not bypass commit signing.

## Notes for AI Assistants

- When editing Doom Emacs config, modify `config.org` (not the tangled `config.el` which is gitignored)
- Hyprland config uses `$variable` syntax for defining reusable values
- Fish functions should be in separate files under `fish/functions/` (not in `config.fish`)
- Many configs use the Nord color theme
