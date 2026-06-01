# OOPforge — Roadmap

OOPforge가 지향하는 방향과 우선순위. 단기(다음 릴리스), 중기(분기), 장기(연간)로 나눈다.

## 핵심 원칙 (유지)

이미 잘하고 있는 것은 손대지 않는다:

- 작은 스킬 (200줄/스킬, 한 스킬 한 개념)
- 측정 가능한 하드 룰 (300줄/파일, 20줄/메서드)
- 단계별 휴먼 체크포인트 (Discovery → Design → ... → Test)
- 도메인 우선, 프레임워크는 어댑터로

이 원칙이 OOPforge의 정체성이다. 변경할 때는 매우 신중히.

## Next sprint — v0.2.1 (proof gap)

README/스킬은 5종 스택을 약속하지만 runnable examples는 hexagonal 2개만 있는 **신뢰 갭**을 메운다.

- [x] `examples/order-java-layered/` — Spring 3-tier, same place-order, `./gradlew test`
- [x] `examples/order-python-flask/` — Flask 3-tier + flask-smorest, same place-order, `pytest`
- [x] `examples/README.md` — stack ↔ folder 매핑 표
- [x] README 4개 locale examples 표 갱신
- [x] 각 예제: domain test + OpenAPI smoke (`/v3/api-docs` or `/api/v1/openapi.json`)

**다음 (v0.2.2 / 런칭 직전):** asciinema 30초 (`/oopforge:route` → skeleton) → README 상단  
**런칭:** OKKY · dev.to → (proof 후) r/* · HN Show HN

---

## 단기 (다음 릴리스)

### 1. 점진적 채택 경로 명문화
- 3계층(layered) → 헥사고날/clean → CQRS/event-sourcing
- 각 단계 진입 기준을 체크리스트로 (어댑터 수, 도메인 수, 팀 크기)
- 마이그레이션 가이드 스킬 추가: `skills/workflow/migrate-layered-to-hexagonal.md`

### 2. Route 커맨드 정착
- `/oopforge:route`를 README/AGENTS.md 1번 진입점으로 격상
- 사용자가 워크플로 전체를 외울 필요 없음 — Route가 안내

### 3. OpenAPI 기본 탑재
- 모든 백엔드 스켈레톤이 Swagger UI를 기본으로 켜고 시작
- 에러 응답 스키마(`ErrorResponse`) 단일화

### 4. Python 1급 시민화
- Java 편향 해소: Flask 레이아웃, Python aggregate/event 스킬 추가됨
- `examples/order-python`을 FastAPI clean + Flask layered 두 변종으로 유지

## 중기 (분기)

### 5. 레거시 진입 가이드 (`workflow/adopt-legacy.md`)
- 신규 프로젝트보다 기존 레거시에 OOPforge를 끼워넣는 케이스가 80%
- 작은 bounded context 1개부터 분리하는 절차
- "전체를 다 바꾸지 말 것" 강조

### 6. 린트/강제 템플릿
- 가이드만 있고 강제 없으면 팀 내에서 빠르게 무너짐
- Java: ArchUnit 템플릿 (`skills/lang/java/archunit-rules.md`)
- Python: `import-linter` 설정 템플릿 (`skills/lang/python/import-linter.md`)
- CI에서 자동 검증되게 — 가이드의 핵심 항목을 PR 차단으로 연결

### 7. 안티 패턴 카탈로그 (`skills/antipatterns/`)
- `anemic-domain.md` — 도메인이 데이터백 + 모든 로직이 Service
- `controller-fat.md` — Controller에 비즈니스 로직
- `repository-with-business-logic.md` — Repository에 판단 로직
- `god-aggregate.md` — Aggregate가 모든 걸 한꺼번에
- 코드 리뷰 에이전트(`@domain-reviewer`)가 이 카탈로그를 참조하면 강력해짐

### 8. 도구 자동 설치
- `install.sh`에 옵션 추가: `--with-lint` → ArchUnit/import-linter 설정 자동 생성
- `--with-openapi` → springdoc/flask-smorest 의존성 추가 가이드 출력

## 장기 (연간)

### 9. 언어 확장
우선순위 순:

1. **Kotlin Spring** — OOP/DDD 친화도 매우 높음, Java 코드 거의 재활용
2. **TypeScript NestJS** — 데코레이터·DI가 Spring과 유사, Node 생태계 커버
3. **Go** — 구조체 기반이지만 인터페이스로 헥사고날 가능. 별도 가이드 필요
4. **C# .NET** — 엔터프라이즈 수요, MediatR 패턴과 자연스럽게 결합

각 언어는 layered + hexagonal 두 변종 모두 제공.

### 10. 팀 도입 자료
- README 첫 화면에 30초 install + 5분 데모 GIF/asciinema
- "팀에 도입할 때 받는 흔한 질문 10개" FAQ
- 1시간 워크숍 슬라이드 템플릿

### 11. 도메인 리뷰 자동화
- `@domain-reviewer`가 PR diff에 대해 안티패턴/하드 룰 위반 자동 코멘트
- GitHub Action 템플릿 제공

### 12. 커뮤니티 패턴 라이브러리
- 사용자가 만든 도메인별 패턴 (e.g., 결제, 재고, 회원, 알림)을 모은 별도 레포
- OOPforge 본체와 분리해 안정성 유지

## 비-목표 (의도적으로 안 함)

- **메가 스킬/메가 프롬프트** — 한 파일에 5개 개념 묶지 않음
- **GUI/IDE 플러그인** — CLI/에이전트 통합으로 충분
- **자동 코드 생성기** — 패턴은 가르치고, 코드는 에이전트가 작성
- **모든 패턴 커버** — DDD 핵심 + 백엔드 OOP에 집중. UI/모바일/ML 영역 진출 X
- **불안정한 통합을 default install에 포함** — OpenCode 등은 experimental 유지

## 성공 지표

- 신규 사용자가 README → 첫 도메인 스켈레톤까지 **10분 이하**
- 팀이 OOPforge 도입 후 PR 평균 크기 **감소** (300줄/파일 룰의 효과)
- `/oopforge:route`가 전체 커맨드 호출의 **30%+** (워크플로 강제가 깨졌다는 증거)
- 안티패턴 카탈로그가 코드 리뷰에서 인용되는 빈도

## 기여 우선순위

새 컨트리뷰터에게 추천하는 작업 순서:

1. 안티패턴 카탈로그 1개 추가 (가장 작은 단위 기여)
2. 기존 스킬에 "변형" 섹션 보강
3. 신규 언어 layered 레이아웃 추가
4. 린트 템플릿 추가
5. 레거시 진입 가이드 케이스 스터디 추가
