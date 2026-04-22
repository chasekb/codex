#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

objective="nelson plugin integration package conversion"
payload="{\"task\":{\"class\":\"implement\",\"objective\":\"$objective\"},\"classification\":{\"confidence\":0.92}}"

python3 "$root/../../hooks/_internal/runtime/hook-pipeline" TaskStart <<<"$payload" >/dev/null
python3 "$root/../../hooks/_internal/runtime/hook-pipeline" TaskComplete <<<"{}" >/dev/null

test -f "$root/validation/nelson-coordination-log.jsonl"
test -f "$root/validation/nelson-action-state.json"
grep -Fq "$objective" "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"hook_name": "TaskStart"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"skill_id": "nelson-conversion"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"command_id": "nelson-context"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"agent_id": "nelson-coordinator"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"plugin_id": "nelson"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"current_action"' "$root/validation/nelson-action-state.json"
grep -Fq '"status": "pass"' "$root/validation/nelson-action-state.json"

printf 'nelson-coordination-ledger:ok\n'
