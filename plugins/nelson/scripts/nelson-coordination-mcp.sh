#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

context="$("$root/scripts/package-context.sh")"
printf '%s\n' "$context"
