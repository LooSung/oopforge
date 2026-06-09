# Contributing to OOPforge

Thanks for considering a contribution. OOPforge values **small, opinionated, measurable** additions over broad refactors. Read this once before opening your first PR.

## What kind of contributions we love

In rough priority order:

1. **Clarifying existing aggregate skills** — keep OOP rules in `skills/oop/domain-model.md` or `skills/oop/use-case-boundary.md`
2. **Backend stack / skeleton improvements** — stack selection in `skills/lang/backend-stack.md`, package structure in `skills/skeleton/backend-skeleton.md`
3. **Workflow fixes** — Discovery → Test behavior, Craft routing, or verification clarity
4. **Example projects** — runnable variants in `examples/`
5. **Translations** — Korean docs (English is primary; other languages only on request)
6. **Bug fixes / typos** — always welcome

## What we do not accept

- New narrowly scoped skill files when an existing aggregate skill can be extended
- Framework-specific code in `skills/oop/` (those must stay language-agnostic)
- Domain examples that import frameworks (`@Entity`, `@Component`, `from fastapi import` in domain code)
- Skills longer than 200 lines — split instead
- Files longer than 300 lines, methods longer than 20 lines (in examples)
- New runtime dependencies for installer scripts unless there's no shell alternative

See `AGENTS.md` → "Hard Rules" for the full ruleset.

## Workflow

### 1. Open an issue first (for anything non-trivial)

For new skills, language layouts, or workflow changes, open an issue describing the idea. Quick alignment saves a wasted PR.

Typo fixes and obvious bug fixes can skip this step.

### 2. Set up locally

```bash
git clone https://github.com/LooSung/oopforge.git
cd oopforge
./scripts/setup/install.sh         # installs to ~/.oopforge via symlinks
./scripts/setup/doctor.sh          # verifies links
```

### 3. Choose the smallest existing skill to edit

Categories:

| Category | What goes here |
|---|---|
| `skills/workflow/` | Stage-level process (Discovery, Design, ...) |
| `skills/oop/domain-model.md` | Aggregate, Value Object, Domain Event |
| `skills/oop/use-case-boundary.md` | Application service and Repository port |
| `skills/lang/backend-stack.md` | Backend stack selection |
| `skills/skeleton/backend-skeleton.md` | Backend package structure / skeleton |

### 4. Verify locally

```bash
./scripts/ci/lint-skills.sh        # 200-line rule, frontmatter, AGENTS.md refs
./scripts/ci/smoke-test.sh         # clean-HOME install test
```

CI runs both on every PR.

### 5. Wire in cross-references

If you edit or add a skill, update these so it gets discovered:

- `AGENTS.md` — "Task → skill" table and "Skill Selection" section
- `skills/SKILL.md` — "Supporting Skills" section
- `CHANGELOG.md` — add a line under `## [Unreleased]` → `### Added`

The lint script will tell you if you forgot a reference.

### 6. Open the PR

Use the PR template. Keep PRs focused — one skill or one feature per PR.

## Skill writing rules (short version)

Every skill must:

1. Start with YAML frontmatter (`name`, `description`, `tags`, `stability`)
2. Be ≤ 200 lines total
3. Have a **`## 언제 쓰나`** (when to use) section explaining the trigger condition
4. Have a **`## 체크리스트`** (checklist) with measurable items
5. Have a **`## 금지`** (forbidden) section — what *not* to do is usually the most valuable signal for AI agents
6. Have at least one code example if the skill involves code
7. Be focused on one concept (split if you find yourself teaching two)

## Language policy

| Area | Language |
|---|---|
| README & docs | English (primary) + Korean only; other languages only on request |
| `AGENTS.md`, scripts, CI | English |
| Skills (`skills/`) | Korean (default); English translations welcome under `skills/en/` (future) |
| PR descriptions, commit messages | English (preferred) or Korean |
| Issue discussions | English or Korean |

## Commit messages

Conventional Commits style:

```
docs(oop): clarify domain-model rules
fix(skeleton): correct java-spring-layered package path
docs(readme): clarify /oopforge:craft examples
chore(ci): bump lint script
```

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Be kind, assume good intent, focus on the work.

## Getting help

- **Bug?** Open an issue with the "bug" template.
- **Idea for a skill?** Open an issue with the "new skill" template.
- **Quick question?** Start a discussion (Discussions tab).

Thanks again — every small, well-scoped contribution makes the pack sharper.
