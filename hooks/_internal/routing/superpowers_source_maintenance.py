#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "hooks.json").is_file() and (candidate / "skills").is_dir() and (candidate / "rules").is_dir():
            return candidate
    return current


def git(*args: str, cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def configured_superpowers_path(root: Path) -> str:
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return "superpowers"
    rc, out = git("config", "-f", str(gitmodules), "--get", "submodule.superpowers.path", cwd=root)
    if rc == 0:
        path = out.strip()
        if path:
            return path
    return "superpowers"


def superpowers_repo(root: Path) -> Path:
    return root / configured_superpowers_path(root)


def parse_submodule_status(root: Path) -> dict[str, str]:
    rc, out = git("submodule", "status", "--", configured_superpowers_path(root), cwd=root)
    if rc != 0:
        return {"marker": "", "commit": "", "raw": ""}
    line = out.strip().splitlines()[0] if out.strip() else ""
    if not line:
        return {"marker": "", "commit": "", "raw": ""}
    marker = line[:1]
    commit = line[1:41].strip()
    return {"marker": marker, "commit": commit, "raw": line}


def upstream_ref(repo: Path) -> str:
    rc, out = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", cwd=repo)
    return out.strip() if rc == 0 else ""


def ahead_behind(repo: Path, upstream: str) -> tuple[int | None, int | None]:
    if not upstream:
        return None, None
    rc, out = git("rev-list", "--left-right", "--count", f"{upstream}...HEAD", cwd=repo)
    if rc != 0:
        return None, None
    parts = out.strip().split()
    if len(parts) != 2:
        return None, None
    try:
        behind = int(parts[0])
        ahead = int(parts[1])
    except ValueError:
        return None, None
    return ahead, behind


def repo_status(root: Path | None = None) -> dict[str, object]:
    root_path = repo_root(root)
    repo = superpowers_repo(root_path)
    status: dict[str, object] = {
        "status": "blocked",
        "root": str(root_path),
        "superpowers_path": str(repo),
        "initialized": False,
        "detached_head": False,
        "dirty": False,
        "branch": "",
        "head": "",
        "origin": "",
        "upstream": "",
        "ahead": None,
        "behind": None,
        "marker": "",
        "raw_submodule_status": "",
        "blocking_reasons": [],
    }

    if not repo.is_dir():
        status["blocking_reasons"] = ["missing_superpowers_checkout"]
        return status

    status["initialized"] = True

    rc, out = git("branch", "--show-current", cwd=repo)
    branch = out.strip() if rc == 0 else ""
    status["branch"] = branch
    status["detached_head"] = not bool(branch)

    rc, out = git("rev-parse", "HEAD", cwd=repo)
    if rc == 0:
        status["head"] = out.strip()

    rc, out = git("remote", "get-url", "origin", cwd=repo)
    if rc == 0:
        status["origin"] = out.strip()

    rc, out = git("status", "--porcelain", cwd=repo)
    status["dirty"] = bool(out.strip()) if rc == 0 else False

    status["upstream"] = upstream_ref(repo)
    ahead, behind = ahead_behind(repo, status["upstream"])
    status["ahead"] = ahead
    status["behind"] = behind

    submodule = parse_submodule_status(root_path)
    status["marker"] = submodule.get("marker", "")
    status["raw_submodule_status"] = submodule.get("raw", "")

    blocking = []
    if status["detached_head"]:
        blocking.append("detached_head")
    if not status["origin"]:
        blocking.append("missing_origin")
    if status["marker"] in {"-", "U"}:
        blocking.append("submodule_not_ready")
    if not blocking:
        status["status"] = "ready"
    status["blocking_reasons"] = blocking
    return status


def build_plan(root: Path | None = None, commit_message: str = "", parent_message: str = "") -> dict[str, object]:
    status = repo_status(root)
    repo = Path(status["superpowers_path"])
    plan_steps: list[str] = []
    blocking = [reason for reason in status["blocking_reasons"] if reason != "detached_head"]

    if not status["initialized"]:
        return {
            "status": "blocked",
            "ready": False,
            "blocking_reasons": blocking,
            "steps": ["git submodule update --init --recursive superpowers"],
            "status_snapshot": status,
        }

    branch = str(status["branch"] or "")
    if status["detached_head"]:
        plan_steps.append("git -C superpowers switch -c codex/superpowers-maintenance")
        branch = "codex/superpowers-maintenance"

    if status["behind"] and int(status["behind"] or 0) > 0 and not status["dirty"]:
        upstream = str(status["upstream"] or "origin/main")
        plan_steps.append(f"git -C superpowers pull --rebase --autostash {upstream}")

    if status["dirty"]:
        if not commit_message.strip():
            blocking.append("missing_commit_message")
        else:
            plan_steps.append("git -C superpowers add -A")
            plan_steps.append(f'git -C superpowers commit -m "{commit_message.strip()}"')
            plan_steps.append("git -C superpowers push -u origin HEAD")
            parent_message = parent_message.strip() or "chore: bump superpowers submodule"
            plan_steps.append("git add superpowers")
            plan_steps.append(f'git commit -m "{parent_message}"')

    ready = not blocking
    mode = "publish" if status["dirty"] else "sync" if int(status.get("behind") or 0) > 0 else "inspect"
    if blocking:
        mode = "blocked"

    return {
        "status": "ok",
        "ready": ready,
        "mode": mode,
        "branch": branch,
        "blocking_reasons": blocking,
        "steps": plan_steps,
        "status_snapshot": status,
        "publish_branch": branch or "codex/superpowers-maintenance",
    }


def execute_plan(plan: dict[str, object], cwd: Path | None = None) -> dict[str, object]:
    if not plan.get("ready"):
        return {"status": "blocked", "reason": plan.get("blocking_reasons", []), "steps": plan.get("steps", [])}

    steps = []
    for step in plan.get("steps", []):
        proc = subprocess.run(
            ["/bin/bash", "-lc", str(step)],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return {"status": "failed", "step": step, "returncode": proc.returncode, "steps": steps, "output": (proc.stdout or "") + (proc.stderr or "")}
        steps.append(step)
    return {"status": "ok", "steps": steps}


def print_json(payload: dict[str, object]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect and publish Superpowers source-repo updates.")
    parser.add_argument("command", choices=["status", "plan", "publish"])
    parser.add_argument("--root", default="", help="Codex repository root. Defaults to auto-detection from CWD.")
    parser.add_argument("--commit-message", default="", help="Commit message for superpowers changes.")
    parser.add_argument("--parent-message", default="", help="Commit message for the parent Codex submodule pointer.")
    parser.add_argument("--execute", action="store_true", help="Execute publish steps instead of only printing the plan.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else None

    if args.command == "status":
        return print_json(repo_status(root))

    plan = build_plan(root, commit_message=args.commit_message, parent_message=args.parent_message)
    if args.command == "plan":
        return print_json(plan)

    if not args.execute:
        return print_json(plan)

    result = execute_plan(plan, cwd=repo_root(root))
    if result.get("status") == "ok":
        return print_json({"status": "ok", "plan": plan, "result": result})
    return print_json({"status": result.get("status", "failed"), "plan": plan, "result": result})


if __name__ == "__main__":
    raise SystemExit(main())
