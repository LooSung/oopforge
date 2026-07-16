# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [0.9.5] - 2026-07-16

C2 도메인 리뷰 자동화 MVP — PR diff에서 **신규 하드룰 위반만** 코멘트하는 read-only 리뷰어.

### Added

- **`scripts/ci/review/`** — 순수 stdlib PR 도메인 리뷰어. `ReviewRun` 애그리거트가 **new-only + line-level** 불변식을 소유(라인 번호 대신 `SubjectKey`로 base↔head 매칭해 라인 시프트 오탐 방지). 어댑터: `changeset`(git diff -U0 파싱)·`detectors`(파일 300줄·스킬 200줄·`domain/` 프레임워크 import)·`delivery`(요약 코멘트 + machine JSON). 검증은 항상 NEUTRAL(비차단).
- **`.github/workflows/domain-review.yml`** — `pull_request`에서 리뷰어 실행, 요약 코멘트를 마커로 멱등 upsert, `review-findings.json` 아티팩트 업로드. 코드 미수정·머지 미차단. OOPforge 레포 자체에 먼저 dogfooding.
- **`scripts/ci/test-review.py`** — 도메인 로직 self-test(diff 파싱·detector·new-only/line-level·delivery). `lint.yml`에 연결.

### Changed

- **플러그인 매니페스트** — `.claude-plugin` / `.codex-plugin` / `.cursor-plugin` `version`을 `0.9.5`로.

### Notes

- MVP 범위: 하드룰만(안티패턴·메서드 20줄·archlint 재사용·waiver·자가교정 루프는 후속). 기존 위반이 "더 나빠지는" 경우는 의도적으로 미탐지(문서화된 트레이드오프).

## [0.9.4] - 2026-07-15

C4의 포지셔닝과 재현 가능한 증거 기준을 확립하고, 검증되지 않은 Cursor headless plugin 주장을 제거했다.

### Added

- **`docs/positioning.md`** — OOPforge의 카테고리, 대상 사용자, 대안 대비 차별점, 비-목표, 증거 기준과 메시지 가드레일을 정의. 측정되지 않은 위반율·재작업 개선을 사실처럼 주장하지 않도록 C4 proof 기준을 명문화.
- **C4 재현 실험 하네스** — `docs/proof/`에 고정 과제·대조군·평가·공개 프로토콜과 결과 템플릿을 추가하고, `scripts/proof/`에 동일 모델 control/OOPforge 실행기와 결정적 평가기를 추가. `auto` 모델·저장소 내부 workspace를 거부하고 control 오염/treatment 로드를 검증하며, 평가기 self-test를 `lint.yml`에 연결.

### Changed

- **README proof 상태** — EN/KO 첫 화면에서 positioning·proof 프로토콜을 연결하고, 유효한 짝 실험 전에는 Before/After 구조 예시를 측정된 개선율로 표현하지 않도록 증거 상태를 명시.
- **Cursor 설정 정정** — clean headless smoke test에서 `--plugin-dir`의 Craft 로드를 증명하지 못해 자동화 경로 주장을 제거. 검증된 프로젝트 로컬 `.cursor/skills/oopforge` 링크를 실험적 설정으로 문서화.
- **Roadmap C4 잔여 범위** — 완료된 positioning·프로토콜은 이력으로 옮기고, 반복 짝 실험 공개와 README Craft 데모만 미래 작업으로 유지.

## [0.9.3] - 2026-07-13

README 랜딩 명확화 — 설치·대상 프로젝트·Craft·수동 업데이트를 Quickstart에서 한눈에 보이게.

### Changed

- **`README.md` / `README.ko.md` Quickstart** — (1) install + `doctor.sh` (2) 대상 프로젝트 `cd` (3) 에이전트 로드·Cursor `--plugin-dir` (4) Craft (5) **Release는 자동 설치 아님** → `git pull` + `install.sh update`.
- **Codex 설치 섹션** — 잘못된 `/oopforge:craft` 예시를 `Use OOPforge craft:`로 수정.
- **플러그인 매니페스트** — version `0.9.3`.

## [0.9.2] - 2026-07-13

