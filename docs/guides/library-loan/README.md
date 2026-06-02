# Library Loan — Full OOPforge Walkthrough

> End-to-end **library loan system** in Java (Spring Boot) and Python (FastAPI).  
> Follow Discovery → Design → Delivery Plan → Skeleton → Implement → Test.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

This guide shows **how to use OOPforge end to end**. For a minimal runnable proof, see [`examples/order-java`](../../../examples/order-java/) and [`examples/order-python`](../../../examples/order-python/).

---

## Scenario

A member **borrows** a book. A book already on loan cannot be borrowed again. Borrowing publishes a `BookBorrowed` event.

---

## Craft Prompts

**Java track:**

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:craft Test borrow-book
```

**Python track** — same Discovery/Design/Delivery Plan; Skeleton only changes:

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in python-fastapi
/oopforge:craft Test borrow-book
```

Pick **one stack** per project. Both tracks implement the same `borrow-book` use case.

Natural language works too:

```text
Follow OOPforge workflow for a library loan domain. Start at Discovery — no code yet.
```

---

## Steps

| Step | Java | Python |
|---|---|---|
| 1. Discovery | [01-discovery.md](./01-discovery.md) | same |
| 2. Design | [02-design.md](./02-design.md) | same |
| 3. Skeleton | [03-skeleton.md](./03-skeleton.md) § Java | [03-skeleton.md](./03-skeleton.md) § Python |
| 4. Implement | [04-implement-java.md](./04-implement-java.md) | [04-implement-python.md](./04-implement-python.md) |
| 5. Test | [05-test.md](./05-test.md) § Java | [05-test.md](./05-test.md) § Python |
| 6. Layer rules | [06-layer-rules.md](./06-layer-rules.md) | same |

Each step file includes language links (EN · KO · JA · ZH) at the top.

---

## Short samples (agent output)

If you only need **expected Discovery/Design shape** for prompts:

| Language | Discovery | Design |
|---|---|---|
| English | [discovery-library.md](../../sample-output/discovery-library.md) | [design-library.md](../../sample-output/design-library.md) |
| 한국어 | [discovery-library.ko.md](../../sample-output/discovery-library.ko.md) | [design-library.ko.md](../../sample-output/design-library.ko.md) |
| 日本語 | [discovery-library.ja.md](../../sample-output/discovery-library.ja.md) | [design-library.ja.md](../../sample-output/design-library.ja.md) |
| 中文 | [discovery-library.zh.md](../../sample-output/discovery-library.zh.md) | [design-library.zh.md](../../sample-output/design-library.zh.md) |

---

## After each step

OOPforge expects a **human checkpoint**. Do not skip to the next stage until you approve the output.

After Implement, ask `/oopforge:craft` to review the result against the Hard Rules if you want a rule-violation pass.
