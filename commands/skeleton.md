---
description: OOPforge Skeleton 단계 — 패키지 구조와 인터페이스 파일 생성
---

**OOPforge Skeleton** 단계를 수행하라. 대상 언어/스택:

**$ARGUMENTS** (예: `java-spring`, `python-fastapi`)

## 사전 조건

- `docs/design.md` 가 존재해야 한다. 없으면 Design 먼저 안내.

## 절차

1. `skills/oopforge/workflow/skeleton.md` 를 먼저 읽는다.
2. 언어별 레이아웃 스킬을 반드시 참조:
   - `java-spring`: `skills/oopforge/lang/java/spring-hexagonal-layout.md`
     - Splearn-style Spring hexagonal layout (`application/provided`, `application/required`, `adapter`)
   - `python-fastapi`: `skills/oopforge/lang/python/clean-fastapi-layout.md`
     - `app/application/domain/infrastructure/presentation/shared` clean layout
3. 패키지 구조 생성 + 빈 클래스/인터페이스 파일.
4. 메서드는 시그니처만, 본문은 `throw new UnsupportedOperationException()` 또는 `raise NotImplementedError`.
5. 빌드/실행 확인.
6. 사용자에게:
   - "Skeleton 검토하고 Implement 시작할 유스케이스를 골라주세요."

## 금지

- 메서드 본문 작성 (NotImplementedError 외)
- if/for 등 로직
- 비즈니스 룰 작성
- 레이어 의존 규칙 위반
