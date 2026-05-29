# Step 6 — Layer dependency rules

[English](./06-layer-rules.md) · [한국어](./06-layer-rules.ko.md) · [日本語](./06-layer-rules.ja.md) · [中文](./06-layer-rules.zh.md)

```text
Presentation / Adapter
        │
        ▼
   Application (调用 provided port)
        │
        ▼
      Domain  ←── framework import 0
        ▲
        │
   Application (定义 required port)
        ▲
        │
Infrastructure (实现 required port)
```

| 层 | 可以知道 | 不能知道 |
|---|---|---|
| Domain | 业务规则 | Spring, FastAPI, JPA, SQLAlchemy |
| Application | Domain、port 接口 | 具体 repository、HTTP |
| Infrastructure | Application port | Domain 不变量 (直接修改) |
| Presentation | Application port | Controller 直接调用 Domain |

> 若 Domain 测试需要 Spring context 或 DB fixture，说明依赖方向已破坏。

---

目录: [README.zh.md](./README.zh.md)
