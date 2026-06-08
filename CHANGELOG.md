# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [Unreleased]

## [0.7.1] - 2026-06-08

v0.7.0 follow-up — Cursor manifest parity + Hard Rules CI enforcement.

### Added

- **아키텍처 린터 (`scripts/ci/archlint.py`) + CI 차단 (`.github/workflows/arch-lint.yml`)** — Layer layout·CQRS Hard Rule을 기계적으로 강제(모델 준수에 비의존). `scripts/ci/test-archlint.py`로 린터 자체를 CI에서 자가 검증. layered 예제만 검사(헥사고날 제외). 순수 stdlib.

### Fixed

- **`.cursor-plugin/plugin.json` 버전** — Claude/Codex manifest와 동일하게 `0.7.0`으로 맞춤(v0.7.0 릴리스 시 누락).

## [0.7.0] - 2026-06-08

작은 모델 견고성 라운드 — 암묵적 가이드를 명시적·검증 가능·결정론적 체크로 전환.

### Added

- **CQRS 스킬 (`skills/oop/cqrs.md`)** — 미디엄 수준(Command/Query 분리, 스토어 공유). layered/헥사고날 매핑, 진입 기준 체크리스트, 금지. event-sourcing은 범위 밖(장기).
- **안티패턴 카탈로그 시작 (`skills/antipatterns/flat-package.md`)** — layered인데 레이어를 폴더로 안 나누고 파일명 suffix로만 분리한 안티패턴: 증상·원인·교정.
- **Hard Rules — Layer layout** — layered는 각 레이어가 별도 폴더, 파일명 분리 금지, Controller→Repository 직접 호출 금지.
- **Hard Rules — CQRS** — 쿼리 측 부수효과 금지, 커맨드 측 read-shaped 반환 금지(ID/void).
- **스켈레톤 셀프 체크 게이트 (`skills/skeleton/backend-skeleton.md`)** — 스켈레톤 직후 디렉터리 트리로 레이어 폴더 존재를 직접 확인·보고. `skills/workflow/skeleton.md` 체크리스트에 연결.
- **프로젝트 설정 디렉티브 (`AGENTS.md`)** — `OOPforge continuity: off` 추가 문서화.

### Changed

- **Continuity 자동 생성 (opt-out)** — opt-in 묻기를 폐기하고, 실행 작업(feature/refactor/bugfix)이면 `.craft/<kind>-<slug>.md`를 묻지 않고 자동 생성한 뒤 한 줄 고지. advisory·초소형 작업은 생성 안 함. `OOPforge continuity: off`로 끌 수 있음.
- **Craft 완료 게이트 (`skills/workflow/craft.md`)** — continuity 문서가 있으면 그 문서를 갱신하기 전에는 done 보고 금지. 시작 0번 스텝을 자동 생성으로 변경.
- **`skills/SKILL.md` / `AGENTS.md` 라우팅** — CQRS·안티패턴 스킬 항목 추가.
- **`skills/lang/backend-stack.md`** — CQRS를 layered/헥사고날 위에 얹는 변형으로 명시.

## [0.6.3] - 2026-06-02

Continuity opt-in — `.craft`는 사용자가 원할 때만.

### Changed

- **Continuity (opt-in)** — `.craft/<kind>-<slug>.md` 생성 전 Craft가 사용자에게 먼저 묻는다. 거절하면 넘어간다. 명시적 요청·기존 문서 이어가기는 예외.
- **`skills/workflow/continuity.md`** — 첫 세션을 선택(opt-in)으로 변경; 확인 없이 `.craft/` 생성 금지.
- **`skills/workflow/craft.md`** — 시작 시 묻기, 완료 시 문서 **있을 때만** 갱신.
- **README (EN/KO/JA/ZH)** — memory store 섹션에 opt-in 안내.

## [0.6.2] - 2026-06-02

Codex 호출 방법 문서 정정 및 대상 프로젝트 경로 규칙.

### Changed

- **README Quickstart (EN/KO/JA/ZH)** — Craft 3단계를 하네스별로 분리: Claude/Cursor는 `/oopforge:craft`, Codex는 `$oopforge` + `craft:` (선행 `/` 없음).
- **`docs/codex.md`** — Codex에서 `/oopforge:craft`가 동작하지 않는 이유, `/skills`/`$oopforge` 호출법, **대상 프로젝트에서 `codex` 시작** 안내.
- **`docs/cursor.md`** — `/oopforge:craft` 슬래시 커맨드, 대상 프로젝트에서 `--plugin-dir` 실행.
- **`skills/SKILL.md`** — 하네스별 진입점 + **Project vs pack** 경로 규칙.
- **`skills/workflow/craft.md`** — 시작 절차에 대상 프로젝트 확인 및 사용자 파일 경로는 팩이 아닌 작업 레포 기준 해석.

## [0.6.1] - 2026-06-02

연속성 기능 다듬기.

### Changed

