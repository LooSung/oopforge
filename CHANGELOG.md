# Changelog

완료된 사용자 가시 변경은 릴리스 전 `Unreleased`에 기록한다.
[Keep a Changelog](https://keepachangelog.com/) 형식.
미래 계획, 백로그, 내부 지표는 이 파일에서 관리하지 않는다.

## [Unreleased]

### Fixed

- **Cursor Test source isolation** — 전역 OOPforge Test intent가 임시 후보보다
  먼저 선택돼도 실행별 probe가 explicit/project-local 후보를 구분한다.

## [1.4.1] - 2026-08-26

### Fixed

- **설치본 Claude live smoke** — Bash 3.2의 `set -u`에서 빈 배열 확장이 중단되던 경로를 명시적 installed/candidate 분기로 교체했다.

## [1.4.0] - 2026-08-26

### Added

- **Test command** — Claude Code의 `/oopforge:test`와 Codex/Cursor의
  `Use OOPforge test: …`가 저장소 근거로 가장 작은 테스트 범위를 고르며,
  제품 코드 변경과 자동 E2E 실행을 금지한다.

### Changed

- **공개 커맨드 안내** — 영문·한국어 README와 세 하네스 설정 문서에서
  Craft, Refactor, Consult, Test의 호출법과 서로 다른 쓰기 범위를 바로 보여준다.
- **하네스 Test 근거** — 정적 패키징 검사와 세 하네스의 Test 전용
  positive/source-isolated negative live smoke를 추가했다.

## [1.3.1] - 2026-08-25

### Fixed

- **Harness live-smoke isolation** — Codex negative token의 무해한 문장부호를
  허용하면서 loaded-token 충돌은 계속 차단하고, Cursor는 실행별 임시 source
  probe로 전역 Claude skill 자동 발견과 현재 후보 로드를 구분한다.

## [1.3.0] - 2026-08-25

### Added

- **Refactor command** — Claude Code의 `/oopforge:refactor`와 Codex/Cursor의
  `Use OOPforge refactor: …`가 기존 동작 보존 Refactor workflow로 직접 진입한다.
- **Consult command (experimental)** — 질문·대안·검토·명시적 계획 문서를
  answer/proposal/review/document 중 한 모드로 처리하며 기본은 읽기 전용이다.

### Changed

- **Craft command boundary** — Craft를 호환 가능한 기본 진입점으로 유지하면서,
  명시적인 리팩터 요청은 기능 변경을 금지하는 좁은 command 계약으로 분리했다.
- **Cursor 검증 경계 문서화** — 명시적 plugin과 project-local 로드는 동작하지만,
  최신 CLI가 전역 Claude skill도 발견해 source-isolation negative control을
  오염시킬 수 있음을 지원 범위에 기록했다.

## [1.2.0] - 2026-08-25

### Changed

- **공개 문서 책임 축소** — 공개 로드맵과 분산된 future-work 표현을 제거하고,
  tracked 문서는 현재 동작·지원 범위·검증 근거·완료 이력만 설명하도록 정리했다.
- **루트 문서 정리** — GitHub가 자동 인식하는 기여·행동강령·보안 정책을
  `.github/`로 이동하고 기여 가이드의 실제 스킬 규칙과 Covenant 버전을
  저장소 기준에 맞췄다.
- **하네스 경로 정합성** — Claude 매니페스트 스키마, Cursor skill 상대 경로와
  command 범위, 설치 환경변수 및 6단계 워크플로 설명을 실제 지원 계약에 맞췄다.
- **가이드와 검증 정렬** — library-loan walkthrough의 Delivery Plan·조립·이벤트
  경계를 보완하고 Proof 입력 고정, fork PR delivery, 예제 검증 명령을 교정했다.
- **릴리스 이력 보관** — 300줄 리뷰 한계를 지키면서 과거 기록을 보존하도록
  0.x 이력을 [`docs/releases/`](docs/releases/)로 분리했다.

## [1.1.1] - 2026-08-24

### Fixed

- **Python 테스트 타입 게이트** — 세 FastAPI 참조 프로젝트의 strict mypy
  범위를 `tests`까지 확장하고 fixture·fake·negative test 타입 오류를
  suppression 없이 바로잡았다.

## [1.1.0] - 2026-08-24

### Added

- **Python Pydantic 타입 안전성** — FastAPI 경계의 직접 Pydantic 의존성,
  mypy 공식 플러그인, strict 정적 검사, 요청 계약 테스트를 정본 스킬과 세
  Python 계산기 예제에 추가했다.

### Changed

- **명시적 요청 계약** — 계산 요청은 알 수 없는 필드, 숫자 문자열,
  `NaN`/`Infinity`를 거부하고 CQRS 시간 응답은 OpenAPI `date-time` 의미를
  보존한다.

## [1.0.0] - 2026-08-21

### Added

- **3-Harness 지원 범위** — Claude Code, Codex CLI, Cursor Agent CLI의 canonical
  로드 경로와 Craft 호출을 문서화하고 같은 후보에서 재검증했다.
- **스킬 성숙도 레지스트리** — 배포되는 모든 스킬을 `stable` 또는
  `experimental`로 등록하고 정적 검사로 누락과 중복을 차단한다.
- **재현 가능한 활성화 검사** — 세 하네스의 positive control, 격리된
  negative control, advisory Craft 라우팅 증거를 기록했다.
- **v1 핵심 호환성 계약** — canonical load path, Craft 호출, 단계·체크포인트,
  Hard Rule, OOP Contract, stable 기본 경로의 1.x SemVer 경계를 명시했다.
- **강제 timeout 실행기** — 로컬 하네스 프로브가 자식 프로세스와 함께 제한
  시간 안에 종료되는 표준 라이브러리 기반 실행기와 자체 테스트를 추가했다.

### Changed

- **문서 책임 분리** — `docs/`를 setup, reference, project, verification으로
  구조화하고 탐색 인덱스와 전체 내부 링크를 정렬했다.
- **릴리즈 위생** — 보안 정책, 하네스 호출 예시, issue/workflow 템플릿과
  v1 로드맵을 실제 지원 범위에 맞췄다.
- **라이브 검증 가시성** — 세 하네스의 CLI 버전과 각 positive/negative probe
  시작을 출력하고, provider credential은 로컬 검증에만 사용하도록 명시했다.

## [0.15.0] - 2026-08-20

### Added

- **Production Readiness gate** — 명시적 deploy/production 요청에만 입력 검증,
  safe error, API 멱등성, retry/timeout, 관측성, audit, PII·secret 정책을
  adapter 책임으로 적용하는 workflow를 추가했다.
- **Java/Python NFR 경계 테스트** — plain hexagonal API에서 invalid input,
  duplicate replay/conflict, safe domain/unexpected error, generated/provided
  correlation ID, secret-free audit를 실행 테스트로 고정했다.

### Changed

- **조건부 workflow 연결** — Craft, Delivery Plan, Implement, Test, reviewer
  checklist가 Production Readiness를 배포 신호가 있을 때만 선택한다.
- **운영 adapter reference** — 두 언어의 in-memory 예제가 idempotency,
  correlation, observability, audit를 domain 변경 없이 처리한다. 실제 배포에는
  durable shared store로 교체해야 함을 문서화했다.

## [0.14.0] - 2026-08-20

### Added

- **Domain Events 스킬** — Domain Event와 Integration Event, save 후
  pop/dispatch, handler 경계, outbox 전달, message-ID 멱등성, schema versioning을
  한 실행 계약으로 정의했다.
- **Java/Python 실행 reference** — plain hexagonal 계산기가 같은 트랜잭션의
  Aggregate 저장과 versioned outbox append, commit 후 relay, 멱등 소비자를
  domain/use-case/integration 테스트로 증명한다.

### Changed

- **이벤트 책임 분리** — domain model, use-case boundary, transaction boundary,
  outbox 스킬의 중복을 제거하고 Domain Events 스킬로 교차 연결했다.
- **미사용 이벤트 제거** — layered/CQRS 계산기에서 소비자 없이 기록 후 버리던
  이벤트를 제거해 필요한 구조만 남겼다.

## [0.13.0] - 2026-08-20

### Added

- **정합 proof pair 4** — 교정된 reference와 schema-v2 evaluator로 같은 고정
  작업을 다시 실행했다. 두 조건 모두 기계·사람 판정 0건으로 일치했으며 원시
  비교 artifact는 GitHub Release에 첨부한다.

### Changed

- **Reference 정렬** — layered·hexagonal 예제의 경계 규칙과 문서를 같은
  정본 템플릿에 맞췄다.
- **Evaluator 통합** — proof 평가가 domain-review detector와 공통 finding ID를
  재사용하며 schema v2로 공개 mutable 도메인 상태까지 기계 검출한다.
- **Plain hexagonal 차단 게이트** — Python은 import-linter, Java는 Gradle의
  ArchUnit으로 경계를 검사해 저장소 CI 실패 시 PR을 차단한다.
- **Adopter 정책** — 기본 domain-review 템플릿은 non-blocking 피드백이며,
  import-linter/ArchUnit 필수 상태 검사는 adopter가 명시적으로 opt-in한다.

## [0.12.2] - 2026-08-20

### Changed

- **v0.13.0 C1 릴리스 범위** — reference 예제, proof/domain-review evaluator,
  hexagonal 경계 검사, CI 차단 정책과 재현 artifact를 같은 규칙으로 정렬하는
  다음 minor 릴리스를 로드맵에 고정했다.

### Fixed

- **증거보다 강한 방법론 표현** — 제한된 공개 proof를 일반 효과처럼 읽히게 한
  문구와 모든 하드룰이 CI에서 차단된다는 설명을 실제 검증·차단 범위에 맞췄다.

## [0.12.1] - 2026-08-20

### Changed

- **첫 사용자 온보딩** — 영문·한국어 README를 300줄 이하의 사용자 동선으로
  재구성하고 Quickstart, Craft 성공 기준, 핵심 workflow, 근거와 설치 수명주기를
  앞에서부터 읽히는 순서로 정리했다.
- **하네스별 활성화 안내** — `doctor.sh`의 범위와 Claude/Codex/Cursor의 실제
  Craft 진입점을 분리하고, main 추적·릴리스 고정 clone의 업데이트 및 Cursor
  수동 링크 제거 절차를 명시했다.

### Fixed

- **Codex·Cursor 호출 혼동** — 한국어 문서가 Codex에 Claude 전용
  `/oopforge:craft`를 권하던 오류를 제거하고 자연어 Craft 진입점으로 통일했다.
- **설치 검증과 제거 안전성** — doctor가 Cursor 패키징 어댑터를 검사하고 검증된
  설정 문서를 안내한다. uninstall은 다른 대상을 가리키는 동명 symlink를
  보존하며 smoke test가 이 동작을 고정한다.

## [0.12.0] - 2026-08-20

### Added

- **Cursor 로컬 플러그인 어댑터** — Cursor 규약의
  `skills/oopforge/SKILL.md` 패키징 어댑터를 추가했다. 격리한 빈 작업공간에서
  `--plugin-dir ~/.cursor/plugins/local/oopforge`가 Craft 지침을 자동 로드함을
  검증했다. 디렉터리 자동 탐색과 `/oopforge:craft`는 실패 결과 그대로 남긴다.
- **문서 링크 무결성 CI** — git 추적 Markdown의 상대 파일과 heading anchor를
  stdlib-only 검사기로 검증하고 self-test를 `lint.yml`에 연결했다.

### Changed

- **Agent Skills 정렬** — 루트 Skill에 license·compatibility 메타데이터를
  추가하고, Craft command의 공식 `name` frontmatter와 세 manifest 버전·Cursor
  component 경로를 저장소 lint로 강제한다.

### Fixed

- **끊긴 문서 링크** — Claude Code 가이드의 library-loan 링크 두 개를 고치고,
  proof result template을 프로토콜 문서에서 직접 연결했다.

### Removed

- **반영 완료된 피드백 원문** — v0.9.5 개선 항목이 모두 스킬에 반영된 뒤에도
  고아로 남아 있던 `docs/feedback/2026-08-11.md`를 제거했다.

## [0.11.0] - 2026-08-20

### Added

- **Transactional Outbox 스킬 (`skills/oop/outbox.md`)** — 상태 변경과 나가는
  이벤트를 같은 트랜잭션 한 커밋에 넣고, 전달은 그 기록에서 따로 한다.
  publish-후-commit이 만드는 ghost 이벤트와 commit-후-publish가 만드는 lost
  이벤트를 실패 표로 가르치고, outbox 행이 **두 번째 Aggregate가 아님**을 못
  박아 "한 TX 한 Aggregate"와 충돌하지 않게 했다. 전달 기본값은 폴링 relay,
  CDC는 이미 로그 기반 파이프라인이 있을 때만. at-least-once만 약속하고
  중복 제거는 소비자 멱등성으로 넘긴다. saga·이벤트 스키마 버저닝은 범위 밖(장기).

## [0.10.0] - 2026-08-20

### Added

- **C4 반복 Proof 3짝** — Cursor `gpt-5.6-sol-high`로 유효한 control/OOPforge
  짝 세 개를 공개했다. 1은 중립, 2·3은 메서드 길이에서 유리. 불리한 짝은
  이 조건에서 관측되지 않았고 그 부재를 기록한다. 세 짝 모두 공개
  mutable `voided_at` 유출이 남았다. 일반 개선율로 쓰지 않는다.
- **Craft asciinema** — Assumptions·OOP Contract·검증 게이트를 보여주는
  예시 세션을 README에 연결했다. 재구성 재생이며 라이브 tty가 아니다.
- **C2+ 도메인 리뷰 확장** — 공개 mutable 도메인 필드 탐지, archlint
  layered/CQRS 재사용, 타깃 프로젝트 Action 템플릿, 위반 JSON·교정
  프롬프트로 자가교정 루프를 이었다.

## [0.9.10] - 2026-08-20

### Added

- **Python/Java 메서드 길이 탐지** — PR 리뷰와 Proof 평가기가 같은
  stdlib-only 스캐너로 20줄 초과 메서드를 판정한다.

### Changed

- **신규뿐 아니라 악화도 귀속** — 기준선부터 20줄을 넘은 같은 메서드라도
  이번 변경으로 더 길어지면 `METHOD_TOO_LONG`으로 보고한다.

## [0.9.9] - 2026-08-20

### Added

- **첫 C4 비교 실험 결과** — Cursor `gpt-5.6-sol-high`로 control/OOPforge 짝
  실험을 실행하고 중립 결과를 공개했다. 양쪽 모두 테스트 14개를 통과했지만
  변경 귀속 아키텍처 위반 2건과 재작업 1회가 필요했다. 단일 실행을 개선율로
  일반화하지 않는다.

## Older releases

- [0.8.x–0.9.8](docs/releases/changelog-0.8-0.9.md)
- [0.1.x–0.7.x](docs/releases/changelog-0.1-0.7.md)
