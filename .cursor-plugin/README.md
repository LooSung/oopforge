# Cursor packaging

`plugin.json` and `skills/oopforge/SKILL.md` package the verified explicit
`--plugin-dir` path. The adapter delegates to the canonical root skill.

- Setup: [`../docs/setup/cursor.md`](../docs/setup/cursor.md)
- Support contract: [`../docs/reference/support-scope.md`](../docs/reference/support-scope.md)
- Verification: `scripts/ci/harness-smoke.sh live cursor`

Use `cursor-agent --plugin-dir ~/.oopforge` and invoke
`Use OOPforge craft: …`. Marketplace installation, automatic discovery, and
headless `/oopforge:craft` are outside the current support contract.
