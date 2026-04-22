#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="$root/.codex-plugin/plugin.json"
scenario_file="$root/validation/mission-scenarios.md"
mapping_file="$root/validation/nelson-mapping.json"

test -f "$manifest"
test -f "$scenario_file"
test -f "$mapping_file"

python3 - "$root" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
scenario_lines = [
    line.strip()
    for line in (root / "validation" / "mission-scenarios.md").read_text(encoding="utf-8").splitlines()
    if line.strip().startswith(tuple(str(i) + "." for i in range(1, 10)))
]
mapping = json.loads((root / "validation" / "nelson-mapping.json").read_text(encoding="utf-8"))
command_registry = (root / "commands" / "registry.yaml").read_text(encoding="utf-8")
command_ids = []
in_commands = False
for raw in command_registry.splitlines():
    stripped = raw.strip()
    if stripped == "commands:":
        in_commands = True
        continue
    if not in_commands:
        continue
    if stripped.startswith("- id:"):
        command_ids.append(stripped.split(":", 1)[1].strip())

agent_registry = (root / "agents" / "registry.yaml").read_text(encoding="utf-8")
agent_ids = []
in_agents = False
for raw in agent_registry.splitlines():
    stripped = raw.strip()
    if stripped == "agents:":
        in_agents = True
        continue
    if not in_agents:
        continue
    if stripped.startswith("- id:"):
        agent_ids.append(stripped.split(":", 1)[1].strip())

component_counts = {
    "commands": len(command_ids),
    "agents": len(agent_ids),
    "skills": sum(1 for _ in (root / "skills").rglob("SKILL.md")),
    "hooks": sum(1 for _ in (root / "hooks").rglob("*") if _.is_file()),
    "rules": sum(1 for _ in (root / "rules").rglob("*.rules")),
    "workflows": sum(1 for _ in (root / "workflows").rglob("*.yaml")),
    "mapped_concepts": len(mapping.get("concepts", [])),
}

summary = (
    f"{manifest['name']} {manifest['version']} package loaded with "
    f"{component_counts['commands']} command(s), "
    f"{component_counts['agents']} agent(s), "
    f"{component_counts['skills']} skill(s), "
    f"{component_counts['hooks']} hook file(s), "
    f"{component_counts['rules']} rule file(s), and "
    f"{component_counts['workflows']} workflow file(s). "
    f"Mission coverage: {len(scenario_lines)} scenario(s) documented."
)

payload = {
    "additionalContext": summary,
    "package": {
        "name": manifest.get("name"),
        "version": manifest.get("version"),
        "displayName": manifest.get("interface", {}).get("displayName"),
        "components": component_counts,
        "commands": command_ids,
        "agents": agent_ids,
        "mission_scenarios": len(scenario_lines),
        "mapped_concepts": len(mapping.get("concepts", [])),
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
PY
