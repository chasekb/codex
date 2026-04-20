#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path


SUPPORTED_ARTIFACT_TYPES = {"hook", "rule", "skill", "workflow"}


def first_text(*values):
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def now_utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def content_hash(payload):
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(data).hexdigest()


def render_template(template, mapping):
    rendered = template
    for key, value in mapping.items():
        rendered = rendered.replace("{" + key + "}", str(value))
    return rendered


def run_command(command, cwd=None):
    proc = subprocess.run(
        ["/bin/bash", "-lc", command],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def normalize_source(payload, artifact_type):
    record = dict(payload)
    record["source_type"] = first_text(payload.get("source"), payload.get("source_type"), "github")
    record["artifact_type"] = first_text(artifact_type, payload.get("artifact_type"), "skill")
    record["name"] = first_text(payload.get("name"), payload.get("id"))
    record["repo"] = first_text(payload.get("repo"), payload.get("repository"))
    record["path"] = first_text(payload.get("path"), payload.get("source_path"))
    record["ref"] = first_text(payload.get("ref"), payload.get("branch"), "main")
    record["origin_ref"] = first_text(
        payload.get("origin_ref"),
        f"{record['repo']}@{record['ref']}:{record['path']}" if record["repo"] and record["path"] else "",
    )
    record["content_hash"] = content_hash(payload)
    record["fetched_at"] = first_text(payload.get("fetched_at"), now_utc())
    record["upstream_version"] = first_text(payload.get("upstream_version"), record["ref"])
    record["baseline_version"] = first_text(payload.get("baseline_version"))
    record["validation_state"] = first_text(payload.get("validation_state"), "pending")
    record["validation_notes"] = list(payload.get("validation_notes") or [])
    return record


def validate_manifest(record):
    missing = []
    for key in ("name", "artifact_type", "origin_ref", "content_hash"):
        if not first_text(record.get(key)):
            missing.append(key)
    if record.get("artifact_type") not in SUPPORTED_ARTIFACT_TYPES:
        return {
            "state": "blocked",
            "notes": [f"unsupported_type:{record.get('artifact_type', '')}"],
        }
    if missing:
        return {
            "state": "blocked",
            "notes": [f"missing:{key}" for key in missing],
        }
    return {"state": "approved", "notes": []}


def provenance_record(record):
    return {
        "name": record.get("name", ""),
        "artifact_type": record.get("artifact_type", ""),
        "source_type": record.get("source_type", ""),
        "origin_ref": record.get("origin_ref", ""),
        "content_hash": record.get("content_hash", ""),
        "fetched_at": record.get("fetched_at", now_utc()),
        "upstream_version": record.get("upstream_version", ""),
        "baseline_version": record.get("baseline_version", ""),
    }


def audit_record(stage, record, notes=None):
    return {
        "stage": stage,
        "name": record.get("name", ""),
        "artifact_type": record.get("artifact_type", ""),
        "source_type": record.get("source_type", ""),
        "origin_ref": record.get("origin_ref", ""),
        "content_hash": record.get("content_hash", ""),
        "validation_state": record.get("validation_state", "pending"),
        "notes": list(notes or []),
        "timestamp": now_utc(),
    }


def sandbox_validate(record):
    sandbox_template = os.environ.get("CODEX_EXTERNAL_ORIGIN_SANDBOX_CMD", "").strip()
    if sandbox_template:
        mapping = {
            "name": record.get("name", ""),
            "artifact_type": record.get("artifact_type", ""),
            "repo": record.get("repo", ""),
            "path": record.get("path", ""),
            "ref": record.get("ref", ""),
            "origin_ref": record.get("origin_ref", ""),
            "content_hash": record.get("content_hash", ""),
        }
        rc, out = run_command(render_template(sandbox_template, mapping))
        if rc == 0:
            return {"state": "approved", "notes": [], "output": out[:2000]}
        return {"state": "blocked", "notes": [f"sandbox_exit:{rc}"], "output": out[:2000]}
    if record.get("artifact_type") in {"hook", "workflow"}:
        return {"state": "blocked", "notes": ["sandbox:command_required"], "output": ""}
    if record.get("validation_state") != "approved":
        return {"state": "blocked", "notes": ["sandbox:requires_approved_manifest"], "output": ""}
    return {"state": "approved", "notes": [], "output": ""}


def detect_drift(current, baseline):
    if not baseline:
        return {"state": "baseline_missing", "notes": []}
    if current.get("content_hash") != baseline.get("content_hash"):
        return {"state": "drifted", "notes": ["content_hash_changed"]}
    return {"state": "unchanged", "notes": []}


def update_check(record, fetch_current):
    latest = fetch_current(record) if callable(fetch_current) else dict(record)
    baseline = None
    baseline_hash = first_text(record.get("baseline_content_hash"), record.get("baseline_hash"))
    if baseline_hash:
        baseline = {"content_hash": baseline_hash}
    drift = detect_drift(latest, baseline)
    return {"state": drift["state"], "latest": latest, "notes": drift["notes"]}


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":"), sort_keys=True), encoding="utf-8")


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, separators=(",", ":"), sort_keys=True) for row in rows) + ("\n" if rows else ""), encoding="utf-8")


def render_intake_markdown(report):
    lines = [
        "# External-Origin Intake",
        "",
        f"Status: {report.get('status', 'unknown')}",
        f"Candidate count: {report.get('candidate_count', 0)}",
        f"Selected: {report.get('selected', {}).get('name', 'none') if report.get('selected') else 'none'}",
        "",
        "## Candidates",
    ]
    for candidate in report.get("candidates", []):
        lines.append(
            f"- `{candidate.get('name', '')}` source={candidate.get('source_type', '')} "
            f"artifact={candidate.get('artifact_type', '')} state={candidate.get('validation_state', '')}"
        )
    return "\n".join(lines) + "\n"


def write_intake_outputs(root, report):
    root = Path(root)
    write_json(root / "outputs" / "external-origin-intake.json", report)
    write_text = root / "outputs" / "external-origin-intake.md"
    write_text.parent.mkdir(parents=True, exist_ok=True)
    write_text.write_text(render_intake_markdown(report), encoding="utf-8")
    write_jsonl(root / "outputs" / "external-origin-provenance.jsonl", report.get("provenance", []))
    write_jsonl(root / "outputs" / "external-origin-validation.jsonl", report.get("validation", []))
    write_jsonl(root / "outputs" / "external-origin-drift.jsonl", report.get("drift", []))
