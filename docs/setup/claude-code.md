# Claude Code Setup

OOPforge supports Claude Code through the symlink-installed skill and the
`/oopforge:craft`, `/oopforge:refactor`, `/oopforge:consult`, and
`/oopforge:test` commands defined in the [support scope](../reference/support-scope.md).

## Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Restart Claude Code. Check the pack and installed links:

```bash
~/.oopforge/scripts/setup/doctor.sh
```

`doctor.sh` does not execute a workflow. To verify activation, start Claude Code
from the backend project and confirm that the commands are registered:

```text
/oopforge:craft Advise only: which path fits adding one Email value object? Do not edit files.
/oopforge:refactor Improve the billing module structure while preserving its API and behavior.
/oopforge:consult Review the billing boundaries without changing files.
/oopforge:test Run the smallest useful tests for the billing approval rule.
```

Maintainers can run the authenticated positive/negative check with:

```bash
./scripts/ci/harness-smoke.sh live claude
```

This optional local check uses the maintainer's existing Claude authentication;
the repository does not require provider secrets. It loads a self-contained
temporary candidate plugin and does not change global configuration. After
installing a release, set `OOPFORGE_INSTALLED_SMOKE=1` to require the real skill
and command symlinks during the same check.

Installed paths:

- `~/.claude/skills/oopforge`
- `~/.claude/commands/oopforge`

If you are maintaining OOPforge itself, start from the OOPforge repository and
treat that repository as the work target.

## Slash commands

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:refactor Improve imported billing structure without changing behavior
/oopforge:consult Compare two payment designs without changing files
/oopforge:test Strengthen unit tests for the borrow-book invariants
```

**First time?** Follow the [library loan walkthrough](../guides/library-loan/README.md) step by step.
Localized index: [KO](../guides/library-loan/README.ko.md)

## Update after pull

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Skill content updates immediately via symlinks; re-run `scripts/setup/install.sh update` when new link targets are added.

## Reference example

```text
Use examples/calculator-java-hexagonal as the structural reference for the calculate use case.
```

## Related

- [Codex setup](./codex.md) (Codex skill entry point and slash-like prompts)
- [Cursor setup](./cursor.md) (explicit local plugin or project-local skill)
