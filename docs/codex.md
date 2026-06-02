# Codex Setup

OOPforge is supported on Codex through a Codex skill entry point at `skills/SKILL.md`.

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

## Slash-Like Prompts

Codex does not need the Claude Code `commands/` directory. Type Craft as a normal prompt:

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in python-fastapi
/oopforge:craft Refactor imported billing module without changing behavior
```

The Codex `oopforge` skill routes Craft requests to the matching workflow files.

Natural language also works:

```text
Use OOPforge Discovery for the payment domain. Do not write code yet.
Use OOPforge Implement for approve-payment with tests.
```

## Update After Pull

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Skill content updates immediately via symlinks; restart Codex when the skill entry point or metadata changes.

## Related

- [Claude Code setup](./claude-code.md)
- [Cursor setup](./cursor.md) (Cursor Agent CLI via `--plugin-dir`)