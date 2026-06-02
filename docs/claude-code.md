# Claude Code Setup

OOPforge is **fully supported** on Claude Code via symlink install.

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Restart Claude Code. Verify:

```bash
~/.oopforge/scripts/setup/doctor.sh
```

Installed paths:

- `~/.claude/skills/oopforge`
- `~/.claude/commands/oopforge`

## Slash commands

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:craft Refactor imported billing module without changing behavior
```

**First time?** Follow the [library loan walkthrough](../guides/library-loan/README.md) step by step.  
Localized index: [KO](../guides/library-loan/README.ko.md) · [JA](../guides/library-loan/README.ja.md) · [ZH](../guides/library-loan/README.zh.md)

## Update after pull

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Skill content updates immediately via symlinks; re-run `scripts/setup/install.sh update` when new link targets are added.

## Reference example

```text
Use examples/order-java as the structural reference for place-order.
```

## Related

- [Codex setup](./codex.md) (Codex skill entry point and slash-like prompts)
- [Cursor setup](./cursor.md) (Cursor Agent CLI via `--plugin-dir`)