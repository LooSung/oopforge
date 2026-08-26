#!/usr/bin/env bash
#
# Static packaging checks and authenticated harness activation probes.
set -euo pipefail
PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEMP_DIRS=()
ACTIVATION_TOKEN="OOPFORGE_ACTIVATION_PROBE"
TEST_ROUTING_PROBE="OOPFORGE_TEST_ROUTING_PROBE"
NEGATIVE_PROBE="$ACTIVATION_TOKEN. If no loaded OOPforge instruction defines \
this probe, output exactly OOPFORGE_NOT_LOADED."
green() { printf "\033[32m%s\033[0m\n" "$*"; }
red() { printf "\033[31m%s\033[0m\n" "$*" >&2; }
probe_step() { printf "RUN %s\n" "$*" >&2; }
cleanup() {
  local path
  set +u
  for path in "${TEMP_DIRS[@]}"; do
    rm -rf "$path"
  done
  set -u
}
trap cleanup EXIT
require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    red "FAIL missing command: $1"
    exit 1
  }
}
require_link_target() {
  local link="$1"
  local expected="$2"
  if [ ! -L "$link" ] || [ "$(readlink "$link")" != "$expected" ]; then
    red "FAIL expected link: $link -> $expected"
    exit 1
  fi
}
run_timed() {
  python3 "$PACK_DIR/scripts/ci/run-with-timeout.py" \
    "${OOPFORGE_HARNESS_TIMEOUT:-1200}" "$@"
}
probe_failure() {
  local message="$1"
  local output="$2"
  red "FAIL $message"
  printf '%s\n' "--- probe output ---" >&2
  sed -n '1,80p' "$output" >&2
  return 1
}
assert_positive() {
  local output="$1"
  grep -Fxq "OOPFORGE_LOADED" "$output" ||
    { probe_failure "positive probe did not load OOPforge" "$output"; return 1; }
  grep -Eq "^Assumptions:?$" "$output" ||
    { probe_failure "positive probe missed Assumptions" "$output"; return 1; }
  grep -Eq "^OOP Contract:?$" "$output" ||
    { probe_failure "positive probe missed OOP Contract" "$output"; return 1; }
  if grep -Eq '^OOPFORGE_NOT_LOADED[.!]?$' "$output"; then
    probe_failure "positive probe also reported not loaded" "$output"
    return 1
  fi
  green "PASS positive activation probe"
}
assert_negative() {
  local output="$1"
  grep -Eq '^OOPFORGE_NOT_LOADED[.!]?$' "$output" ||
    { probe_failure "negative control did not report isolation" "$output"; return 1; }
  if grep -Eq '^OOPFORGE_LOADED[.!]?$' "$output"; then
    probe_failure "negative control loaded OOPforge" "$output"
    return 1
  fi
  green "PASS negative activation control"
}
assert_test_route() {
  local output="$1"
  local source="${2:-}"
  grep -Fxq "OOPFORGE_TEST_ROUTED" "$output" ||
    { probe_failure "Test probe missed route token" "$output"; return 1; }
  grep -Fxq "Level: auto" "$output" ||
    { probe_failure "Test probe missed auto level" "$output"; return 1; }
  grep -Fxq "Production code: forbidden" "$output" ||
    { probe_failure "Test probe missed production boundary" "$output"; return 1; }
  [ -z "$source" ] || grep -Fxq "Source: $source" "$output" ||
    { probe_failure "Test probe loaded another source" "$output"; return 1; }
  green "PASS Test command routing"
}
static_smoke() {
  python3 "$PACK_DIR/scripts/ci/check-harness-packaging.py" "$PACK_DIR"
}
prepare_claude_probe() {
  local plugin_dir="$1"
  mkdir -p "$plugin_dir/.claude-plugin"
  cp "$PACK_DIR/.claude-plugin/plugin.json" "$plugin_dir/.claude-plugin/plugin.json"
  cp -R "$PACK_DIR/commands" "$plugin_dir/commands"
  cp -R "$PACK_DIR/skills" "$plugin_dir/skills"
  python3 - "$plugin_dir/commands/test.md" "$plugin_dir/skills" <<'PY'
import pathlib
import sys
path = pathlib.Path(sys.argv[1])
path.write_text(path.read_text().replace("~/.claude/skills/oopforge", sys.argv[2]))
PY
}
link_codex_auth() {
  local target_home="$1"
  local source_home="${CODEX_HOME:-$HOME/.codex}"
  mkdir -p "$target_home"
  if [ -f "$source_home/auth.json" ]; then
    ln -s "$source_home/auth.json" "$target_home/auth.json"
  elif [ -z "${CODEX_API_KEY:-}" ]; then
    red "FAIL Codex requires CODEX_API_KEY or $source_home/auth.json"
    exit 1
  fi
}
live_claude() {
  require_command claude
  claude --version >&2
  local run_dir candidate positive negative load_mode
  run_dir="$(mktemp -d)"
  TEMP_DIRS+=("$run_dir")
  load_mode="candidate"
  if [ "${OOPFORGE_INSTALLED_SMOKE:-0}" = "1" ]; then
    require_link_target "$HOME/.claude/skills/oopforge" "$PACK_DIR/skills"
    require_link_target "$HOME/.claude/commands/oopforge" "$PACK_DIR/commands"
    load_mode="installed"
  else
    candidate="$run_dir/candidate"
    prepare_claude_probe "$candidate"
  fi
  positive="$run_dir/positive.txt"
  negative="$run_dir/negative.txt"
  (
    cd "$run_dir"
    printf 'def test_example():\n    assert True\n' >test_example.py
    probe_step "Claude Test command positive"
    if [ "$load_mode" = "installed" ]; then
      run_timed claude -p --no-session-persistence --permission-mode bypassPermissions \
        --tools "Read" --add-dir "$PACK_DIR" >"$positive" \
        <<<"/oopforge:test Before running test_example.py, $TEST_ROUTING_PROBE"
    else
      run_timed claude -p --no-session-persistence --permission-mode bypassPermissions \
        --tools "Read" --add-dir "$candidate" --plugin-dir "$candidate" >"$positive" \
        <<<"/oopforge:test Before running test_example.py, $TEST_ROUTING_PROBE"
    fi
    probe_step "Claude safe-mode negative"
    run_timed claude --safe-mode -p --no-session-persistence \
      --permission-mode plan --tools "" >"$negative" <<<"$NEGATIVE_PROBE"
  )
  assert_test_route "$positive"
  assert_negative "$negative"
}

