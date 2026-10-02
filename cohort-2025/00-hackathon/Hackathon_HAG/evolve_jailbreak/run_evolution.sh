#!/usr/bin/env bash
# ── GamePlan Evolution Runner ──
# Runs the OpenEvolve pipeline to discover jailbreak prompts.
# All configuration comes from evolve_config.yaml — no .env file needed.
#
# Usage:
#   ./run_evolution.sh [--iterations 200] [--checkpoint PATH]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CONFIG_FILE="${SCRIPT_DIR}/evolve_config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Use Python to load config and export env vars
eval "$(python3 -c "
import os, yaml
with open('$CONFIG_FILE') as f:
    c = yaml.safe_load(f)
api = c['api']
m = c['models']
exp = c.get('experiment', {})
t_base = m['target'].get('api_base', api['openrouter_base'])
j_base = m['judge'].get('api_base', api['openrouter_base'])
print(f'export OPENROUTER_API_KEY=\"{api[\"openrouter_key\"]}\"')
print(f'export EVOLVER_API_BASE=\"{c[\"llm\"][\"api_base\"]}\"')
print(f'export EVOLVER_API_KEY=\"{api[\"openrouter_key\"]}\"')
print(f'export EVOLVER_MODEL=\"{m[\"evolver\"][\"name\"]}\"')
print(f'export TARGET_API_BASE=\"{t_base}\"')
print(f'export TARGET_API_KEY=\"{api[\"openrouter_key\"]}\"')
print(f'export TARGET_MODEL=\"{m[\"target\"][\"name\"]}\"')
print(f'export TARGET_MAX_TOKENS="{m["target"].get("max_tokens", 4096)}"')
print(f'export JUDGE_API_BASE=\"{j_base}\"')
print(f'export JUDGE_API_KEY=\"{api[\"openrouter_key\"]}\"')
print(f'export JUDGE_MODEL=\"{m[\"judge\"][\"name\"]}\"')
print(f'export JUDGE_MAX_TOKENS="{m["judge"].get("max_tokens", 512)}"')
print(f'export GAMEPLAN_VERBOSE=\"{\"1\" if exp.get(\"verbose\", False) else \"0\"}\"')
")"

# ── Resolve OpenEvolve ──
PYTHON_BIN=$(which python3 2>/dev/null || which python 2>/dev/null || echo "python3")

if $PYTHON_BIN -c "import openevolve" 2>/dev/null; then
    echo "[OK] OpenEvolve found via pip install"
    EVOLVE_CMD="$PYTHON_BIN -m openevolve.cli"
else
    OPENEVOLVE_DIR="${OPENEVOLVE_DIR:-/tmp/openevolve}"
    if [ -f "$OPENEVOLVE_DIR/openevolve-run.py" ]; then
        echo "[OK] Using OpenEvolve from: $OPENEVOLVE_DIR"
        EVOLVE_CMD="$PYTHON_BIN $OPENEVOLVE_DIR/openevolve-run.py"
        export PYTHONPATH="${OPENEVOLVE_DIR}:${PYTHONPATH:-}"
    else
        echo "ERROR: OpenEvolve not found. Install with: pip install openevolve"
        exit 1
    fi
fi

# ── Resolve template_dir to absolute path in resolved config ──
TMP_CONFIG=$(mktemp /tmp/openevolve_config.XXXXXX.yaml)
trap "rm -f $TMP_CONFIG" EXIT

$PYTHON_BIN -c "
import yaml
from pathlib import Path
with open('$CONFIG_FILE') as f:
    c = yaml.safe_load(f)
template_dir = c.get('prompt', {}).get('template_dir', 'templates')
if not str(template_dir).startswith('/'):
    c['prompt']['template_dir'] = str((Path('$SCRIPT_DIR') / template_dir).resolve())
for key in ['api', 'models', 'experiment']:
    c.pop(key, None)
with open('$TMP_CONFIG', 'w') as f:
    yaml.dump(c, f, default_flow_style=False, sort_keys=False)
"

echo "Configuration:"
echo "  Evolver: $EVOLVER_MODEL @ $EVOLVER_API_BASE"
echo "  Target:  $TARGET_MODEL @ $TARGET_API_BASE"
echo "  Judge:   $JUDGE_MODEL @ $JUDGE_API_BASE"
echo ""

# ── Run evolution ──
$EVOLVE_CMD \
    initial_jailbreak_prompt.txt \
    evaluator.py \
    --config "$TMP_CONFIG" \
    "$@"

# ── Report ──
RESULT_DIR="openevolve_output"
if [ -f "$RESULT_DIR/best/best_program.txt" ]; then
    echo ""
    echo "══════════════════════════════════════════════════════════════════"
    echo "  BEST JAILBREAK PROMPT DISCOVERED:"
    echo "══════════════════════════════════════════════════════════════════"
    cat "$RESULT_DIR/best/best_program.txt"
    echo ""
    echo "══════════════════════════════════════════════════════════════════"
    if [ -f "$RESULT_DIR/best/best_program.metadata.json" ]; then
        echo "  Metrics:"
        $PYTHON_BIN -c "import json; m=json.load(open('$RESULT_DIR/best/best_program.metadata.json')); [print(f'    {k}: {v}') for k,v in m.get('metrics',{}).items()]"
    fi
fi
