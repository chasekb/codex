#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$root/.codex-plugin/plugin.json"
test -f "$root/.app.json"
test -f "$root/.mcp.json"
test -d "$root/hooks"
test -d "$root/rules"
test -d "$root/workflows"
test -d "$root/skills"
test -d "$root/scripts"
test -d "$root/assets"
test -f "$root/validation/mission-scenarios.md"

grep -q '"name": "nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"displayName": "Nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"skills": "./skills/"' "$root/.codex-plugin/plugin.json"

printf 'nelson-package:ok\n'
