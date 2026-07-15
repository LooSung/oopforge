# Cursor Setup (Experimental)

Use OOPforge with **Cursor Agent CLI** (`cursor-agent`) as a project-local
skill. There is no `scripts/setup/install.sh` target for Cursor. Marketplace
packaging is Phase 2 (no ETA).

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

## 2. Link the skill into the target project

From the backend project, create a local skill link and keep it out of Git:

```bash
cd /path/to/your-backend-project
mkdir -p .cursor/skills
ln -s ~/.oopforge/skills .cursor/skills/oopforge
printf '%s\n' '.cursor/skills/oopforge' >> .git/info/exclude
```

Cursor discovers project-local skills, including symlinks. Start the agent from
this target project so paths like `docs/foo.md` resolve in the app repository.

## 3. Run Craft

Start Cursor Agent and invoke Craft by name:

```bash
cursor-agent
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
cursor-agent -p "Use OOPforge Discovery: order domain. No code yet."
```

After `git pull` in `~/.oopforge`, restart `cursor-agent` to pick up skill
changes through the symlink.

## 4. Example prompts

```text
Follow the OOPforge library loan walkthrough: docs/guides/library-loan/README.md
(Localized: README.ko.md in the same folder.)
Design an Order aggregate using OOPforge. Start at Discovery — no code yet.
```

```text
OOPforge Skeleton for place-order. Use skills/skeleton/backend-skeleton.md.
Domain layer framework imports: 0.
```

## 5. Recommended flow

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

Do not skip stages for new domains. See [README](../README.md#the-basic-workflow).

## 6. Reference example

```text
Match the structure in examples/calculator-java-hexagonal/ — domain has zero framework imports.
```

## Limitations

- **Project-local setup** — each target repository needs its own skill link.
- **`--plugin-dir` is not the verified headless path** — clean one-shot smoke
  tests did not prove that it loaded Craft, so this guide does not claim it for
  automation.
- **No bootstrap auto-link** — unlike Claude Code / Codex, `install.sh` does not configure Cursor.
- **Marketplace** — Phase 2; `.cursor-plugin/plugin.json` is a manifest only today.

## Related

- [Claude Code setup](./claude-code.md)