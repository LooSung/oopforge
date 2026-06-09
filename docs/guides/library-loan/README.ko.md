# 도서관 대출 — OOPforge 전체 워크플로우

> Java (Spring Boot)와 Python (FastAPI)로 **도서관 대출 시스템**을 처음부터 끝까지 구현합니다.  
> Discovery → Design → Delivery Plan → Skeleton → Implement → Test 순서로 진행합니다.

[English](./README.md) · [한국어](./README.ko.md)

OOPforge **사용법**을 단계별로 보여주는 가이드입니다. 최소 실행 예제는 [`examples/calculator-java-hexagonal`](../../../examples/calculator-java-hexagonal/), [`examples/calculator-python-hexagonal`](../../../examples/calculator-python-hexagonal/)를 참고하세요.

---

## 시나리오

회원이 도서를 **대출**한다. 대출 중인 도서는 다시 대출할 수 없다. 대출하면 `BookBorrowed` 이벤트가 발행된다.

---

## 슬래시 명령 (Claude Code)

**Java 트랙:**

```text
/oopforge:craft library loan domain Discovery부터 시작. 코드는 아직 작성하지 마.
/oopforge:craft java-spring으로 borrow-book 구현
/oopforge:craft borrow-book 테스트
```

**Python 트랙** — Discovery/Design/Delivery Plan은 동일. Skeleton만 다름:

```text
/oopforge:craft library loan domain Discovery부터 시작. 코드는 아직 작성하지 마.
/oopforge:craft python-fastapi로 borrow-book 구현
/oopforge:craft borrow-book 테스트
```

프로젝트당 **한 스택**만 선택하세요. 두 트랙 모두 같은 `borrow-book` 유스케이스를 구현합니다.

자연어로 시작해도 됩니다:

```text
Follow OOPforge workflow for a library loan domain. Start at Discovery — no code yet.
```

---

## 단계

| 단계 | Java | Python |
|---|---|---|
| 1. Discovery | [01-discovery.ko.md](./01-discovery.ko.md) | 동일 |
| 2. Design | [02-design.ko.md](./02-design.ko.md) | 동일 |
| 3. Skeleton | [03-skeleton.ko.md](./03-skeleton.ko.md) § Java | [03-skeleton.ko.md](./03-skeleton.ko.md) § Python |
| 4. Implement | [04-implement-java.ko.md](./04-implement-java.ko.md) | [04-implement-python.ko.md](./04-implement-python.ko.md) |
| 5. Test | [05-test.ko.md](./05-test.ko.md) § Java | [05-test.ko.md](./05-test.ko.md) § Python |
| 6. 레이어 규칙 | [06-layer-rules.ko.md](./06-layer-rules.ko.md) | 동일 |

각 단계 파일 상단에서 EN · KO 전환 가능.

---

## 각 단계 이후

OOPforge는 **사람 승인**을 전제로 합니다. 출력을 검토·승인하기 전에 다음 단계로 넘어가지 마세요.

Implement 이후 규칙 위반 점검이 필요하면 `/oopforge:craft`에 Hard Rules 리뷰를 요청합니다.
