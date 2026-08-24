#!/usr/bin/env bash
#
# Run the reproducible control-versus-OOPforge comparison.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
STARTER_PATH="examples/calculator-python-hexagonal"
SOURCE_COMMIT="$(git -C "$PACK_DIR" rev-parse HEAD)"
MODEL="${PROOF_MODEL:-}"
MODE="${PROOF_MODE:-run}"
RUN_ID="${PROOF_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_BASE="${PROOF_OUTPUT_BASE:-${TMPDIR:-/tmp}/oopforge-proof-runs}"
OUTPUT_BASE="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$OUTPUT_BASE")"
OUTPUT_ROOT="$OUTPUT_BASE/$RUN_ID"

TASK='Add a void-calculation use case. A calculation may be voided once and only within five minutes of being performed. A second void or a late void must be rejected. Expose POST /calculations/{id}/void; return 404 when the calculation does not exist and 409 when the transition is invalid. Persist the changed calculation and add domain, use-case, and API tests. Use an injectable clock so tests do not depend on sleep or wall-clock timing. Do not change unrelated behavior.'

if [ "$MODE" != "run" ] && [ "$MODE" != "export" ]; then
  printf 'PROOF_MODE must be run or export.\n' >&2
  exit 2
fi

if [ "$MODE" = "run" ] && [ -z "$MODEL" ]; then
  printf 'PROOF_MODEL is required so both runs use an explicit model.\n' >&2
  exit 2
fi

if [ "$MODE" = "run" ] && [ "$MODEL" = "auto" ]; then
  printf 'PROOF_MODEL=auto is invalid: both runs must pin one model ID.\n' >&2
  exit 2
fi

case "$OUTPUT_BASE/" in
  "$PACK_DIR/"*)
    printf 'Proof workspaces must be outside the OOPforge repository.\n' >&2
    printf 'Choose an external PROOF_OUTPUT_BASE (default: system temp).\n' >&2
    exit 2
    ;;
esac

if [ "${PROOF_ALLOW_DIRTY:-0}" != 1 ] &&
   [ -n "$(git -C "$PACK_DIR" status --porcelain -- "$STARTER_PATH" skills)" ]; then
  printf 'Commit starter and skill changes before running proof.\n' >&2
  exit 2
fi

if [ "$MODE" = "run" ] && ! command -v cursor-agent >/dev/null 2>&1; then
  printf 'cursor-agent is required.\n' >&2
  exit 2
fi

if [ "$MODE" = "run" ] && ! cursor-agent status >/dev/null 2>&1; then
  printf 'Cursor Agent is not authenticated. Run: cursor-agent login\n' >&2
  exit 2
fi

prepare_workspace() {
  local name="$1"
  local workspace="$OUTPUT_ROOT/$name/workspace"

  mkdir -p "$workspace"
  git -C "$PACK_DIR" archive "$SOURCE_COMMIT" "$STARTER_PATH" |
    tar -x -C "$workspace" --strip-components=2
  if [ "$name" = "treatment" ]; then
    mkdir -p "$workspace/.cursor/skills"
    mkdir -p "$workspace/.cursor/skills/oopforge"
    git -C "$PACK_DIR" archive "$SOURCE_COMMIT" skills |
      tar -x -C "$workspace/.cursor/skills/oopforge" --strip-components=1
  fi
  git -C "$workspace" init -q
  git -C "$workspace" add .
  git -C "$workspace" \
    -c user.name=OOPforge \
    -c user.email=proof@oopforge.local \
    commit -q -m "Proof baseline"
}

run_agent() {
  local name="$1"
  local prompt="$2"
  shift 2
  local workspace="$OUTPUT_ROOT/$name/workspace"

  cursor-agent \
    --print \
    --trust \
    --force \
    --sandbox enabled \
    --model "$MODEL" \
    --workspace "$workspace" \
    "$@" \
    "$prompt" \
    >"$OUTPUT_ROOT/$name/agent-output.txt" 2>&1

  git -C "$workspace" add -N . >/dev/null
  git -C "$workspace" diff --stat >"$OUTPUT_ROOT/$name/diff-stat.txt"
  git -C "$workspace" diff --no-ext-diff >"$OUTPUT_ROOT/$name/changes.patch"
}

