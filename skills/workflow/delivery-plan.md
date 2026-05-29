---
name: workflow-delivery-plan
description: 요구사항 확인부터 구현 순서, 테스트, 리뷰, 배포 리스크까지 하나의 실행 계획으로 정리한다.
tags: [workflow, planning, delivery]
stability: stable
---

# Workflow — Delivery Plan

## 언제 쓰나
Discovery/Design 이후, 또는 요구사항이 들어왔지만 바로 구현하기엔 범위와 계약이 불명확할 때.
기존 tech spec과 kickoff 문서를 **하나의 실행 계획**으로 합친다.

## 목적
- 무엇을 만들지 명확히 한다.
- 무엇을 만들지 않을지 명확히 한다.
- 어떤 순서로 구현하고 검증할지 합의한다.
- 리뷰, 커밋, 머지, 배포 전에 확인할 리스크를 드러낸다.

## 체크리스트
- [ ] Problem 1-Pager 작성: Background, Problem, Goal, Non-goals, Constraints
- [ ] 유스케이스와 성공 기준 정의
- [ ] API/CLI/UI 등 외부 계약이 있으면 입력/출력/에러를 정의
- [ ] 도메인 모델, 애플리케이션 서비스, 포트, 어댑터 책임을 분리
- [ ] 구현 순서를 작게 나눈다
- [ ] 테스트 전략: 단위, 통합, E2E 확인 포인트
- [ ] 리뷰 체크리스트: 파일 크기, 레이어 의존성, 도메인 규칙
- [ ] 커밋/푸시/MR/릴리스 메모 초안
- [ ] 롤백 또는 되돌리기 전략

## 산출물

`docs/delivery-plan.md` 또는 `docs/<domain>/delivery-plan.md` 에 저장:

```markdown
# <Feature> — Delivery Plan

## Problem 1-Pager
- Background:
- Problem:
- Goal:
- Non-goals:
- Constraints:

## Scope
- In:
- Out:

## Contract
- Use cases:
- Inputs:
- Outputs:
- Errors:

## Responsibility Map
| Concern | Domain | Application | Infrastructure | Interfaces |
|---|---|---|---|---|
|  |  |  |  |  |

## Implementation Order
1. Domain model / value objects
2. Application use case
3. Ports and adapters
4. Interface layer
5. Tests and E2E checks

## Test Plan
- Unit:
- Integration:
- E2E:

## Review / Merge / Release
- Review checklist:
- Commit summary:
- MR notes:
- Deploy risks:
- Rollback:

## Open Questions
- 
```

## 금지
- **구현 결과 보고서처럼 쓰기 금지** — 앞으로 할 일을 정리한다.
- **확정되지 않은 계약을 확정처럼 쓰기 금지** — 모르면 Open Questions에 남긴다.
- **회사/프레임워크 전용 규칙 강제 금지** — 프로젝트 `AGENTS.md`에 있는 규칙만 따른다.
- **긴 파일 경로 나열 금지** — 책임 경계와 순서가 더 중요하다.

## 다음 단계
사용자 승인 후 → `workflow-skeleton` 또는 바로 작은 `workflow-implement`
