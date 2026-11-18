# OOPforge Proof Result — <date, model>

## Status

- Result: valid | invalid
- Invalid reason: none | <reason>
- Source commit:
- Starter:
- Cursor Agent version:
- Model:
- Run ID:

## Task

Use the fixed task from [`README.md`](./README.md#fixed-task).

## Conditions

- Control plugin: none
- Treatment delivery: project-local OOPforge skill at the source commit above
- Manual edits during runs: none
- Same model and starter confirmed: yes | no
- Treatment skill load confirmed by `.craft/` creation: yes | no

## Control

- Tests:
- Changed files:
- Architecture violations:
- Missing coverage:
- Architecture-driven rework:
- Raw artifact location or durable link:

## OOPforge

- Tests:
- Changed files:
- Architecture violations:
- Missing coverage:
- Architecture-driven rework:
- Raw artifact location or durable link:

## Finding-by-finding comparison

List each evaluator finding, the affected file, and whether human review agrees.
Explain false positives and false negatives instead of silently removing them.

## Cost and human attention

Record per arm. These are context for the violation counts, not success metrics.

| Measure | Control | Treatment |
|---|---|---|
| Wall time | | |
| Tokens used | | |
| Decisions asked of the human | | |
| Of those, answers that changed the recommendation | | |

A high share of "as recommended" answers marks questions the workflow could
default instead.

## Design-stage findings

List defects the treatment caught before writing code, such as a lost-data path
found during Design. For each, state what it would have cost if found after
implementation: the files to rework and whether users would have seen it. The
violation count above does not measure this.

## Interpretation

State only what this pair demonstrates. Do not generalize a single run into a
percentage improvement or a claim about other models, stacks, or tasks.

## Validity notes

- Starter-architecture bias:
- Model stochasticity:
- Evaluator limitations:
- Evaluator commit, recorded before the runs:
- Other:

