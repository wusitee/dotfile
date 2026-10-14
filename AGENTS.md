# AGENTS.md

## Scope and instruction layout

This is the canonical repository-wide policy for agents maintaining this
personal dotfiles repository. `CLAUDE.md` remains a compatibility entry point
that directs Claude Code here; do not duplicate this policy there.

Read `doom/AGENTS.md` before Doom work. Read relevant repo-local skill
instructions when using those skills. Preserve existing Claude tooling and
configuration unless the task explicitly changes them.

Keep this policy focused on durable maintenance rules. Application inventories,
themes, keybindings, hardware details, deployment mappings, and usage belong in
system documentation or the relevant configuration. Do not turn task-specific
choices into standing rules without explicit authorization.

## Working approach

Before editing, inspect `git status --short`, the diff for target files, and
relevant source, documentation, and live configuration. Preserve existing edits
and untracked files; do not reset, overwrite, stage, or clean unrelated work.

State material assumptions. Resolve routine implementation choices from the
repository and task context. Ask when ambiguity changes scope, intended
behavior, or whether a conflicting file may be replaced.

For multi-step work, give a short plan with verifiable outcomes. Make the
smallest complete change, match existing style, and avoid speculative features,
unrelated refactoring, formatting, or cleanup.

## Repository hygiene

Use Git-ignored `tmp/` for drafts, plans, work logs, experiments, temporary
reproductions, and one-off validation artifacts. Create it only when needed.
Maintained configuration, scripts, tests, documentation, and workflows must not
depend on it. Do not relocate existing content to impose a new directory layout.

Changes intended for Git must be complete, maintainable, and validated. Keep
generated output, application state, credentials, backups, reject files, and
bundled third-party code separate from configuration sources. Do not remove
existing snapshots or state merely because they are already tracked.

This repository intentionally maintains personal and machine-specific dotfiles.
Keep settings that are part of the requested setup in their appropriate tracked
configuration. Keep agent-only local preferences and secrets in ignored,
tool-supported local configuration or external credential storage. Do not add
credentials to the repository; retain Emacs `auth-source` integration.

## Source and deployment

There is no repository-wide installer or Stow manifest. `docs/computer.org`
records deployment relationships, but its dated inventory must be checked
against the current machine before use.

Identify both the repository source and live destination. Inspect destinations
with `ls -ld` and `readlink -f`; compare independent files before copying or
linking them. An edit through a deployed symlink can immediately change the live
configuration. Preserve independent live edits and existing link arrangements.
Use relative targets for new symlinks where practical.

Deploy only the intended files within the task's authorized scope. Do not
bulk-copy directories or overwrite a conflicting destination without resolving
its contents and replacement authorization. Preserve unrelated provider settings,
plugins, runtime state, and user data.

Respect these source boundaries:

- Doom: edit `doom/config.org`; tangle to the ignored `doom/config.el`.
  Follow `doom/AGENTS.md` for module, package, Org-stack, and validation work.
- Fish: place new functions in `fish/functions/`. Do not overwrite live
  universal variables when deploying a function or `config.fish`.
- Rime: manage `rime/default.custom.yaml` as a single-file customization;
  preserve generated dictionaries and user data. Compare the older Fcitx5
  snapshot before deploying it over a live profile.
- Vim: manage `vim/vimrc`; preserve the live plugin and runtime directories.
- systemd: manage user units individually. Keep the lid and idle hold services
  on demand; do not enable them at login as routine deployment.
- External integrations: verify referenced executables and settings; changes to
  dotfiles do not authorize modifying the external application's implementation.

## Documentation

Project documentation language is English, following `docs/computer.org`. This
setting does not require translating policy files, source, identifiers,
comments, commit messages, logs, or existing content outside the task.

Keep durable system documentation in `docs/`. Start with `docs/computer.org`
as the main system guide; add focused pages only when the content benefits from
separation. Preserve Org format unless a format change is requested. Create
documentation files and directories only when there is maintained content.

