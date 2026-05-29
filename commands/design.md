---
description: OOPforge Design 단계 — 유스케이스 시그니처와 애그리거트 윤곽 (구현 X)
---

**OOPforge Design** 단계를 수행하라. 대상:

**$ARGUMENTS**

## 사전 조건

- `docs/discovery.md` 가 존재해야 한다. 없으면 사용자에게 알리고 Discovery 먼저 하도록 안내.

## 절차

1. `skills/oopforge/workflow/design.md` 를 먼저 읽는다.
2. 관련 OOP 스킬도 참조:
   - `skills/oopforge/oop/aggregate-root.md`
   - `skills/oopforge/oop/value-object.md`
   - `skills/oopforge/oop/repository-port.md`
3. 체크리스트대로 산출물을 `docs/design.md` 에 저장.
4. 완료 후 사용자에게:
   - "Design 검토하고 Skeleton 단계로 넘어가도 될까요?"

## 금지

- 메서드 본문 작성
- 프레임워크 어노테이션
- DTO 설계 (Skeleton/Implement 단계로 미룸)
- 무한 추상화 (1단계 인터페이스까지)
