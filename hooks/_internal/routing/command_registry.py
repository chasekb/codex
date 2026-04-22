#!/usr/bin/env python3
import os
from pathlib import Path

from skill_registry import plugin_entries, tokenize


def parse_registry(path):
    entries = []
    path = Path(path)
    if not path.is_file():
        return entries

    current = None
    in_commands = False
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if stripped == "commands:":
                in_commands = True
                continue
            if not in_commands:
                continue
            if stripped.startswith("- id:"):
                if current:
                    entries.append(current)
                current = {
                    "id": stripped.split(":", 1)[1].strip(),
                    "file": "",
                    "tags": [],
                    "priority": 99,
                    "registry": str(path),
                }
                continue
            if current is None:
                continue
            if stripped.startswith("file:"):
                current["file"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("priority:"):
                try:
                    current["priority"] = int(float(stripped.split(":", 1)[1].strip()))
                except Exception:
                    pass
            elif stripped.startswith("tags:"):
                value = stripped.split(":", 1)[1].strip()
                if value.startswith("[") and value.endswith("]"):
                    current["tags"] = [part.strip().strip("'\"") for part in value[1:-1].split(",") if part.strip()]
        if current:
            entries.append(current)
    return entries


def command_registry_candidates(root=None, code_home=None):
    root = Path(root or Path.cwd())
    code_home = Path(code_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    candidates = [
        root / "commands" / "registry.yaml",
    ]
    for entry in plugin_entries(root=root, code_home=code_home):
        registry = entry.get("commands_registry", "")
        if registry:
            candidates.append(Path(registry))
    return [path for path in candidates if path.is_file()]


def resolve_command_entry(command_id, root=None, code_home=None):
    root = Path(root or Path.cwd())
    code_home = Path(code_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    for registry in command_registry_candidates(root=root, code_home=code_home):
        for entry in parse_registry(registry):
            if entry.get("id") != command_id:
                continue
            command_file = entry.get("file", "")
            if command_file and not os.path.isabs(command_file):
                command_file = str(Path(registry).parent / command_file)
            if command_file and Path(command_file).is_file():
                resolved = dict(entry)
                resolved["file"] = command_file
                resolved["registry"] = str(registry)
                resolved["registry_label"] = "core" if registry == root / "commands" / "registry.yaml" else "plugin:nelson"
                return resolved
    return None


def score_entry(entry, task_class, terms):
    command_id = entry.get("id", "")
    haystack = " ".join([command_id, entry.get("file", ""), " ".join(entry.get("tags", []) or [])]).lower()
    tokens = set(tokenize(haystack))
    score = 0.0

    def token_matches(term, token):
        return token == term or token.startswith(term) or term.startswith(token)

    if task_class and any(token_matches(task_class.lower(), token) for token in tokens):
        score += 2.0
    if terms:
        score += sum(1.0 for term in terms if any(token_matches(term, token) for token in tokens))

    if score <= 0:
        return None

    try:
        score += max(0.0, 1.0 - (float(entry.get("priority", 99)) * 0.05))
    except Exception:
        pass

    return score
