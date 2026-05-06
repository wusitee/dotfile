# AGENTS.md

This file is the canonical guidance for AI coding agents working in this repository.
`CLAUDE.md` and `.claude/` are part of the repo history and tooling, but this file
should be treated as the primary source of truth for repo-specific instructions.

## Project Overview

This is a personal dotfiles repository for a daily Arch Linux environment on a
Huawei MateBook X Pro 2021. It contains configuration files, shell scripts, and
system documentation for the user's desktop setup. Claude Code has been used to
manage this repo and the surrounding configuration, so keep existing Claude-era
conventions in mind instead of flattening them away.

The repository is hosted at `git@github.com:wusitee/dotfile.git`.

## Technology Stack

- Operating System: Arch Linux
- Window Manager / Compositor: Hyprland primary, with Sway and i3 fallbacks
- Terminal Emulator: Ghostty primary, Alacritty secondary
- Text Editors: Doom Emacs primary, Neovim secondary
- Shell: Fish primary, with Nushell and PowerShell profiles
- Status Bar: Waybar
- Application Launcher: Rofi
- File Manager: Yazi
- Notification Center: Swaync
- Screen Lock / Idle: Hyprlock + Hypridle
- Wallpaper Daemon: awww
- Input Method: Fcitx5 + Pinyin
- Prompt: Starship
- Clipboard Manager: CopyQ
- Desktop Theming: GTK 3/4 settings, Qt via `qt6ct`

## Repository Structure

```
├── hypr/                    # Hyprland configuration
│   ├── hyprland.conf        # Main compositor config
│   ├── hypridle.conf        # Idle management (lock / dpms off / suspend)
│   ├── hyprlock.conf        # Screen lock UI config
│   └── hyprland_without_hy3.conf  # Fallback config without hy3
├── doom/                    # Doom Emacs configuration
│   ├── config.org           # Primary literate config (edit this)
│   ├── config.el            # Tangled output (do not edit directly)
│   ├── init.el              # Doom module selection
│   └── packages.el          # Third-party package declarations
├── nvim/                    # Neovim configuration
│   ├── init.lua
│   └── lua/
│       ├── config/lazy.lua
│       └── plugins/which-key.lua
├── fish/                    # Fish shell configuration
│   ├── config.fish
│   └── functions/
├── ghostty/                 # Ghostty terminal config
│   ├── config
│   └── keybinds
├── alacritty/               # Alacritty configs
│   ├── alacritty.toml
│   └── alacritty.yml
├── waybar/                  # Status bar config + style
├── rofi/                    # Launcher config + themes
├── yazi/                    # File manager config, plugins, package manifest
├── starship/                # Prompt configuration
├── swaync/                  # Notification center config + style
├── fcitx5/                  # Input method config, profile, and module settings
├── gtk-3.0/                 # GTK 3 settings
├── gtk-4.0/                 # GTK 4 settings
├── script/                  # Custom utility scripts
├── dotfiles-huawei-wmi/     # Huawei battery threshold restore hook
├── computer.org             # System documentation and install notes
├── CLAUDE.md                # Legacy Claude Code guidance
└── .claude/                 # Claude Code local settings
```

## Editing Conventions

### Doom Emacs

- Always edit `doom/config.org`, not `doom/config.el`.
- `config.el` is tangled from `config.org` and is generated output.
- Run `doom sync` after changing `doom/init.el` or `doom/packages.el`.
- Current Doom config includes `chinese`, `japanese`, `corfu`, `vertico`, `doom`,
  `treemacs`, `evil`, `lsp`, `magit`, `pdf`, `org` with `+roam2 +pretty`, `python`,
  `rust`, `llm`, and related modules.
- The config currently carries AI-related setup for `gptel`, `claude-code-ide`,
  `claude-code-ide-extras`, `kimi-code-ide`, `copilot`, and `org-roam-ui`.
- The active editor theme is `doom-horizon`; the font is Maple Mono Normal NF CN
  at size 15 with alpha background 90.

### Fish Shell

- Add new functions as separate files under `fish/functions/`.
- `fish/config.fish` currently keeps shared shell init plus the inline `y`
  function for Yazi cwd integration.
- The standalone `ff` helper lives in `fish/functions/ff.fish`.

### Hyprland

- Config uses `$variable` syntax for reusable values.
- Monitor scale is `2` for the laptop panel.
- Autostart is declared with `exec-once` in `hyprland.conf`.
- Primary layout is `hy3`; `hyprland_without_hy3.conf` is the fallback.
- The config also uses `hyprexpo` and `hyprpm reload -n` at startup.
- Keybindings use `SUPER` as the main modifier.

