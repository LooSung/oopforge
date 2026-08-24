# OOPforge skill path convention

Commands and agents reference skills from the **pack root**, never through a
legacy `skills/oopforge/...` source path.

## Resolve the pack root

1. `$OOPFORGE_HOME` when set
2. `~/.oopforge` after bootstrap installation
3. The repository root while maintaining this pack

## Source paths

```text
{pack}/skills/workflow/discovery.md
{pack}/skills/oop/domain-model.md
{pack}/skills/lang/backend-stack.md
{pack}/skills/skeleton/backend-skeleton.md
```

The installed Claude path uses `oopforge` as the harness folder name:

```text
~/.claude/skills/oopforge/workflow/discovery.md
  → {pack}/skills/workflow/discovery.md
```