- **작업 폴더 이름** — 설치 팩 경로 `~/.oopforge`와의 혼동을 피하려 작업 디렉터리를 `.oopforge/` → **`.craft/`**로 변경.
- **README (EN/KO/JA/ZH)** — 워크플로 섹션에 "기억 저장소(세션 간 이어가기)" 안내 추가.

## [0.6.0] - 2026-06-02

세션 간 작업 연속성(메모리) 도입.

### Added

- **`skills/workflow/continuity.md`** — 작업당 단일 문서(`.oopforge/<kind>-<slug>.md`)에 결정·진행·다음 할 일을 누적하고, 다음 세션에서 먼저 읽어 맥락을 복원하는 연속성 규칙. work dir은 기본 `.oopforge/`(gitignore), 대상 프로젝트 `AGENTS.md`의 `OOPforge work dir:` 한 줄로 오버라이드.

### Changed

- **Craft** — 시작 절차에 Resume(기존 작업 문서 읽기), 완료 시 작업 문서 갱신을 연결.
- **AGENTS.md** — Skill Routing/Selection에 continuity 추가.

## [0.5.2] - 2026-06-02

릴리스 표면 정리 및 README 첫 화면 축소.

### Changed

- **README (EN/KO/JA/ZH)** — Quickstart를 설치 → 재시작 → `/oopforge:craft` 3단계만 남기고, 스택 표·Craft 상세·하네스 링크는 **Advanced Usage**로 이동.
- **Public roadmap** — 런칭 채널·내부 KPI 제거; 공개용 방향·비-목표·기여 우선순위만 유지.
- **`.gitignore`** — `docs/planning/` 추가 (내부 계획 메모). `docs/release/` tracked 파일 untrack.

### Removed

- **GitHub topic `flask`** — Python 스택은 FastAPI layered/clean만 지원 (4 stacks).
- **`docs/release/` from git** — 릴리스 초안은 로컬/internal only.

## [0.5.1] - 2026-06-02

CI 안전망 보강.

### Added

- **Cron 실패 알림** — 주간 스케줄 `examples` 빌드가 실패하면 이슈를 자동 생성해 의존성 드리프트를 능동적으로 표면화.

### Changed

- **GitHub Actions Node 24 대응** — `actions/checkout@v4→v5`, `actions/setup-java@v4→v5`, `actions/setup-python@v5→v6` (lint·examples 워크플로 모두). 2026-06-16 Node 20 강제 종료 대비.

## [0.5.0] - 2026-06-02

예제 검증 CI 추가 및 스택 버전 안정화.

### Added

- CI builds and tests all four runnable examples (Java 21 + Python 3.12 matrix).

### Changed

- **Example stacks pinned to current stable LTS** — Java 17 → **Java 21 LTS**, Spring Boot 3.4.1 → **3.5.14**; Python `>=3.11` → **`>=3.12`**, FastAPI `>=0.115.0` → **`>=0.136.3`**. All four examples build and test green on the new versions.

## [0.4.1] - 2026-06-02

README 메시지 정리.

### Changed

- **README 헤드라인 (EN/KO/JA/ZH)** — "AI ships the feature. OOPforge keeps the architecture." 헤드라인과 "Forge small. Compose forever." 태그라인을 도입하고, 장황한 소개 단락을 압축.
- **Reference** — 스킬 라우팅과 "가장 작은 경로" 철학 참고로 [pstack by Lauren (Cursor)](https://cursor.com/en-US/lp-team/lauren) 추가.

## [0.4.0] - 2026-06-02

스킬 경계 정리 — 스택 선택과 스켈레톤 구조를 분리.

### Added

- **`skills/lang/backend-stack.md`** — 백엔드 스택 선택 (지원 스택, layered vs hexagonal/clean 기준, OpenAPI 기본 방침).
- **`skills/skeleton/backend-skeleton.md`** — 선택된 스택별 패키지 구조, 빈 타입, 공통 경계 규칙, 스켈레톤 금지사항.

### Changed

- **Stack vs skeleton split** — `skills/lang/backend-layout.md`를 위 두 파일로 분리. Skeleton workflow, AGENTS.md, README/docs/examples 참조를 모두 갱신.
- **Craft 검증** — `docs/reviewer-checklist.md`를 더 넓은 레이어별 리뷰 단계로 연결.
- **`doctor.sh`** — `skills/skeleton/` 디렉터리 구조 검사 추가.

### Removed

- **`skills/lang/backend-layout.md`** — 스택 선택과 스켈레톤 구조 책임이 섞여 있어 분리 후 제거.

## [0.3.1] - 2026-06-02

문서 표면 정리 — Craft 중심 README와 하네스별 적용 방법 보강.

### Changed

- **README (EN/KO)** — simplify the first screen around `/oopforge:craft <request>` and add concise Claude Code, Codex CLI, and Cursor Agent CLI setup sections.
- **Terminology cleanup** — align remaining execution-mode wording from Forge to Craft in agent instructions, skills, examples, roadmap, and setup docs.

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
