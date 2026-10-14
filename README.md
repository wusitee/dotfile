# Dotfiles

Personal configuration for an Arch Linux desktop, with Hyprland, Fish, Ghostty,
Doom Emacs, and supporting applications. The repository also preserves secondary
editor, terminal, and desktop configurations.

## Getting started

Clone the repository, then follow the [system setup guide](docs/computer.org) for
dependencies and component-specific deployment instructions.

There is no repository-wide installer. Some live configurations are symlinks;
others are independent files. Inspect existing destinations and compare their
contents before linking or copying configuration. The deployment inventory is
dated and should be checked against the current machine.

## Documentation

- [System setup and maintenance](docs/computer.org): installation, deployment,
  usage, validation, reload steps, and troubleshooting.
- [Agent policy](AGENTS.md): repository-wide maintenance and GitHub Flow rules.
- [Doom agent guidance](doom/AGENTS.md): literate configuration and Org-stack
  maintenance.

Use a focused branch and signed Conventional Commits for updates, then open a
pull request with relevant validation. Keep temporary work in Git-ignored `tmp/`.
