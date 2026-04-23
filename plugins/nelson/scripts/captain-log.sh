#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$root" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
action_path = root / "validation" / "nelson-action-state.json"
log_path = root / "validation" / "nelson-coordination-log.jsonl"

action_state = {}
if action_path.is_file():
    action_state = json.loads(action_path.read_text(encoding="utf-8"))

recent_entries = []
if log_path.is_file():
    for raw in log_path.read_text(encoding="utf-8").splitlines()[-5:]:
        raw = raw.strip()
        if not raw:
            continue
        try:
            recent_entries.append(json.loads(raw))
        except Exception:
            recent_entries.append({"raw": raw})

payload = {
    "workflow": "nelson-captain-log",
    "status": "passed",
    "current_action": action_state.get("current_action", {}),
    "latest_session": action_state.get("session", {}),
    "entry_count": len(recent_entries),
    "recent_entries": recent_entries,
    "message": "Nelson captain's log surface returned current action state and recent coordination history.",
}

print(json.dumps(payload, indent=2, sort_keys=True))
PY
