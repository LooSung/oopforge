# 図書館貸出 — OOPforge フルウォークスルー

> Java (Spring Boot) と Python (FastAPI) で **図書館貸出システム**を最初から最後まで実装します。  
> Discovery → Design → Delivery Plan → Skeleton → Implement → Test の順で進めます。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

OOPforge の **使い方**を段階的に示すガイドです。最小実行例は [`examples/calculator-java-hexagonal`](../../../examples/calculator-java-hexagonal/) と [`examples/calculator-python-hexagonal`](../../../examples/calculator-python-hexagonal/) を参照してください。

---

## シナリオ

会員が書籍を **貸出**する。貸出中の書籍は再貸出できない。貸出時に `BookBorrowed` イベントが発行される。

---

## スラッシュコマンド (Claude Code)

**Java トラック:**

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:craft Test borrow-book
```

**Python トラック** — Discovery/Design/Delivery Plan は同じ。Skeleton のみ変更:

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in python-fastapi
/oopforge:craft Test borrow-book
```

プロジェクトごとに **1 スタック**を選んでください。両トラックは同じ `borrow-book` ユースケースを実装します。

自然言語でも開始できます:

```text
Follow OOPforge workflow for a library loan domain. Start at Discovery — no code yet.
```

---

## ステップ

| ステップ | Java | Python |
|---|---|---|
| 1. Discovery | [01-discovery.ja.md](./01-discovery.ja.md) | 同じ |
| 2. Design | [02-design.ja.md](./02-design.ja.md) | 同じ |
| 3. Skeleton | [03-skeleton.ja.md](./03-skeleton.ja.md) § Java | [03-skeleton.ja.md](./03-skeleton.ja.md) § Python |
| 4. Implement | [04-implement-java.ja.md](./04-implement-java.ja.md) | [04-implement-python.ja.md](./04-implement-python.ja.md) |
| 5. Test | [05-test.ja.md](./05-test.ja.md) § Java | [05-test.ja.md](./05-test.ja.md) § Python |
| 6. レイヤー規則 | [06-layer-rules.ja.md](./06-layer-rules.ja.md) | 同じ |

各ステップファイル上部で EN · KO · JA · ZH を切り替え可能。

---

## 短いサンプル (エージェント出力)

プロンプト用の **Discovery/Design 期待形式**のみ必要な場合:

| 言語 | Discovery | Design |
|---|---|---|
| English | [discovery-library.md](../../sample-output/discovery-library.md) | [design-library.md](../../sample-output/design-library.md) |
| 한국어 | [discovery-library.ko.md](../../sample-output/discovery-library.ko.md) | [design-library.ko.md](../../sample-output/design-library.ko.md) |
| 日本語 | [discovery-library.ja.md](../../sample-output/discovery-library.ja.md) | [design-library.ja.md](../../sample-output/design-library.ja.md) |
| 中文 | [discovery-library.zh.md](../../sample-output/discovery-library.zh.md) | [design-library.zh.md](../../sample-output/design-library.zh.md) |

---

## 各ステップの後

OOPforge は **human checkpoint** を前提とします。出力を承認するまで次のステージに進まないでください。

Implement 後にルール違反を確認したい場合は、`/oopforge:craft` に Hard Rules レビューを依頼します。
