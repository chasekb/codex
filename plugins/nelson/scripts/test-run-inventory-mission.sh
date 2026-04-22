#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
output="$(bash "$root/scripts/run-inventory-mission.sh")"

printf '%s\n' "$output" | grep -q '"workflow": "nelson-inventory"'
printf '%s\n' "$output" | grep -q '"mission": "inventory"'
printf '%s\n' "$output" | grep -q '"status": "passed"'
printf '%s\n' "$output" | grep -q '"mission_scenarios": 6'
printf '%s\n' "$output" | grep -q '"commands": \['
printf '%s\n' "$output" | grep -q '"agents": \['

printf 'nelson-run-inventory-mission:ok\n'
