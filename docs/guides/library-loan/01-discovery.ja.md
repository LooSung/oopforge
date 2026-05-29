# Step 1 — Discovery

[English](./01-discovery.md) · [한국어](./01-discovery.ko.md) · [日本語](./01-discovery.ja.md) · [中文](./01-discovery.zh.md)

> **コードなし。** 言語、境界、用語のみ定義する。

スキル: `{pack}/skills/workflow/discovery.md`

出力保存先: `docs/library/discovery.md` (プロジェクト内)

---

## 出力例

```markdown
# Library — Discovery

## Glossary
- **Book**: 図書館が所蔵する物理的な書籍。固有 ISBN で識別。
- **Member**: 貸出権限を持つ登録会員。
- **Loan**: 特定 Member が特定 Book を借りた事実。返却で終了。
- **LoanId**: Loan を識別する値オブジェクト。

## Bounded Contexts
1. **Lending** — Loan、Book (可用性)、Member (資格)
2. **Catalog** — Book メタデータ (タイトル、著者) — Lending から分離

## Aggregate Candidates
- Lending: `Loan` (root)
- Book 可用性は Lending コンテキスト内の別 lookup で処理

## Actors / External
- Member (Web クライアント)
- Catalog Service (外部 — 書籍存在確認)

## Non-Functional
- 貸出処理は同期、p99 300ms 以内
- 同一書籍への同時貸出リクエスト → 1 件のみ成功 (楽観ロック or ユニーク制約)

## Open Questions
- 会員あたり最大貸出冊数は?
- 延滞時の貸出ブロックポリシー?
- 返却期限は固定か、書籍種別で異なるか?
```

---

## チェックポイント

質問: *"Discovery の結果を確認し、Design に進んでもよいですか?"*

次: [02-design.ja.md](./02-design.ja.md)
