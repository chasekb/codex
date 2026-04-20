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
test -f "$root/workflows/pipelines/conversion.yaml"
test -f "$root/rules/conversion.rules"
test -f "$root/skills/nelson-conversion/SKILL.md"
test -f "$root/hooks/session-start"
test -f "$root/scripts/package-context.sh"
test -x "$root/hooks/session-start"
test -x "$root/scripts/package-context.sh"

grep -q '"name": "nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"displayName": "Nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"skills": "./skills/"' "$root/.codex-plugin/plugin.json"

bash "$root/scripts/package-context.sh" | grep -q '"additionalContext": "nelson 0.1.0 package loaded'
bash "$root/scripts/validate-mission-scenarios.sh" >/dev/null

printf 'nelson-package:ok\n'
