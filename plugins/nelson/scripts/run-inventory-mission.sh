#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

package_context="$(bash "$root/scripts/package-context.sh")"
scenario_count="$(python3 - "$root" <<'PY'
import sys
from pathlib import Path
root = Path(sys.argv[1])
scenarios = root / "validation" / "mission-scenarios.md"
count = 0
for line in scenarios.read_text(encoding="utf-8").splitlines():
    if line.strip().startswith(tuple(str(i) + "." for i in range(1, 10))):
        count += 1
print(count)
PY
)"

python3 - "$package_context" "$scenario_count" <<'PY'
import json
import sys

package_context = json.loads(sys.argv[1])
scenario_count = int(sys.argv[2])
package = package_context.get("package", {})
components = package.get("components", {})

payload = {
    "workflow": "nelson-inventory",
    "status": "passed",
    "mission": "inventory",
    "additionalContext": package_context.get("additionalContext", ""),
    "package": {
        "name": package.get("name"),
        "version": package.get("version"),
        "displayName": package.get("displayName"),
        "commands": package.get("commands", []),
        "agents": package.get("agents", []),
        "components": components,
        "mission_scenarios": scenario_count,
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
PY
