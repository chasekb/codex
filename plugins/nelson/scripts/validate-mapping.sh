#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
mapping="$root/validation/nelson-mapping.json"

test -f "$mapping"

python3 - "$mapping" <<'PY'
import json
import sys
from pathlib import Path

mapping = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
concepts = mapping.get("concepts", [])
boundary = mapping.get("package_boundary", {})

expected = {
    "Workflow orchestration",
    "Hook behavior",
    "Skill behavior",
    "Rule behavior",
    "Plugin boundary",
    "Static assets",
    "Mission scenarios",
}
found = {entry.get("concept") for entry in concepts}

missing = sorted(expected - found)
if missing:
    raise SystemExit(f"missing_concepts={','.join(missing)}")

required_boundary = {"assets", "hooks", "manifest", "rules", "skills", "workflows"}
if set(boundary) != required_boundary:
    raise SystemExit("invalid_package_boundary")

print("nelson-mapping:ok")
PY
