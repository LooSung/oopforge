# Cursor Plugin Manifest

`.cursor-plugin/plugin.json` is the experimental Cursor marketplace manifest.

## Use today

Register the pack as a local plugin, then pass the directory explicitly:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s ~/.oopforge ~/.cursor/plugins/local/oopforge
cd /path/to/your-backend-project
cursor-agent --plugin-dir ~/.cursor/plugins/local/oopforge
```

Invoke Craft with `Use OOPforge craft: <request>`. There is no
`scripts/setup/install.sh` symlink target for Cursor.

## Local plugin verdict

The current package loaded Craft in a clean headless Cursor Agent test on
2026-08-20 (`2026.08.11-e8db854`) when supplied with `--plugin-dir`.

Test conditions:

- empty temporary workspace;
- existing Claude and Codex OOPforge links temporarily isolated;
- this repository linked at `~/.cursor/plugins/local/oopforge`;
- fresh one-shot sessions with positive and negative controls.

The explicit plugin run automatically read the packaged adapter,
`skills/SKILL.md`, `workflow/craft.md`, and `principles/oop-discipline.md`.
Directory discovery without `--plugin-dir` returned `OOPFORGE_NOT_LOADED`, and
`/oopforge:craft` did not expand as a headless Cursor command.

Result: the explicit local-plugin command and the project-local skill link are
verified. Marketplace publication and bootstrap integration remain future
work.
