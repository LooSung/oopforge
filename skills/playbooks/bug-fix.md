---
name: playbook-bug-fix
description: 도메인 버그를 실패 테스트로 재현하고 가장 작은 변경으로 해결하는 실행 플레이북.
tags: [playbook, bug-fix, tdd]
stability: experimental
---

# Playbook — Bug Fix

## 사용 시점

잘못된 상태 전이, 불변식 위반, 중복 처리, 권한 오류,
회귀 버그를 수정할 때 사용한다.

테스트 설계와 실행 기록은 `skills/workflow/test.md`를 따른다.
OOP Contract 형식과 최종 검증은 `skills/workflow/craft.md`를 따른다.

## 체크리스트

- [ ] 증상을 한 문장으로 적는다.
- [ ] 영향을 받는 Aggregate와 유스케이스를 찾는다.
- [ ] 버그를 재현하는 실패 테스트를 작성한다.
- [ ] 수정 전 테스트가 실제로 실패하는지 확인한다.
- [ ] 근본 원인을 적는다.
- [ ] 가장 작은 코드 변경으로 수정한다.
- [ ] 실패 테스트와 관련 회귀 테스트가 통과하는지 확인한다.
- [ ] `skills/workflow/craft.md`의 검증과 완료 보고를 따른다.

## 금지

- 실패 테스트 없이 바로 수정하지 않는다.
- 증상만 가리는 조건문을 추가하지 않는다.
- 버그 수정과 구조 개편을 한 번에 섞지 않는다.
- 재현하지 못했다면 완료했다고 말하지 않는다.
