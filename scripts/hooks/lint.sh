#!/usr/bin/env bash
# PostToolUse hook (Edit|Write): lints the edited Python file and reports what ruff could not fix.
# Unused imports are reported, never removed: Claude adds an import before the edit that uses it.
set -euo pipefail

file=$(jq -r '.tool_input.file_path // empty')
[[ $file == *.py ]] || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}"
uv run --quiet ruff check --fix --unfixable F401 "$file" >&2 || exit 2