백엔드 깊이 — 안티패턴 카탈로그 핵심 4종 + 트랜잭션 경계 스킬. Craft 리뷰·하드룰·리뷰어 체크리스트에 연결.

### Added

- **`skills/antipatterns/anemic-domain.md`** — 도메인 데이터백 + Service에 규칙.
- **`skills/antipatterns/controller-fat.md`** — Controller/Router에 비즈니스 로직·직접 Repository 호출.
- **`skills/antipatterns/repository-with-business-logic.md`** — Repository에 판단·정책·오케스트레이션.
- **`skills/antipatterns/god-aggregate.md`** — 한 Aggregate에 무관한 불변식·생명주기 몰아넣기.
- **`skills/oop/transaction-boundary.md`** — 한 트랜잭션 = 한 Aggregate 수정. 다중 Aggregate 쓰기는 일관성 설계 신호.

### Changed

- **`AGENTS.md`** — 라우팅·Skill Selection·Hard Rule(one Aggregate per TX). Code review가 `skills/antipatterns/`를 참조.
- **`skills/workflow/craft.md`** — 실행 경로에 transaction-boundary·antipattern 매칭. Verification에 안티패턴 spot-check·TX 경계 확인.
- **`skills/SKILL.md`**, **`docs/reviewer-checklist.md`**, **`docs/methodology.ko.md`**, **`docs/roadmap.md`** — 신규 스킬 반영.
- **플러그인 매니페스트** — version `0.9.2`.

## [0.9.1] - 2026-07-13

에이전트 행동 가드레일 — 가정 노출·외과수술식 수정·목표 verify를 Craft에 흡수(Karpathy식 코딩 실패 패턴 대응). 통째 가이드 복제가 아니라 OOPforge 수직 레이어에만 얹음.

### Added

- **`skills/principles/oop-discipline.md` #10 "Surface assumptions before coding"** — 해석이 갈릴 때 조용히 하나 고르지 말고 Assumptions를 먼저 드러냄. Craft Ambiguity resolution과 짝; 새 도메인/대형 기능의 Discovery→Skeleton은 면제하지 않음.
- **`skills/principles/oop-discipline.md` #11 "Surgical changes only"** — 요청에 필요한 곳만 수정. 인접 코드·주석·포맷 드라이브바이 금지. 이번 변경이 만든 orphan만 정리, 기존 죽은 코드는 언급만.
- **`skills/workflow/craft.md` Assumptions 게이트** — OOP Contract 앞에 Assumptions/Alternatives/Why this path 블록. Completion report에 `Scope drift: none | …`.
- **Playbook `verify:`** — `feature.md`·`bug-fix.md` 체크리스트 각 단계에 검증 문장 추가(Goal-Driven 형식 고정).

### Changed

- **`AGENTS.md` Hard Rules** — Surgical changes only 한 줄 추가. Craft 설명에 Assumptions → Contract → surgical scope 검증 순서 반영.
- **`docs/methodology.ko.md`** — 원칙 #10·#11 및 하드룰 외과수술식 수정 개념 반영.
- **플러그인 매니페스트** — `.claude-plugin` / `.codex-plugin` / `.cursor-plugin` `version`을 `0.9.1`로 맞춤(0.8.3에서 정체되어 있던 표기 갱신).

## [0.9.0] - 2026-06-16

스킬 정본 언어를 영어로 통일 — 에이전트가 읽는 지시문을 모국어로 맞추고, 한국어 사용자는 단일 개념 가이드로 흡수한다.

### Changed

- **모든 스킬(`skills/`) 본문·frontmatter를 영어로 번역** (19개 파일; `SKILL.md`·`commands/craft.md`는 기존 영어). skills는 사람이 읽는 문서가 아니라 **에이전트 실행 지시문**이므로, LLM이 설계·구현에서 더 안정적으로 따르는 영어를 **정본**으로 확정. docs 정책(영어 정본)과의 불일치도 해소. 측정 가능 규율·표·코드블록·상호 링크는 그대로 보존, 전 스킬 200줄 하드룰 통과.
- **언어 정책 갱신** — `README.md`·`README.ko.md`·`CONTRIBUTING.md`의 정책 표를 "skills = 영어 정본"으로 변경.

### Added

