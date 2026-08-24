## What this PR does

One sentence.

## Type of change

- [ ] New skill
- [ ] Skill edit (clarification, fix, restructure)
- [ ] New language layout / example
- [ ] Workflow command change
- [ ] Documentation / README / translation
- [ ] Installer / CI / scripts
- [ ] Bug fix
- [ ] Other:

## OOPforge rules checklist

- [ ] Each touched file is **≤ 300 lines**; each skill is **≤ 200 lines**
- [ ] Methods kept around **≤ 20 lines** where reasonable
- [ ] Example domain layers have **0 framework imports** (when applicable)
- [ ] New/edited skills follow the conditional structure in `CONTRIBUTING.md`
- [ ] New skills are registered in `skills/stability.json` and routed where needed
- [ ] User-visible completed work is recorded under `CHANGELOG.md` → `Unreleased`
- [ ] Local lint passes: `./scripts/ci/lint-skills.sh`

## How I tested

- [ ] `./scripts/ci/lint-skills.sh`
- [ ] `./scripts/ci/smoke-test.sh`
- [ ] Tried the skill/command with an agent (Claude Code / Codex / Cursor): _____
- [ ] Other:

## Related issue

Closes #

## Notes for reviewers

Anything reviewers should focus on, trade-offs you considered, things you're unsure about.
