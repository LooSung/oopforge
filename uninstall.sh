#!/usr/bin/env bash
#
# OOPforge uninstaller
#   설치된 심볼릭 링크만 제거한다 (원본 폴더는 건드리지 않음).
#
set -euo pipefail

yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }

rm_link() {
  if [ -L "$1" ]; then
    rm "$1"
    green "제거: $1"
  else
    [ -e "$1" ] && yellow "심링크 아님 (수동 확인): $1"
  fi
}

rm_link "$HOME/.claude/skills/oopforge"
rm_link "$HOME/.claude/agents/oopforge"
rm_link "$HOME/.claude/commands/oopforge"
rm_link "$HOME/.codex/skills/oopforge"
rm_link "$HOME/.config/opencode/skills/oopforge"

green "==> 제거 완료."
