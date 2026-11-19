# Claude Code packaging

`plugin.json` describes the Claude Code package. `marketplace.json` is the
`forge` catalog: this repository as `./`, plus Compforge and FuseForge by HTTPS
git URL.

The supported runtime path is the symlink-installed skill and `/oopforge:craft`
command. The marketplace install (`/plugin install oopforge@forge`) is
experimental.

- Setup: [`../docs/setup/claude-code.md`](../docs/setup/claude-code.md)
- Support contract: [`../docs/reference/support-scope.md`](../docs/reference/support-scope.md)
- Verification: `scripts/ci/harness-smoke.sh live claude` and
  [`marketplace-2026-11-19.md`](../docs/verification/marketplace-2026-11-19.md)
