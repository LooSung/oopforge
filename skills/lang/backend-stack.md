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

## 스택 범위 게이트 (먼저 통과)

OOPforge가 지원하는 백엔드는 **Java Spring · Python FastAPI 뿐**이다. 새 빌드 요청에서 언어가 정해지지 않았거나 다른 스택을 함의하면 코드 전에 처리한다.

- **언어 미지정**: 임의로 고르지 말고 지원 스택(Java/Python)만 제시하고 사용자가 고르게 한다.
- **지원 외 스택**(JavaScript/TypeScript, 프론트엔드, 모바일, 셸/CLI 등)을 함의: OOPforge를 그 스택에 **적용할 수 없음**을 분명히 알린다.
- 그래도 사용자가 그 스택을 고집하면: OOPforge 규율(스켈레톤/하드룰) 없이 **일반(비-OOPforge) 빌드**로만 진행하고, OOPforge 범위 밖임을 고지한다.

## 결정 절차

1. 위 범위 게이트로 언어를 확정한다 (Java Spring 또는 Python FastAPI).
2. 위 기준으로 layered 또는 hexagonal/clean을 고른다.
3. 모호하면 사용자에게 "3계층(layered)인지 헥사고날/clean인지" 묻는다.
4. 정해진 stack 식별자 하나를 다음 단계로 넘긴다.

## CQRS 변형 (선택)

- CQRS는 별도 스택이 아니라 layered/헥사고날 **위에 얹는 변형**이다. 진입 경로: `layered → hexagonal/clean → CQRS`.
- 읽기/쓰기 모델이 크게 다르거나 복잡 조회가 도메인을 오염시킬 때만 도입한다. 적용 규칙과 진입 기준은 `skills/oop/cqrs.md`.

## OpenAPI 기본 방침

- 모든 백엔드 스택은 OpenAPI/Swagger를 개발 환경에서 바로 확인할 수 있어야 한다.
- 구체적인 도구 설정과 폴더 구조는 `skills/skeleton/backend-skeleton.md`를 따른다.

## 금지

- 스택을 정하지 않은 채 폴더 구조나 빈 타입을 만들지 않는다.
- 한 프로젝트에 여러 스택을 섞지 않는다.
- 근거 없이 hexagonal/clean을 기본값으로 강요하지 않는다.
- 지원 외 스택(JS/TS 등)에 OOPforge 스켈레톤·하드룰을 적용하지 않는다. 적용 불가를 먼저 알린다.
