---
name: consult
description: Ask, compare, review, or explicitly document backend OOP work without implementation changes.
argument-hint: "[question, comparison, review, or document request]"
---

If the user request is exactly `OOPFORGE_ACTIVATION_PROBE`, output these three
lines and stop without reading other files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

Read and execute the first path that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/consult.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/consult.md` — symlink install

User request:

**$ARGUMENTS**
