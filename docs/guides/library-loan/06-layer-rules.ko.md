# Step 6 — Layer dependency rules

[English](./06-layer-rules.md) · [한국어](./06-layer-rules.ko.md) · [日本語](./06-layer-rules.ja.md) · [中文](./06-layer-rules.zh.md)

```text
Presentation / Adapter
        │
        ▼
   Application (provided port 호출)
        │
        ▼
      Domain  ←── framework import 0
        ▲
        │
   Application (required port 정의)
        ▲
        │
Infrastructure (required port 구현)
```

| 레이어 | 알 수 있음 | 알면 안 됨 |
|---|---|---|
| Domain | 비즈니스 규칙 | Spring, FastAPI, JPA, SQLAlchemy |
| Application | Domain, port 인터페이스 | 구체 repository, HTTP |
| Infrastructure | Application port | Domain 불변식 (직접 변경) |
| Presentation | Application port | Controller에서 Domain 직접 호출 |

> Domain 테스트에 Spring context나 DB fixture가 필요하면 의존 방향이 깨진 것이다.

---

목차: [README.ko.md](./README.ko.md)
