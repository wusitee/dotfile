---
name: check-application-updates
description: Track installed versions of applications used by this dotfiles repository, check Arch/AUR and official upstream updates, review release notes for changes that intersect the current configuration, and persist actionable reminders. Use when asked to inventory current application versions, check for updates, assess whether an update breaks or changes dotfiles, initialize or refresh the application-update baseline, or resolve a saved update reminder.
---

# Check Application Updates

Track application versions without installing or upgrading anything. Persist the last observation, reviewed upstream range, and unresolved config-impact reminders in `.app-update-tracker.json`.

## Safety Boundaries

- Run read-only inventory and update-check commands only.
- Never run `pacman -Sy`, `pacman -Syu`, `yay -Syu`, `doom upgrade`, `hyprpm update`, `bob update`, or another mutating update command.
- Use `checkupdates` for official Arch updates and `yay -Qua` for AUR updates. Treat `checkupdates` exit code 2 as "no updates."
- Use `vercmp` for Arch package versions. Do not compare Arch versions as SemVer.
- Use official release notes, migration guides, repositories, or package pages. If the relevant notes cannot be retrieved, report the impact as `unknown`; do not claim that the config is unaffected.
- Never recommend a Hyprland update while an active hy3 compatibility gate is `blocked` or `unknown`.
- Do not claim background monitoring. This skill runs only when invoked; scheduled reminders require separate automation.

## Start Every Run

1. Work from the dotfiles repository root and read `AGENTS.md`.
2. Read `doom/AGENTS.md` before inspecting or changing Doom configuration.
3. Validate `.app-update-tracker.json` with `python -m json.tool`.
4. Run the local collector:

```bash
python .agents/skills/check-application-updates/scripts/collect_versions.py --pretty
```

5. Surface every reminder whose status is `open` before reporting new results.

The collector is local-only and must not modify the tracker. Treat missing applications, commands, or config paths as findings rather than collector failures.

## Initialize Or Refresh The Baseline

Use this flow when `observed` or `review.through` is null, or when explicitly asked to record current versions.

1. Collect current versions and config fingerprints.
2. Copy each collector result into the application's `observed` object and add the collector's `captured_at` value.
3. Set `review.through` to the current installed version, Git commit, or recorded TOML revision. This establishes a forward-looking baseline; do not invent a historical review.
4. Set top-level `last_snapshot_at` to the same timestamp.
5. Preserve every existing reminder and tracker definition.
6. Report installed, missing, and unreadable applications separately.

Edit the JSON with a structured parser or a focused patch. Validate it again after writing.

## Check For Updates

### 1. Compare Local State

- Compare the collector's normalized `installed.version` and config fingerprint with `observed`.
- Report a changed installed version, missing executable/package, changed config fingerprint, or tracker error before checking upstream.
- Do not overwrite the stored observation until the differences have been reported and the release range has been reviewed.

### 2. Find Candidates

- Run `checkupdates` and filter its output to every package candidate declared in a `pacman` tracker.
- Run `yay -Qua` and filter it the same way. Use `yay -Qua --devel` only when explicitly requested or when deliberately checking VCS packages.
- For `github-releases`, query the declared repository's official releases and tags. Prefer `gh api`; use the official GitHub page if needed.
- For `github-commits`, compare the stored commit with the declared repository's remote HEAD or branch using `git ls-remote` or the GitHub compare API.
- For `release-notes-url`, read the declared official page.
- For command-managed applications such as Neovim, use the tracker version plus the declared upstream source; do not assume the package-manager result covers it.
- For a Neovim nightly tracker, compare both upstream HEAD and the latest stable release. Prefer a fully reviewed stable release when unreleased HEAD changes intersect pinned plugins.

Request network approval when the environment requires it. Record an unavailable source as `unknown` and continue with other applications.

### 3. Gate Hyprland Updates On hy3

Run this gate before recommending each Hyprland target when the active config uses `layout = hy3`, loads hy3 through HyprPM, or contains an active `plugin { hy3 { ... } }` block.

1. Normalize the target Arch package version to the upstream release version, such as `0.55.4-1` to `0.55.4`.
2. Resolve the exact commit for the official Hyprland tag `v{version}`.
3. Read `hyprpm.toml` from the current default branch of `outfoxxed/hy3`.
4. For this HyprPM installation, require an exact `commit_pins` entry whose first value is the Hyprland release commit. Confirm that the mapped hy3 commit exists upstream.
5. Classify the gate:
   - `compatible`: the exact Hyprland commit has a valid hy3 pin.
   - `blocked`: the manifest is available but has no exact pin, or the mapped hy3 commit is missing.
   - `unknown`: the release commit or current manifest cannot be retrieved.
