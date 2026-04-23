#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
runtime_root="$root/../.."

selection_out="$(hooks/_internal/routing/select-workflow general 0.9 "nelson mission lifecycle planning dispatch execution recovery summary" "$runtime_root")"
echo "$selection_out" | tail -n1 | grep -qx 'nelson-mission'

test -f "$root/workflows/pipelines/mission.yaml"
grep -q 'id: nelson-mission' "$root/workflows/pipelines/mission.yaml"
grep -q 'mission_plan' "$root/workflows/pipelines/mission.yaml"
grep -q 'mission_summary' "$root/workflows/pipelines/mission.yaml"

printf 'nelson-mission-lifecycle:ok\n'
