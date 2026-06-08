---
name: workflow-skeleton
description: Design/Delivery Plan 다음 단계. 언어별 기본 패키지 구조와 인터페이스 파일을 생성한다. 비즈니스 로직은 아직 X.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Skeleton

## 언제 쓰나
Design과 Delivery Plan이 끝났을 때. Implement 이전.
**패키지 구조 + 빈 클래스/인터페이스**만 만든다.

## 체크리스트
- [ ] 대상 스택 확인 (없으면 `skills/lang/backend-stack.md`로 선택)
- [ ] `skills/skeleton/backend-skeleton.md`를 먼저 읽음
- [ ] 레이어 폴더 생성 (3계층 또는 헥사고날/클린)
- [ ] 애그리거트/엔티티 클래스 골격 생성 (필드 + 빈 메서드)
- [ ] 값 객체 클래스 골격
- [ ] 포트 인터페이스 / Repository 인터페이스 정의 (구현체 X)
- [ ] 유스케이스/Service 클래스 골격 (빈 execute 메서드)
- [ ] 빌드 도구 파일 (Gradle, pyproject.toml 등) 의존성만
- [ ] 테스트 폴더 미러링
- [ ] **셀프 체크**: `skills/skeleton/backend-skeleton.md`의 "셀프 체크" 통과 — 레이어가 각각 별도 폴더, 한 폴더에 파일명 suffix로만 분리 금지

## 스택과 레이아웃 분리

스택 선택과 구조 생성은 분리한다.

- 스택을 아직 고르지 않았다면 → `skills/lang/backend-stack.md`로 하나를 정한다.
- 스택이 정해졌다면 → `skills/skeleton/backend-skeleton.md`의 표준 구조를 따른다.

Skeleton은 직접 레이아웃을 발명하지 않는다.

## 산출물

- 빈 메서드 시그니처만 있는 파일들
- 컴파일/실행은 가능 (`UnsupportedOperationException`, `NotImplementedError`, TODO)
- 테스트 폴더 구조 (테스트는 비어 있어도 됨)
- `docs/skeleton.md` 또는 `docs/<domain>/skeleton.md` 에 생성 구조 기록

## 금지
- **메서드 본문 작성 금지** — `throw new UnsupportedOperationException()` 또는 `raise NotImplementedError`
- **`if`, `for` 등 로직 금지**
- **데이터베이스 스키마 정의 금지** — Implement 단계로 미룸
- **레이어 위반 금지** — domain은 다른 어느 레이어도 import 하지 않음
- **백엔드 레이아웃 무시 금지** — Java/Python 기본 구조는 `skills/skeleton/backend-skeleton.md`를 우선한다.

## 다음 단계
사용자 승인 후 → `workflow-implement` (유스케이스 단위로)
