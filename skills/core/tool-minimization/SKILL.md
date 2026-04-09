---
name: tool-minimization
description: Select one primary tool path and avoid unnecessary tool fan-out.
---

# tool-minimization

## When to use
- task involves multiple possible tools
- user asks for token or latency efficiency

## Inputs
- `task_class`
- `intent`
- `confidence`

## Outputs
- `primary_tool`
- `fallback_policy`
- `stop_conditions`

## Tool dependencies
- `MCP/routing.yaml`
- `MCP/budgets/token-budgets.yaml`

## Stop conditions
- primary tool produced sufficient evidence
- budget soft cap reached without progress

## Instructions
- choose one primary tool before any fallback
- use fallback only on failure/insufficient evidence
- avoid parallel dependent calls
