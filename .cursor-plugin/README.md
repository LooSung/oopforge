# Cursor Plugin Manifest

`.cursor-plugin/plugin.json` declares skills, agents, and commands paths for Cursor Agent CLI.

## Use today (Cursor Agent CLI)

After bootstrap, load the pack at runtime:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

Point `--plugin-dir` at the **pack root** (`~/.oopforge`), not this `.cursor-plugin/` directory.

There is no `scripts/setup/install.sh` symlink target for Cursor.

## Phase 2

Marketplace-style packaging and bootstrap integration (no ETA).
