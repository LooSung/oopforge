# OOPforge

> **Forge small. Compose forever.**
>
> Claude Code、Codex CLI、Cursor などの AI コーディングエージェントに、OOP/DDD とクリーンアーキテクチャの規律を注入する methodology pack。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## なぜ OOPforge か

[obra/superpowers](https://github.com/obra/superpowers) や [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework) のような優れた汎用ワークフローパックはすでに存在します。OOPforge はそれらと競合するのではなく、**補完**します。

| | obra/superpowers | SuperClaude | **OOPforge** |
|---|---|---|---|
| **Focus** | Workflow · TDD | Full platform · slash commands | **DDD · Hexagonal · OOP domain modeling** |
| **Language** | General | General | **Java + Python** |
| **UI Language** | EN | EN, ZH, JA | **EN-first + KO/JA/ZH** |
| **Rules** | Guidelines | Behavioral modes | **Concrete metrics** |

要するに、OOPforge は **DDD を真剣に扱う開発者のための superpowers** です。

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

- Claude Code → `~/.claude/{skills,agents,commands}/oopforge`
- Codex CLI → `~/.codex/skills/oopforge`
- Cursor → `.cursor-plugin/` manifest prepared for Phase 2
- OpenCode → experimental。必要な場合のみ `INSTALL_OPENCODE=1 ./install.sh`

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
├── workflow/        Discovery → Design → Skeleton → Implement
├── oop/             Aggregate Root, Value Object, Domain Event, ...
└── lang/
    ├── java/        Spring hexagonal layout, JPA repository
    └── python/      Pydantic value objects, clean FastAPI layout

agents/              ddd-architect subagent
commands/            slash commands for each workflow stage
AGENTS.md            cross-agent repository instructions
CLAUDE.md            Claude Code bootstrap instructions
```

---

## Hard Rules

- Domain layer framework imports: **0**
- One file: **≤ 300 lines**
- One method: **≤ 20 lines preferred**
- One skill file: **≤ 200 lines**
- No public setters; use static factory methods
- Defensive copy collections at boundaries
- No domain logic without tests

---

## Roadmap

- **Phase 1** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## License

MIT
