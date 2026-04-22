#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$root/.codex-plugin/plugin.json"
test -f "$root/.app.json"
test -f "$root/.mcp.json"
test -x "$root/scripts/nelson-coordination-mcp.sh"
test -d "$root/hooks"
test -d "$root/rules"
test -d "$root/workflows"
test -d "$root/skills"
test -d "$root/commands"
test -d "$root/agents"
test -d "$root/scripts"
test -d "$root/assets"
test -f "$root/validation/mission-scenarios.md"
test -f "$root/commands/registry.yaml"
test -f "$root/agents/registry.yaml"
test -f "$root/commands/context.md"
test -f "$root/commands/inventory.md"
test -f "$root/commands/validate.md"
test -f "$root/agents/coordinator.md"
test -f "$root/agents/captain-log.md"
test -f "$root/workflows/pipelines/conversion.yaml"
test -f "$root/workflows/pipelines/inventory.yaml"
test -f "$root/rules/conversion.rules"
test -f "$root/skills/nelson-conversion/SKILL.md"
test -f "$root/hooks/session-start"
test -f "$root/scripts/package-context.sh"
test -f "$root/scripts/validate-mapping.sh"
test -f "$root/scripts/run-mission-scenarios.sh"
test -f "$root/scripts/run-inventory-mission.sh"
test -f "$root/scripts/test-coordination-ledger.sh"
test -f "$root/scripts/test-run-inventory-mission.sh"
test -f "$root/scripts/test-selection-state.sh"
test -x "$root/hooks/session-start"
test -x "$root/scripts/package-context.sh"
test -x "$root/scripts/validate-mapping.sh"
test -x "$root/scripts/run-mission-scenarios.sh"
test -x "$root/scripts/run-inventory-mission.sh"
test -x "$root/scripts/test-select-command.sh"
test -x "$root/scripts/test-select-agent.sh"
test -x "$root/scripts/test-coordination-ledger.sh"
test -x "$root/scripts/test-run-inventory-mission.sh"
test -x "$root/scripts/test-selection-state.sh"

grep -q '"name": "nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"displayName": "Nelson"' "$root/.codex-plugin/plugin.json"
grep -q '"skills": "./skills/"' "$root/.codex-plugin/plugin.json"
grep -q '"commands": "./commands/"' "$root/.codex-plugin/plugin.json"
grep -q '"agents": "./agents/"' "$root/.codex-plugin/plugin.json"
grep -q '"id": "nelson-coordination"' "$root/.mcp.json"
grep -q '"id": "nelson-coordination"' "$root/.app.json"

bash "$root/scripts/validate-mapping.sh" >/dev/null
bash "$root/scripts/package-context.sh" | grep -q '"mission_scenarios": 6'
bash "$root/scripts/test-select-command.sh" >/dev/null
bash "$root/scripts/test-select-agent.sh" >/dev/null
bash "$root/scripts/test-coordination-ledger.sh" >/dev/null
bash "$root/scripts/test-run-inventory-mission.sh" >/dev/null
bash "$root/scripts/test-selection-state.sh" >/dev/null
bash "$root/scripts/nelson-coordination-mcp.sh" | grep -q '"name": "nelson"'
bash "$root/scripts/run-mission-scenarios.sh" >/dev/null
bash "$root/scripts/validate-mission-scenarios.sh" >/dev/null

printf 'nelson-package:ok\n'
