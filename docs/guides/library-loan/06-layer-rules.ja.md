# Step 6 — Layer dependency rules

[English](./06-layer-rules.md) · [한국어](./06-layer-rules.ko.md) · [日本語](./06-layer-rules.ja.md) · [中文](./06-layer-rules.zh.md)

```text
Presentation / Adapter
        │
        ▼
   Application (provided port 呼び出し)
        │
        ▼
      Domain  ←── framework import 0
        ▲
        │
   Application (required port 定義)
        ▲
        │
Infrastructure (required port 実装)
```

| レイヤー | 知ってよい | 知ってはいけない |
|---|---|---|
| Domain | ビジネスルール | Spring, FastAPI, JPA, SQLAlchemy |
| Application | Domain、port インターフェース | 具象 repository、HTTP |
| Infrastructure | Application port | Domain 不変条件 (直接変更) |
| Presentation | Application port | Controller から Domain 直接呼び出し |

> Domain テストに Spring context や DB fixture が必要なら、依存方向が壊れている。

---

目次: [README.ja.md](./README.ja.md)
