#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agent_registry import agent_registry_candidates, parse_registry, score_entry
from skill_registry import tokenize


EXTERNAL_AGENT_IDS = {
    "hermes-delegate": "hermes",
    "aider-edit-worker": "aider",
    "openhands-sandbox-worker": "openhands",
    "codex-native-subagent": "codex-native",
}


def infer_source_label(entry: dict[str, str]) -> str:
    source = entry.get("source_label", "")
    if source:
        return source
    return EXTERNAL_AGENT_IDS.get(entry.get("id", ""), "")


def infer_execution_mode(entry: dict[str, str]) -> str:
    mode = entry.get("execution_mode", "")
    if mode:
        return mode
    agent_id = entry.get("id", "")
    if agent_id == "hermes-delegate":
        return "delegate"
    if agent_id == "aider-edit-worker":
        return "edit"
    if agent_id == "openhands-sandbox-worker":
        return "sandbox"
    return "parent-lane"


def classify_task_shape(task_class: str, keywords: str) -> str:
    text = f"{task_class} {keywords}".lower()
    if any(term in text for term in ("sandbox", "openhands", "isolated", "container", "review", "autonomous")):
        return "sandboxed-autonomy"
    if any(term in text for term in ("aider", "git-native", "patch", "commit", "diff", "undo", "refactor", "edit loop")):
        return "small-edit-loop"
    if any(term in text for term in ("hermes", "delegate", "memory", "coordination", "multi-step", "orchestration", "subagent")):
        return "bounded-coordination"
    if any(term in text for term in ("parent lane", "dependent", "shared state", "reuse", "fallback")):
        return "parent-lane"
    return "parent-lane"


def best_registry_entry(task_class: str, keywords: str, workspace_root: Path) -> dict[str, str]:
    code_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    terms = [term for term in tokenize(f"{task_class} {keywords}") if term]
    best = None
    best_score = -1.0
    best_index = 10**6
    for index, registry_path in enumerate(agent_registry_candidates(root=workspace_root, code_home=code_home)):
        for entry in parse_registry(registry_path):
            score = score_entry(entry, task_class, terms)
            if score is None:
                continue
            if score > best_score or (score == best_score and index < best_index):
                best = dict(entry)
                best_score = score
                best_index = index

    if best is None:
        return {}
    best["source_label"] = infer_source_label(best)
    best["execution_mode"] = infer_execution_mode(best)
    return best


def select_external_agent(task_class: str, confidence: str, keywords: str, workspace_root: Path) -> dict[str, object]:
    task_shape = classify_task_shape(task_class, keywords)
    best = best_registry_entry(task_class, keywords, workspace_root)
    registry_label = "core" if best.get("id") else ""

    if not best:
        best = {
            "id": "codex-native-subagent",
            "source_label": "codex-native",
            "execution_mode": "parent-lane",
            "stdout_capture": "true",
            "stderr_capture": "true",
            "result_extraction": "parent_lane_summary",
            "registry_label": "core",
        }

    selected_id = best.get("id", "codex-native-subagent")
    source_label = infer_source_label(best) or "codex-native"
    execution_mode = infer_execution_mode(best)
    stdout_capture = str(best.get("stdout_capture", "true")).lower() == "true"
    stderr_capture = str(best.get("stderr_capture", "true")).lower() == "true"
    result_extraction = best.get("result_extraction", "")

    routing_reason = {
        "hermes-delegate": "bounded coordination and reusable context",
        "aider-edit-worker": "small git-native edit loop",
        "openhands-sandbox-worker": "sandboxed autonomous work",
        "codex-native-subagent": "parent-lane fallback",
    }.get(selected_id, "registry match")

    return {
        "agent_id": selected_id,
        "agent_source_label": source_label,
        "registry_label": registry_label or best.get("registry_label", ""),
        "execution_mode": execution_mode,
        "stdout_capture": stdout_capture,
        "stderr_capture": stderr_capture,
        "result_extraction": result_extraction,
        "task_shape": task_shape,
        "confidence": confidence,
        "routing_reason": routing_reason,
        "source_file": best.get("file", ""),
        "tags": best.get("tags", []),
    }


def main() -> int:
    task_class = sys.argv[1] if len(sys.argv) > 1 else "general"
    confidence = sys.argv[2] if len(sys.argv) > 2 else "1.0"
    keywords = sys.argv[3] if len(sys.argv) > 3 else ""
    workspace_root = Path(sys.argv[4]) if len(sys.argv) > 4 else Path.cwd()

    report = select_external_agent(task_class, confidence, keywords, workspace_root)
    print(json.dumps(report, sort_keys=True))
    print(
        "agent-adapter:selected "
        f"id={report['agent_id']} "
        f"source={report['agent_source_label']} "
        f"mode={report['execution_mode']} "
        f"shape={report['task_shape']} "
        f"confidence={report['confidence']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
