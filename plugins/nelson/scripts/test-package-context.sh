#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

output="$(bash "$root/scripts/package-context.sh")"

printf '%s\n' "$output" | grep -q '"additionalContext"'
printf '%s\n' "$output" | grep -q '"name": "nelson"'
printf '%s\n' "$output" | grep -q '"commands": \['
printf '%s\n' "$output" | grep -q '"commands": 3'
printf '%s\n' "$output" | grep -q '"agents": \['
printf '%s\n' "$output" | grep -q '"agents": 2'
printf '%s\n' "$output" | grep -q '"public_vocabulary": \['
printf '%s\n' "$output" | grep -q '"public_vocabulary_count": 4'
printf '%s\n' "$output" | grep -q '"sailing orders"'
printf '%s\n' "$output" | grep -q '"battle plan"'
printf '%s\n' "$output" | grep -q '"action station"'
printf '%s\n' "$output" | grep -q '"captain'"'"'s log"'
printf '%s\n' "$output" | grep -q '"mission_scenarios": 7'
