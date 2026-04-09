---
name: plan-verify-execute
description: Run deterministic plan -> change -> verify loop for reliability.
---

# plan-verify-execute

## When to use
- implementation tasks
- bug fixes

## Inputs
- `objective`
- `constraints`
- `impacted_files`

## Outputs
- `phased_plan`
- `patch_summary`
- `verification_evidence`

## Tool dependencies
- `workflows/pipelines/implement-small.yaml`
- `workflows/pipelines/debug-rca.yaml`

## Stop conditions
- all checks pass and output contract satisfied
- no_progress_after_retry

## Instructions
- keep changes minimal and scoped
- run smallest relevant verification gate first
- report only contract-required fields
