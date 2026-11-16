---
type: llm
weight: 1
---

The review identifies at least four of these five defects (wording may differ):
1. business rules (return state change, penalty calculation) live in the controller instead of the domain or a use case;
2. a missing loan returns 200 / "ok" instead of a not-found error;
3. an already-returned loan raises 500 instead of a client error such as 409 or 422;
4. two writes (loan and member) happen without one transaction or consistency boundary, so a partial write is possible;
5. `datetime.now()` without a timezone or injected clock makes the penalty wrong or untestable.
Pass only if at least four are reported.
