# OpenCode Setup (Experimental)

OpenCode integration is **opt-in** and not part of the default install path.

## Install skills only

```bash
INSTALL_OPENCODE=1 ~/.oopforge/install.sh
```

Or from a clone:

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
INSTALL_OPENCODE=1 ~/.oopforge/install.sh
```

Target: `~/.config/opencode/skills/oopforge`

## Verify

```bash
CHECK_OPENCODE=1 ~/.oopforge/doctor.sh
```

## Usage

Skills appear in OpenCode context. Ask in natural language:

```text
Follow OOPforge Discovery for an inventory domain. No code yet.
```

There are no dedicated OpenCode slash commands in this pack today. Use workflow skill names (`discovery`, `design`, `skeleton`, `implement`, `test`) explicitly in prompts.

## Stability

OpenCode is experimental. Do not document it as a first-class harness until `install.sh`, `doctor.sh`, and a clean-session smoke test pass consistently.

## Related

- [Claude Code setup](./claude-code.md)
- [Cursor setup](./cursor.md)
