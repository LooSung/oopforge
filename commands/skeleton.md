---
description: OOPforge Skeleton 단계 — 패키지 구조와 인터페이스 파일 생성
---

**OOPforge Skeleton** 단계를 수행하라.

대상 언어/스택: **$ARGUMENTS**

예: `java-spring`, `python-fastapi`

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 사전 조건

- `docs/design.md`가 존재해야 한다.
- 없으면 Design 먼저 하도록 안내한다.

## 절차

1. `{pack}/skills/workflow/skeleton.md`를 먼저 읽는다.
2. 언어별 레이아웃 스킬을 반드시 참조한다.
   - `java-spring`: `{pack}/skills/lang/java/spring-hexagonal-layout.md`
   - `python-fastapi`: `{pack}/skills/lang/python/clean-fastapi-layout.md`
3. 패키지 구조를 생성한다.
4. 빈 클래스/인터페이스 파일을 생성한다.
5. 메서드는 시그니처만 작성하고 본문은 `throw new UnsupportedOperationException()` 또는 `raise NotImplementedError`로 둔다.
6. 빌드/실행을 확인한다.
7. 사용자에게 다음을 묻는다.

> Skeleton 검토하고 Implement 시작할 유스케이스를 골라주세요.

## 금지

- 메서드 본문 작성, 단 NotImplementedError류는 허용
- if/for 등 로직 작성
- 비즈니스 룰 작성
- 레이어 의존 규칙 위반
