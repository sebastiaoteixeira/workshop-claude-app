#!/usr/bin/env bash
# Asks Claude whether the diff between a base ref and HEAD leaks secrets; exits 1 when it does.
set -euo pipefail

base=${1:?usage: review_secrets.sh <base-ref>}

prompt='You are a secrets scanner. Review the unified diff on stdin for leaked credentials:
API keys, access tokens, passwords, private keys, signed URLs, connection strings with
credentials. Placeholders, documented defaults and obvious dummies (such as "changeme",
"dev-token", "xxx", "<your-key>") are not secrets. Report only added lines. Answer with
JSON only: {"secrets_found": boolean, "findings": [{"file": string, "line": string, "reason": string}]}.'

schema='{
  "type": "object",
  "properties": {
    "secrets_found": {"type": "boolean"},
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file": {"type": "string"},
          "line": {"type": "string"},
          "reason": {"type": "string"}
        },
        "required": ["file", "line", "reason"]
      }
    }
  },
  "required": ["secrets_found", "findings"]
}'

# The JSON is the result object, or an array of events when user settings enable verbose.
verdict=$(
  git diff "$base"..HEAD \
    | claude -p "$prompt" --output-format json --json-schema "$schema" --tools "" \
    | jq -e '[.] | flatten | map(select(.type == "result"))[-1].structured_output'
) || { echo "review_secrets: Claude returned no valid verdict" >&2; exit 1; }

jq -r '.findings[] | "\(.file):\(.line): \(.reason)"' <<<"$verdict"
[[ $(jq -r '.secrets_found' <<<"$verdict") == false ]]
