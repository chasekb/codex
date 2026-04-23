#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

selection_out="$(hooks/_internal/routing/select-command general 0.9 "nelson captain log recent history" "$root")"
echo "$selection_out" | tail -n1 | grep -qx 'nelson-captain-log'

output="$(bash "$root/scripts/captain-log.sh")"
printf '%s\n' "$output" | grep -q '"workflow": "nelson-captain-log"'
printf '%s\n' "$output" | grep -q '"current_action"'
printf '%s\n' "$output" | grep -q '"recent_entries"'

printf 'nelson-captain-log:ok\n'
