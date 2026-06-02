# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI は機能を作る。OOPforge はアーキテクチャを守る。**
>
> *バイブコーディングがバックエンドを壊さないようにするハーネスエンジニアリング。*

**Forge small. Compose forever.** OOPforge は OOP/DDD をエージェントが従う方言として定義する — スキルは文法、ハードルールはリント、実行可能な `examples/` はリファレンス実装、install・コマンドはランタイムです。方法論パックかつエージェント・ハーネスであり、汎用 agent framework ではありません。

Claude Code、Codex CLI、Cursor などの互換エージェントが、コードを書く前に **ドメインモデル**、**集約**、**ポート**、**アダプター**、**テスト可能なユースケース** を中心に設計できるようにします。

**Java (Spring)** · **Python (FastAPI)** 特化 — **3層 (Controller/Service/Repository)** または **hexagonal/clean** から選択、**OpenAPI/Swagger** 標準搭載。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## クイックスタート

### 1. インストール

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### 2. エージェントを再起動

Claude Code、Codex CLI、Cursor Agent CLI のセッションを再起動し、skills と commands を読み込む。

**Cursor:** パックを明示的にロード:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

### 3. Craft を実行

エントリポイントは全ハーネスで **Craft**。**呼び方だけ**が異なります。

| Harness | 呼び方 |
|---|---|
| **Claude Code** | `/oopforge:craft <request>` — スラッシュコマンド |
| **Codex CLI** | `/skills` → **oopforge** を選び、**先頭 `/` なし**でプロンプト (Codex は `/` を自前コマンド用に予約) |
| **Cursor Agent CLI** | `--plugin-dir` 後に自然言語 ([Cursor setup](docs/cursor.md)) |

**Claude Code:**

```text
/oopforge:craft Email 値オブジェクトを 1 つ追加
```

**Codex CLI** (`/skills` → oopforge 後):

```text
Use OOPforge craft: Email 値オブジェクトを 1 つ追加
```

**Cursor:**

```text
Use OOPforge craft: Email 値オブジェクトを 1 つ追加
```

---

## Advanced Usage

アドバイスのみのリクエストでは Craft は実装せず、最小経路だけ提案する (全ハーネス共通)。

上級ユーザーは Discovery、Design、Delivery Plan、Skeleton、Implement、Test、Refactor など特定の workflow stage から Craft に依頼できる。

