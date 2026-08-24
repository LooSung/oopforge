# Library Loan — Full OOPforge Walkthrough

> End-to-end **library loan system** in Java (Spring Boot) and Python (FastAPI).  
> Follow Discovery → Design → Delivery Plan → Skeleton → Implement → Test.

[English](./README.md) · [한국어](./README.ko.md)

This guide shows **how to use OOPforge end to end**. For a minimal runnable proof, see [`examples/calculator-java-hexagonal`](../../../examples/calculator-java-hexagonal/) and [`examples/calculator-python-hexagonal`](../../../examples/calculator-python-hexagonal/).

---

## Scenario

A member **borrows** a book. A book already on loan cannot be borrowed again.
Borrowing records and dispatches a `BookBorrowed` event in process.

---

## Craft Prompts

**Shared stages, with a human checkpoint after each command:**

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Continue the approved library loan work to Design. Signatures only.
/oopforge:craft Create the Delivery Plan for the approved borrow-book design.
/oopforge:craft Create the approved Skeleton in java-spring-hexagonal.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:craft Test borrow-book
```

**Python track** — use the same approved artifacts and change only the stack:

```text
/oopforge:craft Create the approved Skeleton in python-fastapi-clean.
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
| 3. Delivery Plan | [03-delivery-plan.md](./03-delivery-plan.md) | same |
| 4. Skeleton | [04-skeleton.md](./04-skeleton.md) § Java | [04-skeleton.md](./04-skeleton.md) § Python |
| 5. Implement | [05-implement-java.md](./05-implement-java.md) | [05-implement-python.md](./05-implement-python.md) |
| 6. Test | [06-test.md](./06-test.md) § Java | [06-test.md](./06-test.md) § Python |
| 7. Layer rules | [07-layer-rules.md](./07-layer-rules.md) | same |

Each step file includes language links (EN · KO) at the top.

---

## After each step

OOPforge expects a **human checkpoint**. Do not skip to the next stage until you approve the output.

After Implement, ask `/oopforge:craft` to review the result against the Hard Rules if you want a rule-violation pass.
