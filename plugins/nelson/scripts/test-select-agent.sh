#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

coordinator_out="$(hooks/_internal/routing/select-agent general 0.9 "nelson orchestration background work" "$root")"
echo "$coordinator_out" | tail -n1 | grep -qx 'nelson-coordinator'

mission_out="$(hooks/_internal/routing/select-agent general 0.9 "nelson mission lifecycle planning dispatch" "$root")"
echo "$mission_out" | tail -n1 | grep -qx 'nelson-coordinator'

captain_out="$(hooks/_internal/routing/select-agent general 0.9 "nelson captain log action state" "$root")"
echo "$captain_out" | tail -n1 | grep -qx 'nelson-captain-log'

printf 'nelson-select-agent:ok\n'
