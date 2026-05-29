# OOPforge skill path convention

Commands and agents must reference skills using the **pack root**, not `skills/oopforge/...`.

## Resolve pack root

1. `$OOPFORGE_HOME` if set
2. `~/.oopforge` after bootstrap install
3. Repository root when developing this pack

## Path pattern

```text
{pack}/skills/workflow/discovery.md
{pack}/skills/oop/aggregate-root.md
{pack}/skills/lang/java/spring-hexagonal-layout.md
```

Installed Claude path (symlink name `oopforge` is the harness folder, not part of the skill path):

```text
~/.claude/skills/oopforge/workflow/discovery.md  → same files as {pack}/skills/workflow/discovery.md
```
