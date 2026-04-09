---
name: global-runtime
description: Enforce the mirrored global Codex stack for routing, workflows, hooks, and memory.
---

# global-runtime

## When to use
- global policy or routing behavior is needed
- task depends on the hook and workflow stack under `~/.codex`

## Inputs
- `intent`
- `task_class`
- `confidence`

## Outputs
- `active_workflow`
- `active_skill`
- `validation_status`

## Tool dependencies
- `MCP/routing.yaml`
- `workflows/index.yaml`
- `hooks/_internal/*`
- `~/.agents/skills/registry.yaml`

## Stop conditions
- preflight passes and required files resolve
- selected skill validates and workflow is identifiable

## Instructions
- execute internal hooks with `~/.codex` as working root
- resolve behavior by `rules/00-index.md` precedence
- route by `MCP/routing.yaml` before ad-hoc execution
- enforce output contracts from `workflows/shared/*`
