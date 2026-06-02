---
name: backend-stack
description: Java Spring과 Python FastAPI 백엔드에서 layered 또는 hexagonal/clean 스택 하나를 선택한다.
tags: [backend, stack, java, python]
stability: stable
---

# Backend Stack

## 언제 쓰나

새 백엔드 작업에서 **어떤 스택을 쓸지 아직 정하지 않았을 때** 사용한다.
스택을 정하는 단계이며, 폴더 구조나 빈 타입은 만들지 않는다.
구조 생성은 `skills/skeleton/backend-skeleton.md`가 맡는다.

## 지원 스택

| Stack | 아키텍처 |
|---|---|
| `java-spring-layered` | 3계층 (Controller/Service/Repository) |
| `java-spring-hexagonal` | 헥사고날 (domain/application/adapter) |
| `python-fastapi-layered` | 3계층 (Router/Service/Repository) |
| `python-fastapi-clean` | 클린 (domain/application/infrastructure/presentation) |

## 선택 기준

| 상황 | 선택 |
|---|---|
| 작은 서비스, MVP, 도메인 1~2개 | layered |
| 도메인 규칙이 복잡함 | hexagonal/clean |
| 외부 adapter가 많음 | hexagonal/clean |
| 팀이 아직 아키텍처 학습 중 | layered로 시작, 경계 규칙은 유지 |

기본 권장: 도메인 2개 이하 + 어댑터 적음 → layered. 그 외 → hexagonal/clean.

## 결정 절차

1. 언어를 정한다 (Java Spring 또는 Python FastAPI).
2. 위 기준으로 layered 또는 hexagonal/clean을 고른다.
3. 모호하면 사용자에게 "3계층(layered)인지 헥사고날/clean인지" 묻는다.
4. 정해진 stack 식별자 하나를 다음 단계로 넘긴다.

## OpenAPI 기본 방침

- 모든 백엔드 스택은 OpenAPI/Swagger를 개발 환경에서 바로 확인할 수 있어야 한다.
- 구체적인 도구 설정과 폴더 구조는 `skills/skeleton/backend-skeleton.md`를 따른다.

## 금지

- 스택을 정하지 않은 채 폴더 구조나 빈 타입을 만들지 않는다.
- 한 프로젝트에 여러 스택을 섞지 않는다.
- 근거 없이 hexagonal/clean을 기본값으로 강요하지 않는다.