live_codex() {
  require_command codex
  codex --version >&2
  local run_dir workspace positive_home negative_home positive negative
  run_dir="$(mktemp -d)"
  TEMP_DIRS+=("$run_dir")
  workspace="$run_dir/workspace"
  positive_home="$run_dir/codex-positive"
  negative_home="$run_dir/codex-negative"
  positive="$run_dir/positive.txt"
  negative="$run_dir/negative.txt"
  mkdir -p "$workspace" "$positive_home/skills"
  printf 'def test_example():\n    assert True\n' >"$workspace/test_example.py"
  link_codex_auth "$positive_home"
  link_codex_auth "$negative_home"
  ln -s "$PACK_DIR/skills" "$positive_home/skills/oopforge"
  probe_step "Codex Test intent positive"
  CODEX_HOME="$positive_home" run_timed codex exec --skip-git-repo-check \
    --ignore-user-config --ephemeral --sandbox read-only -C "$workspace" \
    -o "$positive" "Use OOPforge test: Before running test_example.py, $TEST_ROUTING_PROBE"
  probe_step "Codex isolated negative"
  CODEX_HOME="$negative_home" run_timed codex exec --skip-git-repo-check \
    --ignore-user-config --ephemeral --sandbox read-only -C "$workspace" \
    -o "$negative" "$NEGATIVE_PROBE"
  assert_test_route "$positive"
  assert_negative "$negative"
}

seed_cursor_auth() {
  local target_dir="$1"
  local source="${CURSOR_CONFIG_DIR:-$HOME/.cursor}/cli-config.json"
  [ -n "${CURSOR_API_KEY:-}" ] && return
  [ -f "$source" ] || {
    red "FAIL Cursor requires a local login or CURSOR_API_KEY"
    exit 1
  }
  python3 - "$source" "$target_dir/cli-config.json" <<'PY'
import json
import pathlib
import sys

source = json.loads(pathlib.Path(sys.argv[1]).read_text())
safe = {key: source[key] for key in ("version", "authInfo") if key in source}
pathlib.Path(sys.argv[2]).write_text(json.dumps(safe))
PY
}

