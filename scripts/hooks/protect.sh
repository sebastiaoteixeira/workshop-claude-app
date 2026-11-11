#!/usr/bin/env bash
# PreToolUse hook (Edit|Write): refuses writes to local secrets and applied migrations.
set -euo pipefail

file=$(jq -r '.tool_input.file_path // empty')

case /$file in
  */.env | */migrations/*)
    echo "Blocked: $file is protected. Secrets live outside the repo and applied migrations are never edited; add a new numbered migration instead." >&2
    exit 2
    ;;
esac
