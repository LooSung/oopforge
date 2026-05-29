# Step 1 — Discovery

[English](./01-discovery.md) · [한국어](./01-discovery.ko.md) · [日本語](./01-discovery.ja.md) · [中文](./01-discovery.zh.md)

> **不写代码。** 只定义语言、边界和术语。

技能: `{pack}/skills/workflow/discovery.md`

输出保存至: `docs/library/discovery.md` (项目内)

---

## 示例输出

```markdown
# Library — Discovery

## Glossary
- **Book**: 图书馆持有的实体书。以唯一 ISBN 标识。
- **Member**: 有借阅权限的注册会员。
- **Loan**: 某 Member 借阅某 Book 的事实。归还时结束。
- **LoanId**: 标识 Loan 的值对象。

## Bounded Contexts
1. **Lending** — Loan、Book (可用性)、Member (借阅资格)
2. **Catalog** — Book 元数据 (书名、作者) — 与 Lending 分离

## Aggregate Candidates
- Lending: `Loan` (root)
- Book 可用性在 Lending 上下文内通过单独查询处理

## Actors / External
- Member (Web 客户端)
- Catalog Service (外部 — 验证书籍存在)

## Non-Functional
- 借阅处理同步，p99 300ms 以内
- 同一图书并发借阅请求 → 仅一条成功 (乐观锁或唯一约束)

## Open Questions
- 每位会员最大借阅册数?
- 逾期是否禁止继续借阅?
- 归还期限固定还是按图书类型不同?
```

---

## 检查点

提问: *"Discovery 结果是否 OK，可以进入 Design?"*

下一步: [02-design.zh.md](./02-design.zh.md)