すでにインストール済みなら [Install](#install) で手動設定・更新・トラブルシュートを参照。

ハーネスガイド: [Claude Code](docs/claude-code.md) · [Codex](docs/codex.md) · [Cursor](docs/cursor.md)

---

## なぜ OOPforge か

OOPforge は **DDD / OOP 専門の AI エンジニアリング pack** です。汎用 agent framework ではありません。**OOP 方言のためのハーネス・エンジニアリング** — スキルは文法、ハードルールはリンター、`examples/` は参照実装、install とコマンドはランタイムです。

| 原則 | 意味 |
|---|---|
| **Small** | 1 skill = 1 concept、200 行以下 |
| **Measurable** | 300 行/ファイル、20 行/メソッド |
| **Workflow-first** | Discovery → Test、human checkpoint |
| **Proof over philosophy** | 実行可能な Java/Python 例 |
| **Domain-first** | domain layer に framework import 0 |

要約: **構造をデフォルト**にして God Service 生成を防ぐ。

---

## OOPforge の使い方

**初めての方はこちら:** **[図書館貸出ガイド →](docs/guides/library-loan/README.ja.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

ガイド目次: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md) · [JA](docs/guides/library-loan/README.ja.md) · [ZH](docs/guides/library-loan/README.zh.md)

| 資料 | 用途 |
|---|---|
| [図書館貸出ガイド](docs/guides/library-loan/README.ja.md) | フルワークフロー チュートリアル |
| [Examples index](examples/README.md) | 実行可能な証明 — 4 スタック、同一 place-order |
| [order-java](examples/order-java/) · [order-java-layered](examples/order-java-layered/) | Java hexagonal · Java 3-tier |
| [order-python](examples/order-python/) · [order-python-layered](examples/order-python-layered/) | FastAPI clean · FastAPI 3-tier |
| [Discovery サンプル (library)](docs/sample-output/discovery-library.ja.md) | 期待される agent 出力 ([EN](docs/sample-output/discovery-library.md) · [KO](docs/sample-output/discovery-library.ko.md) · [ZH](docs/sample-output/discovery-library.zh.md)) |
| [Design サンプル (library)](docs/sample-output/design-library.ja.md) | 期待される agent 出力 ([EN](docs/sample-output/design-library.md) · [KO](docs/sample-output/design-library.ko.md) · [ZH](docs/sample-output/design-library.zh.md)) |

各ステージの終わりに **human checkpoint** — 先に進まないでください。

---

## Philosophy

> **Model is replaceable. Workflow is permanent.**

モデルは変わります。Claude、GPT、OSS、その次も。
しかし workflow、contracts、architectural discipline は長く残ります。

OOPforge はモデル層ではなく、**development protocol layer** です。

### 4 Principles

1. **Small** — 1 skill は 1 concept。200 行以下。
2. **Clean** — Domain layer に framework import を入れない。
3. **Composable** — 小さな部品を時間をかけて組み合わせる。
4. **Sustainable** — mega prompt を避け、人間の checkpoint を残す。

---

## Install

### Setup commands (from `~/.oopforge` or this repo)

```bash
./scripts/setup/install.sh          # install symlinks
./scripts/setup/doctor.sh           # check pack + links
./scripts/setup/install.sh update   # refresh symlinks after git pull
```

### Quick

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### Manual

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

`scripts/setup/install.sh` は検出された Claude Code / Codex CLI の設定ディレクトリへ OOPforge を symlink します。

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Experimental | `cursor-agent --plugin-dir ~/.oopforge` |
Symlink インストールでは `~/.oopforge` で `git pull` するだけでスキル内容が更新されます。リンク先の再作成が必要な場合は `./scripts/setup/install.sh update` を実行してください。

### ローカル smoke test

```bash
./scripts/ci/smoke-test.sh
```

---

## Use

### `/oopforge:craft` — 何から始めるか分からないとき

```text
/oopforge:craft Add a refund use case to the existing payment domain
/oopforge:craft Fix the bug that allows cancellation after shipment
```

`/oopforge:craft` はリクエストを確認し、最小の OOP path を推薦または実行します。

### Stack 識別子

| Stack | Architecture | 用途 |
|---|---|---|
| `java-spring-layered` | 3層 (Controller/Service/Repository) | 小規模・MVP |
| `java-spring-hexagonal` | Hexagonal | ドメイン複雑 |
| `python-fastapi-layered` | 3層 (Router/Service/Repository) | 小規模・MVP |
| `python-fastapi-clean` | Clean | ドメイン複雑 |

すべての backend skeleton は **OpenAPI/Swagger UI を標準で有効化** (springdoc / FastAPI 内蔵)。

### Full workflow

```text
/oopforge:craft Start Discovery for the order domain. No code yet.
/oopforge:craft Implement place-order in java-spring-layered
```

または自然言語で依頼します。

> "Build an Order aggregate in Java, following OOPforge rules."

### メモリーストア (セッションをまたいで再開)

会話が変わっても作業が残るよう、軽量なメモリを残します。書いておき、必要なときに取り出します。

- 作業ごとに 1 つのドキュメント `.craft/<kind>-<slug>.md` (例: `.craft/feature-member-management.md`) に決定・進捗・次の作業を蓄積します。
- 戻ってきたら Craft が該当ドキュメントを**先に読み**、そこから続けます。
- `.craft/` はデフォルトで gitignore (個人ノート)。場所はプロジェクト `AGENTS.md` の `OOPforge work dir: <path>` 行で変更します。

詳細: [`skills/workflow/continuity.md`](skills/workflow/continuity.md).

---

## What's inside

```
skills/
├── workflow/        Recommended: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
├── principles/      OOP decision principles
├── playbooks/       Craft task checklists
├── oop/             Domain model + use-case boundary
├── lang/            Backend stack selection (layered vs hexagonal/clean)
└── skeleton/        Backend package structure + empty types

commands/            Claude Code slash command entry point + /oopforge:craft
docs/roadmap.md      方向・優先順位・非ゴール
AGENTS.md            cross-agent repository instructions
CLAUDE.md            Claude Code bootstrap instructions
scripts/
├── setup/           bootstrap, install, uninstall, doctor
├── ci/              lint-skills, smoke-test
└── path-convention.md
```

---

## Hard Rules

Enforceable measurable rules live in [`AGENTS.md`](./AGENTS.md). This README keeps the user-facing overview.

---

## Roadmap

Packaging:

- **Phase 1** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces (Cursor CLI: `--plugin-dir` today; bootstrap symlink + marketplace pending)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

方向性・優先順位・非ゴール (短期/中期/長期、言語拡張、lint 強制、anti-pattern カタログ): **[docs/roadmap.md](./docs/roadmap.md)**

---

## Inspiration

- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing Domain-Driven Design*
- Robert C. Martin, *Clean Architecture*
- Kent Beck, *Test-Driven Development: By Example*

---

## Reference

Reference only — packaging and layout ideas, not a dependency.

- Multi-harness plugin structure: [obra/superpowers](https://github.com/obra/superpowers)
- スキルルーティングと「最小経路」の思想: [pstack by Lauren (Cursor)](https://cursor.com/en-US/lp-team/lauren)

---

## License

MIT
