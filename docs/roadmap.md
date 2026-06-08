# OOPforge — Roadmap

OOPforge가 지향하는 방향과 우선순위. **미래 지향** 문서다 — 완료된 변경의 상세 이력은 [`CHANGELOG.md`](../CHANGELOG.md)에 있다.

기간은 단기(다음 릴리스) · 중기(분기) · 장기(연간)로 나눈다.

## 핵심 원칙 (유지)

이미 잘하고 있는 것은 손대지 않는다. 이 원칙이 OOPforge의 정체성이며, 변경할 때는 매우 신중히 한다.

- 작은 스킬 (200줄/스킬, 한 스킬 한 개념)
- 측정 가능한 하드 룰 (300줄/파일, 20줄/메서드)
- 단계별 휴먼 체크포인트 (Discovery → Design → … → Test)
- 도메인 우선, 프레임워크는 어댑터로

## 최근 완료 (요약)

상세는 [`CHANGELOG.md`](../CHANGELOG.md) 참조. 현재 최신: **v0.8.2**.

- **runnable 예제 패밀리** — `calculator` 한 도메인을 java/python × layered/hexagonal/hexagonal-cqrs 6종으로 통일. README/스킬 ↔ 예제 신뢰 갭 해소.
- **아키텍처 강제 (2겹)** — 빠른 stdlib `archlint.py`(레이어 레이아웃 + CQRS 하드룰) + 표준 도구(import-linter, ArchUnit)를 `arch-lint.yml`에서 PR 차단. 린터 self-test 포함.
- **Craft 진입점 정착** — `/oopforge:craft`가 단일 진입점. 모호성 해소 + 스택 범위 게이트(Java Spring / Python FastAPI).
- **Continuity 자동화** — 실행 작업이면 `.craft/` 자동 생성(opt-out).
- **스킬 추가** — CQRS, 안티패턴 시작(`flat-package`), 린트 강제 가이드(`lint-enforcement`).

## 단기 (다음 릴리스)

### 1. 안티패턴 카탈로그 확장 (`skills/antipatterns/`)

현재 `flat-package` 하나뿐. Craft 리뷰·CI가 참조할 핵심 4종 추가:

- `anemic-domain.md` — 도메인은 데이터백, 로직은 전부 Service
- `controller-fat.md` — Controller/Router에 비즈니스 로직
- `repository-with-business-logic.md` — Repository에 판단 로직
- `god-aggregate.md` — Aggregate가 모든 걸 한꺼번에

### 2. 점진적 채택 경로 명문화

- layered → 헥사고날/clean → CQRS 단계별 **진입 기준 체크리스트**(어댑터 수, 도메인 수, 팀 크기)
- 마이그레이션 스킬: `skills/workflow/migrate-layered-to-hexagonal.md`

### 3. 레거시 진입 가이드 (`skills/workflow/adopt-legacy.md`)

- 신규보다 기존 레거시에 끼워넣는 케이스가 다수
- 작은 bounded context 1개부터 분리하는 절차, "전체를 다 바꾸지 말 것" 강조

## 중기 (분기)

### 4. 린트 강제 확장

- 헥사고날 예제용 import-linter/ArchUnit 변종(현재 layered만 표준 도구 강제)
- (수요 생기면) 타깃 프로젝트 부트스트랩 — `--with-lint`(ArchUnit/import-linter 설정), `--with-openapi`. `install.sh`에 얹기보다 별도 스크립트가 적합(설치기와 책임 분리)

### 5. OpenAPI 기본 탑재 완성

- 모든 백엔드 스켈레톤이 Swagger UI를 기본으로 켜고 시작(현재 Java layered만 springdoc 탑재)
- 에러 응답 스키마(`ErrorResponse`) 단일화

### 6. 도메인 리뷰 자동화

- Craft 기반 PR diff 리뷰가 안티패턴/하드룰 위반을 자동 코멘트
- GitHub Action 템플릿 제공

## 장기 (연간)

### 7. 언어 확장

우선순위 순. 각 언어는 layered + hexagonal 두 변종 제공.

1. **Kotlin Spring** — OOP/DDD 친화도 매우 높음, Java 코드 거의 재활용
2. **TypeScript NestJS** — 데코레이터·DI가 Spring과 유사, Node 생태계 커버
3. **Go** — 구조체 기반이지만 인터페이스로 헥사고날 가능. 별도 가이드 필요
4. **C# .NET** — 엔터프라이즈 수요, MediatR과 자연스럽게 결합

### 8. 팀 도입 자료

- README 첫 화면에 30초 install + 5분 데모 GIF/asciinema
- "팀 도입 시 흔한 질문 10개" FAQ, 1시간 워크숍 슬라이드 템플릿

### 9. 커뮤니티 패턴 라이브러리

- 도메인별 패턴(결제·재고·회원·알림)을 모은 **별도 레포**. 본체와 분리해 안정성 유지

## 비-목표 (의도적으로 안 함)

- **메가 스킬/메가 프롬프트** — 한 파일에 여러 개념 묶지 않음
- **GUI/IDE 플러그인** — CLI/에이전트 통합으로 충분
- **자동 코드 생성기** — 패턴은 가르치고, 코드는 에이전트가 작성
- **모든 패턴 커버** — DDD 핵심 + 백엔드 OOP에 집중. UI/모바일/ML 진출 X
- **불안정한 통합을 default install에 포함** — 실험적 통합은 별도 opt-in

## 기여 우선순위

새 컨트리뷰터 추천 순서(작은 단위부터):

1. 안티패턴 카탈로그 1개 추가
2. 기존 스킬에 "변형" 섹션 보강
3. 신규 언어 layered 레이아웃 추가
4. 린트 템플릿/변종 추가
5. 레거시 진입 가이드 케이스 스터디 추가
