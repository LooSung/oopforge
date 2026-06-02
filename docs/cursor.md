# Cursor Setup

Use OOPforge with **Cursor Agent CLI** (`cursor-agent`) via `--plugin-dir`.

There is no `scripts/setup/install.sh` symlink target for Cursor. Marketplace packaging is Phase 2 (no ETA).

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

## 2. Load the plugin

Point `--plugin-dir` at the **pack root** (`~/.oopforge`), not `.cursor-plugin/`:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

Planning-only sessions (Discovery, Design, Delivery Plan):

```bash
cursor-agent --plugin-dir ~/.oopforge --plan
```

One-shot (non-interactive):

```bash
cursor-agent --plugin-dir ~/.oopforge -p "OOPforge Discovery: order domain. No code yet."
```

Optional shell alias:

```bash
alias cursor-oop='cursor-agent --plugin-dir ~/.oopforge'
```

After `git pull` in `~/.oopforge`, restart `cursor-agent` to pick up skill changes.

## 3. Example prompts

```text
Follow the OOPforge library loan walkthrough: docs/guides/library-loan/README.md
(Localized: README.ko.md · README.ja.md · README.zh.md in the same folder.)
Design an Order aggregate using OOPforge. Start at Discovery — no code yet.
```

```text
OOPforge Skeleton for place-order. Use skills/skeleton/backend-skeleton.md.
Domain layer framework imports: 0.
```

## 4. Recommended flow

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

Do not skip stages for new domains. See [README](../README.md#the-basic-workflow).

## 5. Reference example

```text
Match the structure in examples/order-java/ — domain has zero framework imports.
```

## Limitations

- **`--plugin-dir` per session** — pass the flag each run, or use a shell alias.
- **No bootstrap auto-link** — unlike Claude Code / Codex, `install.sh` does not configure Cursor.
- **Marketplace** — Phase 2; `.cursor-plugin/plugin.json` is a manifest only today.

## Related

- [Claude Code setup](./claude-code.md)