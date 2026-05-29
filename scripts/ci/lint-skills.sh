#!/usr/bin/env bash
#
# OOPforge repository lint
# Validates skill frontmatter, line limits, plugin JSON, and AGENTS.md references.

set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FAILED=0
SKILL_LINE_LIMIT="${SKILL_LINE_LIMIT:-200}"

cyan() { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
red() { printf "\033[31m%s\033[0m\n" "$*"; }

fail() { red "FAIL $*"; FAILED=1; }
ok() { green "OK $*"; }

check_skill_file() {
  local file="$1"
  local rel="${file#"$PACK_DIR"/}"
  local lines
  local name_line
  local desc_line

  if [ ! -f "$file" ]; then
    fail "missing skill file: $rel"
    return
  fi

  if ! head -n 1 "$file" | grep -q '^---$'; then
    fail "$rel: frontmatter must start with ---"
    return
  fi

  if ! awk 'NR > 1 && /^---$/ { found=1 } END { exit found ? 0 : 1 }' "$file"; then
    fail "$rel: frontmatter closing --- missing"
    return
  fi

  name_line="$(awk 'NR > 1 && /^---$/ { exit } /^name: / { print; exit }' "$file")"
  desc_line="$(awk 'NR > 1 && /^---$/ { exit } /^description: / { print; exit }' "$file")"

  if [ -z "$name_line" ]; then
    fail "$rel: frontmatter missing name:"
  fi

  if [ -z "$desc_line" ]; then
    fail "$rel: frontmatter missing description:"
  fi

  lines="$(wc -l < "$file" | tr -d ' ')"
  if [ "$lines" -gt "$SKILL_LINE_LIMIT" ]; then
    fail "$rel: $lines lines (limit: $SKILL_LINE_LIMIT)"
  else
    ok "$rel ($lines lines)"
  fi
}

check_json_file() {
  local file="$1"
  local rel="${file#"$PACK_DIR"/}"

  if ! python3 -m json.tool "$file" >/dev/null 2>&1; then
    fail "invalid JSON: $rel"
  else
    ok "$rel"
  fi
}

check_agents_skill_refs() {
  local agents_file="$PACK_DIR/AGENTS.md"
  local path

  if [ ! -f "$agents_file" ]; then
    fail "missing AGENTS.md"
    return
  fi

  while IFS= read -r path; do
    if [ ! -f "$PACK_DIR/$path" ]; then
      fail "AGENTS.md references missing file: $path"
    else
      ok "AGENTS.md reference: $path"
    fi
  done < <(grep -oE 'skills/[^`[:space:]]+\.md' "$agents_file" | sort -u || true)
}

cyan "==> OOPforge lint"

cyan "--- Skill files"
while IFS= read -r -d '' file; do
  check_skill_file "$file"
done < <(find "$PACK_DIR/skills" -name '*.md' -print0)

cyan "--- Plugin manifests"
check_json_file "$PACK_DIR/.claude-plugin/plugin.json"
check_json_file "$PACK_DIR/.codex-plugin/plugin.json"
check_json_file "$PACK_DIR/.cursor-plugin/plugin.json"

cyan "--- AGENTS.md skill references"
check_agents_skill_refs

if [ "$FAILED" -eq 0 ]; then
  green "==> lint complete: no issues"
else
  red "==> lint failed: review FAIL items above"
  exit 1
fi
