---
name: workflow-craft
description: 기존 백엔드 OOP 작업을 분류하고 가장 작은 실행 경로로 수행하는 OOPforge 실행 오케스트레이터.
tags: [workflow, oop, ddd]
stability: experimental
---

# Workflow — Craft

## 목적

기존 백엔드 OOP 작업을 가장 작은 적절한 실행 경로로 수행한다.
코드 양을 늘리는 것이 목적이 아니다.
도메인 객체가 책임을 갖게 하고 application service가 orchestration을 넘지 않게 한다.

## 시작 절차

0. `skills/workflow/continuity.md`의 Resume 프로토콜로 기존 작업 문서가 있으면 먼저 읽고 이어간다.
1. `skills/principles/oop-discipline.md`를 읽는다.
2. 사용자 요청과 기존 코드를 확인한다.
3. 아래 표에서 가장 작은 실행 경로 하나를 선택한다.
4. advisory 요청이면 경로만 추천하고 구현하지 않는다.
5. 실행 요청이면 선택한 skill, playbook, 또는 workflow의 체크리스트를 작업 목록에 복사한다.
6. 생략한 단계가 있다면 이유를 한 줄로 남긴다.
7. 비즈니스 로직 구현 전 OOP Contract를 작성한다.
8. 선택한 경로대로 구현하고 테스트한다.
9. `AGENTS.md`의 Hard Rules와 실행한 테스트 결과를 확인한다.
10. 완료 보고 형식에 맞춰 설계 결정, 검증 결과, 남은 위험을 기록하고, `continuity.md`를 쓰는 작업이면 작업 문서에 반영한다.

## 실행 경로 선택

| 요청 신호 | 실행 경로 |
|---|---|
| 단일 Aggregate, Value Object, Domain Event 설계 | `skills/oop/domain-model.md` |
| 단일 use case, application service, Repository port 설계 | `skills/oop/use-case-boundary.md` |
| 기존 도메인에 행동, 유스케이스, API 추가 | `skills/playbooks/feature.md` |
| 비즈니스 규칙 오류, 회귀, 잘못된 상태 전이 수정 | `skills/playbooks/bug-fix.md` |
| God Service, 책임 이동, 중복 제거, 동작 보존 정리 | `skills/workflow/refactor.md` |
| 새 도메인 또는 큰 기능 | `skills/workflow/discovery.md`부터 기존 전체 workflow |
| 모호하거나 추천만 원하는 요청 | 가장 작은 경로만 추천하고 구현하지 않음 |

## OOP Contract

Craft에서 구현이 필요한 작업은 코드 작성 전에 아래 형식을 한 번 채운다.
해당하지 않는 항목은 `none`이라고 쓰고 이유를 남긴다.

```markdown
## OOP Contract

Use Case:
Aggregate Root:
Domain Invariants:
State Transition:
Required Ports:
Transaction Boundary:
```

## 검증

- 선택한 playbook 또는 workflow의 체크리스트를 완료한다.
- `AGENTS.md`의 Hard Rules를 변경 파일 기준으로 확인한다.
- 더 넓은 리뷰가 필요하면 `docs/reviewer-checklist.md`로 레이어별 점검을 수행한다.
- 필요한 테스트를 실행하고 명령과 결과를 기록한다.
- 실패하거나 생략한 검증이 있으면 이유와 위험을 남긴다.

## 완료 보고

```markdown
## Design Decisions
-

## Verification
- Tests:
- Hard Rules:

## Remaining Risks
-
```

## 단계 경계

새 도메인 또는 큰 기능은 기존 Discovery → Test 단계와 사람 승인을 유지한다.
Craft는 이 경계를 지우지 않는다. 기존 도메인의 집중 작업을 더 엄격하게 수행한다.
