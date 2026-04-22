#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

bash "$root/scripts/validate-mapping.sh" >/dev/null
bash "$root/scripts/test-package-context.sh" >/dev/null
bash "$root/scripts/test-session-start.sh" >/dev/null
bash "$root/scripts/test-run-inventory-mission.sh" >/dev/null
bash "$root/scripts/validate-mission-scenarios.sh" >/dev/null

python3 - "$root" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
mapping = json.loads((root / "validation" / "nelson-mapping.json").read_text(encoding="utf-8"))
scenario_count = sum(
    1
    for line in (root / "validation" / "mission-scenarios.md").read_text(encoding="utf-8").splitlines()
    if line.strip().startswith(tuple(str(i) + "." for i in range(1, 10)))
)
print(
    json.dumps(
        {
            "missions": ["nelson-conversion", "nelson-inventory"],
            "status": "passed",
            "mapped_concepts": len(mapping.get("concepts", [])),
            "mission_scenarios": scenario_count,
            "message": "Nelson conversion and inventory missions exercised end to end.",
        },
        indent=2,
        sort_keys=True,
    )
)
PY