- **`docs/methodology.ko.md`** — 한국어 개념 가이드 1개. 스킬 1:1 미러가 아니라 방법론·워크플로·Craft·원칙·사다리·DRY·하드룰을 개념 수준으로 설명(미러는 드리프트, 개념 가이드는 안정). v0.8.3에서 JA/ZH 미러를 지운 이유와 동일한 정책.

## [0.8.5] - 2026-06-16

DRY를 DDD 가드레일로 추가 — 순진한 중복 제거가 아니라 "언제 멈출지"를 가르친다.

### Added

- **`skills/principles/oop-discipline.md` #9 "Duplicate before the wrong abstraction"** — SOLID/원칙 감사에서 유일하게 빈칸이던 DRY를 채움. 잘못된 추상화 비용 > 중복 비용 전제 위에 **Rule of Three**(세 번째 중복에야 추상화), **바운디드 컨텍스트 가로지르는 도메인 모델 공유 금지**(닮아도 따로 진화 → 중복이 옳음), **흩어진 비즈니스 규칙만 도메인 행동 메서드로 모으기**(God Service·anemic domain 예방). LSP·OCP·Composition은 수직 정체성상 의도적으로 제외.

## [0.8.4] - 2026-06-16

과설계 방지 "사다리"를 방법론에 도입 — 코드 작성을 마지막 수단으로 강제한다.

### Changed

- **`skills/principles/oop-discipline.md` #7 강화** — 산문 한 문장이던 "Subtract before abstracting"를 작성 직전 **번호 사다리**(존재 필요? → 표준/언어 → 프레임워크 기본 → 기존 의존성 → 한 줄 → 최소)로 명문화. 핵심은 **본질 vs 우발 복잡성 구분**: 사다리는 우발적 복잡성만 깎고 Aggregate 경계·불변식·포트 같은 도메인 구조는 면제. 신뢰 경계 검증·데이터 손실·보안도 어느 칸에서도 생략 금지. 의도적으로 미룬 부분은 upgrade path 표식을 남긴다.
- **`skills/workflow/implement.md`** — 구현 순서 직후에 "작성 직전: 사다리를 밟는다" 게이트 추가. 각 조각을 쓰기 전에 #7 사다리를 거치도록 발화 지점에 연결(도메인 구조·안전 항목 예외 명시).

## [0.8.3] - 2026-06-09

레포 군살 제거 — 죽은/중복 문서를 들어내 유지보수 표면을 줄였다.

### Removed

- **`docs/sample-output/` 전체** — Discovery/Design 샘플 출력은 `docs/guides/library-loan/` 가이드 본문과 중복이라 제거. 메인 README 표·트리·리소스 링크와 가이드의 "Short samples" 섹션 참조도 함께 정리.
- **일본어(JA)·중국어(ZH) 문서 전체** — README 및 `library-loan` 가이드의 `*.ja.md`·`*.zh.md`(~20개) 제거. 솔로 유지보수에서 4개국어 동기화로 인한 번역 드리프트를 막기 위해 **영어 정본 + 한국어** 2개 언어로 축소.

### Changed

- **언어 선택자 정리** — 모든 문서 상단 선택자와 가이드 목차를 `EN · KO`로 통일(README ×2, 가이드 step ×14, 가이드 README ×2, `docs/claude-code.md`, `docs/cursor.md`).
- **예제 개수 표기 수정** — README의 "5 architectures / 5종 아키텍처"를 실제 예제 수에 맞춰 "6 examples / 6종 예제"로 정정.
- **언어 정책을 EN+KO로 명문화** — `CONTRIBUTING.md`·`README.md`의 "KO/JA/ZH 번역 환영" 지시문을 "영어(정본) + 한국어, 그 외 언어는 요청 시에만"으로 변경. 에이전트/기여자가 무심코 JA/ZH 문서를 다시 만들지 않도록 생성 유도 문구 자체를 제거.

## [0.8.2] - 2026-06-09

calculator 예제 패밀리를 대칭으로 완성 — Java에도 hexagonal + CQRS 예제 추가.

### Added

