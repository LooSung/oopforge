---
name: jira
description: Write one Jira task, story, bug, epic, or backlog item, or the child tasks of one existing epic or story, in the fixed Korean template without changing code.
argument-hint: "[card request, or the parent key for child tasks]"
---

If the user request is exactly `OOPFORGE_ACTIVATION_PROBE`, output these three
lines and stop without reading other files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

When the parent epic or story already exists and the request is to create its
child issues, read and execute the first path that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/jira-children.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/jira-children.md` — symlink install

Otherwise read and execute the first path that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/workflow/jira-card.md` — session plugin
2. `~/.claude/skills/oopforge/workflow/jira-card.md` — symlink install

A request that asks for a new or rewritten issue and its children in the same
breath still reads `workflow/jira-card.md`. That file writes one issue. Children
are the next turn.

User request:

**$ARGUMENTS**
