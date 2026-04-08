---
name: eval-driven-improvement
description: Improve behaviors by measurable eval loops and regression checks.
---

# eval-driven-improvement

## When to use
- recurring workflow tuning
- quality regressions

## Inputs
- `workflow_id`
- `baseline_metrics`
- `candidate_change`

## Outputs
- `score_delta`
- `pass_fail`
- `rollback_or_promote`

## Tool dependencies
- `hooks/_internal/postrun-metrics`
- `hooks/_internal/regression-guard`

## Stop conditions
- candidate outperforms baseline under thresholds
- regression threshold exceeded

## Instructions
- define pass metrics before changes
- compare against rolling baseline, not anecdotes
- reject candidate if regressions exceed threshold
