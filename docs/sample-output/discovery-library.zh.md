# 样本输出 — Discovery: 图书馆借阅领域

[English](./discovery-library.md) · [한국어](./discovery-library.ko.md) · [日本語](./discovery-library.ja.md) · [中文](./discovery-library.zh.md)

供 agent prompt 使用的简短参考。完整指南: [图书馆借阅指南](../guides/library-loan/README.zh.md).

## 业务目标

会员借阅图书。已借出的图书不能再次借出。借阅时发布 `BookBorrowed` 事件。

## 限界上下文

- **Lending** — Loan、图书可用性、会员借阅资格
- **Catalog** — 图书元数据 (书名、作者) — 与 Lending 分离

## 核心概念

- Book, Member, Loan, LoanId, BookBorrowed

## 聚合候选

- **Loan** (Lending 上下文根)

## 关键不变量

- 图书存在活跃借阅时禁止再次借阅
- 已归还借阅不能再次归还
- Catalog 仅通过 ID 引用，禁止嵌入对象

## 待决问题

- 每位会员最大借阅册数?
- 逾期策略?
- 固定 vs 可变借阅期限?
