#!/usr/bin/env bash
#
# Static packaging checks and authenticated harness activation probes.

set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEMP_DIRS=()
ACTIVATION_TOKEN="OOPFORGE_ACTIVATION_PROBE"
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
  if grep -Fxq "OOPFORGE_NOT_LOADED" "$output"; then
    probe_failure "positive probe also reported not loaded" "$output"
    return 1
  fi
  green "PASS positive activation probe"
}

assert_negative() {
  local output="$1"
  grep -Fxq "OOPFORGE_NOT_LOADED" "$output" ||
    { probe_failure "negative control did not report isolation" "$output"; return 1; }
  if grep -Fxq "OOPFORGE_LOADED" "$output"; then
    probe_failure "negative control loaded OOPforge" "$output"
    return 1
  fi
  green "PASS negative activation control"
}

static_smoke() {
  python3 - "$PACK_DIR" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
manifests = [
    root / ".claude-plugin/plugin.json",
    root / ".codex-plugin/plugin.json",
    root / ".cursor-plugin/plugin.json",
]
versions = {json.loads(path.read_text())["version"] for path in manifests}
if len(versions) != 1:
    raise SystemExit("manifest versions differ")

registry = json.loads((root / "skills/stability.json").read_text())
stable = registry["stable"]
experimental = registry["experimental"]
listed = stable + experimental
actual = sorted(
    str(path.relative_to(root))
    for path in (root / "skills").rglob("*.md")
)
if len(listed) != len(set(listed)):
    raise SystemExit("skill stability registry contains duplicates")
if sorted(listed) != actual:
    missing = sorted(set(actual) - set(listed))
    extra = sorted(set(listed) - set(actual))
    raise SystemExit(f"skill stability mismatch: missing={missing}, extra={extra}")
if registry["schema"] != "oopforge.skill-stability.v1":
    raise SystemExit("unexpected skill stability schema")
for status in ("stable", "experimental"):
    for relative in registry[status]:
        frontmatter = (root / relative).read_text().split("---", 2)[1]
        if f"stability: {status}" not in frontmatter:
            raise SystemExit(f"stability frontmatter mismatch: {relative}")

required = [
    "commands/craft.md",
    ".cursor-plugin/skills/oopforge/SKILL.md",
    "docs/reference/support-scope.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"missing harness path: {relative}")
for relative in ["commands/craft.md", "skills/SKILL.md",
                 ".cursor-plugin/skills/oopforge/SKILL.md"]:
    if "OOPFORGE_ACTIVATION_PROBE" not in (root / relative).read_text():
        raise SystemExit(f"missing activation probe: {relative}")
print("PASS static harness packaging")
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
  require_link_target "$HOME/.claude/skills/oopforge" "$PACK_DIR/skills"
  require_link_target "$HOME/.claude/commands/oopforge" "$PACK_DIR/commands"
  claude --version >&2
  local run_dir positive negative
  run_dir="$(mktemp -d)"
  TEMP_DIRS+=("$run_dir")
  positive="$run_dir/positive.txt"
  negative="$run_dir/negative.txt"
  (
    cd "$run_dir"
    probe_step "Claude command positive"
    run_timed claude -p --no-session-persistence --permission-mode plan \
      --tools "" >"$positive" <<<"/oopforge:craft $ACTIVATION_TOKEN"
    probe_step "Claude safe-mode negative"
    run_timed claude --safe-mode -p --no-session-persistence \
      --permission-mode plan --tools "" >"$negative" <<<"$NEGATIVE_PROBE"
  )
  assert_positive "$positive"
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
  link_codex_auth "$positive_home"
  link_codex_auth "$negative_home"
  ln -s "$PACK_DIR/skills" "$positive_home/skills/oopforge"
  probe_step "Codex global-skill positive"
  CODEX_HOME="$positive_home" run_timed codex exec --skip-git-repo-check \
    --ignore-user-config --ephemeral --sandbox read-only -C "$workspace" \
    -o "$positive" "Use OOPforge craft: $NEGATIVE_PROBE"
  probe_step "Codex isolated negative"
  CODEX_HOME="$negative_home" run_timed codex exec --skip-git-repo-check \
    --ignore-user-config --ephemeral --sandbox read-only -C "$workspace" \
    -o "$negative" "$NEGATIVE_PROBE"
  assert_positive "$positive"
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

live_cursor() {
  require_command cursor-agent
  cursor-agent --version >&2
  local run_dir plugin_workspace local_workspace clean_workspace
  local plugin_output local_output negative_output
  run_dir="$(mktemp -d)"
  TEMP_DIRS+=("$run_dir")
  plugin_workspace="$run_dir/plugin"
  local_workspace="$run_dir/project-local"
  clean_workspace="$run_dir/clean"
  plugin_output="$run_dir/plugin.txt"
  local_output="$run_dir/project-local.txt"
  negative_output="$run_dir/negative.txt"
  mkdir -p "$plugin_workspace" "$local_workspace/.cursor/skills" "$clean_workspace"
  probe_step "Cursor explicit-plugin positive"
  run_cursor "$plugin_workspace" "$plugin_output" \
    "Use OOPforge craft: $NEGATIVE_PROBE" --plugin-dir "$PACK_DIR"
  ln -s "$PACK_DIR/skills" "$local_workspace/.cursor/skills/oopforge"
  probe_step "Cursor project-local positive"
  run_cursor "$local_workspace" "$local_output" \
    "Use OOPforge craft: $NEGATIVE_PROBE" --add-dir "$PACK_DIR"
  probe_step "Cursor isolated negative"
  run_cursor "$clean_workspace" "$negative_output" "$NEGATIVE_PROBE"
  assert_positive "$plugin_output"
  assert_positive "$local_output"
  assert_negative "$negative_output"
}

usage() {
  echo "Usage: $0 static|assert-positive FILE|assert-negative FILE|live HARNESS"
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
