#!/usr/bin/env bash
#
# OOPforge smoke test — install and doctor in an isolated HOME.
#
set -euo pipefail

PACK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
TMP_HOME="$(mktemp -d)"
trap 'rm -rf "$TMP_HOME"' EXIT

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }

cyan "==> OOPforge smoke test (HOME=$TMP_HOME)"

export HOME="$TMP_HOME"
mkdir -p "$HOME/.claude" "$HOME/.codex"

"$PACK_DIR/install.sh"
"$PACK_DIR/doctor.sh"

test -L "$HOME/.claude/skills/oopforge"
test -L "$HOME/.claude/agents/oopforge"
test -L "$HOME/.claude/commands/oopforge"

actual_skills="$(readlink "$HOME/.claude/skills/oopforge")"
if [ "$actual_skills" != "$PACK_DIR/skills" ]; then
  printf "FAIL skills link: %s (expected %s)\n" "$actual_skills" "$PACK_DIR/skills" >&2
  exit 1
fi

cyan "==> install.sh update"
"$PACK_DIR/install.sh" update
test -L "$HOME/.claude/skills/oopforge"

cyan "==> uninstall"
"$PACK_DIR/uninstall.sh"
test ! -e "$HOME/.claude/skills/oopforge"

green "==> Smoke test passed"
