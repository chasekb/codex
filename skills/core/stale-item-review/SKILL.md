---
name: stale-item-review
description: Review overdue backlog recommendations and implementation tasks, then decide whether to keep, defer, or drop them.
---

# Stale Item Review

## When to use
- a backlog item has aged past the review threshold
- stale recommendations or tasks need to be classified
- you need a concise decision on whether to keep, defer, or drop aging work

## Inputs
- `backlog_file`
- `stale_after_days`
- `wip_limit`

## Outputs
- `stale_recommendations`
- `stale_tasks`
- `stale_count`
- `stale_task_count`
- `stale_total_count`
- `next_actions`

## Tool dependencies
- `hooks/_internal/backlog/backlog-manager`
- `MCP/backlog/backlog.json`
- `workflows/shared/step-library.md`

## Stop conditions
- stale recommendations and tasks are separated clearly
- the report identifies what should be kept, deferred, or dropped
- the next action stays within backlog maintenance

## Instructions
- read the canonical backlog review report first
- inspect both recommendations and implementation tasks for age
- keep the recommendation/task distinction explicit in the summary
- prefer defer or drop for stale noise, keep for active work with clear value
- do not expand into runtime metrics or external project flow
