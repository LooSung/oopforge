# Harness verification

Harness verification is release evidence, separate from the methodology
experiments under [`../proof/`](../proof/).

Each release record includes:

- the candidate commit and date;
- Claude Code, Codex CLI, and Cursor Agent CLI versions;
- positive activation and isolated negative-control results;
- one advisory Craft routing result per harness;
- skipped or failed checks and their release impact.

The v1 baseline is recorded in [`harness-v1.0.0.md`](harness-v1.0.0.md).
