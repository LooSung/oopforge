# Codex Setup

OOPforge supports Codex through the global skill entry point at
`skills/SKILL.md`. This is the canonical path in the
[support scope](../reference/support-scope.md).

Codex installs **skills only** — not Claude Code `commands/`. OOPforge strings
such as `/oopforge:craft`, `/oopforge:refactor`, `/oopforge:consult`, and
`/oopforge:test` are **not** Codex slash commands; Codex reserves `/` for built-ins.

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Restart Codex. Check the pack and installed links:

```bash
~/.oopforge/scripts/setup/doctor.sh
```

`doctor.sh` does not execute Craft. In Codex, run `/skills` and confirm that
**oopforge** appears before using the natural-language entry point below.

Installed path:

- `~/.codex/skills/oopforge`

Because this path is a symlink to `~/.oopforge/skills`, Codex sees:

- `~/.codex/skills/oopforge/SKILL.md`
- `~/.codex/skills/oopforge/workflow/*.md`
- `~/.codex/skills/oopforge/oop/*.md`
- `~/.codex/skills/oopforge/lang/*.md`

Works in **any project directory** — skills are global under `~/.codex/skills/`.

**Important:** start Codex **from your target project**, not from `~/.oopforge`:

```bash
cd /path/to/your-backend-project
codex
```

If `pwd` is `~/.oopforge`, relative paths like `docs/integration/foo.md` will be resolved in the **pack**, not your app repo. Use an absolute path or restart Codex after `cd` to your project.

Exception: when you are maintaining OOPforge itself, start Codex from the
OOPforge repository and treat that repository as the work target.

## Run OOPforge commands on Codex

1. Start Codex in your backend project: `cd /path/to/your-project && codex`
2. Type `/skills` and select **oopforge**
3. Prompt **without** a leading `/`:

```text
Use OOPforge craft: Start Discovery for the library loan domain. No code yet.
Use OOPforge craft: Implement borrow-book in python-fastapi
Use OOPforge refactor: Improve imported billing structure without changing behavior
Use OOPforge consult: Review billing boundaries without changing files
Use OOPforge test: Run the smallest useful tests for the borrow-book rule
```

One-shot (non-interactive):

```bash
codex exec "Use OOPforge craft: Add a single Email value object"
```

The `oopforge` skill routes Craft to the smallest OOP path, Refactor to
behavior-preserving work, Consult to advisory work, and Test to test-only work
without production changes.

Maintainers can run the authenticated positive/negative check with:

```bash
./scripts/ci/harness-smoke.sh live codex
```

This optional local check uses the maintainer's existing Codex authentication;
the repository does not require provider secrets.

## Why not OOPforge slash commands?

| Harness | OOPforge `/` commands |
|---|---|
| Claude Code | Work — `commands/` is installed |
| Codex CLI | **Fails** — Codex parses `/…` as its own command menu |

If an OOPforge `/` command is unrecognized, you typed a Codex slash command, not an agent prompt. Use `/skills` + natural language instead.

## Update After Pull

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Skill content updates immediately via symlinks; restart Codex when the skill entry point or metadata changes.

## Related

- [Claude Code setup](./claude-code.md) — slash commands for Craft, Refactor, Consult, and Test
- [Cursor setup](./cursor.md) (explicit local plugin or project-local skill)
