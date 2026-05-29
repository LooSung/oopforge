#!/usr/bin/env bash
#
# OOPforge bootstrap installer
#   Clone or update ~/.oopforge, then run install.sh update.
#
set -euo pipefail

REPO_URL="${OOPFORGE_REPO_URL:-https://github.com/LooSung/oopforge.git}"
INSTALL_DIR="${OOPFORGE_HOME:-$HOME/.oopforge}"
BRANCH="${OOPFORGE_BRANCH:-main}"

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    red "Required command not found: $1"
    exit 1
  fi
}

clone_or_update() {
  if [ -d "$INSTALL_DIR/.git" ]; then
    cyan "==> Updating existing OOPforge at $INSTALL_DIR"
    git -C "$INSTALL_DIR" fetch --quiet origin "$BRANCH"
    git -C "$INSTALL_DIR" checkout --quiet "$BRANCH"
    git -C "$INSTALL_DIR" pull --ff-only --quiet origin "$BRANCH"
    return
  fi

  if [ -e "$INSTALL_DIR" ]; then
    red "Install path exists but is not a git repository: $INSTALL_DIR"
    yellow "Use a different path: OOPFORGE_HOME=/path/to/oopforge ./bootstrap.sh"
    exit 1
  fi

  cyan "==> Cloning OOPforge to $INSTALL_DIR"
  git clone --quiet --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
}

require git

clone_or_update
chmod +x "$INSTALL_DIR/install.sh" "$INSTALL_DIR/uninstall.sh"

cyan "==> Running install.sh update"
"$INSTALL_DIR/install.sh" update

if [ -f "$INSTALL_DIR/doctor.sh" ]; then
  cyan "==> Running doctor.sh"
  chmod +x "$INSTALL_DIR/doctor.sh"
  "$INSTALL_DIR/doctor.sh"
fi

green "==> OOPforge bootstrap complete"
