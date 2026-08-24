# 3단계 — Delivery Plan

[English](./03-delivery-plan.md) · [한국어](./03-delivery-plan.ko.md)
> **범위, 순서, 테스트, 위험을 합의합니다.** 프로덕션 파일은 만들지 않습니다.

읽을 스킬: `{pack}/skills/workflow/delivery-plan.md`

저장 위치: `docs/library/delivery-plan.md`

---

## 예시 산출물

```markdown
# 도서 대출 — Delivery Plan

## 목표와 인수 조건
- 회원이 대출 가능한 도서를 빌리고 Loan ID를 받는다.
- 활성 대출이 있는 도서는 거절한다.
- 대출 시 `BookBorrowed`를 기록하고 디스패치한다.

## 범위
- `borrowBook(memberId, bookId): LoanId`
- Loan Aggregate 행동과 이벤트
- Repository와 이벤트 디스패치 포트
- 인메모리 어댑터와 HTTP 엔드포인트 하나

## 제외 범위
- 도서 반납
- 영속 저장소나 외부 메시징
- Production Readiness 항목

## 구현 순서
1. 승인된 Java 또는 Python 스켈레톤을 만든다.
2. Loan 행동과 도메인 테스트를 구현한다.
3. Repository·dispatcher fake로 유스케이스를 구현한다.
4. 조립 코드와 HTTP 어댑터를 추가한다.
5. 단위·경계·아키텍처 검사를 실행한다.

## 위험
- 활성 대출 유일성은 프로덕션에서 DB 제약이 필요하다.
- 인프로세스 이벤트 디스패치는 외부 메시지 전달이 아니다.
```

---

## 체크포인트

질문: *"스켈레톤을 만들기 전에 이 범위와 구현 순서가 원하는 내용과
맞나요?"*

다음: [04-skeleton.ko.md](./04-skeleton.ko.md)
