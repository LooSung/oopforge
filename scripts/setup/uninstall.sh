#!/usr/bin/env bash
#
# OOPforge uninstaller
# Removes installed symlinks only. It never deletes the source pack.

set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/setup/lib/common.sh
source "$SETUP_DIR/lib/common.sh"

rm_link() {
  local path="$1"

  if [ -L "$path" ]; then
    rm "$path"
    green "Removed: $path"
    return
  fi

  if [ -e "$path" ]; then
    yellow "Not a symlink; leaving untouched: $path"
  fi
}

rm_link "$HOME/.claude/skills/oopforge"
rm_link "$HOME/.claude/agents/oopforge"
rm_link "$HOME/.claude/commands/oopforge"
rm_link "$HOME/.codex/skills/oopforge"
rm_link "$HOME/.config/opencode/skills/oopforge"

green "==> Uninstall complete."
