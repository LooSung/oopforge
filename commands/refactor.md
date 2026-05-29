---
description: OOPforge Refactor 단계 — 기존/외부 소스를 동작 보존 전제로 정리
---

**OOPforge Refactor** 단계를 수행하라. 대상:

**$ARGUMENTS**

## 사전 조건

- 보존해야 할 동작이나 계약을 먼저 식별한다.
- 기능 변경 요청이면 Refactor가 아니라 Delivery Plan으로 분리한다.

## 절차

1. `skills/oopforge/workflow/refactor.md` 를 먼저 읽는다.
2. In-scope / Out-of-scope를 명시한다.
3. 기존 동작을 테스트 또는 재현 시나리오로 고정한다.
4. 작은 단위로 책임 분리, 이름 정리, 중복 제거를 수행한다.
5. 각 단계 후 테스트/빌드/핵심 시나리오를 확인한다.
6. 완료 후 사용자에게:
   - "동작 보존 검증 결과를 확인하고 commit/push로 넘어가도 될까요?"

## 금지

- 새 기능 추가
- 테스트/재현 시나리오 없이 큰 구조 변경
- API 계약 몰래 변경
- 도메인 규칙 변경
