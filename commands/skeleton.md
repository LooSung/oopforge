---
description: OOPforge Skeleton 단계 — 패키지 구조와 인터페이스 파일 생성
---

**OOPforge Skeleton** 단계를 수행하라. 대상 언어/스택:

**$ARGUMENTS** (예: `java-spring`, `python-fastapi`)

## 스킬 경로

OOPforge 팩 루트: `$OOPFORGE_HOME` → `~/.oopforge` → (개발 시) 이 저장소 루트. 아래 `{pack}` 는 그 루트.

## 사전 조건

- `docs/design.md` 가 존재해야 한다. 없으면 Design 먼저 안내.

## 절차

1. `{pack}/skills/workflow/skeleton.md` 를 먼저 읽는다.
2. 언어별 레이아웃 스킬을 반드시 참조:
   - `java-spring`: `{pack}/skills/lang/java/spring-hexagonal-layout.md`
   - `python-fastapi`: `{pack}/skills/lang/python/clean-fastapi-layout.md`
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
