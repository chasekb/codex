#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

output="$("$root/hooks/session-start")"

printf '%s\n' "$output" | grep -q '"additionalContext"'
printf '%s\n' "$output" | grep -q '"package"'
printf '%s\n' "$output" | grep -q '"name": "nelson"'
printf '%s\n' "$output" | grep -q '"commands": \['
printf '%s\n' "$output" | grep -q '"nelson-captain-log"'
printf '%s\n' "$output" | grep -q '"agents": \['
