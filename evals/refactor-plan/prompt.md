---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Use OOPforge refactor: in our FastAPI library-loan service, the loan-return endpoint calculates the overdue penalty and changes loan state inside the controller. Plan the refactor before touching code; behavior must not change. The service code is not available in this session, so write the plan from this description and mark what must be checked against the real code.
