# Cursor Setup

OOPforge supports **Cursor Agent CLI** (`cursor-agent`) through the explicit
pack directory or a project-local skill. These are the canonical paths
in the [support scope](../reference/support-scope.md). There is no
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

`doctor.sh` checks the pack but does not configure Cursor or execute Craft.

## 2. Choose the load path

The primary path passes the installed pack directly with
`--plugin-dir ~/.oopforge`; no additional registration link is needed.

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

## 3. Run OOPforge commands

Start Cursor Agent and invoke Craft by name:

```bash
cd /path/to/your-backend-project
cursor-agent --plugin-dir ~/.oopforge
```

```text
Use OOPforge craft: Add a single Email value object
Use OOPforge craft: Read docs/integration/image-storage.md and advise only.
Use OOPforge refactor: Improve billing structure while preserving behavior.
```

Planning-only sessions (Discovery, Design, Delivery Plan):

```bash
cursor-agent --plan
```

One-shot (non-interactive):

```bash
cursor-agent --plugin-dir ~/.oopforge \
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

Restart `cursor-agent` after the pull. Cursor paths are not managed by
`scripts/setup/install.sh`. If you created the project-local alternative,
remove it with:

```bash
rm -f /path/to/your-backend-project/.cursor/skills/oopforge
```

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

Do not skip stages for new domains. See [README](../../README.md#the-basic-workflow).

## 7. Reference example

```text
Match the structure in examples/calculator-java-hexagonal/ — domain has zero framework imports.
```

## Limitations

- **Explicit load required** — a clean headless session loaded Craft with
  `--plugin-dir ~/.oopforge`; the pack directory without that flag
  returned `OOPFORGE_NOT_LOADED`.
- **Natural-language entry point** — use `Use OOPforge craft: …` or `Use
  OOPforge refactor: …`. OOPforge `/` commands are not supported Cursor
  headless commands.
- **External symlink target** — project-local symlink startup includes
  `--add-dir ~/.oopforge` so headless mode may read the pack.
- **No bootstrap auto-link** — unlike Claude Code / Codex, `install.sh` does not configure Cursor.
- **Marketplace** — local packaging is verified; marketplace publication is
  not supported.

### Local plugin smoke evidence

Maintainers can reproduce explicit-plugin, project-local, and no-skill controls
with an authenticated Cursor CLI:

```bash
./scripts/ci/harness-smoke.sh live cursor
```

The check requires `OOPFORGE_LOADED`, Assumptions, and OOP Contract from both
supported paths. Its isolated no-skill workspace must return
`OOPFORGE_NOT_LOADED`. It uses temporary workspaces and `CURSOR_CONFIG_DIR`
while retaining the real `HOME` so the OS credential-store token remains
available. Only non-secret login metadata (`version` and `authInfo`) is copied
into each temporary config. The negative control catches any user-level
OOPforge installation that would contaminate isolation. Never add a provider
key as a repository secret; live smoke remains a local release check.

## Related

- [Claude Code setup](./claude-code.md)