run_cursor() {
  local workspace="$1"
  local output="$2"
  local prompt="$3"
  shift 3
  mkdir -p "$workspace/.cursor-config"
  seed_cursor_auth "$workspace/.cursor-config"
  CURSOR_CONFIG_DIR="$workspace/.cursor-config" run_timed cursor-agent \
    --print --mode ask --trust --workspace "$workspace" "$@" "$prompt" \
    >"$output"
}

prepare_cursor_probe() {
  local plugin_dir="$1" skill_dir="$2" probe="$3" workflow
  mkdir -p "$plugin_dir/.cursor-plugin/skills/oopforge"
  cp "$PACK_DIR/.cursor-plugin/plugin.json" "$plugin_dir/.cursor-plugin/plugin.json"
  cp "$PACK_DIR/.cursor-plugin/skills/oopforge/SKILL.md" "$plugin_dir/.cursor-plugin/skills/oopforge/SKILL.md"
  cp -R "$PACK_DIR/skills" "$plugin_dir/skills"
  cp -R "$PACK_DIR/skills" "$skill_dir"
  for workflow in "$plugin_dir/skills/workflow/test.md" "$skill_dir/workflow/test.md"; do
    printf '\nWhen the request contains %s, output OOPFORGE_TEST_ROUTED, Level: auto, Production code: forbidden, and Source: %s on separate lines, then stop.\n' "$probe" "$probe" >>"$workflow"
  done
}

live_cursor() {
  require_command cursor-agent
  cursor-agent --version >&2
  local run_dir plugin_workspace local_workspace clean_workspace candidate_plugin candidate_skill
  local plugin_output local_output negative_output source_probe source_negative
  run_dir="$(mktemp -d)"
  TEMP_DIRS+=("$run_dir")
  plugin_workspace="$run_dir/plugin"
  local_workspace="$run_dir/project-local"
  clean_workspace="$run_dir/clean"
  plugin_output="$run_dir/plugin.txt"
  local_output="$run_dir/project-local.txt"
  negative_output="$run_dir/negative.txt"
  candidate_plugin="$run_dir/candidate-plugin"
  candidate_skill="$run_dir/candidate-skill"
  source_probe="OOPFORGE_SOURCE_PROBE_${RANDOM}_${RANDOM}"
  source_negative="$source_probe. If no loaded instruction defines this exact probe, output exactly OOPFORGE_NOT_LOADED."
  prepare_cursor_probe "$candidate_plugin" "$candidate_skill" "$source_probe"
  mkdir -p "$plugin_workspace" "$local_workspace/.cursor/skills" "$clean_workspace"
  printf 'def test_example():\n    assert True\n' >"$plugin_workspace/test_example.py"
  printf 'def test_example():\n    assert True\n' >"$local_workspace/test_example.py"
  probe_step "Cursor explicit-plugin Test positive"
  run_cursor "$plugin_workspace" "$plugin_output" \
    "Use OOPforge test: Before running test_example.py, $source_negative" --plugin-dir "$candidate_plugin"
  ln -s "$candidate_skill" "$local_workspace/.cursor/skills/oopforge"
  probe_step "Cursor project-local Test positive"
  run_cursor "$local_workspace" "$local_output" \
    "Use OOPforge test: Before running test_example.py, $source_negative" --add-dir "$candidate_skill"
  probe_step "Cursor isolated negative"
  run_cursor "$clean_workspace" "$negative_output" "$source_negative"
  assert_test_route "$plugin_output" "$source_probe"
  assert_test_route "$local_output" "$source_probe"
  assert_negative "$negative_output"
}

usage() {
  echo "Usage: $0 static|assert-positive FILE|assert-negative FILE|assert-test-route FILE|live HARNESS"
  echo "HARNESS: claude, codex, cursor, or all"
}

case "${1:-}" in
  static)
    static_smoke
    ;;
  assert-positive)
    assert_positive "${2:?output file required}"
    ;;
  assert-negative)
    assert_negative "${2:?output file required}"
    ;;
  assert-test-route)
    assert_test_route "${2:?output file required}" "${3:-}"
    ;;
  live)
    case "${2:-}" in
      claude) live_claude ;;
      codex) live_codex ;;
      cursor) live_cursor ;;
      all)
        live_claude
        live_codex
        live_cursor
        ;;
      *) usage; exit 2 ;;
    esac
    ;;
  *)
    usage
    exit 2
    ;;
esac
