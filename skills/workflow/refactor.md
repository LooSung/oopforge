---
name: workflow-refactor
description: 외부 또는 기존 소스를 가져와 동작 보존을 전제로 구조를 정리한다. 기능 변경 없이 품질을 회복할 때 사용한다.
tags: [workflow, refactor, quality]
stability: stable
---

# Workflow — Refactor

## 언제 쓰나
기존 코드나 외부에서 가져온 소스의 동작은 유지하면서 구조, 이름, 책임 경계, 중복을 정리할 때.
기본 delivery 흐름의 필수 단계가 아니라 **필요할 때 쓰는 보조 workflow**다.

## 핵심 원칙
- 기능 변경과 리팩토링을 섞지 않는다.
- 먼저 현재 동작을 테스트나 재현 시나리오로 고정한다.
- 작게 바꾸고 자주 검증한다.
- public behavior, API contract, domain rule은 유지한다.
- 바뀌어야 한다면 새 delivery plan 대상이다.

## 체크리스트
- [ ] In-scope / Out-of-scope 명시
- [ ] 보존해야 할 동작과 계약 정의
- [ ] characterization test 또는 수동 재현 시나리오 작성
- [ ] 책임 분리 후보 식별
- [ ] 중복, 죽은 코드, 모호한 이름 검색
- [ ] 레이어 의존성 위반 확인
- [ ] 작은 단계로 변경
- [ ] 각 단계 후 테스트/빌드/핵심 시나리오 확인
- [ ] 변경 요약과 남은 리스크 기록

## 산출물

`docs/refactor-plan.md` 또는 `docs/<domain>/refactor-plan.md` 에 저장:

```markdown
# <Area> — Refactor Plan

## Scope
- In:
- Out:

## Behavior To Preserve
- Public API:
- Domain rules:
- Side effects:

## Characterization
- Tests:
- Manual scenarios:

## Refactor Steps
1.
2.
3.

## Verification
- Commands:
- Results:

## Risks
- 
```

## 금지
- **새 기능 추가 금지**
- **테스트/재현 시나리오 없이 큰 구조 변경 금지**
- **도메인 규칙 변경 금지**
- **기존 API 계약을 몰래 변경 금지**
- **프레임워크 편의를 이유로 도메인 순수성 훼손 금지**

## 다음 단계
검증 완료 후 → review, commit, push. 기능 변경이 필요하면 `workflow-delivery-plan`으로 분리.
