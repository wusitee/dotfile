# Doom Emacs Maintenance Instructions

Use this file only for Doom Emacs work in `/home/wste/dotfile/doom/`.
For non-Emacs dotfile tasks, use the repo root guidance instead.

## Scope

- Primary config: `doom/config.org`.
- Module selection: `doom/init.el`.
- Package declarations: `doom/packages.el`.
- Generated output: `doom/config.el`, tangled from `config.org`.
- System notes: update `../computer.org` when a Doom change materially affects
  setup, usage, troubleshooting, or reload steps.

## Working Rules

- Edit `config.org`, not `config.el`.
- Tangle after changing `config.org` so the local generated file stays usable.
- Run `doom sync` after changing `init.el` or `packages.el`.
- Do not run `doom upgrade` casually. This setup uses a custom Org package
  recipe and unpinned Org packages.
- Keep API keys and model credentials out of the repo. AI packages should use
  Emacs `auth-source` or external environment files.
- Avoid broad Doom refactors unless the user explicitly asks for them. Keep
  changes near the relevant section in `config.org`.

## Current Doom Shape

- Active theme: `doom-horizon`.
- Font: `Maple Mono Normal NF CN`, size 15.
- Background alpha: 90.
- Important modules include:
  - input: `chinese`, `japanese`
  - completion: `(corfu +orderless)`, `vertico`
  - editor: `(evil +everywhere)`, snippets, format-on-save
  - tools: `lsp`, `magit`, `pdf`, `tree-sitter`, `llm`
  - lang: `(org +gnuplot +journal +present +dragndrop +roam2 +pretty)`,
    `(python +lsp +pyright +tree-sitter)`, `(rust +lsp)`, Java, LaTeX, and
    related language modules
  - config: `literate`, `(default +bindings +smartparens)`

## Custom Org Stack

- `packages.el` overrides Org to Tecosaur's Org mirror/dev branch with
  `:pin nil`.
- `packages.el` also unpins `org` and `org-roam`.
- Treat Org-related upgrades as risky until the live straight.el checkouts are
  inspected.
- Org-heavy customizations live in `config.org`, including:
  - LaTeX preview settings
  - `org-modern`, `org-appear`, and agenda display
  - `org-roam`, `org-roam-ui`, capture, export, and database helpers
  - `org-super-agenda`, `org-habit`, `valign`, and `org-sliced-images`

## Agenda Setup

- Agenda files are added from:
  - `~/research/todo.org`
  - `~/research/plan/schedule.org`
  - `~/research/papers/papers.org`
- `org-super-agenda` is installed for grouping.
- The custom `n` agenda command shows the agenda plus a lower TODO list.
- The lower TODO list uses `org-agenda-todo-ignore-with-date` so scheduled,
  deadline, habit, and timestamped entries do not repeat below the agenda.

## AI/Agent Packages

The config intentionally includes several AI-related packages:

- `gptel`
- `claude-code-ide`
- `claude-code-ide-extras`
- `kimi-code-ide`
- `copilot`
- `org-roam-ui`

Do not remove Claude or Kimi tooling just because another agent is active.

## Validation

- For `config.org` changes:
  - Tangle with Emacs or Doom's normal literate workflow.
  - Run a Lisp syntax check on the tangled output when practical.
  - For agenda changes, open or batch-generate the affected agenda command if
    possible.
- For `init.el` or `packages.el` changes:
  - Run `doom sync`.
  - Restart Emacs or run the appropriate Doom reload step before declaring the
    change fully validated.
- For package recipe or Org changes:
  - Inspect the current straight.el checkout before recommending upgrades.
  - Prefer conservative changes that preserve the custom Org setup.

## Commit Notes

- Follow the repo's signed Conventional Commit rules.
- Use `feat(doom):`, `fix(doom):`, or `docs(doom):` as appropriate.
- If signing times out, ask the user to fix GPG/password-manager setup. Do not
  bypass signing with `--no-gpg-sign`.
