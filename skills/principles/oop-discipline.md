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

## 7. Subtract before abstracting — 작성 전 사다리

코드를 짜는 것은 마지막 수단이다. 무언가를 만들기 전에 위 칸부터 밟고,
처음으로 해결되는 칸에서 멈춘다. 아래로 내려갈수록 코드가 늘어난다.

```
1. 이게 존재할 필요가 있나?     → 아니면 안 만든다 (YAGNI)
2. 표준 라이브러리·언어 기능?    → 그걸 쓴다
3. 프레임워크 기본 제공?        → 그걸 쓴다 (Spring/FastAPI 내장)
4. 이미 깐 의존성?             → 그걸 쓴다
5. 한 줄·한 메서드로 되나?      → 그걸로 끝낸다
6. 그래도 안 되면             → 동작하는 최소만 직접 짠다
```

**본질 vs 우발.** 사다리는 *우발적 복잡성*(불필요한 추상화, 중복, 죽은 코드,
안 쓰는 유연성)만 깎는다. *본질적 복잡성*(Aggregate 경계, 불변식, 포트,
레이어 분리)은 의도적 구조이므로 사다리 대상이 아니다.

**게으르지만 태만하지 않다.** 신뢰 경계 입력 검증·데이터 손실 처리·보안은
어느 칸에서도 생략하지 않는다.

**미룬 것은 흔적을 남긴다.** 의도적으로 최소만 했으면 그 자리에 무엇을 미뤘는지와
올라갈 길(upgrade path)을 표식으로 남긴다 — "나중에"가 "영영"이 되지 않도록.

## 8. Encode lessons in structure

같은 실수를 두 번 설명하게 되면 문서를 더 쓰지 않는다.
테스트, 린트, 검증 스크립트, 예제로 남긴다.

## 9. Duplicate before the wrong abstraction

DRY는 **지식(규칙)의 중복**을 없애는 것이지, 닮아 보이는 코드를 무조건 합치는
것이 아니다. 잘못된 추상화를 되돌리는 비용이 중복을 두는 비용보다 크다.

- 두 번째 중복은 참는다. **세 번째에야 추상화한다 (Rule of Three).**
- **바운디드 컨텍스트를 가로질러 도메인 모델을 공유하지 않는다.** 두 컨텍스트의
  개념이 닮아 보여도 서로 다르게 진화하므로, 여기서는 중복이 옳다.
- 진짜 합칠 것은 흩어진 *비즈니스 규칙*이다 — 도메인 행동 메서드 한 곳으로
  모은다. (규칙이 Service 곳곳에 복제되면 God Service·anemic domain의 씨앗)
