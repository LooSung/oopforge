---
description: OOPforge Implement 단계 — 유스케이스 1개를 테스트와 함께 구현
---

**OOPforge Implement** 단계를 수행하라.

구현할 유스케이스: **$ARGUMENTS**

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 사전 조건

- Skeleton이 존재해야 한다.
- 유스케이스 1개만 지정한다.
- 여러 유스케이스를 동시에 구현하지 않는다.

## 절차

1. `{pack}/skills/workflow/implement.md`를 먼저 읽는다.
2. 관련 OOP 스킬을 참조한다.
   - `{pack}/skills/oop/application-service.md`
   - `{pack}/skills/oop/aggregate-root.md`
   - `{pack}/skills/oop/value-object.md`
   - `{pack}/skills/oop/repository-port.md`
3. 안에서 밖으로 순서대로 구현한다.
   1. 도메인 모델 메서드 + 단위 테스트
   2. 유스케이스 클래스
   3. outbound adapter, 예: repository 구현
   4. inbound adapter, 예: controller/router
   5. 통합 테스트 최소 1개
4. 단위 테스트와 통합 테스트를 모두 실행한다.
5. 완료 후 사용자에게 다음을 묻는다.

> 구현 완료. 코드 리뷰 후 머지 + 다음 유스케이스로 넘어가도 될까요?

## Definition of Done

- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 도메인 어노테이션 0
- [ ] 한 파일 300줄 이하
- [ ] CHANGELOG 또는 PR 설명에 요약

## 금지

- 여러 유스케이스 동시 구현
- 테스트 없는 도메인 로직 커밋
- 도메인에 프레임워크 어노테이션 추가
- 임시 레이어 위반
