#!/usr/bin/env bash
#
# OOPforge doctor
# Validates local pack structure and installed symlinks.

set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/setup/lib/common.sh
source "$SETUP_DIR/lib/common.sh"

PACK_DIR="$(oopforge_pack_dir "$SETUP_DIR")"
FAILED=0

ok() { green "OK $*"; }
warn() { yellow "WARN $*"; }
fail() { red "FAIL $*"; FAILED=1; }

check_file() {
  local path="$1"
  if [ -f "$PACK_DIR/$path" ]; then
    ok "$path"
  else
    fail "missing file: $path"
  fi
}

check_dir() {
  local path="$1"
  if [ -d "$PACK_DIR/$path" ]; then
    ok "$path/"
  else
    fail "missing directory: $path/"
  fi
}

check_link() {
  local label="$1"
  local dst="$2"
  local expected="$3"

  if [ ! -e "$(dirname "$dst")" ]; then
    warn "$label config directory missing: $(dirname "$dst")"
    return
  fi

  if [ ! -L "$dst" ]; then
    warn "$label link missing: $dst"
    return
  fi

  local actual
  actual="$(readlink "$dst")"

  if [ "$actual" = "$expected" ]; then
    ok "$label link: $dst -> $actual"
  else
    fail "$label link target mismatch: $dst -> $actual (expected: $expected)"
  fi
}

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    ok "$command_name found: $(command -v "$command_name")"
  else
    warn "$command_name not found"
  fi
}

cyan "==> OOPforge doctor"

cyan "--- Pack structure"
check_dir "skills"
check_dir "skills/workflow"
check_dir "skills/oop"
check_dir "skills/lang/java"
check_dir "skills/lang/python"
check_dir "agents"
check_dir "commands"
check_dir ".claude-plugin"
check_dir ".codex-plugin"
check_dir ".cursor-plugin"
check_dir ".opencode"
check_dir "scripts/setup"
check_dir "scripts/ci"
check_file "scripts/setup/bootstrap.sh"
check_file "scripts/setup/install.sh"
check_file "scripts/setup/uninstall.sh"
check_file "scripts/setup/doctor.sh"
check_file "scripts/setup/lib/common.sh"
check_file "scripts/ci/lint-skills.sh"
check_file "scripts/ci/smoke-test.sh"
check_file "skills/SKILL.md"
check_file ".claude-plugin/plugin.json"
check_file ".codex-plugin/plugin.json"
check_file ".cursor-plugin/plugin.json"
check_file ".opencode/README.md"

cyan "--- Harness commands"
check_command "claude"
check_command "codex"
check_command "cursor-agent"

cyan "--- Cursor Agent CLI"
if command -v cursor-agent >/dev/null 2>&1; then
  ok "load command: cursor-agent --plugin-dir $PACK_DIR"
else
  warn "cursor-agent not found (install Cursor CLI to use OOPforge with Cursor)"
fi
warn "No scripts/setup/install.sh symlink target; marketplace packaging is Phase 2."

cyan "--- Installed links"
check_link "Claude skills" "$HOME/.claude/skills/oopforge" "$PACK_DIR/skills"
check_link "Claude agents" "$HOME/.claude/agents/oopforge" "$PACK_DIR/agents"
check_link "Claude commands" "$HOME/.claude/commands/oopforge" "$PACK_DIR/commands"
check_link "Codex skills" "$HOME/.codex/skills/oopforge" "$PACK_DIR/skills"

if [ -n "${CHECK_OPENCODE:-}" ]; then
  cyan "--- OpenCode opt-in"
  check_command "opencode"
  check_link "OpenCode skills" "$HOME/.config/opencode/skills/oopforge" "$PACK_DIR/skills"
else
  warn "OpenCode checks skipped by default (use CHECK_OPENCODE=1 ./scripts/setup/doctor.sh)."
fi

if [ "$FAILED" -eq 0 ]; then
  green "==> doctor complete: no critical issues"
else
  red "==> doctor failed: review FAIL items above"
  exit 1
fi
