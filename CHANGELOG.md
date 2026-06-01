# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [Unreleased]

### Changed

- **Cursor** — document Cursor Agent CLI setup via `cursor-agent --plugin-dir ~/.oopforge`; remove project-rules / `.cursor/skills` symlink guidance.
- **docs/cursor.md** — rewrite for CLI `--plugin-dir` workflow.
- **doctor.sh** — show `--plugin-dir` load command instead of AGENTS.md project-rules warning.

## [0.1.0] - 2026-05-29

Initial public release — portable OOP/DDD methodology pack for AI coding agents.

### Added

- **Skills** — workflow (Discovery → Test, Refactor), OOP patterns, Java/Python layout skills (≤200 lines each).
- **Harness** — Claude Code slash commands, `ddd-architect` and `domain-reviewer` agents.
- **Install** — `scripts/setup/` (bootstrap, install, uninstall, doctor); `scripts/ci/` (lint, smoke-test).
- **Examples** — runnable `examples/order-java` (Spring hexagonal) and `examples/order-python` (FastAPI).
- **Guides** — library loan walkthrough (`docs/guides/library-loan/`) in EN/KO/JA/ZH; harness docs (`docs/cursor.md`, `docs/claude-code.md`, `docs/opencode.md`).
- **Docs** — README in EN/KO/JA/ZH, Before/After, setup command cheat sheet, sample agent outputs.
- **CI** — GitHub Actions: shellcheck, skill lint, isolated HOME smoke test.

### Notes

- **Claude Code / Codex CLI** — supported via symlink install.
- **Cursor** — manifest only (Phase 2); use project `AGENTS.md`.
- **OpenCode** — experimental opt-in (`INSTALL_OPENCODE=1`).

### Install

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

From `~/.oopforge`:

```bash
./scripts/setup/install.sh
./scripts/setup/doctor.sh
./scripts/setup/install.sh update   # after git pull
```
