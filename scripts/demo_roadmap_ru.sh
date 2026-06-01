#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python"
fi

DATABASE=".data/demo/cofounder_demo.sqlite3"
EXPORT_DIR=".data/demo/exports"
OUTPUT_FILE="hair_salon_roadmap.md"
INPUT_FILE="docs/examples/domains/hair_salon_input.md"

bold() {
  printf '\033[1m%s\033[0m\n' "$1"
}

muted() {
  printf '\033[2m%s\033[0m\n' "$1"
}

ok() {
  printf '\033[32m%s\033[0m\n' "$1"
}

section() {
  printf '\n\033[1;36m%s\033[0m\n' "$1"
}

section "AI Roadmap Studio - локальное демо"
muted "Цель: показать, как из описания workflow получается AI implementation roadmap."

section "1. Вход"
printf 'Business profile: %s\n' "$INPUT_FILE"
printf 'Demo domain: hair salon booking + reminders\n'

section "2. Команда"
cat <<CMD
$PYTHON_BIN -m workflow_agent_studio.cli roadmap \\
  --database $DATABASE \\
  --run-id hair-salon-demo \\
  --business-profile $INPUT_FILE \\
  --privacy-mode lightweight_cloud \\
  --export-dir $EXPORT_DIR \\
  --output $OUTPUT_FILE
CMD

section "3. Генерация roadmap"
mkdir -p "$EXPORT_DIR"
RESULT="$(
  "$PYTHON_BIN" -m workflow_agent_studio.cli roadmap \
    --database "$DATABASE" \
    --run-id hair-salon-demo \
    --business-profile "$INPUT_FILE" \
    --privacy-mode lightweight_cloud \
    --export-dir "$EXPORT_DIR" \
    --output "$OUTPUT_FILE"
)"
ok "Roadmap generated"
printf '%s\n' "$RESULT"

REPORT_PATH="$("$PYTHON_BIN" -c 'import json,sys; print(json.loads(sys.stdin.read())["path"])' <<<"$RESULT")"

section "4. Что получилось"
"$PYTHON_BIN" - "$REPORT_PATH" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

checks = [
    ("Draft label", "Status: Draft"),
    ("Executive summary", "## Executive Summary"),
    ("Do-not-automate", "Top Do-Not-Automate-Yet Items:"),
    ("Privacy mode", "## Cloud Vs Local/Private Recommendation"),
    ("Cost/time/team", "## Cost, Time, And Team Plan"),
    ("Verification appendix", "## Verification Appendix"),
]

print(f"Markdown path: {path}")
for label, marker in checks:
    status = "OK" if marker in text else "MISSING"
    print(f"{label}: {status}")

highlights = [
    "Appointment booking and reminder automation",
    "Lightweight cloud only after contact fields are redacted.",
    "Cancellation penalty decisions",
    "medical or skin-condition advice",
]

print("\nHighlights:")
for item in highlights:
    print(f"- {item}: {'present' if item in text else 'missing'}")
PY

section "5. Быстрая proof-команда"
cat <<CMD
$PYTHON_BIN -m pytest \\
  tests/integration/test_roadmap_generation.py \\
  tests/integration/test_roadmap_markdown_export.py \\
  tests/integration/test_roadmap_cli.py \\
  tests/eval/test_roadmap_quality_eval.py \\
  -q
CMD

section "6. Финальный смысл"
bold "Это не agent builder."
bold "Это AI roadmap layer: что внедрять, что не внедрять, privacy, cost, eval и handoff."

section "7. Public-source workflow пример"
PUBLIC_INPUT="tests/fixtures/public_sources/hvac_lead_intake.notes.md"
PUBLIC_OUTPUT="public_hvac_roadmap.md"
cat <<CMD
$PYTHON_BIN -m workflow_agent_studio.cli roadmap \\
  --database $DATABASE \\
  --run-id public-hvac-demo \\
  --business-profile $PUBLIC_INPUT \\
  --privacy-mode lightweight_cloud \\
  --export-dir $EXPORT_DIR \\
  --output $PUBLIC_OUTPUT
CMD

PUBLIC_RESULT="$(
  "$PYTHON_BIN" -m workflow_agent_studio.cli roadmap \
    --database "$DATABASE" \
    --run-id public-hvac-demo \
    --business-profile "$PUBLIC_INPUT" \
    --privacy-mode lightweight_cloud \
    --export-dir "$EXPORT_DIR" \
    --output "$PUBLIC_OUTPUT"
)"
ok "Public-source roadmap generated"
printf '%s\n' "$PUBLIC_RESULT"
muted "Важно: public-source demo доказывает работу на публичном workflow, но не buyer demand."
ok "Demo complete"
