# Claude Code Setup

OOPforge is **fully supported** on Claude Code via symlink install.

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

Restart Claude Code. Verify:

```bash
~/.oopforge/doctor.sh
```

Installed paths:

- `~/.claude/skills/oopforge`
- `~/.claude/agents/oopforge`
- `~/.claude/commands/oopforge`

## Slash commands

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:delivery-plan place-order
/oopforge:skeleton java-spring
/oopforge:implement place-order
/oopforge:test place-order
/oopforge:refactor imported billing module
```

## Subagents

```text
@ddd-architect Model the payment bounded context with OOPforge.
@domain-reviewer Review this module for God Service and framework leakage.
```

## Update after pull

```bash
cd ~/.oopforge && git pull && ./install.sh update
```

Skill content updates immediately via symlinks; re-run `install.sh update` when new link targets are added.

## Reference example

```text
Use examples/order-java as the structural reference for place-order.
```

## Related

- [Cursor setup](./cursor.md) (project rules, no installer yet)
- [OpenCode opt-in](./opencode.md)
