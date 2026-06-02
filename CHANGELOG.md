# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [Unreleased]

## [0.3.0] - 2026-06-02

대규모 surface 정리 — 단일 진입점, 스킬 통합, 실험적 통합 제거.

### Added

- **`/oopforge:craft`** — 단일 사용자 진입점. 요청을 보고 가장 작은 OOP 경로를 선택하거나 추천한다.
- **`skills/workflow/craft.md`** — Craft 실행 오케스트레이터 (분류, OOP Contract, 경로 선택, 검증, 완료 보고).
- **`skills/oop/domain-model.md`** — Aggregate, Value Object, Domain Event, Factory Method 규칙 통합.
- **`skills/oop/use-case-boundary.md`** — Application Service, Repository Port 경계 규칙 통합.
- **`skills/lang/backend-layout.md`** — Java Spring + Python FastAPI 레이아웃·OpenAPI 규칙 통합.
- **`skills/principles/oop-discipline.md`** — 개념적 OOP 원칙 (책임, 경계, 테스트, 구조 학습).
- **`skills/playbooks/feature.md`**, **`skills/playbooks/bug-fix.md`** — 기능 추가·버그 수정 전용 체크리스트.

### Changed

- **`/oopforge:craft`로 리네임** — 이전 `/oopforge:forge` 진입점 제거.
- **스킬 통합** — 17개 개별 skill 파일(oop/\*, lang/java/\*, lang/python/\*, lang/api/\*, _meta/\*)을 3개 통합 파일로 교체.
- **`agents/` 제거** — `ddd-architect`, `domain-reviewer` 서브에이전트 파일 및 설치 심볼릭 링크 제거.
- **OpenCode 제거** — `.opencode/`, `docs/opencode.md`, 설치 스크립트의 opt-in 블록 제거.
- **빈 폴더 정리** — `skills/lang/java/`, `skills/lang/python/`, `skills/lang/api/` 제거.
- **`commands/`** — 개별 단계별 커맨드 파일 제거, `craft.md` 하나만 유지.

### Removed

- `commands/route.md`, `commands/forge.md` 및 모든 단계별 slash command 파일
- `skills/workflow/forge.md` (→ `craft.md`로 대체)
- `skills/playbooks/refactor.md` (→ `skills/workflow/refactor.md`로 통합)
- `agents/ddd-architect.md`, `agents/domain-reviewer.md`
- `.opencode/`, `docs/opencode.md`
- 17개 개별 skill 파일 (oop/\*, lang/java/\*, lang/python/\*, lang/api/\*, skills/_meta/\*)

## [0.2.2] - 2026-06-02

Layered runnable proofs for all 4 stacks; Python standardized on FastAPI only.

### Added

- **`examples/order-java-layered/`** — Spring 3-tier place-order, springdoc, domain + OpenAPI contract tests.
- **`examples/order-python-layered/`** — FastAPI 3-tier place-order (Router/Service/Repository), pytest + OpenAPI smoke.
- **`examples/README.md`** — stack command ↔ folder mapping for all runnable proofs.

### Changed

- **README (EN/KO/JA/ZH)** — examples table links to 4 runnable projects + index.
- **`docs/roadmap.md`** — proof-gap sprint checklist complete.
- **Flask removed** — `python-flask-layered` skeleton and `flask-layered-layout.md` deleted. Python stacks are `python-fastapi-layered` and `python-fastapi-clean` only (**4 stacks total**).
- **OpenAPI / skeleton docs** — Flask references removed from backend layout guidance, skeleton workflow docs, and `AGENTS.md`.

## [0.2.1] - 2026-06-01

_Skipped tag — changes folded into [0.2.2]._

## [0.2.0] - 2026-06-01

3-tier layered support, Python 1급 시민화, OpenAPI 기본 탑재, intent routing.

### Added

- **3-tier layered layouts** — Java/Python layered layout guidance. Controller/Service/Repository(+config/infrastructure) 구조. 헥사고날까지 필요 없는 작은 서비스의 기본 진입점.
- **OpenAPI/Swagger conventions** — Java/Python API docs guidance. springdoc(Java) / FastAPI 내장 / flask-smorest(Flask) 기본 탑재.
- **Python 1급 시민화** — Python 도메인 패턴 커버리지 균형. Flask 레이아웃 추가로 백엔드 프레임워크 커버리지 확장.
- **Intent routing command** — 사용자 의도(신규 도메인/기존 확장/단일 컴포넌트/리팩토링)에 맞춰 최소 단위 스킬·커맨드만 추천. 전체 워크플로 강제 안 함.
- **Roadmap** — `docs/roadmap.md`. 단기/중기/장기 방향, 비-목표, 성공 지표.

### Changed

- **Skeleton command/workflow** — 스택 선택지를 5종(`java-spring-layered`, `java-spring-hexagonal`, `python-fastapi-layered`, `python-fastapi-clean`, `python-flask-layered`)으로 확장. API 백엔드는 OpenAPI 컨벤션 스킬을 함께 적용.
- **Java/Python 기존 레이아웃 스킬** — 체크리스트에 OpenAPI 항목 추가.
- **AGENTS.md / skills/SKILL.md** — Route 단계, layered/hexagonal 분리, Python 패턴/OpenAPI/roadmap 링크 등재.
- **README (EN/KO/JA/ZH)** — intent routing examples, 5종 스택 표, Flask, OpenAPI 기본 탑재, What's Inside 트리, roadmap 링크 반영.
- **Codex** — add `skills/SKILL.md` as the Codex skill entry point so the Forge prompt routes to OOPforge workflows.
- **Docs** — add `docs/codex.md` and clarify Codex vs Claude Code command usage.
- **Cursor** — document Cursor Agent CLI setup via `cursor-agent --plugin-dir ~/.oopforge`; remove project-rules / `.cursor/skills` symlink guidance.
- **docs/cursor.md** — rewrite for CLI `--plugin-dir` workflow.
- **doctor.sh** — show `--plugin-dir` load command instead of AGENTS.md project-rules warning.

## [0.1.0] - 2026-05-29

Initial public release — portable OOP/DDD methodology pack for AI coding agents.

### Added

- **Skills** — workflow (Discovery → Test, Refactor), OOP patterns, Java/Python layout skills (≤200 lines each).
- **Harness** — Claude Code `/oopforge:craft` slash command and skill entry points.
- **Install** — `scripts/setup/` (bootstrap, install, uninstall, doctor); `scripts/ci/` (lint, smoke-test).
- **Examples** — runnable `examples/order-java` (Spring hexagonal) and `examples/order-python` (FastAPI).
- **Guides** — library loan walkthrough (`docs/guides/library-loan/`) in EN/KO/JA/ZH; harness docs (`docs/cursor.md`, `docs/claude-code.md`).
- **Docs** — README in EN/KO/JA/ZH, Before/After, setup command cheat sheet, sample agent outputs.
- **CI** — GitHub Actions: shellcheck, skill lint, isolated HOME smoke test.

### Notes

- **Claude Code / Codex CLI** — supported via symlink install.
- **Cursor** — manifest only (Phase 2); use project `AGENTS.md`.
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
