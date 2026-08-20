# Cursor Setup

OOPforge 1.x supports **Cursor Agent CLI** (`cursor-agent`) through an explicit
local plugin directory or a project-local skill. These are the canonical paths
in the [support contract](./support-contract.md). There is no
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

Project-local skill links remain a supported alternative. Because the symlink
target is outside the project, include the pack with `--add-dir`:

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

If you chose the project-local skill alternative, start with
`cursor-agent --add-dir ~/.oopforge` and omit `--plugin-dir`. After
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
  `/oopforge:craft` is not a supported Cursor headless command.
- **External symlink target** — project-local symlink startup includes
  `--add-dir ~/.oopforge` so headless mode may read the pack.
- **No bootstrap auto-link** — unlike Claude Code / Codex, `install.sh` does not configure Cursor.
- **Marketplace** — local packaging is verified; marketplace publication is
  separate future work.

### Local plugin smoke evidence

Maintainers can reproduce explicit-plugin, project-local, and no-skill controls
with an authenticated Cursor CLI:

```bash
./scripts/ci/harness-smoke.sh live cursor
```

The check requires `OOPFORGE_LOADED`, Assumptions, and OOP Contract from both
supported paths. Its isolated no-skill workspace must return
`OOPFORGE_NOT_LOADED`. CI runs this contract on tags and the weekly schedule;
a missing `CURSOR_API_KEY` fails the gate.

## Related

- [Claude Code setup](./claude-code.md)