### Neovim

- The Neovim setup is intentionally minimal.
- `nvim/lua/plugins/which-key.lua` currently holds the plugin specs.
- Active plugins include `tokyonight`, `which-key`, `neorg`, `nvim-cmp`,
  `treesj`, `dial.nvim`, `nvim-web-devicons`, `dressing.nvim`, and
  `vim-startuptime`.

### Ghostty

- Active config is `ghostty/config`.
- Font: `Maple Mono Normal NF CN` at size 13.
- Window decoration is disabled, theme is dark, and `focus-follows-mouse = true`.
- `ghostty/keybinds` defines the tab/split/window shortcuts.

### Alacritty

- `alacritty/alacritty.toml` is the active config.
- `alacritty/alacritty.yml` is a legacy config kept for reference.

### Waybar

- Height is 22px and the bar is positioned at the top.
- Left modules: `hyprland/workspaces`, `tray`.
- Center module: `clock`.
- Right modules: `pulseaudio`, `backlight`, `cpu`, `memory`, `battery`.
- Styling currently uses a Maple Mono NF font stack and a dark palette.

### Rofi

- Modes: `window`, `drun`, `ssh`, `combi`, `run`.
- Terminal: `ghostty`.
- Theme: `Arc-Dark`.

### Yazi

- Plugins live under `yazi/plugins/` and include `restore`, `clipboard`, and `ucp`.
- `yazi/package.toml` pins those plugin dependencies.
- Keymap binds `u` and `d u` to `plugin restore`, with an interactive `d U`
  variant.
- The opener uses `xdg-open` via `parallel`.

### Fcitx5

- Default group: `Default` with `keyboard-us` and `pinyin`.
- Trigger key: `Control+space`.
- Alternative trigger: `Shift_L`.
- Theme: `Nord-Dark`.

## Configuration Reload Commands

This repository has no build/test commands. Apply changes by reloading the
relevant service or restarting the app:

| Component | Reload Command |
| --- | --- |
| Hyprland | `hyprctl reload` |
| Doom Emacs | `doom sync` after `init.el` or `packages.el` changes |
| Fish | `source ~/.config/fish/config.fish` |
| Waybar | `killall waybar && waybar` |
| Swaync | `killall swaync && swaync` |
| Ghostty | Restart Ghostty |
| Yazi | Restart Yazi |

## Commit Guidelines

This repository requires GPG-signed commits. Do not bypass signing with
`--no-gpg-sign`; if signing fails, ask the user to check their GPG agent or
password manager.

Use Conventional Commits:

```text
<type>(<scope>): <description>

- Details about what changed
- Why it changed
```

Types: `feat`, `fix`, `docs`
Scopes: `doom`, `hyprland`, `fish`, `ghostty`, `yazi`, `waybar`, `nvim`,
`rofi`, `swaync`, `fcitx5`, `computer`, and similar.

## Hardware-Specific Notes

This setup is tailored for a Huawei MateBook X Pro 2021.

- `dotfiles-huawei-wmi/install.sh` installs the systemd-sleep hook to
  `/usr/lib/systemd/system-sleep/`.
- `dotfiles-huawei-wmi/huawei-wmi-thresholds.sh` restores battery thresholds
  after suspend/resume from `/etc/default/huawei-wmi/charge_control_thresholds`.
- `matebook-applet` runs at startup from `hyprland.conf`.
- `sof-firmware` is required; sound-after-suspend notes live in `computer.org`.

## System Documentation

`computer.org` is the main system documentation. It covers:

- Arch Linux and AUR package installation commands
- Firewall setup
- Desktop environment setup notes
- GTK, Qt, and app theming
- Firefox CSS tweaks
- Application-specific configuration
- Troubleshooting references
- Dotfiles management notes

Keep `computer.org` in sync when configuration directories are added, removed,
or materially changed.

## Security Considerations

- GPG signing is enforced for commits.
- API keys for AI integrations are stored through Emacs `auth-source` and are
  not present in this repository.
- The Huawei battery restore installer must be run with `sudo`.
- Custom scripts in `script/` interact with `systemd-inhibit` and
  `systemctl --user`; verify paths before editing.

## Notes for AI Assistants

- Prefer `cat` or shell reads for files with encoding quirks.
- The Neovim config is intentionally small; do not assume a full IDE setup.
- `CLAUDE.md` is legacy guidance, but the repo still carries Claude-specific
  tooling and settings.
- Avoid touching unrelated user changes.
- Keep directory-level documentation and the actual configs aligned.
