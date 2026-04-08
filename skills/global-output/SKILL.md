---
name: global-output
description: Enforce concise, decision-first output with evidence.
---

# global-output

## When to use
- responding with plans, implementation updates, or verification results
- output needs strict brevity and structure

## Inputs
- `response_type`
- `evidence`
- `changed_files`

## Outputs
- `concise_summary`
- `evidence_block`
- `next_steps`

## Tool dependencies
- `rules/10-token-budgeting.md`
- `rules/11-verbosity-contract.md`
- `workflows/shared/output-contracts.yaml`

## Stop conditions
- response leads with conclusion
- evidence and changed files are included when applicable

## Instructions
- prioritize decision/result before details
- use compact bullets and avoid filler narrative
- keep within verbosity contract targets
- state blockers and residual risk explicitly
