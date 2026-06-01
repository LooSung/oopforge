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

- [ ] Each new/edited skill file is **≤ 200 lines**
- [ ] Each touched code file is **≤ 300 lines**
- [ ] Methods kept around **≤ 20 lines** where reasonable
- [ ] Domain layer in examples has **0 framework imports**
- [ ] Skill follows `skills/_meta/skill-template.md` structure (frontmatter, 언제 쓰나, 체크리스트, 금지)
- [ ] New skill is referenced from `AGENTS.md` and `skills/SKILL.md` (so it gets discovered)
- [ ] `CHANGELOG.md` updated under `## [Unreleased]`
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
