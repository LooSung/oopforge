# 도서관 대출 — OOPforge 전체 워크플로우

> Java (Spring Boot)와 Python (FastAPI)로 **도서관 대출 시스템**을 처음부터 끝까지 구현합니다.  
> Discovery → Design → Delivery Plan → Skeleton → Implement → Test 순서로 진행합니다.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

OOPforge **사용법**을 단계별로 보여주는 가이드입니다. 최소 실행 예제는 [`examples/order-java`](../../../examples/order-java/), [`examples/order-python`](../../../examples/order-python/)를 참고하세요.

---

## 시나리오

회원이 도서를 **대출**한다. 대출 중인 도서는 다시 대출할 수 없다. 대출하면 `BookBorrowed` 이벤트가 발행된다.

---

## 슬래시 명령 (Claude Code)

**Java 트랙:**

```text
/oopforge:discovery library loan domain
/oopforge:design borrow-book use case
/oopforge:delivery-plan borrow-book
/oopforge:skeleton java-spring
/oopforge:implement borrow-book
/oopforge:test borrow-book
```

**Python 트랙** — Discovery/Design/Delivery Plan은 동일. Skeleton만 다름:

```text
/oopforge:discovery library loan domain
/oopforge:design borrow-book use case
/oopforge:delivery-plan borrow-book
/oopforge:skeleton python-fastapi
/oopforge:implement borrow-book
/oopforge:test borrow-book
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

각 단계 파일 상단에서 EN · KO · JA · ZH 전환 가능.

---

## 짧은 샘플 (에이전트 출력)

프롬프트용 **Discovery/Design 기대 형태**만 필요할 때:

| 언어 | Discovery | Design |
|---|---|---|
| English | [discovery-library.md](../../sample-output/discovery-library.md) | [design-library.md](../../sample-output/design-library.md) |
| 한국어 | [discovery-library.ko.md](../../sample-output/discovery-library.ko.md) | [design-library.ko.md](../../sample-output/design-library.ko.md) |
| 日本語 | [discovery-library.ja.md](../../sample-output/discovery-library.ja.md) | [design-library.ja.md](../../sample-output/design-library.ja.md) |
| 中文 | [discovery-library.zh.md](../../sample-output/discovery-library.zh.md) | [design-library.zh.md](../../sample-output/design-library.zh.md) |

---

## 각 단계 이후

OOPforge는 **사람 승인**을 전제로 합니다. 출력을 검토·승인하기 전에 다음 단계로 넘어가지 마세요.

Implement 이후 `@domain-reviewer`로 규칙 위반 여부를 점검할 수 있습니다.
