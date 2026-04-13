# Step Library (Reusable Macros)

## inspect
- list target files
- read only relevant sections

## plan
- define objective and success criteria
- map impact surface and phased steps
- define verification before mutation

## skill_select
- choose skill by task class, confidence, and keywords
- consider overlay skills after core runtime skills
- fallback to context-compaction when confidence is low

## skill_load
- load metadata-only skill content by default
- cap loaded skill chars per budget
- record skill source when the selected skill comes from an overlay library

## memory_load
- read top relevant memory records first
- cap memory payload by workflow budget
- keep memory runtime-owned even when skills come from overlay libraries

## patch
- apply minimal change
- avoid unrelated edits

## verify
- run smallest relevant gate
- capture pass/fail summary only

## report
- changed files
- verification evidence
- final status

## debug_deep_dive
- reproduce or inspect the repeating failure
- load systematic-debugging metadata only before any patching
- capture root-cause notes before mutation
- patch minimally after root cause is understood
- verify the same failure path after the change

## memory_commit
- write only verified high-signal facts/decisions
- enforce compact one-line record format

## backlog_load
- read the canonical backlog store first
- surface open recommendations before implementation tasks
- keep recommendation and task lists separate

## backlog_review
- refresh the backlog review cadence and timestamp
- sort open items by priority and age
- flag stale recommendations and WIP pressure
- keep the weekly review report separate from implementation closeout

## skill_maintenance
- review learning context and queued skill candidates
- classify the gap as create, update, discover, install, or runtime policy
- keep reusable behavior in Superpowers and execution policy in Codex
- prefer metadata-only skill loads until the target path is clear

## backlog_triage
- classify items as recommendation, task, or noise
- prioritize by impact, urgency, and dependency
- promote only accepted recommendations

## backlog_promote
- promote accepted recommendations into implementation tasks
- keep the source recommendation open until the derived task closes
- record parent-child linkage explicitly

## task_decompose
- break recommendations into independently verifiable tasks
- keep tasks scoped to one outcome each
- capture explicit success criteria

## backlog_sync
- close tasks with commit and verification evidence
- keep recommendations open until derived tasks close
- mirror to external project surfaces only when configured
- use the ClawHub backlog sync command when present

## review_request
- load requesting-code-review metadata only
- keep review context focused on the current diff and plan
- run review before marking work complete

## branch_finish
- load finishing-a-development-branch metadata only
- verify tests before merge or PR decisions
- present completion options after the work is verified

## worktree_setup
- load using-git-worktrees metadata only
- ensure the workspace is isolated before multi-file implementation
- prefer an existing worktree if one is already present

## parallel_dispatch
- load dispatching-parallel-agents metadata only
- split independent tasks before dispatching subagents
- keep dependent edits in one lane

## subagent_development
- load subagent-driven-development metadata only
- use a fresh subagent per independent task
- require spec review before quality review before closeout
