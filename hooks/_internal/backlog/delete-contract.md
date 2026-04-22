# Backlog Delete Contract

This document defines the read-only delete contract for the canonical backlog manager.

## Supported targets

- `recommendation`
- `task`

The delete contract only accepts one target id at a time.

## Scope rules

- Project scope may delete only items in the current project.
- Global scope may delete only global items.
- `all` scope is explicit and may target any visible item.
- The command must reject targets that are not visible in the active scope.

## Status rules

- Recommendations must be `open` to be eligible for delete preview.
- Tasks must be `pending` to be eligible for delete preview.
- Closed or completed items are not eligible.

## Audit fields

The delete contract reserves these audit fields for the eventual mutating delete path:

- `actor`
- `project_scope`
- `scope_mode`
- `target_id`
- `target_kind`
- `target_title`
- `target_project_id`
- `target_status`
- `requested_at`
- `reason`
- `result`
- `stats_before`
- `stats_after`

## Accounting invariants

- Deleting a recommendation decrements `open_recommendations` by one.
- Deleting a task decrements `open_tasks` by one.
- Deleting an item never changes `completed_tasks`.
- Counts never drop below zero.

## Failure cases

- `missing_target_id`
- `missing_target`
- `missing_confirmation`
- `kind_mismatch`
- `wrong_project`
- `unsupported_status`

## Contract output

The `delete-contract` preview command returns:

- the contract specification
- the matched target snapshot
- the active scope mode
- the reserved audit payload
- the projected stats after deletion

## Mutating command

The mutating `delete` command uses the same validation rules as `delete-contract`, but it also requires explicit confirmation:

- `confirm: true`
- optional `reason`
- optional `actor`

On success it:

- removes the target item from the canonical store
- recomputes stats through the normal save path
- appends an audit record to `outputs/backlog-delete-audit.jsonl` unless overridden by `CODEX_BACKLOG_DELETE_AUDIT_FILE`
