#!/usr/bin/env bash
#
# OOPforge uninstaller
#   Removes installed symlinks only (does not delete the source pack).
#
set -euo pipefail

green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }

rm_link() {
  if [ -L "$1" ]; then
    rm "$1"
    green "Removed: $1"
    return
  fi

  if [ -e "$1" ]; then
    yellow "Not a symlink (manual check needed): $1"
  fi
}

rm_link "$HOME/.claude/skills/oopforge"
rm_link "$HOME/.claude/agents/oopforge"
rm_link "$HOME/.claude/commands/oopforge"
rm_link "$HOME/.codex/skills/oopforge"
rm_link "$HOME/.config/opencode/skills/oopforge"

green "==> Uninstall complete."
