# Codex Setup

OOPforge is supported on Codex through a skill entry point at `skills/SKILL.md`.

Codex installs **skills only** — not Claude Code `commands/`. The string `/oopforge:craft` is **not** a Codex slash command; Codex reserves `/` for built-ins such as `/skills` and `/model`.

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Restart Codex. Verify:

```bash
~/.oopforge/scripts/setup/doctor.sh
```

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

## Run Craft on Codex

1. Start Codex in your backend project: `cd /path/to/your-project && codex`
2. Type `/skills` and select **oopforge**
3. Prompt **without** a leading `/`:

```text
Use OOPforge craft: Start Discovery for the library loan domain. No code yet.
Use OOPforge craft: Implement borrow-book in python-fastapi
Use OOPforge craft: Refactor imported billing module without changing behavior
```

One-shot (non-interactive):

```bash
codex exec "Use OOPforge craft: Add a single Email value object"
```

The `oopforge` skill routes Craft requests to `workflow/craft.md` and the smallest OOP path.

## Why not `/oopforge:craft`?

| Harness | `/oopforge:craft` |
|---|---|
| Claude Code | Works — `commands/` is installed |
| Codex CLI | **Fails** — Codex parses `/…` as its own command menu |

If you see `Unrecognized command '/oopforge:craft'`, you typed a Codex slash command, not an agent prompt. Use `/skills` + natural language instead.

## Update After Pull

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Skill content updates immediately via symlinks; restart Codex when the skill entry point or metadata changes.

## Related

- [Claude Code setup](./claude-code.md) — slash command `/oopforge:craft`
- [Cursor setup](./cursor.md) (experimental project-local skill setup)
