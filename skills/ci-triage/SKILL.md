---
name: ci-triage
description: Use when a GitHub Actions workflow failed and you need to inspect logs, isolate the cause, and choose the next action.
---

# CI Triage

## When to use
- A GitHub Actions workflow failed.
- You need root-cause evidence before changing code.

## Inputs
- Repository, branch, PR, or run ID.
- Failing workflow/job names if known.
- Error logs or links if already available.

## Outputs
- Failure summary.
- Likely cause.
- Evidence.
- Next action.
- Confidence.

## Tool dependencies
- `gh`
- GitHub Actions workflow files under `.github/workflows/`

## Stop conditions
- The likely failure source is identified.
- No matching workflow or logs are available.

## Instructions
1. Inspect the failing workflow, run, and job logs first.
2. Prefer the smallest failing surface over broad retries.
3. Separate infrastructure flake from code regression.
4. Report only the evidence-backed cause and the next concrete action.
