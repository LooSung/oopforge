# Install, update, and remove OOPforge

## Latest `main`

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

The bootstrap clones or updates `~/.oopforge` and installs detected Claude Code
and Codex links. It does not configure Cursor; follow the
[Cursor setup](cursor.md).

## Claude Code plugin marketplace (experimental)

```text
/plugin marketplace add LooSung/oopforge
/plugin install oopforge@forge
```

Read permission, update, and removal:
[Claude Code setup](claude-code.md#plugin-marketplace-experimental).

## A pinned release

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
git checkout v1.12.0
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

## Install targets

| Harness | Installed or registered path |
|---|---|
| **Claude Code** | `~/.claude/skills/oopforge` and `~/.claude/commands/oopforge` |
| **Codex CLI** | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Manual local plugin or project-local skill; `install.sh` does not configure it |

`install.sh` only creates Claude and Codex links when their config directories
exist. Set `INSTALL_CLAUDE=1` or `INSTALL_CODEX=1` to create a missing target
explicitly.

## Update

A GitHub Release does not update an existing clone. Pull the pack, refresh
Claude/Codex link targets, and restart the agent:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

That command is for a `main`-tracking clone. A release-pinned clone must
`git fetch --tags`, check out the chosen newer tag, and then run
`./scripts/setup/install.sh update`.

Cursor's manually registered symlink is not managed by `install.sh`; after the
pull, restart `cursor-agent`.

## Verify and troubleshoot

Run these commands from `~/.oopforge`:

```bash
./scripts/setup/doctor.sh              # pack structure and installed links
./scripts/setup/install.sh --dry-run   # planned link changes
./scripts/setup/install.sh --force     # replace conflicting symlinks
./scripts/ci/smoke-test.sh             # isolated Claude/Codex install lifecycle
```

`doctor.sh` validates the pack and available symlinks. A successful result does
not prove that a running agent loaded Craft. If it warns that your chosen Claude
or Codex link is missing, run `INSTALL_CLAUDE=1 ~/.oopforge/scripts/setup/install.sh`
or the Codex equivalent. Verify activation with the entry point documented in
the relevant harness guide: [Claude Code](claude-code.md) · [Codex](codex.md) ·
[Cursor](cursor.md).

## Remove

```bash
./scripts/setup/uninstall.sh
```

This removes only OOPforge-managed Claude and Codex links. It keeps
`~/.oopforge` and any project-local `.cursor/skills/oopforge` link; remove those
manually if you want a complete uninstall.
