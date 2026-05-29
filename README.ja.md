# OOPforge

> **Forge small. Compose forever.**
>
> Claude Code、Codex CLI、Cursor などの AI コーディングエージェントに、OOP/DDD とクリーンアーキテクチャの規律を注入する methodology pack。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## なぜ OOPforge か

OOPforge は **DDD / OOP 専門の AI エンジニアリング pack** です。汎用 agent framework ではありません。

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
| [examples/order-java](examples/order-java/) · [order-python](examples/order-python/) | 最小実行可能な証明 (place-order) |
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
| **Claude Code** | Supported | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor** | Not yet (Phase 2) | No installer — manifest only at `.cursor-plugin/` |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./scripts/setup/install.sh` |

Symlink インストールでは `~/.oopforge` で `git pull` するだけでスキル内容が更新されます。リンク先の再作成が必要な場合は `./scripts/setup/install.sh update` を実行してください。

### ローカル smoke test

```bash
./scripts/ci/smoke-test.sh
```

---

## Use

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:skeleton java-spring
/oopforge:implement place-order
```

または自然言語で依頼します。

> "Build an Order aggregate in Java, following OOPforge rules."

---

## What's inside

```
skills/
├── workflow/        Recommended: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
├── oop/             Aggregate Root, Value Object, Domain Event, ...
└── lang/
    ├── java/        Spring hexagonal layout, JPA repository
    └── python/      Pydantic value objects, clean FastAPI layout

agents/              ddd-architect subagent
commands/            Claude Code slash commands for workflow stages
AGENTS.md            cross-agent repository instructions
CLAUDE.md            Claude Code bootstrap instructions
scripts/
├── setup/           bootstrap, install, uninstall, doctor
├── ci/              lint-skills, smoke-test
└── path-convention.md
```

---

## Hard Rules

- Domain layer framework imports: **0**
- One file: **≤ 300 lines** — reviewable PR diff size
- One method: **≤ 20 lines preferred** — single responsibility
- One skill file: **≤ 200 lines** — one concept per agent context load
- No public setters; use static factory methods
- Defensive copy collections at boundaries
- No domain logic without tests

---

## Roadmap

- **Phase 1** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces (Cursor: no ETA; manifest only)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

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

---

## License

MIT
