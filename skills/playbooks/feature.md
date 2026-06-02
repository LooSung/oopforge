---
name: playbook-feature
description: 기존 도메인에 OOPforge 규칙으로 유스케이스 하나를 추가하는 실행 플레이북.
tags: [playbook, feature, oop]
stability: experimental
---

# Playbook — Feature

## 사용 시점

기존 도메인에 새로운 행동 또는 유스케이스를 하나 추가할 때 사용한다.
새 도메인 또는 큰 기능이라면 Discovery부터 진행한다.

상세 구현 순서는 `skills/workflow/implement.md`를 따른다.
OOP Contract 형식과 최종 검증은 `skills/workflow/craft.md`를 따른다.

## 체크리스트

- [ ] 관련 Aggregate, application service, port, adapter를 읽는다.
- [ ] 기존 도메인 규칙과 테스트를 확인한다.
- [ ] 새 행동의 책임을 가질 도메인 객체를 정한다.
- [ ] 필요한 port와 adapter 변경 범위를 최소화한다.
- [ ] `skills/workflow/implement.md`의 한 유스케이스 구현 절차를 따른다.
- [ ] `skills/workflow/craft.md`의 검증과 완료 보고를 따른다.

## 금지

- 새 행동을 application service의 private method로 숨기지 않는다.
- 범용 Manager, Helper, Util 클래스를 먼저 만들지 않는다.
- 한 번에 여러 유스케이스를 구현하지 않는다.
- 관련 없는 리팩터링을 섞지 않는다.
