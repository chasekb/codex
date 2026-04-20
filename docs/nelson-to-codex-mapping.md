# Nelson to Codex Mapping

This document maps the Nelson plugin concepts into Codex primitives and defines the package boundary for the conversion.

## Mapping Matrix

| Nelson concept | Codex primitive | Handling |
|---|---|---|
| Workflow orchestration | `workflows/pipelines/*.yaml` | Convert Nelson orchestration steps into explicit Codex pipelines with named stages. |
| Hook behavior | `hooks/_internal/*` | Convert interception, routing, and validation behavior into internal hooks. |
| Skill behavior | `skills/*` | Convert reusable user-facing actions into skills. |
| Rule behavior | `rules/*` | Convert policy and guardrail logic into rules. |
| Plugin boundary | `.codex-plugin/plugin.json` and plugin folder layout | Convert the Nelson package boundary into a Codex plugin manifest plus stable folder structure. |
| Static assets | `assets/` and `scripts/` | Preserve assets and helper scripts as companion files under the plugin root. |
| Mission scenarios | Regression and verification cases | Convert Nelson-level scenarios into explicit validation and test cases. |

## Rejection And Deferral Rules

Some Nelson behaviors may not map one-to-one into Codex primitives. Handle them like this:

- If a behavior is orchestration-only, keep it in workflows.
- If a behavior is policy-only, keep it in rules.
- If a behavior is reusable but not user-facing, keep it in hooks or scripts instead of making it a skill.
- If a behavior depends on Nelson-specific runtime services, mark it as deferred until the Codex equivalent exists.

## Package Boundary

The Codex-native plugin package should separate concerns as follows:

- `workflows/` for explicit sequencing and orchestration
- `hooks/` for runtime interception and adapter logic
- `skills/` for reusable user-facing behaviors
- `rules/` for policy and guardrails
- `assets/` for static resources
- `.codex-plugin/plugin.json` for package metadata and install identity

Suggested top-level layout:

```text
plugins/nelson/
  .codex-plugin/plugin.json
  workflows/
  hooks/
  skills/
  rules/
  assets/
  scripts/
```

## Implementation Notes

- Do not keep a single monolithic Nelson entrypoint if the source plugin combines multiple responsibilities.
- Split Nelson behaviors into Codex primitives that can be tested independently.
- Keep the mapping document as the source of truth for the next package assembly task.

## Follow-Up Task

This mapping is the input for:

- `TASK-20260420-006` - package the conversion and validate mission scenarios

