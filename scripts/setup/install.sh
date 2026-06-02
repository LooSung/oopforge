#!/usr/bin/env bash
#
# OOPforge installer
# Symlinks OOPforge into detected Claude Code / Codex CLI config directories.
#
# Environment overrides:
#   INSTALL_CLAUDE=1 INSTALL_CODEX=1 ./scripts/setup/install.sh
#
# Usage:
#   ./scripts/setup/install.sh             Install (skip existing links)
#   ./scripts/setup/install.sh update      Remove OOPforge links, then reinstall
#   ./scripts/setup/install.sh --force     Replace existing symlinks only
#   ./scripts/setup/install.sh --dry-run   Print actions without linking

set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/setup/lib/common.sh
source "$SETUP_DIR/lib/common.sh"

PACK_DIR="$(oopforge_pack_dir "$SETUP_DIR")"
DRY_RUN=0
FORCE=0
MODE="install"

usage() {
  cat <<USAGE
OOPforge installer

Usage:
  ./scripts/setup/install.sh [update] [--force] [--dry-run]

Environment:
  INSTALL_CLAUDE=1    Install Claude Code links even if ~/.claude is missing
  INSTALL_CODEX=1     Install Codex links even if ~/.codex is missing
USAGE
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      update)
        MODE="update"
        ;;
      --force|-f)
        FORCE=1
        ;;
      --dry-run|-n)
        DRY_RUN=1
        ;;
      --help|-h)
        usage
        exit 0
        ;;
      *)
        red "Unknown argument: $1"
        usage
        exit 1
        ;;
    esac
    shift
  done
}

link_path() {
  local src="$1"
  local dst="$2"
  local dst_parent
  dst_parent="$(dirname "$dst")"

  if [ ! -e "$src" ]; then
    red "Source does not exist: $src"
    exit 1
  fi

  if [ -L "$dst" ]; then
    local current
    current="$(readlink "$dst")"
    if [ "$current" = "$src" ]; then
      green "Already linked: $dst -> $src"
      return
    fi

    if [ "$FORCE" -eq 1 ]; then
      if [ "$DRY_RUN" -eq 1 ]; then
        yellow "[dry-run] would replace symlink: $dst -> $src"
      else
        rm "$dst"
        mkdir -p "$dst_parent"
        ln -s "$src" "$dst"
        green "Re-linked: $dst -> $src"
      fi
      return
    fi

    yellow "Different symlink exists: $dst -> $current (use --force to replace)"
    return
  fi

  if [ -e "$dst" ]; then
    yellow "Path exists and is not a symlink: $dst (skipped)"
    return
  fi

  if [ "$DRY_RUN" -eq 1 ]; then
    yellow "[dry-run] would link: $dst -> $src"
  else
    mkdir -p "$dst_parent"
    ln -s "$src" "$dst"
    green "Linked: $dst -> $src"
  fi
}

do_install() {
  if [ -d "$HOME/.claude" ] || [ -n "${INSTALL_CLAUDE:-}" ]; then
    cyan "--- Claude Code detected"
    link_path "$PACK_DIR/skills" "$HOME/.claude/skills/oopforge"
    link_path "$PACK_DIR/commands" "$HOME/.claude/commands/oopforge"
  fi

  if [ -d "$HOME/.codex" ] || [ -n "${INSTALL_CODEX:-}" ]; then
    cyan "--- Codex CLI detected"
    link_path "$PACK_DIR/skills" "$HOME/.codex/skills/oopforge"
  fi

}

parse_args "$@"

if [ "$MODE" = "update" ]; then
  cyan "==> OOPforge update ($([ "$DRY_RUN" -eq 1 ] && echo dry-run || echo live))"
  if [ "$DRY_RUN" -eq 1 ]; then
    cyan "[dry-run] would run scripts/setup/uninstall.sh"
  else
    "$SETUP_DIR/uninstall.sh"
  fi
else
  cyan "==> OOPforge install ($([ "$DRY_RUN" -eq 1 ] && echo dry-run || echo live))"
fi

do_install

green "==> Done."
yellow "Restart each agent to pick up changes."

if [ "$DRY_RUN" -eq 1 ]; then
  yellow "Run again without --dry-run to apply changes."
fi
