---
name: refactor
description: Improve backend OOP structure while preserving behavior.
argument-hint: "[code area and the smell to remove]"
---

If the user request is exactly `OOPFORGE_ACTIVATION_PROBE`, output these three
lines and stop without reading other files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

Read and execute the first path that exists for Craft startup, continuity,
verification, and completion reporting:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/craft.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/craft.md` — symlink install

Then read and execute the first path that exists for Refactor execution.
Do not reclassify this request as feature work:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/refactor.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/refactor.md` — symlink install

User request:

**$ARGUMENTS**