prepare_constraints() {
  local workspace="$OUTPUT_ROOT/control/workspace"
  python3 -m venv "$OUTPUT_ROOT/dependency-venv"
  "$OUTPUT_ROOT/dependency-venv/bin/python" -m pip install -q \
    -e "${workspace}[dev]"
  "$OUTPUT_ROOT/dependency-venv/bin/python" -m pip freeze --exclude-editable \
    >"$OUTPUT_ROOT/constraints.txt"
  rm -rf "$OUTPUT_ROOT/dependency-venv"
}

run_tests() {
  local name="$1"
  local workspace="$OUTPUT_ROOT/$name/workspace"
  local result=0

  (
    cd "$workspace"
    local_status=0
    python3 -m venv .proof-venv
    .proof-venv/bin/python -m pip install -q \
      -c "$OUTPUT_ROOT/constraints.txt" -e ".[dev]"
    .proof-venv/bin/python -m pip freeze --exclude-editable \
      >"$OUTPUT_ROOT/$name/dependency-freeze.txt"
    .proof-venv/bin/python -m mypy || local_status=1
    .proof-venv/bin/lint-imports || local_status=1
    .proof-venv/bin/python -m pytest -q || local_status=1
    exit "$local_status"
  ) >"$OUTPUT_ROOT/$name/test-output.txt" 2>&1 || result=$?

  printf '%s\n' "$result" >"$OUTPUT_ROOT/$name/test-exit-code.txt"
}

validate_dependencies() {
  if ! diff -u \
    "$OUTPUT_ROOT/control/dependency-freeze.txt" \
    "$OUTPUT_ROOT/treatment/dependency-freeze.txt" \
    >"$OUTPUT_ROOT/dependency.diff"; then
    printf 'INVALID: control and treatment resolved different dependencies.\n' >&2
    exit 3
  fi
}

evaluate() {
  local name="$1"
  local workspace="$OUTPUT_ROOT/$name/workspace"
  local result=0

  python3 "$SCRIPT_DIR/evaluate-run.py" "$workspace" \
    >"$OUTPUT_ROOT/$name/evaluation.json" || result=$?
  printf '%s\n' "$result" >"$OUTPUT_ROOT/$name/evaluation-exit-code.txt"
}

validate_control() {
  if [ -d "$OUTPUT_ROOT/control/workspace/.craft" ]; then
    printf 'INVALID: control created .craft; OOPforge instructions contaminated it.\n' >&2
    printf 'Disable user-level OOPforge skills or use a clean OS profile, then retry.\n' >&2
    exit 3
  fi
}

validate_treatment() {
  if [ ! -d "$OUTPUT_ROOT/treatment/workspace/.craft" ]; then
    printf 'INVALID: treatment did not create .craft; skill load is unproven.\n' >&2
    exit 3
  fi
}

write_metadata() {
  {
    printf 'run_id=%s\n' "$RUN_ID"
    printf 'model=%s\n' "$MODEL"
    printf 'cursor_agent_version=%s\n' "$(cursor-agent --version)"
    printf 'source_commit=%s\n' "$SOURCE_COMMIT"
    printf 'starter=%s\n' "$STARTER_PATH"
    printf 'dependency_constraints=constraints.txt\n'
    printf 'treatment_delivery=project-local .cursor/skills/oopforge\n'
    printf 'task=%s\n' "$TASK"
  } >"$OUTPUT_ROOT/metadata.txt"
}

mkdir -p "$OUTPUT_ROOT"
prepare_workspace control
prepare_workspace treatment
printf '%s\n' "$SOURCE_COMMIT" >"$OUTPUT_ROOT/source-commit.txt"

if [ "$MODE" = "export" ]; then
  printf 'Proof export: %s\n' "$OUTPUT_ROOT"
  exit 0
fi

write_metadata
prepare_constraints
run_agent control "$TASK"
validate_control
run_agent treatment \
  "Use the project-local OOPforge Craft skill for this request. Follow its Assumptions, OOP Contract, continuity, and verification gates. $TASK"
validate_treatment

run_tests control
run_tests treatment
validate_dependencies
evaluate control
evaluate treatment

printf 'Proof artifacts: %s\n' "$OUTPUT_ROOT"
printf 'Inspect both evaluation.json and test-output.txt files before publishing.\n'
