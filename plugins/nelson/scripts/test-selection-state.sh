#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
objective="nelson plugin integration package conversion"
payload="{\"task\":{\"class\":\"implement\",\"objective\":\"$objective\"},\"classification\":{\"confidence\":0.92}}"

: > "$root/validation/nelson-coordination-log.jsonl"
rm -f "$root/validation/nelson-action-state.json"

python3 "$root/../../hooks/_internal/runtime/hook-pipeline" TaskStart <<<"$payload" >/dev/null
python3 "$root/../../hooks/_internal/runtime/hook-pipeline" TaskComplete <<<"{}" >/dev/null

test -f "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"workflow": "nelson-conversion"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"skill_id": "nelson-conversion"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"skill_registry_label": "plugin:nelson"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"command_id": "nelson-context"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"command_registry_label": "plugin:nelson"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"agent_id": "nelson-coordinator"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"agent_registry_label": "plugin:nelson"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"plugin_id": "nelson"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"plugin_source": "plugin:nelson"' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"plugin_context": "nelson 0.1.0 package loaded' "$root/../../outputs/hook-runtime-state.json"
grep -Fq '"mission_scenarios": 6' "$root/../../outputs/hook-runtime-state.json"
grep -Fq "$objective" "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"hook_name": "TaskStart"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"hook_name": "TaskComplete"' "$root/validation/nelson-coordination-log.jsonl"
grep -Fq '"current_action"' "$root/validation/nelson-action-state.json"
grep -Fq '"status": "pass"' "$root/validation/nelson-action-state.json"

printf 'nelson-selection-state:ok\n'
