---
description: OOPforge Delivery Plan 단계 — 요구사항, 구현 순서, 테스트, 릴리스 계획 정리
---

**OOPforge Delivery Plan** 단계를 수행하라.

대상: **$ARGUMENTS**

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 사전 조건

- `docs/design.md`가 있으면 먼저 읽는다.
- 없으면 요구사항을 바탕으로 Problem 1-Pager부터 작성한다.

## 절차

1. `{pack}/skills/workflow/delivery-plan.md`를 먼저 읽는다.
2. 필요 시 관련 OOP 스킬을 참조한다.
   - `{pack}/skills/oop/aggregate-root.md`
   - `{pack}/skills/oop/value-object.md`
   - `{pack}/skills/oop/repository-port.md`
   - `{pack}/skills/oop/domain-event.md`
3. 요구사항, 목표/비목표, 계약, 책임 경계, 구현 순서, 테스트 계획을 정리한다.
4. 산출물을 `docs/delivery-plan.md`에 저장한다.
5. 완료 후 사용자에게 다음을 묻는다.

> Delivery Plan 검토하고 Skeleton 또는 Implement 단계로 넘어가도 될까요?

## 금지

- 구현 코드 작성
- 확정되지 않은 계약을 확정처럼 작성
- 회사/프레임워크 전용 규칙 강제
- Open Questions 비워두기
