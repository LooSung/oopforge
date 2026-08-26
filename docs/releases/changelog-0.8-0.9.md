# OOPforge changelog — 0.8.x to 0.9.x

Historical entries moved from the root changelog to keep each tracked file
within the repository's 300-line review limit.

## [0.9.7] - 2026-08-11

### Added

- **Comment discipline** — LLM이 남기는 장황한 "what" 주석을 줄이기 위해 `oop-discipline`에 narration comment 금지 원칙을 추가. 인접 코드 설명 주석은 삭제하거나 이름/메서드 추출로 대체하고, 주석은 why·외부 제약·숨은 불변식·추적되는 임시 결정에만 남기도록 명시.
- **Craft 검증 항목** — 완료 전 comment discipline을 확인하도록 Verification에 `names explain what, comments explain why` 체크를 추가.
- **AGENTS 하드룰 보강** — OOPforge 레포 자체 규칙에도 narration comment 금지와 rename/extract 대체 기준을 추가.

## [0.9.6] - 2026-08-11

### Fixed

- **Craft 실행 지시문 정정** — "The goal is not to add code" 문구를 "code volume이 목표가 아니다"로 바꿔, 필요한 구현은 진행하되 최소 변경을 유지하도록 명확화.
- **비-OOP 작업 경로** — 환경·툴링·문서·운영·조사 작업은 한 줄로 선언하고 Assumptions/OOP Contract를 건너뛰되 Verification/Scope drift는 유지하도록 Craft 라우팅을 추가.
- **원인 주장 검증 게이트** — 원인을 기록하기 전에 반증 가능한 관찰 하나를 확보하도록 `oop-discipline`에 원칙 추가.
- **검증 결과 재현성** — 테스트 수치와 함께 인터프리터 경로/버전, 환경변수 같은 툴체인 정체를 기록하도록 Craft Verification 보강.
- **continuity 모순 정정** — 새 발견이 기존 기록과 어긋나면 work dir 전체를 검색해 앞선 주장도 함께 정정하도록 규칙 추가.
- **프로젝트 규칙 참조 정정** — `AGENTS.md`에 "Hard Rules" 절이 있다고 가정하지 않고, 프로젝트가 선언한 규칙을 이름으로 지목하도록 스킬 문구 정리.
- **OOPforge 자체 유지보수 예외** — `skills/workflow/craft.md`, `skills/SKILL.md`, `docs/claude-code.md`, `docs/codex.md`, `docs/cursor.md`에 OOPforge pack repository를 고치는 작업은 pack root가 올바른 work target임을 명시.

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
