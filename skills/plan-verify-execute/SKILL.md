---
name: plan-verify-execute
description: Run deterministic plan -> change -> verify loop for reliability.
---

# plan-verify-execute

## When to use
- implementation tasks
- bug fixes

## Inputs
- objective
- constraints
- impacted_files

## Outputs
- phased_plan
- patch_summary
- verification_evidence

## Tool dependencies
- `hooks/_internal/implement-small`
- `hooks/_internal/debug-rca`

## Stop conditions
- all checks pass and output contract satisfied
- no_progress_after_retry

## Instructions
1. Keep changes minimal and scoped.
2. Run the smallest relevant verification gate first.
3. Prefer deterministic edits over exploratory changes.
4. Report only contract-required fields.
