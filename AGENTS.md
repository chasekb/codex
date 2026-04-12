# Global Codex Defaults

Apply these defaults in every project unless repository-local instructions are stricter.

## Primary Global Stack
Use global runtime under `~/.codex` and user skills under `~/.agents/skills`:
- `rules/`
- `~/.agents/skills/`
- `workflows/`
- `hooks/`
- `MCP/`
- `outputs/` (runtime artifacts)

## Integration Boundary
- `~/.codex` is the runtime control plane for routing, memory, budgets, validation, logging, and output contracts.
- Superpowers is a managed skills library that can supply reusable behavior content into the Codex selector.
- Core runtime policy stays in `~/.codex`; reusable skill content may live in Superpowers or other overlay libraries.

## Authority Order
1. Repo-local instructions/config for the active project.
2. `~/.codex/rules/00-index.md` precedence chain.
3. Shared global conventions in this file.

## Required Operating Flow
- Recon -> Plan -> Execute -> Verify -> Report.
- Evidence over assumption.
- Minimal, pattern-consistent edits.
- Validate impacted behavior before completion.

## Routing & Contracts
- Route work per `~/.codex/MCP/routing.yaml` and `~/.codex/workflows/index.yaml`.
- Apply shared output/guard contracts from `~/.codex/workflows/shared/*`.
- Use concise, decision-first responses and respect token budgets.

## Global Skills
Prefer these globally installed skills when applicable:
- `global-runtime`
- `tool-minimization`
- `plan-verify-execute`
- `eval-driven-improvement`
- `context-compaction`
- `global-workflow`
- `global-output`
