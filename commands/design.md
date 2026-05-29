---
description: OOPforge Design 단계 — 유스케이스 시그니처와 애그리거트 윤곽 (구현 X)
---

**OOPforge Design** 단계를 수행하라.

대상: **$ARGUMENTS**

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 사전 조건

- `docs/discovery.md`가 존재해야 한다.
- 없으면 사용자에게 알리고 Discovery 먼저 하도록 안내한다.

## 절차

1. `{pack}/skills/workflow/design.md`를 먼저 읽는다.
2. 관련 OOP 스킬도 참조한다.
   - `{pack}/skills/oop/aggregate-root.md`
   - `{pack}/skills/oop/value-object.md`
   - `{pack}/skills/oop/repository-port.md`
3. 체크리스트대로 산출물을 `docs/design.md`에 저장한다.
4. 완료 후 사용자에게 다음을 묻는다.

> Design 검토하고 Skeleton 단계로 넘어가도 될까요?

## 금지

- 메서드 본문 작성
- 프레임워크 어노테이션
- DTO 설계
- 무한 추상화
