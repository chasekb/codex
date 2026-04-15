---
name: project-backlog-management
description: Manage a canonical backlog of incomplete project recommendations and derived implementation tasks. Use when maintaining, prioritizing, promoting, or closing backlog items, and when backlog state must stay synchronized with implementation progress.
---

# Project Backlog Management

## Use When
- A user asks to maintain a running backlog of recommendations
- A recommendation must be promoted into executable tasks
- An implementation task must be marked complete with commit/verification evidence
- Backlog state needs prioritization, triage, or pruning

## Canonical Store
- Keep backlog state in `MCP/backlog/backlog.json`
- Recommendations and implementation tasks are separate lists in the same canonical store
- Only `hooks/_internal/backlog/backlog-manager` mutates the store
- Preserve or set `project_id` on every item; default new items to `CODEX_BACKLOG_PROJECT` when set, otherwise `global`
- Project-local reads should filter to the active project plus shared `global` items

## Workflow
1. Intake the recommendation from a prompt, note, or learning signal.
2. Triage priority, source, and scope.
3. Promote accepted recommendations into implementation tasks.
4. Close tasks only when committed and verified.
5. Keep the recommendation list open until all derived tasks are closed.
6. Require review evidence before closing the source recommendation.

## Guidance
- Prefer concise, outcome-focused backlog items
- Use stable titles and explicit success criteria
- Do not mix strategic recommendations with executable tasks in one item
- Do not reuse another project's backlog items unless they are explicitly scoped as `global`
- Treat ClawHub as an optional external mirror if `CODEX_CLAWHUB_BACKLOG_SYNC_CMD` is configured
- Use `CODEX_CLAWHUB_BACKLOG_DEST` to control where mirror payloads are staged
- Keep the backlog small enough to review regularly
- Use `project-insights` for backlog health snapshots, aging-item summaries, and WIP pressure checks
- Use `stale-item-review` for keep, defer, or drop decisions on stale recommendations and stale tasks
- Use `issue-writing` for GitHub Issues exports of backlog items
- Treat verification and code review as mandatory inputs for completion and recommendation closeout.
