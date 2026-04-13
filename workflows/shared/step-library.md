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

## memory_commit
- write only verified high-signal facts/decisions
- enforce compact one-line record format

## backlog_load
- read the canonical backlog store first
- surface open recommendations before implementation tasks
- keep recommendation and task lists separate

## backlog_triage
- classify items as recommendation, task, or noise
- prioritize by impact, urgency, and dependency
- promote only accepted recommendations

## backlog_sync
- close tasks with commit and verification evidence
- keep recommendations open until derived tasks close
- mirror to external project surfaces only when configured

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
