---
description: OOPforge 진입점 — 의도를 파악해 적합한 스킬/커맨드를 추천. 전체 워크플로 강제 없음.
---

**OOPforge Route** — 사용자가 하고 싶은 일에 맞춰 한두 개의 스킬/커맨드만 추천한다.

사용자 입력: **$ARGUMENTS**

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 절차

1. **사용자 입력이 비었거나 모호하면** 아래 질문을 차례로 한다 (한 번에 한 질문):
   - "지금 하고 싶은 게 뭐예요?"
     - (a) 새 도메인/서비스 만들기
     - (b) 기존 도메인 확장(유스케이스 추가, 강화)
     - (c) 단일 컴포넌트만 만들기(값 객체, Repository 등)
     - (d) 기존 코드 리팩토링
     - (e) 코드 리뷰/규칙 검증
     - (f) 테스트 보강
2. **사용자 입력이 충분히 구체적이면** 바로 아래 "의도 → 추천" 표에서 매칭해 답한다.
3. 추천은 **최소 단위**로 한다. 워크플로 전체를 강제하지 않는다.
4. 추천 후 사용자가 "그거 시작해줘"라고 하면 그 커맨드/스킬로 진입한다.

## 의도 → 추천 매핑

| 의도 신호 | 추천 |
|---|---|
| "새 도메인", "처음부터", "회원관리 만들고 싶어" | `/oopforge:discovery <도메인>` 부터 시작. 그 다음 design → delivery-plan → skeleton → implement 순. |
| "기존 도메인 확장", "결제 강화", "유스케이스 추가" | Discovery 스킵. `{pack}/skills/workflow/design.md` 읽고 유스케이스 1개 설계 → `/oopforge:implement <use-case>` |
| "리팩토링", "구조 정리", "동작은 그대로 두고" | `/oopforge:refactor`. `{pack}/skills/workflow/refactor.md` 우선. 기능 변경 섞지 말 것. |
| "코드 리뷰", "규칙 위반 찾아줘" | `@domain-reviewer` 에이전트 호출. AGENTS.md의 Hard Rules + `examples/` 참조. |
| "테스트 보강", "커버리지" | `/oopforge:test`. `{pack}/skills/workflow/test.md` 우선. |
| "값 객체 하나", "VO 만들기" | `{pack}/skills/oop/value-object.md` 읽고 바로 작성. 워크플로 불필요. |
| "Repository만", "포트 인터페이스" | `{pack}/skills/oop/repository-port.md` |
| "Aggregate 설계" | `{pack}/skills/oop/aggregate-root.md` + 필요 시 `@ddd-architect` |
| "도메인 이벤트" | `{pack}/skills/oop/domain-event.md` |
| "Spring 패키지 구조", "FastAPI 구조" | `/oopforge:skeleton <stack>` — 3계층/헥사고날 중 선택 |
| "OpenAPI/Swagger 추가" | `{pack}/skills/lang/api/openapi-conventions.md` |
| "JPA 어댑터" | `{pack}/skills/lang/java/jpa-repository.md` |
| "레거시에 OOPforge 도입" | `{pack}/docs/roadmap.md`의 "레거시 진입" 섹션. 작은 bounded context 1개부터. |

## 응답 형식

추천은 항상 다음 형식으로:

```
의도 파악: <한 줄 요약>
추천: <커맨드 또는 스킬 경로>
이유: <한 줄>
다음 단계(선택): <있으면>
```

예시:

```
의도 파악: 결제 도메인에 환불 유스케이스 추가
추천: skills/workflow/design.md 읽고 환불 유스케이스 시그니처 작성 → /oopforge:implement refund-order
이유: 신규 도메인이 아니므로 Discovery 불필요. Design부터 충분.
다음 단계: 구현 후 /oopforge:test 로 단위/통합 테스트.
```

## 금지

- **전체 워크플로 강제 금지** — 사용자가 "값 객체 하나"를 원하면 Discovery부터 시키지 말 것.
- **2개 이상 동시 추천 금지** — 가장 작은 단위 하나만. 사용자가 더 원하면 그때 확장.
- **모호한 추천 금지** — "이것저것 보세요" 금지. 항상 파일 경로 또는 명확한 커맨드.
- **사용자 의도 추측 금지** — 입력이 비면 반드시 질문부터.
