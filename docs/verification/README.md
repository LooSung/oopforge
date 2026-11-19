# Harness verification

Harness verification is release evidence, separate from the methodology
experiments under [`../proof/`](../proof/).

When a compatibility baseline is refreshed, its record includes:

- the candidate commit and date;
- Claude Code, Codex CLI, and Cursor Agent CLI versions;
- positive activation and isolated negative-control results;
- one advisory Craft routing result per harness;
- skipped or failed checks and their release impact.

The v1 baseline is recorded in [`harness-v1.0.0.md`](harness-v1.0.0.md).

[`marketplace-2026-11-19.md`](marketplace-2026-11-19.md) records the Claude
Code plugin marketplace install, update, and removal, plus live root and
activation probes on the installed copies.

[`evals-2026-11-16.md`](evals-2026-11-16.md) records `claude plugin eval` with and
without the plugin, plus Haiku and Sonnet, for v1.8.0, including the plugin
load-path defect it found.
