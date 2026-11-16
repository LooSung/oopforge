---
type: llm
weight: 1
---

The response matches the size of a one-line fix: it gives the change and a few lines on how it was or should be verified. It does not fill in a full OOP Contract (aggregates, use case, transaction boundary, ports) form (tree, state placement, props, server data, test targets) and does not write separate Design Decisions and Remaining Risks sections. A one-line note that the change is small, or a short Assumptions line, is fine. A regression test for the bug is expected and does not count against brevity.
