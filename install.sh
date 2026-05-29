#!/usr/bin/env bash
#
# OOPforge installer
#   Symlinks OOPforge into detected Claude Code / Codex CLI config directories.
#
# Environment overrides:
#   INSTALL_CLAUDE=1 INSTALL_CODEX=1 ./install.sh
#
# OpenCode is opt-in:
#   INSTALL_OPENCODE=1 ./install.sh
#
# Usage:
#   ./install.sh              Install (skip existing links)
#   ./install.sh update       Remove OOPforge links, then reinstall
#   ./install.sh --force      Replace existing symlinks only
#   ./install.sh --dry-run    Print actions without linking
#
set -euo pipefail

PACK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRY_RUN=0
FORCE=0
MODE="install"

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }

usage() {
  cat <<EOF
Usage: ./install.sh [update] [--force] [--dry-run]

  (default)   Install symlinks; skip paths that already exist
  update      Run uninstall.sh, then install fresh links
  --force     Replace existing symlinks (non-symlink paths are skipped with a warning)
  --dry-run   Show planned actions without changing the filesystem
EOF
}

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --dry-run) DRY_RUN=1 ;;
      --force)   FORCE=1 ;;
      update)    MODE="update" ;;
      -h|--help) usage; exit 0 ;;
      *)
        red "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
    shift
  done
}

link() {
  local src="$1"
  local dst="$2"
  local dst_parent

  if [ ! -d "$src" ]; then
    yellow "Skip (source missing): $src"
    return
  fi

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ "$FORCE" -eq 1 ]; then
      if [ -L "$dst" ]; then
        if [ "$DRY_RUN" -eq 1 ]; then
          cyan "[dry-run] remove symlink $dst"
        else
          rm "$dst"
        fi
      else
        yellow "Skip (not a symlink): $dst"
        return
      fi
    else
      yellow "Already exists (run './install.sh update' or use --force'): $dst"
      return
    fi
  fi

  dst_parent="$(dirname "$dst")"

  if [ "$DRY_RUN" -eq 1 ]; then
    if [ ! -d "$dst_parent" ]; then
      cyan "[dry-run] mkdir -p $dst_parent"
    fi
    cyan "[dry-run] link $dst -> $src"
  else
    mkdir -p "$dst_parent"
    ln -s "$src" "$dst"
    green "Linked: $dst -> $src"
  fi
}

do_install() {
  if [ -d "$HOME/.claude" ] || [ -n "${INSTALL_CLAUDE:-}" ]; then
    cyan "--- Claude Code detected"
    link "$PACK_DIR/skills"   "$HOME/.claude/skills/oopforge"
    link "$PACK_DIR/agents"   "$HOME/.claude/agents/oopforge"
    link "$PACK_DIR/commands" "$HOME/.claude/commands/oopforge"
  fi

  if [ -d "$HOME/.codex" ] || [ -n "${INSTALL_CODEX:-}" ]; then
    cyan "--- Codex CLI detected"
    link "$PACK_DIR/skills" "$HOME/.codex/skills/oopforge"
  fi

  if [ -n "${INSTALL_OPENCODE:-}" ]; then
    cyan "--- OpenCode opt-in"
    link "$PACK_DIR/skills" "$HOME/.config/opencode/skills/oopforge"
  fi
}

parse_args "$@"

if [ "$MODE" = "update" ]; then
  cyan "==> OOPforge update ($([ "$DRY_RUN" -eq 1 ] && echo dry-run || echo live))"
  if [ "$DRY_RUN" -eq 1 ]; then
    cyan "[dry-run] would run uninstall.sh"
  else
    "$PACK_DIR/uninstall.sh"
  fi
else
  cyan "==> OOPforge install ($([ "$DRY_RUN" -eq 1 ] && echo dry-run || echo live))"
fi

do_install

green "==> Done. Restart each agent to pick up changes."

if [ "$DRY_RUN" -eq 1 ]; then
  yellow "Run again without --dry-run to apply changes."
fi
