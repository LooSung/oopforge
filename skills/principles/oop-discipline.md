---
name: oop-discipline
description: 백엔드 OOP 작업 전에 읽는 OOPforge 핵심 원칙. 객체 책임, 경계, 테스트, 구조적 학습을 고정한다.
tags: [oop, ddd, principles]
stability: experimental
---

# OOP Discipline

백엔드 OOP 작업을 시작하기 전에 읽는다.
완료 보고에는 실제 설계 판단을 바꾼 원칙만 적는다.

## 1. Behavior lives in the domain

비즈니스 규칙은 Controller, application service, repository adapter가 아니라
도메인 객체의 행동 메서드에 둔다.

예: `paymentService.approve(payment)`보다 `payment.approve(approverId)`를 먼저 고려한다.

## 2. Define boundaries before code

코드를 작성하기 전에 Aggregate Root, 불변식, 상태 전이,
포트, 트랜잭션 경계를 먼저 적는다.

## 3. Domain knows no framework

도메인 모델은 프레임워크 편의보다 비즈니스 언어와 규칙을 우선한다.
기술 세부사항은 application 또는 adapter 경계 밖으로 밀어낸다.

## 4. Use case over CRUD

외부에 노출되는 메서드는 CRUD가 아니라 비즈니스 동사로 표현한다.
상태 변경 이름은 저장소 조작이 아니라 사용자의 의도를 드러내야 한다.

## 5. Aggregate references by ID

다른 Aggregate는 객체가 아니라 ID로 참조한다.
경계 밖의 생명주기와 불변식을 한 객체 그래프에 묶지 않는다.

## 6. Failing test before bug fix

버그 수정은 먼저 재현 가능한 실패 테스트를 만든다.
그다음 가장 작은 수정으로 해결한다.

## 7. Subtract before abstracting

새로운 레이어, 인터페이스, 패턴을 추가하기 전에
불필요한 책임, 중복, 죽은 코드를 먼저 제거한다.

## 8. Encode lessons in structure

같은 실수를 두 번 설명하게 되면 문서를 더 쓰지 않는다.
테스트, 린트, 검증 스크립트, 예제로 남긴다.
