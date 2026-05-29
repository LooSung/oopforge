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

### Quick

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

### Manual

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x install.sh uninstall.sh doctor.sh
./install.sh
./doctor.sh
```

`install.sh` は検出された Claude Code / Codex CLI の設定ディレクトリへ OOPforge を symlink します。

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor** | Not yet (Phase 2) | No installer — manifest only at `.cursor-plugin/` |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./install.sh` |

Symlink インストールでは `~/.oopforge` で `git pull` するだけでスキル内容が更新されます。リンク先の再作成が必要な場合は `./install.sh update` を実行してください。

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

## License

MIT
