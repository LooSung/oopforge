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
- `~/.claude/agents/oopforge`
- `~/.claude/commands/oopforge`

## Slash commands

```text
/oopforge:discovery library loan domain
/oopforge:design borrow-book use case
/oopforge:delivery-plan borrow-book
/oopforge:skeleton java-spring
/oopforge:implement borrow-book
/oopforge:test borrow-book
/oopforge:refactor imported billing module
```

**First time?** Follow the [library loan walkthrough](../guides/library-loan/README.md) step by step.  
Localized index: [KO](../guides/library-loan/README.ko.md) · [JA](../guides/library-loan/README.ja.md) · [ZH](../guides/library-loan/README.zh.md)

## Subagents

```text
@ddd-architect Model the payment bounded context with OOPforge.
@domain-reviewer Review this module for God Service and framework leakage.
```

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

- [Cursor setup](./cursor.md) (Cursor Agent CLI via `--plugin-dir`)
- [OpenCode opt-in](./opencode.md)
