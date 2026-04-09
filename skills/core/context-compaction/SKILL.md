---
name: context-compaction
description: Aggressively reduce context payload while preserving decision-critical evidence.
---

# context-compaction

## When to use
- low confidence routing
- high token pressure

## Inputs
- `context_blocks`
- `keywords`
- `budget`

## Outputs
- `compacted_context`
- `dropped_blocks`

## Tool dependencies
- `hooks/_internal/output/truncate-context`
- `hooks/_internal/memory/load-memory`

## Stop conditions
- compacted context under hard cap
- confidence threshold met

## Instructions
- keep only relevant snippets + local memory hits
- dedupe repeated instructions and logs
- prefer summaries over full dumps
