# Contributing to OOPforge

Thanks for considering a contribution. OOPforge values **small, opinionated, measurable** additions over broad refactors. Read this once before opening your first PR.

## What kind of contributions we love

In rough priority order:

1. **New skills** — one concept per file, ≤ 200 lines (e.g., `python-saga.md`, `java-cqrs-handler.md`)
2. **Anti-pattern catalog entries** — `skills/antipatterns/*.md` to teach `@domain-reviewer` what to flag
3. **Lint/enforcement templates** — ArchUnit (Java), `import-linter` (Python) so the rules are PR-blockable
4. **Language layouts** — new stacks (Kotlin Spring, NestJS, .NET) following the existing layered + hexagonal pattern
5. **Example projects** — runnable variants in `examples/` (e.g., `order-java-layered/`, `order-python-layered/`)
6. **Translations** — KO/JA/ZH skill or doc translations
7. **Bug fixes / typos** — always welcome

## What we do not accept

- Mega-skills that teach more than one concept in one file
- Framework-specific code in `skills/oop/` (those must stay language-agnostic)
- Domain examples that import frameworks (`@Entity`, `@Component`, `from fastapi import` in domain code)
- Skills longer than 200 lines — split instead
- Files longer than 300 lines, methods longer than 20 lines (in examples)
- New runtime dependencies for installer scripts unless there's no shell alternative

See `AGENTS.md` → "Hard Rules" and `skills/_meta/skill-template.md` for the full ruleset.

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

### 3. Create your skill from the template

```bash
cp skills/_meta/skill-template.md skills/<category>/<new-skill>.md
# edit
```

Categories:

| Category | What goes here |
|---|---|
| `skills/_meta/` | Meta rules, templates |
| `skills/workflow/` | Stage-level process (Discovery, Design, ...) |
| `skills/oop/` | Language-agnostic OOP/DDD concepts |
| `skills/lang/<lang>/` | Language- or framework-specific concretizations |
| `skills/lang/api/` | API contract conventions (OpenAPI, gRPC) |
| `skills/antipatterns/` | "Don't do this" entries for `@domain-reviewer` |

### 4. Verify locally

```bash
./scripts/ci/lint-skills.sh        # 200-line rule, frontmatter, AGENTS.md refs
./scripts/ci/smoke-test.sh         # clean-HOME install test
```

CI runs both on every PR.

### 5. Wire in cross-references

If you add a new skill, update these so it gets discovered:

- `AGENTS.md` — "Task → skill" table and "Skill Selection" section
- `skills/SKILL.md` — "Supporting Skills" section
- `CHANGELOG.md` — add a line under `## [Unreleased]` → `### Added`

The lint script will tell you if you forgot a reference.

### 6. Open the PR

Use the PR template. Keep PRs focused — one skill or one feature per PR.

## Skill writing rules (short version)

Every skill must:

1. Start with the YAML frontmatter from `skills/_meta/skill-template.md`
2. Be ≤ 200 lines total
3. Have a **`## 언제 쓰나`** (when to use) section explaining the trigger condition
4. Have a **`## 체크리스트`** (checklist) with measurable items
5. Have a **`## 금지`** (forbidden) section — what *not* to do is usually the most valuable signal for AI agents
6. Have at least one code example if the skill involves code
7. Be focused on one concept (split if you find yourself teaching two)

## Language policy

| Area | Language |
|---|---|
| README | English primary, KO/JA/ZH translations welcome |
| `AGENTS.md`, scripts, CI | English |
| Skills (`skills/`) | Korean (default); English translations welcome under `skills/en/` (future) |
| PR descriptions, commit messages | English (preferred) or Korean |
| Issue discussions | Any of EN/KO/JA/ZH |

## Commit messages

Conventional Commits style:

```
feat(oop): add specification-pattern skill
fix(skeleton): correct java-spring-layered package path
docs(readme): clarify /oopforge:route examples
chore(ci): bump lint script
```

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Be kind, assume good intent, focus on the work.

## Getting help

- **Bug?** Open an issue with the "bug" template.
- **Idea for a skill?** Open an issue with the "new skill" template.
- **Quick question?** Start a discussion (Discussions tab).

Thanks again — every small, well-scoped contribution makes the pack sharper.
