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
- [ ] 대상 스택 선택 (아래 표 참조)
- [ ] 언어별 레이아웃 스킬을 먼저 읽음
- [ ] 백엔드 API면 OpenAPI 컨벤션 스킬도 함께 적용 (`skills/lang/api/openapi-conventions.md`)
- [ ] 레이어 폴더 생성 (3계층 또는 헥사고날/클린)
- [ ] 애그리거트/엔티티 클래스 골격 생성 (필드 + 빈 메서드)
- [ ] 값 객체 클래스 골격
- [ ] 포트 인터페이스 / Repository 인터페이스 정의 (구현체 X)
- [ ] 유스케이스/Service 클래스 골격 (빈 execute 메서드)
- [ ] 빌드 도구 파일 (Gradle, pyproject.toml 등) 의존성만
- [ ] 테스트 폴더 미러링

## 언어별 기본 레이아웃

Skeleton은 직접 레이아웃을 발명하지 않는다. 아래 스킬을 따른다.

| Stack | Layout source | 언제 |
|---|---|---|
| `java-spring-layered` | `skills/lang/java/spring-layered-layout.md` | 3계층 (Controller/Service/Repository), 작은 서비스/MVP |
| `java-spring-hexagonal` | `skills/lang/java/spring-hexagonal-layout.md` | Splearn-style 헥사고날, 도메인 복잡 |
| `python-fastapi-layered` | `skills/lang/python/fastapi-layered-layout.md` | 3계층 (Router/Service/Repository), 작은 서비스/MVP |
| `python-fastapi-clean` | `skills/lang/python/clean-fastapi-layout.md` | `app/application/domain/infrastructure/presentation` 클린 |

스택이 모호하면 사용자에게 "3계층(layered)인지 헥사고날/clean인지" 묻고 진행한다.
기본 권장: 도메인 2개 이하 + 어댑터 적음 → layered. 그 외 → hexagonal/clean.

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
- **언어별 레이아웃 무시 금지** — Java/Python 기본 구조는 lang 스킬을 우선한다.

## 다음 단계
사용자 승인 후 → `workflow-implement` (유스케이스 단위로)
