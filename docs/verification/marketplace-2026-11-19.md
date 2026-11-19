# Claude Code plugin marketplace — 2026-11-19

- Harness: Claude Code 2.1.311 on macOS.
- Candidates: uncommitted working trees on Compforge `d48d718`, OOPforge
  `e8e0748`, and FuseForge `9b7183c`. Entries fetched from GitHub used `main` at
  those commits; a plugin entry needs only `.claude-plugin/plugin.json`.
- Catalog: `forge`, in `.claude-plugin/marketplace.json` of each repository. Each
  catalog lists its own repository as `./` and the other two by HTTPS git URL,
  so adding any one repository offers all three plugins.

## Results

| Check | Result |
|---|---|
| `claude plugin validate` on each repository | Pass with warnings: no icon, root `CLAUDE.md` is not plugin context, untracked `.DS_Store` in local folders |
| `plugin marketplace add <compforge path>`, then `plugin install` of all three, isolated `CLAUDE_CONFIG_DIR` | Pass |
| One-step `plugin install <name> --marketplace <path>` from the OOPforge and FuseForge catalogs, fresh config each | Pass, three of three each |
| `plugin details` inventory | Compforge 8 skills, OOPforge 8, FuseForge 3 |
| `plugin update` | Pass with HTTPS `url` sources. With `github` sources, update cloned over SSH and failed without a key, so the catalogs use HTTPS URLs |
| `plugin uninstall`, `marketplace update`, `marketplace remove` | Pass |
| Live: a run-specific command added to each installed copy printed `${CLAUDE_PLUGIN_ROOT}` | Pass, three of three; each printed its installed cache path |
| Live: `/compforge:craft`, `/oopforge:craft`, `/fuseforge:craft` activation probes with the three installed copies loaded | Pass, three of three |
| Real install at local scope in a scratch project: catalog from the OOPforge path, Compforge and FuseForge cloned from GitHub into `~/.claude/plugins/cache/forge` | Pass |
| A command reading its own plugin file from that cache, default permissions, non-interactive | **Refused**: the cache is outside the working directory, so a read needs approval |
| The same read with `Read(~/.claude/plugins/cache/forge/**)` allowed, as `--allowedTools` and as a `--settings` file | Pass, both forms |
| A git-hosted catalog (a committed snapshot served over local smart HTTP): the `./` entry installs under `cache/forge/compforge/<version>` | Pass; the read rule above covers the `./` entry too |
| Adding a second `forge` catalog from another repository in the same config | **Refused** (the name is taken); installing `oopforge@forge` from the first catalog worked |
| `/compforge:consult` with both the symlink install and the plugin present | The user-level symlink command ran, not the plugin's |
| FuseForge `doctor.sh --specialists` with plugin-only specialists | Reports the specialists missing: doctor and bootstrap check script installs only |
| Invoking the plugin skill with the Skill tool, then reading a supporting file | **Refused**: invoking a skill does not grant reads of its directory |

After the local-scope test, the plugins and catalog were removed and the
test-created cache directory deleted; `~/.claude/settings.json`,
`known_marketplaces.json`, and `installed_plugins.json` matched their backups
byte for byte.

## Read permission

A marketplace plugin lives in `~/.claude/plugins/cache/`, outside the user's
project, so every read of its supporting files asks for approval. Compforge and
OOPforge slash commands inline their main workflow and start without a read;
supporting skills, `{pack}` documents, and FuseForge's Craft and Consult
workflow do need one. Approve the prompt when it appears, or add
`Read(~/.claude/plugins/cache/forge/**)` to `permissions.allow`. Non-interactive
runs (`-p`) need the rule. On this machine, `-p` reads through the symlink
install were refused the same way, so the prompt is not new to the plugin path.

## Limits

- An isolated config directory has no login, so the live probes loaded the
  installed cache copies with `--plugin-dir` under the maintainer's config. That
  machine also has symlink installs. The run-specific commands prove the
  installed copies loaded; the `craft` activation probes alone could also be
  answered by a symlinked command. `--safe-mode` disables session plugins, so a
  clean negative control was not possible.
- `/plugin marketplace add LooSung/<repository>` was not run against GitHub,
  because the catalogs are not pushed yet. Run it once after the push.
- A full `/compforge:consult` from a plugin-only install was not isolated: the
  symlink commands on this machine shadow the plugin's. Natural-language use
  without a slash command, in a plugin-only install, was not exercised either. `skills/SKILL.md` in Compforge and OOPforge now names the
  plugin root as the pack root in that case.
- A full FuseForge coordinator run from a plugin-only install was not
  exercised.
- Codex CLI and Cursor Agent paths are unchanged by this record.
