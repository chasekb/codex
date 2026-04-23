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
public_vocabulary = mapping.get("public_vocabulary", {})

expected = {
    "Workflow orchestration",
    "Mission lifecycle",
    "Hook behavior",
    "Skill behavior",
    "Rule behavior",
    "Plugin boundary",
    "Static assets",
    "Mission scenarios",
    "Captain's log surface",
}
found = {entry.get("concept") for entry in concepts}

missing = sorted(expected - found)
if missing:
    raise SystemExit(f"missing_concepts={','.join(missing)}")

required_boundary = {"assets", "hooks", "manifest", "rules", "skills", "workflows"}
if set(boundary) != required_boundary:
    raise SystemExit("invalid_package_boundary")

expected_vocabulary = {
    "sailing orders",
    "battle plan",
    "action station",
    "captain's log",
}
found_vocabulary = set(public_vocabulary)
missing_vocabulary = sorted(expected_vocabulary - found_vocabulary)
if missing_vocabulary:
    raise SystemExit(f"missing_vocabulary={','.join(missing_vocabulary)}")

captain_log = public_vocabulary.get("captain's log", {})
if "commands/captain-log.md" not in captain_log.get("codex_primitive", ""):
    raise SystemExit("captain_log_surface_not_exposed")

print("nelson-mapping:ok")
PY
