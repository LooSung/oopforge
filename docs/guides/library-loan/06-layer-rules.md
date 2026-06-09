# Step 6 — Layer dependency rules

[English](./06-layer-rules.md) · [한국어](./06-layer-rules.ko.md)
```text
Presentation / Adapter
        │
        ▼
   Application (calls provided port)
        │
        ▼
      Domain  ←── framework import 0
        ▲
        │
   Application (defines required port)
        ▲
        │
Infrastructure (implements required port)
```

| Layer | May know | Must not know |
|---|---|---|
| Domain | Business rules | Spring, FastAPI, JPA, SQLAlchemy |
| Application | Domain, port interfaces | Concrete repository, HTTP |
| Infrastructure | Application ports | Domain invariants (direct mutation) |
| Presentation | Application ports | Domain called directly from controller |

> If a domain test needs Spring context or a database fixture, dependency direction is broken.

---

Back to: [README.md](./README.md)
