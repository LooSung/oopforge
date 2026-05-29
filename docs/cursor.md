# Cursor Setup

OOPforge does **not** have a Cursor installer yet (Phase 2). Use project-level rules today.

## 1. Install OOPforge (optional, for skills elsewhere)

If you use Claude Code or Codex too:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

For Cursor-only projects, skip this and copy rules into the repo (step 2).

## 2. Add OOPforge rules to your project

Copy or symlink the shared instructions:

```bash
curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/AGENTS.md -o AGENTS.md
```

In Cursor, reference `AGENTS.md` from project rules:

- **Project Rules** → add a rule that says: *Follow `AGENTS.md` and OOPforge workflow.*
- Or paste the Hard Rules + Required Workflow sections into `.cursor/rules/oopforge.mdc`

## 3. Open Composer / Agent

Example prompts:

```text
Design an Order aggregate using OOPforge. Start at Discovery — no code yet.
```

```text
Follow OOPforge workflow. Implement place-order in Java using examples/order-java as reference.
```

## 4. Recommended flow

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

Do not skip stages for new domains. See [README](../README.md#the-basic-workflow).

## 5. Reference example

Point the agent at the runnable proof:

```text
Match the structure in examples/order-java/ — domain has zero framework imports.
```

## Related

- [Claude Code setup](./claude-code.md)
- [OpenCode opt-in](./opencode.md)
