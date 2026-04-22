#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
scenarios="$root/validation/mission-scenarios.md"

test -f "$scenarios"
test -f "$root/workflows/pipelines/conversion.yaml"
test -f "$root/rules/conversion.rules"
test -d "$root/hooks"
test -d "$root/skills"

grep -q 'A Nelson orchestration path is represented as a Codex workflow\.' "$scenarios"
grep -q 'A Nelson guardrail is represented as a Codex rule\.' "$scenarios"
grep -q 'A reusable Nelson behavior is represented as a Codex skill or hook\.' "$scenarios"
grep -q 'The plugin package can be loaded with the expected manifest and layout\.' "$scenarios"
grep -q 'The converted package supports at least one representative mission end to end\.' "$scenarios"
grep -q 'The package can also run an inventory mission that reports commands, agents, and workflows without using the conversion workflow\.' "$scenarios"

printf 'nelson-mission-scenarios:ok\n'
