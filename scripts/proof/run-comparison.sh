#!/usr/bin/env bash
#
# Run the reproducible C4 control-versus-OOPforge comparison.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
STARTER="$PACK_DIR/examples/calculator-python-hexagonal"
MODEL="${PROOF_MODEL:-}"
RUN_ID="${PROOF_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_BASE="${PROOF_OUTPUT_BASE:-${TMPDIR:-/tmp}/oopforge-proof-runs}"
OUTPUT_BASE="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$OUTPUT_BASE")"
OUTPUT_ROOT="$OUTPUT_BASE/$RUN_ID"

TASK='Add a void-calculation use case. A calculation may be voided once and only within five minutes of being performed. A second void or a late void must be rejected. Expose POST /calculations/{id}/void; return 404 when the calculation does not exist and 409 when the transition is invalid. Persist the changed calculation and add domain, use-case, and API tests. Use an injectable clock so tests do not depend on sleep or wall-clock timing. Do not change unrelated behavior.'

if [ -z "$MODEL" ]; then
  printf 'PROOF_MODEL is required so both runs use an explicit model.\n' >&2
  exit 2
fi

if [ "$MODEL" = "auto" ]; then
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

if ! command -v cursor-agent >/dev/null 2>&1; then
  printf 'cursor-agent is required.\n' >&2
  exit 2
fi

if ! cursor-agent status >/dev/null 2>&1; then
  printf 'Cursor Agent is not authenticated. Run: cursor-agent login\n' >&2
  exit 2
fi

prepare_workspace() {
  local name="$1"
  local workspace="$OUTPUT_ROOT/$name/workspace"

  mkdir -p "$OUTPUT_ROOT/$name"
  cp -R "$STARTER" "$workspace"
  if [ "$name" = "treatment" ]; then
    mkdir -p "$workspace/.cursor/skills"
    cp -R "$PACK_DIR/skills" "$workspace/.cursor/skills/oopforge"
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

run_tests() {
  local name="$1"
  local workspace="$OUTPUT_ROOT/$name/workspace"
  local result=0

  (
    cd "$workspace"
    python3 -m venv .proof-venv
    .proof-venv/bin/python -m pip install -q -e ".[dev]"
    .proof-venv/bin/python -m pytest -q
  ) >"$OUTPUT_ROOT/$name/test-output.txt" 2>&1 || result=$?

  printf '%s\n' "$result" >"$OUTPUT_ROOT/$name/test-exit-code.txt"
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
    printf 'source_commit=%s\n' "$(git -C "$PACK_DIR" rev-parse HEAD)"
    printf 'starter=%s\n' "${STARTER#"$PACK_DIR"/}"
    printf 'treatment_delivery=project-local .cursor/skills/oopforge\n'
    printf 'task=%s\n' "$TASK"
  } >"$OUTPUT_ROOT/metadata.txt"
}

mkdir -p "$OUTPUT_ROOT"
write_metadata
prepare_workspace control
prepare_workspace treatment

run_agent control "$TASK"
validate_control
run_agent treatment \
  "Use the project-local OOPforge Craft skill for this request. Follow its Assumptions, OOP Contract, continuity, and verification gates. $TASK"
validate_treatment

run_tests control
run_tests treatment
evaluate control
evaluate treatment

printf 'Proof artifacts: %s\n' "$OUTPUT_ROOT"
printf 'Inspect both evaluation.json and test-output.txt files before publishing.\n'
