---
name: global-workflow
description: Apply plan/implement/debug/verify routing with evidence-first execution.
---

# global-workflow

## When to use
- request needs workflow selection or execution structure
- confidence is low or scope is ambiguous

## Inputs
- `task_class`
- `intent`
- `confidence`

## Outputs
- `workflow_id`
- `next_steps`
- `verification_plan`

## Tool dependencies
- `MCP/routing.yaml`
- `workflows/index.yaml`
- `workflows/pipelines/*.yaml`

## Stop conditions
- workflow selected with sufficient confidence
- plan includes concrete verification steps

## Instructions
- choose from `plan-only`, `implement-small`, `debug-rca`, `verify`
- route to `plan-only` on low confidence
- keep edits scoped and aligned with existing patterns
- verify highest-signal checks before final report