- **`examples/calculator-java-hexagonal-cqrs`** — Spring Boot hexagonal에 CQRS를 얹은 예제. command 측은 write 포트(`CalculationRepository`)로 `CalculationId`만 반환, query 측은 read 포트(`HistoryQueryRepository`)로 `HistorySummary` 프로젝션만 반환. 두 어댑터가 하나의 `CalculationStore`를 공유(쓰기 시 read model로 프로젝션). 이제 java/python 모두 layered/hexagonal/hexagonal-cqrs 3종을 가진다.
- **ArchUnit CQRS 규칙** — `ArchitectureTest`가 domain 프레임워크 의존 0, command↔query 측 상호 비의존, application→adapter 비의존을 강제(`./gradlew test`).
- **CI 강제** — `examples.yml` 매트릭스에 java-hexagonal-cqrs 추가, `arch-lint.yml`이 이 예제에도 `archlint.py cqrs` 실행. 린터 self-test에 실예제 검증 추가.

## [0.8.1] - 2026-06-08

레이어 경계를 업계 표준 도구로 한 겹 더 강제하고, CI Gradle 래퍼 다운로드를 견고화했다.

### Added

- **import-linter (Python layered)** — `calculator-python-layered/.importlinter`에 `layers`(router > service > repository > domain) + `forbidden`(router→repository 직접 import 금지, 간접 경로는 허용) 계약. `arch-lint.yml`에 `lint-imports` 스텝으로 PR 차단.
- **ArchUnit (Java layered)** — `calculator-java-layered`에 `ArchitectureTest`(layeredArchitecture 규칙 + domain 프레임워크 의존 0). `./gradlew test`에 포함되어 examples 워크플로가 그대로 강제.
- **`skills/skeleton/lint-enforcement.md`** — 빠른 stdlib `archlint` 위에 표준 도구(import-linter/ArchUnit)를 얹는 방법. 예제 설정을 정식 복사 템플릿으로 제공(`--with-lint`를 설치 플래그 대신 가이드로 처리).

### Fixed

- **CI Gradle 래퍼 다운로드 타임아웃** — 두 자바 예제의 `gradle-wrapper.properties`가 `networkTimeout=10000`/`retries=0`이라 배포본 fetch가 한 번만 느려도 잡 전체가 실패했다. `networkTimeout=120000`/`retries=3`으로 강화.

## [0.8.0] - 2026-06-08

예제를 하나의 calculator 도메인으로 통일(java/python × layered/hexagonal + hexagonal-cqrs)하고, 모호한 빌드 요청·스택 범위 가드를 추가했다.

### Added

- **Calculator example family** — `calculator-java-layered`, `calculator-java-hexagonal`, `calculator-python-layered`, `calculator-python-hexagonal`, `calculator-python-hexagonal-cqrs`. One easy-to-grasp domain (calculator + history) across every architecture, replacing the harder-to-read `order-*` examples. CQRS is shown as an overlay on hexagonal (separate command/query ports), not as a peer architecture.
- **`archlint.py` Python support** — layered (router/service/repository folders, router→repository ban) + CQRS (`*query_service.py` / `*command_service.py`), enforced in CI on the layered and CQRS calculator examples.

### Changed

- **Ambiguity & stack scope guard** — under-specified build requests (e.g. "make a calculator") are now handled: `skills/workflow/craft.md` adds a "모호성 해소" step (state defaults, ask only decision-critical questions), and `skills/lang/backend-stack.md` adds a scope gate — OOPforge targets Java Spring / Python FastAPI only; unsupported stacks (JS/TS, frontend, CLI) are flagged as out of scope instead of silently built. `SKILL.md` trigger broadened to catch everyday backend build prompts.
- **Example naming convention** — standardized on `{domain}-{lang}-{architecture}` (`layered` / `hexagonal` / `cqrs`). `4-tier` intentionally avoided: hexagonal is ports & adapters, not a tier count.
- **`skills/skeleton/backend-skeleton.md`** — Python layered now uses per-layer **folders** (router/ service/ repository/ domain/) with wiring in `app/core/`, matching the v0.7 layer-layout Hard Rule.

### Removed

- **`examples/order-*`** (`order-java`, `order-java-layered`, `order-python`, `order-python-layered`) — replaced by the calculator family.

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
