#!/usr/bin/env python3
from __future__ import annotations

import json


class StructuredOutputError(RuntimeError):
    pass


def _parse_first_json_object_text(output: str) -> dict:
    text_output = (output or "").strip()
    if text_output.startswith("{"):
        try:
            parsed = json.loads(text_output)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    buffer = []
    started = False
    depth = 0
    for raw_line in (output or "").splitlines():
        line = raw_line.rstrip("\n")
        if not started and "{" not in line:
            continue
        if not started:
            started = True
        buffer.append(line)
        depth += line.count("{")
        depth -= line.count("}")
        if started and depth <= 0:
            candidate = "\n".join(buffer).strip()
            if candidate.startswith("{"):
                try:
                    parsed = json.loads(candidate)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    pass
            buffer = []
            started = False
            depth = 0
    return {}


def extract_json_object(output) -> dict:
    if isinstance(output, dict):
        return output
    if isinstance(output, str):
        return _parse_first_json_object_text(output)
    return {}


def require_json_object(value, context: str, required_keys=()):
    report = extract_json_object(value)
    if not isinstance(report, dict) or not report:
        raise StructuredOutputError(f"{context}:missing_json_object")
    missing = [str(key) for key in required_keys if str(key) not in report]
    if missing:
        raise StructuredOutputError(f"{context}:missing_keys={','.join(missing)}")
    return report
