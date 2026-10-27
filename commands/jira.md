---
name: jira
description: Write one Jira task, story, bug, epic, or backlog item, or the child tasks of one existing epic or story, in the fixed Korean template without changing code.
---

If the user request is exactly `OOPFORGE_ACTIVATION_PROBE`, output these three
lines and stop without reading other files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

When the parent epic or story already exists and the request is to create its
child issues, read and execute:

`~/.claude/skills/oopforge/workflow/jira-children.md`

Otherwise read and execute:

`~/.claude/skills/oopforge/workflow/jira-card.md`

A request that asks for a new or rewritten issue and its children in the same
breath still reads `workflow/jira-card.md`. That file writes one issue. Children
are the next turn.

User request:

**$ARGUMENTS**
