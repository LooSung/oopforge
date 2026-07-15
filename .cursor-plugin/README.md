# Cursor Plugin Manifest

`.cursor-plugin/plugin.json` is the experimental Cursor marketplace manifest.

## Use today

Use a project-local skill link from the target backend repository:

```bash
mkdir -p .cursor/skills
ln -s ~/.oopforge/skills .cursor/skills/oopforge
printf '%s\n' '.cursor/skills/oopforge' >> .git/info/exclude
cursor-agent
```

Clean headless smoke tests did not prove that `--plugin-dir` loaded Craft, so
the manifest is not presented as the verified automation path. There is no
`scripts/setup/install.sh` symlink target for Cursor.

## Phase 2

Marketplace-style packaging and bootstrap integration (no ETA).
