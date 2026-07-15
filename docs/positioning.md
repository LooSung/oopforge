# OOPforge — Positioning

## One sentence

OOPforge is a spec-driven OOP/DDD methodology and architecture-enforcement pack
for coding agents building Java Spring and Python FastAPI backends.

## Category

OOPforge is **vertical harness engineering for backend architecture**.

It does not replace a coding agent. It gives the agent a domain-modeling
language, a staged delivery workflow, measurable architecture rules, runnable
references, and fitness functions.

The operating model is:

- skills are the grammar;
- `AGENTS.md` is the constitution;
- hard rules and CI checks are the lint;
- runnable examples are the reference implementations;
- Craft is the single entry point.

## The problem

General-purpose coding agents can produce working backend code while quietly
eroding its architecture. Common failure modes include:

- business rules accumulating in services or controllers;
- domain models becoming passive data containers;
- repositories making business decisions;
- framework dependencies leaking into the domain;
- aggregate and transaction boundaries remaining implicit;
- planning, implementation, and verification collapsing into one step.

More prompting is not a durable fix. The constraints must be repeatable,
reviewable, and encoded in the development environment.

## The promise

> AI ships the feature. OOPforge keeps the architecture.

OOPforge makes domain language, object responsibility, use-case boundaries,
and verification explicit before business logic is written. It aims to reduce
architecture violations and architecture-driven rework, not token usage.

## Who it is for

OOPforge is for:

- teams using coding agents on Java Spring or Python FastAPI backends;
- teams that want OOP/DDD discipline without adopting a code generator;
- services where domain behavior and boundaries matter beyond basic CRUD;
- reviewers who want architecture rules expressed as checks, not preferences.

It is especially useful when a team needs a repeatable path from ambiguous
requirements to a domain model, ports, adapters, and tests.

## Who it is not for

OOPforge is not intended for:

- frontend, mobile, data science, or ML development;
- generic code search, indexing, memory, or context compression;
- multi-agent orchestration, worktree management, or session scheduling;
- automatic application generation;
- teams optimizing primarily for token or model cost;
- projects that intentionally prefer transaction scripts or framework-first
  domain models.

## How it differs

### General-purpose coding agents

General agents decide how to solve a task. OOPforge constrains how backend
domain work is discovered, designed, implemented, and verified. It is a layer
on top of the agent, not a competing agent.

### Specification and planning tools

General specification tools help describe what to build. OOPforge specializes
the specification around aggregates, invariants, state transitions, ports,
transaction boundaries, and architecture fitness functions.

### Code generators and templates

Generators produce a predefined structure or implementation. OOPforge teaches
and checks boundaries while leaving code generation to the active coding
agent. Its examples are references, not scaffolding output.

### Static architecture tools

Architecture tools detect dependency violations. OOPforge combines those
checks with the workflow and modeling guidance that prevent violations before
they are introduced. Existing tools such as ArchUnit and import-linter remain
part of the enforcement layer.

### Prompt libraries

Prompt libraries provide reusable instructions. OOPforge adds stage
boundaries, human checkpoints, an OOP Contract, measurable hard rules,
reference implementations, and CI-backed checks.

## The wedge

OOPforge stays narrow to go deep:

1. Java Spring and Python FastAPI backends.
2. Layered and hexagonal/clean architecture.
3. Tactical DDD: aggregates, value objects, domain events, ports, and
   transaction boundaries.
4. Enforcement through review rules, examples, and fitness functions.

Expansion is justified only when the new capability strengthens this vertical
focus and can be demonstrated with runnable references.

## Product principles

- **Workflow before code** — new domains move through Discovery, Design,
  Delivery Plan, Skeleton, Implement, and Test.
- **Small skills** — one concept per skill, no mega-prompts.
- **Domain first** — framework concerns stay outside the domain.
- **Measurable rules** — important constraints should become tests or lint.
- **Human checkpoints** — agents do not silently cross major stage boundaries.
- **Proof over claims** — runnable examples and reproducible comparisons carry
  more weight than architecture prose.

## Evidence standard

OOPforge should not claim effectiveness from a curated code snippet alone.
Positioning claims should be supported by reproducible before/after runs using:

- the same task, target stack, model, and starting repository;
- a control run without OOPforge and a treatment run with OOPforge;
- a published prompt and evaluation checklist;
- architecture-violation counts by rule;
- architecture-driven rework required to pass the same review;
- raw diffs or artifacts that others can inspect.

Token usage and elapsed time may be recorded as context, but they are not the
primary success metrics.

Until such runs are published, statements about reduced violation or rework
rates must be presented as goals rather than measured results.

The canonical experiment design and publication checklist live in the
[proof protocol](proof/README.md).

## Messaging guardrails

Prefer:

- "architecture-enforcement pack for coding agents";
- "spec-driven OOP/DDD methodology";
- "vertical harness engineering for Java and Python backends";
- "reduces architecture violations and rework" when evidence is linked.

Avoid:

- "general AI development framework";
- "autonomous software factory";
- "works for every language and architecture";
- unmeasured percentage improvements;
- claims that workflow instructions alone guarantee compliance.

## Adoption path

The shortest useful adoption path is:

1. install or load the pack;
2. run Craft from the target backend repository;
3. use the smallest execution path for the task;
4. add the relevant architecture checks to CI;
5. compare review findings before and after adoption.

The methodology remains useful without marketplace packaging or an MCP server.
Those integrations reduce friction and tighten feedback; they do not define the product.
