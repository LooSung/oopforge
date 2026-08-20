# Cursor Setup (Experimental)

Use OOPforge with **Cursor Agent CLI** (`cursor-agent`) through an explicit
local plugin directory or a project-local skill. There is no
`scripts/setup/install.sh` target for Cursor.

## 1. Install OOPforge

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Or clone manually:

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x scripts/setup/*.sh
./scripts/setup/doctor.sh
```

`doctor.sh` checks the pack but does not register Cursor or execute Craft.

## 2. Register the local plugin

Link the installed pack into Cursor's local-plugin directory:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s ~/.oopforge ~/.cursor/plugins/local/oopforge
```

Pass this directory explicitly when starting Cursor Agent. Headless sessions
did not discover it from the directory alone.

Project-local skill links remain a verified alternative:

```bash
cd /path/to/your-backend-project
mkdir -p .cursor/skills
ln -s ~/.oopforge/skills .cursor/skills/oopforge
printf '%s\n' '.cursor/skills/oopforge' >> .git/info/exclude
```

Start the agent from the target project so paths like `docs/foo.md` resolve in
the app repository. For OOPforge maintenance, the pack repository is the work
target.

## 3. Run Craft

Start Cursor Agent and invoke Craft by name:

```bash
cd /path/to/your-backend-project
cursor-agent --plugin-dir ~/.cursor/plugins/local/oopforge
```

```text
Use OOPforge craft: Add a single Email value object
Use OOPforge craft: Read docs/integration/image-storage.md and advise only.
```

Planning-only sessions (Discovery, Design, Delivery Plan):

```bash
cursor-agent --plan
```

One-shot (non-interactive):

```bash
cursor-agent --plugin-dir ~/.cursor/plugins/local/oopforge \
  -p "Use OOPforge Discovery: order domain. No code yet."
```

If you chose the project-local skill alternative, omit `--plugin-dir`. After
`git pull` in `~/.oopforge`, restart `cursor-agent` to pick up changes.

## 4. Update or remove

A GitHub Release does not update the local clone:

```bash
cd ~/.oopforge && git pull
```

Restart `cursor-agent` after the pull. Cursor links are not managed by
`scripts/setup/install.sh`. To unregister them:

```bash
rm -f ~/.cursor/plugins/local/oopforge
rm -f /path/to/your-backend-project/.cursor/skills/oopforge
```

The second command applies only if you created the project-local alternative.
Also remove the matching `.cursor/skills/oopforge` line from
`.git/info/exclude` if you added it during setup. The source pack at
`~/.oopforge` is kept.

## 5. Example prompts

```text
Follow the OOPforge library loan walkthrough: docs/guides/library-loan/README.md
(Localized: README.ko.md in the same folder.)
Design an Order aggregate using OOPforge. Start at Discovery — no code yet.
```

```text
OOPforge Skeleton for place-order. Use skills/skeleton/backend-skeleton.md.
Domain layer framework imports: 0.
```

## 6. Recommended flow

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

Do not skip stages for new domains. See [README](../README.md#the-basic-workflow).

## 7. Reference example

```text
Match the structure in examples/calculator-java-hexagonal/ — domain has zero framework imports.
```

## Limitations

- **Explicit load required** — a clean headless session loaded Craft with
  `--plugin-dir ~/.cursor/plugins/local/oopforge`; the local directory alone
  returned `OOPFORGE_NOT_LOADED`.
- **Natural-language entry point** — use `Use OOPforge craft: …`.
  `/oopforge:craft` did not expand as a Cursor headless command.
- **No bootstrap auto-link** — unlike Claude Code / Codex, `install.sh` does not configure Cursor.
- **Marketplace** — local packaging is verified; marketplace publication is
  separate future work.

### Local plugin smoke evidence

The result above was reproduced with Cursor Agent `2026.08.11-e8db854` in an
empty workspace after temporarily isolating other OOPforge links:

```bash
mkdir -p /tmp/oopforge-cursor-plugin-smoke
ln -s ~/.oopforge ~/.cursor/plugins/local/oopforge
PROBE="Use OOPforge craft for an advisory-only Java value-object question. \
If no OOPforge skill is automatically available, output OOPFORGE_NOT_LOADED \
and stop. Do not search the filesystem for OOPforge."
cursor-agent --print --mode ask --trust \
  --workspace /tmp/oopforge-cursor-plugin-smoke \
  --plugin-dir ~/.cursor/plugins/local/oopforge \
  "$PROBE"
cursor-agent --print --mode ask --trust \
  --workspace /tmp/oopforge-cursor-plugin-smoke \
  "$PROBE"
```

With `--plugin-dir`, the probe automatically read the packaged adapter,
`skills/SKILL.md`, `workflow/craft.md`, and `principles/oop-discipline.md`.
Without the flag it returned `OOPFORGE_NOT_LOADED`. The project-local skill
alternative passed the same positive control, while a no-skill workspace
returned `OOPFORGE_NOT_LOADED`.

## Related

- [Claude Code setup](./claude-code.md)
