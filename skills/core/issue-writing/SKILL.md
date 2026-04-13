---
name: issue-writing
description: Turn backlog items into GitHub Issues with clear titles, summaries, labels, and acceptance criteria.
---

# Issue Writing

## When to use
- a backlog item needs to become a GitHub Issue
- backlog text needs to be normalized before submission
- issue titles, summaries, labels, and acceptance criteria need to be consistent

## Inputs
- `backlog_item`
- `repository`
- `labels`

## Outputs
- `issue_title`
- `issue_body`
- `issue_labels`
- `next_actions`

## Tool dependencies
- `gh`
- GitHub Issues API or `gh issue create`
- `MCP/backlog/backlog.json`

## Stop conditions
- the issue captures one backlog item clearly
- labels and acceptance criteria are explicit
- no GitHub Projects item is created in this version

## Instructions
- preserve the original backlog title as the issue title when possible
- include a short summary, context, and acceptance criteria
- add labels that reflect the item type and priority
- keep the issue body compact and actionable
- do not expand into GitHub Projects or roadmap automation
