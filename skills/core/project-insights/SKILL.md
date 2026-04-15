---
name: project-insights
description: Report backlog health, aging items, WIP, and completion rates from the canonical backlog.
---

# Project Insights

## When to use
- you need a backlog health snapshot
- open recommendations or tasks need a concise health report
- aging items, WIP pressure, or completion rate need to be summarized

## Inputs
- `backlog_file`
- `stale_after_days`
- `wip_limit`

## Outputs
- `scope`
- `open_recommendations`
- `open_tasks`
- `completed_tasks`
- `stale_count`
- `wip_over_limit`
- `next_actions`

## Tool dependencies
- `hooks/_internal/backlog/backlog-manager`
- `MCP/backlog/backlog.json`
- `workflows/shared/step-library.md`

## Stop conditions
- the report names the current backlog health clearly
- stale items and WIP pressure are called out explicitly
- the next action is limited to backlog health, not runtime metrics

## Instructions
- read the canonical backlog report first
- report the selected scope before commentary
- summarize counts before commentary
- sort and surface the oldest open recommendations first
- keep the output focused on backlog state only
- recommend review or triage actions when stale items or WIP pressure exist
