#!/usr/bin/env bash
#
# OOPforge doctor
#   Validate local pack structure and installed symlinks.
#
set -euo pipefail

PACK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FAILED=0

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }

ok() {
  green "OK   $*"
}

warn() {
  yellow "WARN $*"
}

fail() {
  red "FAIL $*"
  FAILED=1
}

check_file() {
  local path="$1"
  if [ -f "$PACK_DIR/$path" ]; then
    ok "$path"
  else
    fail "$path 없음"
  fi
}

check_dir() {
  local path="$1"
  if [ -d "$PACK_DIR/$path" ]; then
    ok "$path/"
  else
    fail "$path/ 없음"
  fi
}

check_link() {
  local label="$1"
  local dst="$2"
  local expected="$3"

  if [ ! -e "$(dirname "$dst")" ]; then
    warn "$label 설정 디렉토리 없음: $(dirname "$dst")"
    return
  fi

  if [ ! -L "$dst" ]; then
    warn "$label 링크 없음: $dst"
    return
  fi

  local actual
  actual="$(readlink "$dst")"
  if [ "$actual" = "$expected" ]; then
    ok "$label 링크: $dst -> $actual"
  else
    fail "$label 링크 대상 불일치: $dst -> $actual (expected: $expected)"
  fi
}

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    ok "$command_name 감지: $(command -v "$command_name")"
  else
    warn "$command_name 미감지"
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
check_file "install.sh"
check_file "uninstall.sh"
check_file "bootstrap.sh"
check_file ".claude-plugin/plugin.json"
check_file ".codex-plugin/plugin.json"
check_file ".cursor-plugin/plugin.json"
check_file ".opencode/README.md"

cyan "--- Harness commands"
check_command "claude"
check_command "codex"
check_command "cursor"

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
  warn "OpenCode 검사는 기본 제외됨 (필요 시 CHECK_OPENCODE=1 ./doctor.sh)"
fi

if [ "$FAILED" -eq 0 ]; then
  green "==> doctor 완료: 치명적 문제 없음"
else
  red "==> doctor 실패: FAIL 항목을 확인하세요"
  exit 1
fi
