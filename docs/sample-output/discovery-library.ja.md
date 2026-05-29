# サンプル出力 — Discovery: 図書館貸出ドメイン

[English](./discovery-library.md) · [한국어](./discovery-library.ko.md) · [日本語](./discovery-library.ja.md) · [中文](./discovery-library.zh.md)

エージェント prompt 用の短い参照。フルガイド: [図書館貸出ガイド](../guides/library-loan/README.ja.md).

## ビジネス目標

会員が書籍を貸出する。貸出中の書籍は再貸出不可。貸出時に `BookBorrowed` イベントを発行。

## 境界づけられたコンテキスト

- **Lending** — Loan、書籍可用性、会員資格
- **Catalog** — 書籍メタデータ (タイトル、著者) — Lending から分離

## コア概念

- Book, Member, Loan, LoanId, BookBorrowed

## アグリゲート候補

- **Loan** (Lending コンテキストの root)

## 主要不変条件

- 書籍にアクティブな貸出があると追加貸出不可
- 返却済み貸出は再返却不可
- Catalog は ID のみ参照、オブジェクト埋め込み禁止

## 未決事項

- 会員あたり最大貸出冊数?
- 延滞ポリシー?
- 固定 vs 可変貸出期間?
