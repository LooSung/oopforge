---
name: test
description: Verify, write, or strengthen backend tests for a specific purpose.
argument-hint: "[test target and optional level: unit | use-case | integration | e2e]"
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

Then read and execute the first path that exists for Test execution.
Do not reclassify this request or change production behavior:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/test.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/test.md` — symlink install

User request:

**$ARGUMENTS**
