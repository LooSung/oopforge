# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [Unreleased]

### Added
- `scripts/smoke-test.sh` — isolated HOME install/doctor/update/uninstall verification.
- CI: `bash -n`, smoke test step in lint workflow.
- README CI badge, Troubleshooting section.
- `scripts/path-convention.md` — unified skill path rules.
- Lint check: fail on legacy `skills/oopforge/` paths in commands/agents.
- README Before/After section (EN/KO) with God Service vs OOPforge structure comparison.
- `examples/order-java/` — runnable Spring hexagonal place-order reference with domain tests.
- `examples/order-python/` — runnable FastAPI hexagonal place-order reference (mirrors Java).
- Harness guides: `docs/cursor.md`, `docs/claude-code.md`, `docs/opencode.md`.
- `agents/domain-reviewer.md` — God Service, framework leakage, layer violation review.
- AGENTS.md Skill Routing table (workflow stage → skill → agent).
- GitHub Actions lint workflow: shellcheck, skill frontmatter, 200-line limit, plugin JSON, AGENTS.md references.
- `scripts/lint-skills.sh` for local and CI validation.
- `install.sh update` subcommand and `--force` flag for symlink refresh after upgrades.
- README language policy section; shell script messages unified to English.
- Hard Rules numeric rationale in `AGENTS.md` and README files.
- Explicit Cursor status: Not yet (Phase 2), no installer, no ETA.

### Changed
- Commands and `ddd-architect` use `{pack}/skills/...` paths (`$OOPFORGE_HOME` → `~/.oopforge` → repo root).
- README Why/Inspiration: OOPforge-only philosophy; removed superpowers/SuperClaude references (all locales).
- Plugin READMEs: removed external pack references.
- `bootstrap.sh` runs `install.sh update` instead of plain `install.sh`.
- `doctor.sh` warns that Cursor has manifest only (no install target).
- Cursor README table status changed from "Prepared" to "Not yet (Phase 2)" across all README locales.
- 기본 README 언어를 영어로 전환하고 한국어, 일본어, 중국어 README를 추가.
- 기본 README를 Quickstart, Installation, Basic Workflow, What's Inside, Philosophy 중심으로 재구성.
- README에 권장 workflow 순서와 단일 명령 사용 예시 추가.
- Java/Python Skeleton 기본 패키지 구조를 Splearn-style Spring, Clean FastAPI layout으로 정리.

## [0.1.0] - 2026-05-29

### Added
- 초기 구조 (`skills/`, `agents/`, `commands/`)
- 에이전트 자동 로딩을 위한 루트 지시 파일 `AGENTS.md`, `CLAUDE.md` 추가.
- 메타 스킬: `skills/_meta/skill-template.md`
- 워크플로우 스킬: discovery, design, skeleton, implement
- 워크플로우 스킬 `delivery-plan`, `test`, `refactor` 추가.
- OOP 스킬: aggregate-root, value-object, application-service, repository-port
- Java 스킬: spring-hexagonal-layout, jpa-repository
- Python 스킬: pydantic-value-object, clean-fastapi-layout
- Subagent: `ddd-architect`
- Slash commands: discovery, design, skeleton, implement
- `install.sh`, `uninstall.sh` (Claude Code, Codex CLI, OpenCode 자동 감지)