Keep one canonical copy of each guide. Update references and relative links
when moving documentation. Retain component READMEs and scoped agent policies
in place unless their relocation is part of the task. Keep task briefs,
implementation plans, and work logs in `tmp/`.

Review documentation impact with each change. Update setup, dependencies,
deployment, usage, troubleshooting, or reload instructions when they become
inaccurate or insufficient. Describe the current system, not the request or work
history. Leave accurate documentation unchanged; restoring documented behavior
alone does not require a documentation edit.

If a root README is added or changed, prioritize first-time understanding and
setup, and link to `docs/` from a dedicated documentation section. Include
necessary documentation changes with the implementation in the same commit.

## Tests and validation

There is no unified build or test suite. Use existing component-specific checks
and any applicable scoped instructions. Keep maintained regression tests in the
relevant component, respecting existing or framework-required layouts; do not
create a root test directory solely to satisfy this policy.

Add or extend tests only to cover meaningful behavior or a concrete regression
gap. Keep one-off reproductions in `tmp/`. Within the affected test area,
consolidate redundant cases when justified while preserving distinct failure
modes; do not weaken or skip tests to hide failures.

Run the checks relevant to changed files:

- Fish: `fish -n <file.fish>`.
- Lua: `luac -p <file.lua>`; syntax checks do not validate application APIs.
- Shell: `sh -n <file.sh>` or `bash -n <file.sh>`, matching the shebang.
- systemd user units: `systemd-analyze --user verify <file.service>`.
- TOML / JSON: parse with Python `tomllib` / `json`; use a comment-aware parser
  for JSONC such as Waybar's configuration.
- Doom: follow tangling, Lisp, sync, and behavior checks in `doom/AGENTS.md`.
- Vim: use the existing noninteractive check in `docs/computer.org`, followed by
  terminal behavior verification when affected.
- Documentation: verify referenced files and commands.

For deployed changes, apply the relevant reload or restart from
`docs/computer.org` and verify affected behavior. Static checks alone do not
establish runtime correctness. Do not execute startup hooks, power-management
scripts, or suspend actions merely as syntax checks. Documentation-only edits
need no service reload.

Run mandated checks and the minimum targeted validation needed for concrete
risks. Reuse still-valid results; repeat or broaden checks only for failures,
uncovered risks, or subsequent changes that invalidate them.

## GitHub Flow

For repository updates, create a focused branch from the default branch rather
than committing directly to it. Preserve pending work when preparing the branch.
Use signed, scoped commits and keep related implementation and documentation
together. Push the branch and open a pull request describing the resulting
behavior, validation, and any unresolved limitations.

For user-requested repository changes, completion includes an independent
subagent review. Address actionable findings on the same branch and obtain
review of the final changes. Once review is clear and required checks pass,
merge the pull request without asking for another confirmation. Respect any
request to stop at a draft, review, or unmerged pull request, and do not bypass
GitHub protections. Do not force-push or delete branches unless authorized.

## Completion and commits

Review the scoped diff and run `git diff --check`. Ensure intended changes are
complete, affected documentation is current, and no temporary artifacts or
dependencies on `tmp/` enter Git. Report what changed, what was verified, and
any unresolved failures, unavailable checks, or pending deployment/reload steps.

Stage only explicit intended paths. Use GPG-signed
Conventional Commits: `feat`, `fix`, or `docs`, with a relevant component scope
such as `doom`, `hyprland`, `fish`, or `computer`. Never bypass signing with
`--no-gpg-sign`; if signing fails, ask the user to fix their GPG agent or password
manager.

## Policy changes

Modify this policy or its compatibility entry point only when explicitly
requested. Documentation language settings and broad editing or translation
requests do not authorize policy changes. Prefer revising or removing redundant
rules over accumulating instructions.

When installing a replacement policy, first present its concrete diff and the
disposition of existing project-specific rules. Obtain explicit approval before
replacing a conflicting file or link unless that replacement was already
authorized. Preserve the canonical `AGENTS.md` / `CLAUDE.md` redirect arrangement
and scoped guidance unless a layout change is requested. Verify references and
ignore rules, then tell the user to start a new agent session to load the policy.
