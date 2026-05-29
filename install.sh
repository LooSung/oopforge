#!/usr/bin/env bash
#
# OOPforge installer
#   감지된 Claude Code / Codex CLI 설정 디렉토리에 OOPforge를 심볼릭 링크한다.
#
# 환경변수로 강제 설치도 가능:
#   INSTALL_CLAUDE=1 INSTALL_CODEX=1 ./install.sh
#
# OpenCode는 opt-in:
#   INSTALL_OPENCODE=1 ./install.sh
#
# 옵션:
#   --dry-run    실제로 링크하지 않고 무엇을 할지만 출력
#
set -euo pipefail

PACK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }

link() {
  local src="$1"
  local dst="$2"
  local dst_parent

  if [ ! -d "$src" ]; then
    yellow "건너뜀 (소스 없음): $src"
    return
  fi

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    yellow "이미 존재 (수동 정리 필요): $dst"
    return
  fi

  dst_parent="$(dirname "$dst")"

  if [ "$DRY_RUN" -eq 1 ]; then
    if [ ! -d "$dst_parent" ]; then
      cyan "[dry-run] mkdir -p $dst_parent"
    fi
    cyan "[dry-run] link $dst → $src"
  else
    mkdir -p "$dst_parent"
    ln -s "$src" "$dst"
    green "링크: $dst → $src"
  fi
}

cyan "==> OOPforge 설치 시작 ($([ "$DRY_RUN" -eq 1 ] && echo dry-run || echo live))"

# ---- Claude Code ----
if [ -d "$HOME/.claude" ] || [ -n "${INSTALL_CLAUDE:-}" ]; then
  cyan "--- Claude Code 감지"
  link "$PACK_DIR/skills"   "$HOME/.claude/skills/oopforge"
  link "$PACK_DIR/agents"   "$HOME/.claude/agents/oopforge"
  link "$PACK_DIR/commands" "$HOME/.claude/commands/oopforge"
fi

# ---- Codex CLI ----
if [ -d "$HOME/.codex" ] || [ -n "${INSTALL_CODEX:-}" ]; then
  cyan "--- Codex CLI 감지"
  link "$PACK_DIR/skills" "$HOME/.codex/skills/oopforge"
fi

# ---- OpenCode (opt-in) ----
if [ -n "${INSTALL_OPENCODE:-}" ]; then
  cyan "--- OpenCode opt-in"
  link "$PACK_DIR/skills" "$HOME/.config/opencode/skills/oopforge"
fi

green "==> 완료. 각 에이전트 재시작하면 적용됨."

if [ "$DRY_RUN" -eq 1 ]; then
  yellow "실제 설치하려면 --dry-run 없이 다시 실행하세요."
fi
