# CLAUDE.md

This repository keeps shared agent instructions in `AGENTS.md`.

Claude Code should read and follow `AGENTS.md` first. Treat this file as a
compatibility entry point for Claude Code, not a second source of truth.

Important reminders for Claude Code:

- Do not duplicate repo guidance here; update `AGENTS.md` instead.
- Keep `computer.org` in sync when configuration directories are added, removed,
  or materially changed.
- Commits must remain GPG-signed. If signing fails, ask the user to fix their
  GPG agent or password manager instead of using `--no-gpg-sign`.
- Existing Claude Code tooling and history are intentional; do not remove
  `.claude/` or Claude-related Doom Emacs packages unless the user asks.
