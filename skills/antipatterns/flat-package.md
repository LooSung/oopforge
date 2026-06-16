---
name: antipattern-flat-package
description: The anti-pattern of choosing layered/3-tier but not splitting layers into folders — separating only by filename suffix inside one folder.
tags: [antipattern, layered, structure]
stability: experimental
---

# Anti-pattern — Flat Package

## Symptom

You chose layered (3-tier) but there are no `controller/ service/ repository/ domain/` folders,
and `OrderController`, `OrderService`, `OrderRepository` are distinguished only by filename in one folder.

```text
order/
├── OrderController.java
├── OrderService.java
├── OrderRepository.java
└── Order.java
```

## Why it is bad

- The layer boundary depends only on a **naming convention** with no enforcement. Someone breaks it soon.
- A new file's layer is not revealed by a folder, so a dependency-direction violation (Controller -> Repository direct call) goes unnoticed.
- As the domain grows, filename prefixes get long (`OrderItemQueryServiceImpl`) and navigation collapses.
- When migrating gradually to hexagonal/clean, the unit to move is unclear.

## Why it happens

It is the **path of least resistance** for small models and fast generation. "Make a 3-tier app" -> one folder + filename suffixes.
Without a headless structure enforcement, it always collapses this way.

## Correct shape

Split layers into **physical folders**.

```text
order/
├── controller/OrderController.java
├── service/OrderService.java
├── repository/OrderRepository.java
└── domain/Order.java
```

Follow `skills/skeleton/backend-skeleton.md` for the detailed standard structure.

## Detection

- Right after the skeleton, the directory tree has no `controller/ service/ repository/` folders.
- `*Controller`, `*Service`, `*Repository` sit together in one folder.
- A Controller imports/calls a Repository directly.

## Remediation

1. Create `controller/ service/ repository/ domain/` folders.
2. Move each file into its own layer folder (behavior-preserving, `workflow/refactor.md`).
3. Verify the Controller -> Service -> Repository dependency direction.
4. Mirror the test folder to the same structure.

## Related

- `skills/skeleton/backend-skeleton.md` — standard layout + self-check
- `AGENTS.md` Hard Rules — Layer layout
- `skills/workflow/refactor.md` — behavior-preserving moves
