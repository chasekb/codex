#!/usr/bin/env python3
import os
import re
from pathlib import Path


def tokenize(value):
    if not isinstance(value, str):
        return []
    return [part for part in re.split(r"[^a-z0-9]+", value.lower()) if len(part) > 2]


def find_repo_root(start):
    cur = Path(start).resolve()
    while True:
        if (cur / "hooks.json").is_file() and (cur / "skills").is_dir() and (cur / "rules").is_dir():
            return cur
        if cur.parent == cur:
            raise RuntimeError("repository root not found")
        cur = cur.parent


def _dedupe_paths(paths):
    seen = set()
    ordered = []
    for path in paths:
        if path is None:
            continue
        resolved = Path(path)
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(resolved)
    return ordered


def registry_candidates(root=None, code_home=None, preferred=None):
    root = Path(root or find_repo_root(Path.cwd()))
    code_home = Path(code_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))

    candidates = []
    if preferred:
        candidates.append(preferred)

    env_registry = os.environ.get("CODEX_SKILLS_REGISTRY")
    if env_registry:
        candidates.append(env_registry)

    candidates.extend(
        [
            root / "skills" / "registry.yaml",
            root / "superpowers" / "skills" / "registry.yaml",
            Path(os.environ.get("CODEX_EXTERNAL_SKILLS_REGISTRY", str(code_home / "external-skills" / "registry.yaml"))),
            Path.home() / ".agents" / "skills" / "registry.yaml",
        ]
    )
    return [path for path in _dedupe_paths(candidates) if path.is_file()]


def parse_registry(path):
    entries = []
    path = Path(path)
    if not path.is_file():
        return entries

    current = None
    in_skills = False
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if stripped == "skills:":
                in_skills = True
                continue
            if not in_skills:
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


def registry_label(path, root=None, code_home=None):
    path = Path(path)
    root = Path(root or find_repo_root(Path.cwd()))
    code_home = Path(code_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    if path == root / "skills" / "registry.yaml":
        return "core"
    if path == root / "superpowers" / "skills" / "registry.yaml":
        return "overlay"
    external = Path(os.environ.get("CODEX_EXTERNAL_SKILLS_REGISTRY", str(code_home / "external-skills" / "registry.yaml")))
    if path == external or path == code_home / "external-skills" / "registry.yaml":
        return "external"
    agents_registry = Path.home() / ".agents" / "skills" / "registry.yaml"
    if path == agents_registry:
        return "agents"
    env_registry = os.environ.get("CODEX_SKILLS_REGISTRY")
    if env_registry and path == Path(env_registry):
        return "custom"
    return "custom"


def resolve_skill_entry(skill_id, root=None, code_home=None, preferred=None):
    root = Path(root or find_repo_root(Path.cwd()))
    code_home = Path(code_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    for registry in registry_candidates(root=root, code_home=code_home, preferred=preferred):
        for entry in parse_registry(registry):
            if entry.get("id") != skill_id:
                continue
            skill_file = entry.get("file", "")
            if skill_file and not os.path.isabs(skill_file):
                skill_file = str(Path(registry).parent / skill_file)
            if skill_file and Path(skill_file).is_file():
                resolved = dict(entry)
                resolved["file"] = skill_file
                resolved["registry"] = str(registry)
                resolved["registry_label"] = registry_label(registry, root=root, code_home=code_home)
                return resolved
    return None
