---
name: kotlin-spring
description: Express the OOPforge Hard Rules in Kotlin Spring code — val-only domain state, factory-guarded invariants, copy() visibility, collection copies, and @field validation targets.
tags: [kotlin, spring, domain, validation]
stability: experimental
---

# Kotlin Spring

## When to use

Use this with `skeleton/backend-skeleton.md` for a `kotlin-spring-*` stack.
Kotlin Spring is **experimental**: the references, `archlint.py`, and the domain
review cover it, but it sits outside the 1.x compatibility promise.

## Toolchain

- Same as the Java references: Spring Boot 3.5, Gradle 8.12 wrapper, JDK 21
  toolchain, springdoc, ArchUnit (it reads Kotlin bytecode unchanged).
- Kotlin Gradle plugin 2.4.21 with `plugin.spring` (all-open for Spring beans),
  `jackson-module-kotlin`, `kotlin-reflect`, and `-Xjsr305=strict`.
- Never let `plugin.jpa` or no-arg shape a domain class; JPA entities stay in
  the persistence adapter with a mapper.

## Hard Rules in Kotlin

| Hard Rule | Kotlin form | Checked by |
|---|---|---|
| Domain framework imports: 0 | no `org.springframework`, `jakarta.persistence`, `javax.persistence`, `org.hibernate` in `domain/` | review, ArchUnit |
| No public setters | domain properties are `val`; a state change is a behaviour method over `private set` | review (public `var` in a primary constructor or class body) |
| Factory guards invariants | an Aggregate is a plain `class` with a `private constructor` and a companion factory | code review |
| Boundary collections are copied | accept and expose `toList()` copies; a read-only `List` is a view, not a copy | code review |
| Intent in types | non-null domain types; no `!!` or `lateinit` in `domain/` | code review |

## `data class` and `copy()`

A `data class` with a private constructor still has a **public** `copy()` at
Kotlin 2.4.21 — the compiler only warns — so `copy(amount = -1)` skips the
factory. Choose one:

- annotate it `@ConsistentCopyVisibility`; `copy()` then follows the
  constructor's visibility (verified: an outside call fails to compile), or
- keep the invariant in `init { require(...) }`, which `copy()` cannot skip.

A `data class` with a public constructor and no invariant (an ID wrapper, a
DTO) needs neither.

## Boundary DTOs

- Write Bean Validation constraints with the `@field:` target:
  `data class CalculateRequest(@field:NotNull val operandA: Double?)`.
  Verified: on Kotlin 2.0.21 a bare `@NotNull` on a constructor property is
  silently skipped (missing field → 200); 2.4.21 applies it (→ 400). `@field:`
  is correct on both.
- A non-null `Double`, `Int`, `Long`, or `Boolean` compiles to a JVM primitive,
  so a missing JSON field still becomes `0`/`false`, exactly as in Java. Set
  `spring.jackson.deserialization.fail-on-null-for-primitives: true` to reject
  it with 400 (the layered reference does; verified). A missing non-null
  object type — an enum, a `String` — is already rejected with 400 by
  `jackson-module-kotlin`. Decide which the contract wants.
- `Optional<T>` becomes `T?`.

## Files and names

- One top-level class, interface, or object per file, named after it; the
  application file may also hold `fun main`. The checks key on file names:
  `*Controller.kt`, `*Service.kt`, `*Repository.kt`, `*CommandService.kt`,
  `*QueryService.kt`.
- Every public function in a `*CommandService.kt` declares its return type;
  `archlint.py cqrs` reports an expression body without one.

## What the checks cannot see

- The review scans text: a `var` preceded by an annotation on the same line,
  or a mutation hidden in a custom setter, is not reported.
- Method length counts an expression body until the next line at the same or
  lower indent.
- Collection copies, `!!`, and `lateinit` are code-review items.

## Prohibited

- A public `var`, `lateinit`, or `!!` in `domain/`.
- A private-constructor `data class` without `@ConsistentCopyVisibility` or
  `init` validation.
- Bare Bean Validation annotations on constructor properties.
- Framework annotations or compiler-plugin requirements driving domain design.
