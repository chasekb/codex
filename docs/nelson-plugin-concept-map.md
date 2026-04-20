# Nelson Plugin Concept Map

This document inventories the conversion dimensions for the Nelson plugin so the Codex-native package work can proceed with explicit boundaries.

## Source Status

No Nelson plugin source tree or manifest is checked into this repository. The inventory below captures the concept categories that must be identified in the Nelson source, plus the Codex equivalents that should receive them.

## Nelson Concepts To Inventory

| Nelson concept | What to extract | Codex equivalent |
|---|---|---|
| Workflow orchestration | Trigger points, sequencing, branching, retries | `workflows/pipelines/*.yaml` |
| Hook behavior | Pre/post execution intercepts, routing, validation, logging | `hooks/_internal/*` |
| Skill behavior | User-facing reusable actions and selectors | `skills/*` |
| Rule behavior | Policy, guardrails, and routing constraints | `rules/*` |
| Plugin boundary | Package entrypoint, install shape, metadata, versioning | `.codex-plugin/plugin.json` and plugin directory layout |
| Asset bundle | Static files, scripts, prompts, templates, icons | `assets/`, `scripts/`, and companion folders |
| Mission scenarios | End-to-end behaviors the plugin must support | Task-specific verification cases and regression tests |

## Codex Conversion Targets

The conversion should map Nelson concepts into these Codex primitives:

- Workflows become pipeline YAML entries under `workflows/pipelines/`.
- Routing and runtime intercepts become hooks under `hooks/_internal/`.
- Reusable behavior modules become skills under `skills/`.
- Policy or governance logic becomes rules under `rules/`.
- Packaging metadata becomes a Codex plugin manifest in `.codex-plugin/plugin.json`.

## Inventory Questions To Answer From The Nelson Source

The following items should be extracted from the Nelson plugin before packaging:

1. Which commands or entrypoints exist today?
2. Which pieces are user-facing behavior versus internal orchestration?
3. Which steps are deterministic and can be represented as workflows?
4. Which controls are policy checks and should become rules?
5. Which reusable behaviors are skills rather than workflows?
6. Which assets must be preserved verbatim during conversion?
7. Which scenarios prove the plugin works after conversion?

## Package Boundary Notes

The Codex-native plugin package should preserve a clear separation between:

- routing/orchestration
- reusable skill logic
- policy/rules
- static assets and templates
- packaging metadata

If the Nelson source combines several of these concerns in one entrypoint, the conversion should split them into the corresponding Codex primitives rather than copying the monolith.

## Verification Notes

This concept map is intentionally reviewable before implementation. It should be used as the input for the next two tasks:

- `TASK-20260420-005` - map Nelson concepts to Codex primitives and package boundary
- `TASK-20260420-006` - package the conversion and validate mission scenarios

