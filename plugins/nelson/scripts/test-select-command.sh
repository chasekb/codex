#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

context_out="$(hooks/_internal/routing/select-command general 0.9 "nelson package context" "$root")"
echo "$context_out" | tail -n1 | grep -qx 'nelson-context'

validate_out="$(hooks/_internal/routing/select-command general 0.9 "nelson package validation" "$root")"
echo "$validate_out" | tail -n1 | grep -qx 'nelson-validate'

inventory_out="$(hooks/_internal/routing/select-command general 0.9 "nelson package inventory" "$root")"
echo "$inventory_out" | tail -n1 | grep -qx 'nelson-inventory'

printf 'nelson-select-command:ok\n'
