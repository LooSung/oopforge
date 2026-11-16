---
name: craft
description: Execute backend OOP work with the smallest appropriate path.
argument-hint: "[backend task]"
---

If the user request is exactly `OOPFORGE_ACTIVATION_PROBE`, output these three
lines and stop without reading other files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

Read and execute the first path that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/craft.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/craft.md` — symlink install

User request:

**$ARGUMENTS**