6. Treat a matching `hl{version}` tag as useful evidence for manual or Nix installations, but not as a substitute for the HyprPM commit pin used by this machine.
7. Do not use hy3 `master` or its `flake.lock` alone as proof for a tagged Hyprland release; hy3 documents that mismatched releases can fail to build or load.
8. Persist the result under `hy3.host_compatibility.last_check`. Create or update an `action-required` Hyprland reminder for `blocked` or `unknown` results.
9. Recheck an open compatibility gate on every run, even when `review.through` already contains the target version. Resolve its reminder only after official compatibility appears; keep post-update plugin reload/runtime validation as a separate reported step.

### 4. Review Config Impact

Review only the range after `review.through` through the newest candidate being considered.

1. Read release notes, migration guides, breaking-change notices, and relevant changelog entries for that range.
2. Extract removed or renamed config keys, syntax changes, changed defaults, command-line changes, plugin/API compatibility changes, and required migrations.
3. Search only the application's declared `config_paths` for the exact affected option, command, module, or behavior. Use `rg -n` and cite the current file and line.
4. Classify each result:
   - `action-required`: an exact configured feature is removed/renamed, an enabled integration is incompatible, or a safe validator fails.
   - `review`: release notes mention an exact configured feature but the required action is ambiguous or behavior-dependent.
   - `informational`: an update exists, but the reviewed notes contain no change that intersects the declared config.
   - `unknown`: the release range or relevant documentation could not be reviewed.
5. Keep fallback-only findings labeled as fallback; do not present them as active Hyprland failures.

Do not use `Hyprland --verify-config`: it may execute config commands and misdiagnose plugin dispatchers. When a live Hyprland session exists, `hyprctl configerrors` is the safe check. Other focused validators include:

```bash
ghostty +validate-config --config-file=ghostty/config
fish -n fish/config.fish fish/functions/*.fish
```

Run a validator only when it is read-only and appropriate for the affected application.

### 5. Persist Results

Add one reminder for each `action-required` or `review` result:

```json
{
  "id": "hyprland-v0.56.0-window-rule-change",
  "status": "open",
  "severity": "action-required",
  "introduced_in": "v0.56.0",
  "summary": "Window rule syntax changed.",
  "config_matches": ["hypr/hyprland.conf:402"],
  "source": "https://github.com/hyprwm/Hyprland/releases/tag/v0.56.0",
  "created_at": "2026-07-12T12:00:00+08:00"
}
```

- Reuse an existing reminder when application, introduced version, and issue match; do not duplicate it.
- Advance `review.through` only after the complete release range was actually reviewed. Open reminders may remain after advancing the reviewed range.
- When only part of a commit range is fully reviewable, advance `review.through` only to the last reviewed release or commit and leave the remaining range for the next check.
- Leave `review.through` unchanged for an `unknown` range.
- After reporting and review, replace `observed` with the current collector result and update `last_snapshot_at`.
- Preserve resolved and dismissed reminders as history.
- Validate the tracker JSON after every edit.

## Resolve A Reminder

1. Locate the reminder by ID and show its source and config matches.
2. Fix the config only when requested, following repository instructions and application-specific reload rules.
3. Run an appropriate read-only validator or syntax check.
4. Set `status` to `resolved`, add `resolved_at`, and summarize the resolution. Set `status` to `dismissed` only on explicit user direction.
5. Keep the reminder in the tracker and report any validation that could not be run.

## Report Format

Keep the result concise and ordered as follows:

1. Open reminders.
2. Updates with `action-required` or `review` impact, including source and config line.
3. `unknown` checks that need another pass.
4. Informational updates.
5. Installed-version or config-fingerprint changes since the previous snapshot.

When there are no actionable findings, say so explicitly and state which update sources or validators were unavailable.

## Registry Maintenance

Edit `.app-update-tracker.json` when an actively configured application is added, removed, renamed, or changes installation method. Keep inactive i3, Sway, and Alacritty configs out of the active registry unless the user re-enables them. Track exact config files rather than broad directories when practical so fingerprints and release-note searches remain relevant.
