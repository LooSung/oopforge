---
name: workflow-consult
description: Answer, propose, review, or write one planning document for backend OOP work without changing implementation code.
tags: [workflow, advisory, review, planning]
stability: experimental
---

# Workflow — Consult

## Purpose

Give evidence-backed technical advice without turning an advisory request into
permission to implement. Select exactly one mode per invocation: `answer`,
`proposal`, `review`, or `document`.

## When to use

Use for backend OOP questions, alternatives, architecture or rule review, and
explicit requests to create or update a planning or technical-specification
document. Use Craft for implementation and Refactor for behavior-preserving
code changes.

## Startup

1. Confirm the target project and resolve user paths against it.
2. Read the request and only the code, project rules, and OOPforge skills needed
   to support the answer.
3. Select one mode using the priority below.
4. Begin with `Mode: <mode> | Write permission: <scope>` using the exact
   lowercase mode token. Do not emit narrative before this header.
5. Perform only that mode and report residual uncertainty or verification gaps.

Consult does not auto-create continuity files. If the target project already
has relevant continuity or planning records, read them as evidence.

## Mode selection

Select the first explicit signal that matches:

1. **Document** — create, write, update, save, or document wording.
2. **Review** — review, audit, inspect, or rule-check wording.
3. **Proposal** — alternatives, recommendation, direction, or comparison wording.
4. **Answer** — default for a question or advisory request.

A request to compare options or recommend one is always Proposal, even when it
is phrased as a question.

If the user asks to “review and fix,” complete Review only. Offer Craft or
Refactor as a separate next action; do not change mode silently.

## Answer

Input: a question and optional context.

Output:

- lead with the direct answer;
- cite repository evidence when available;
- label inference, uncertainty, and missing context;
- state the smallest useful next action, if any.

Write permission: none.

## Proposal

Input: a goal, constraints, and optional current-state evidence.

Output:

- present no more than three viable alternatives;
- recommend one and name the deciding tradeoff;
- name the user or repository evidence that earns extra structure; a domain
  label is never evidence;
- without concrete evidence, recommend the simpler path provisionally and ask
  the one question that would justify upgrading it;
- separate current facts from proposed decisions;
- leave unconfirmed decisions in Open Questions.

Write permission: none.

## Review

Input: a target and optional review scope.

Read the target project's rules first. Load only relevant OOPforge Hard Rules,
anti-patterns, and `docs/reference/reviewer-checklist.md` sections.

Output:

1. blocking correctness, safety, or Hard Rule findings with evidence;
2. optional maintainability advice in a separate section;
3. residual risks or checks that were not run.

If there are no findings, say so explicitly. Write permission: none.

## Document

Input: an explicit document request, optional target, and optional output path.

Choose the destination in this order:

1. the user's explicit path;
2. an existing project technical spec or template;
3. the current approved OOPforge workflow artifact;
4. `docs/<feature>/tech-spec.md` when the user explicitly requested a new tech
   spec and the project has no convention.

Inspect relevant current code before documenting implemented behavior. Separate
current facts, proposed decisions, risks, and Open Questions. Do not describe a
proposal as completed work.

For a new domain or large feature, follow Discovery → Design → Delivery Plan
and write only the current approved stage artifact. Stop at its human checkpoint.

Write permission: one planning/specification document. Update a directly
required index or link only when the user requested it or project rules require it.

## Conditional production guidance

Read `skills/workflow/production-readiness.md` only when the user explicitly
asks about deployment, production, or operational readiness. Otherwise keep
ordinary validation, risks, and review on the normal Consult path.

## Prohibited

- Never modify production code, test code, configuration, CI, or dependencies.
- Never apply Review findings or Proposal recommendations in the same request.
- Never write a document without explicit document wording.
- Never manufacture evidence or present inference as observed fact.
- Never collapse required workflow stages or their human checkpoints.
- Never widen OOPforge beyond its supported backend scope.

## Completion

Report the selected mode, evidence inspected, files written (normally none),
open questions, and the next command if implementation or refactoring is needed.
