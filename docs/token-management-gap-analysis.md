# Token Management Gap Analysis

This document defines the runtime analysis for pre-prompt and post-prompt token management.

## Purpose

The Codex runtime already emits:

- pre-prompt budget selection and context loading metrics
- post-prompt run metrics
- tuning history and comparison artifacts

This analysis folds those artifacts into one repeatable report so the runtime can show:

- how Nelson and Superpowers are being loaded as learnable skill inputs
- whether pre-prompt context assembly is staying within budget
- whether post-prompt feedback is rich enough to tune the next prompt
- where the pre-prompt and post-prompt token flows diverge

## Inputs

- `outputs/token-metrics.csv`
- `outputs/budget-report.json`
- `outputs/hook-runtime-state.json`
- `MCP/budgets/tuning-policy.yaml`

## Output Artifacts

- `outputs/token-management-gap-analysis.json`
- `outputs/token-management-gap-analysis.md`

## Metric Groups

### Pre-prompt

- `pre_prompt_budget_soft`
- `pre_prompt_budget_hard`
- `pre_prompt_objective_chars`
- `pre_prompt_context_chars`
- `pre_prompt_estimate_scale`
- `pre_prompt_estimate_scale_pct`
- `pre_prompt_est_tokens`
- `pre_prompt_estimate_error_tokens`
- `pre_prompt_estimate_error_rate`
- `pre_prompt_utilization`
- `pre_prompt_margin_tokens`
- `pre_prompt_adjustment_warranted`

### Budget Controller

- `budget_controller_loaded`
- `budget_controller_prompt_scale`
- `budget_controller_memory_scale`
- `budget_controller_learning_scale`
- `budget_controller_failure_scale`
- `budget_controller_playbook_scale`
- `budget_controller_search_scale`
- `budget_controller_skill_scale`
- `budget_controller_estimate_scale`
- `budget_controller_estimate_scale_pct`

### Post-prompt

- `input_tokens`
- `output_tokens`
- `total_tokens`
- `retries`
- `fallbacks`
- `tools`
- `elapsed_ms`
- `status`
- `contract_valid`

### Context Loading

- `memory_loaded`
- `memory_chars`
- `learning_loaded`
- `learning_chars`
- `failure_history_loaded`
- `failure_history_chars`
- `playbook_loaded`
- `playbook_chars`
- `search_hints_loaded`
- `search_hints_chars`
- `skill_id`
- `skill_loaded_chars`
- `skill_fallback`

### Memory and Tuning Side Effects

- `memory_write_count`
- `memory_dedup_count`
- `memory_compact_kept`
- `output_compact_runs`
- `output_compact_removed`
- `output_compact_compacted`
- `output_compact_kept`
- `search_tool_count`
- `search_query_count`
- `search_source_count`
- `search_reuse_hit`
- `search_memory_write_count`
- `external_skill_discovery_runs`
- `external_skill_install_attempts`
- `external_skill_install_successes`
- `external_skill_id`
- `external_skill_source`

## Gap Criteria

- `adjustment_gap`: utilization is high but no adjustment is warranted or applied
- `estimate_gap`: actual input tokens differ materially from the pre-prompt estimate
- `learning_gap`: the run is pressure-heavy but learning/playbook context is not being loaded
- `feedback_gap`: pressure-heavy runs still show retries, fallbacks, or invalid contracts
- `calibration_gap`: estimate error remains high while the controller does not adjust the estimate scale

The generated report also computes per-workflow summaries and coverage for every metric column in the CSV.
