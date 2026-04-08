---
name: github-actions-remote-build
description: Use when a repository has a GitHub Actions workflow for build, CI, test, package, or release and you should run it remotely instead of rebuilding locally.
---

# GitHub Actions Remote Build

## When to use
- The repository has a GitHub Actions workflow for build, CI, test, package, or release work.
- You should prefer remote CI over recreating the build locally.
- The user wants authoritative build/test results from the repo's CI system.

## Inputs
- Repo path or checkout.
- Branch, commit, or PR under test.
- Available workflow files under `.github/workflows/`.

## Outputs
- Workflow name(s) used.
- Run URL or run ID.
- Final status and any failing job names.

## Tool dependencies
- `gh`
- GitHub Actions workflows under `.github/workflows/`

## Stop conditions
- A matching remote workflow has been run and inspected.
- No matching workflow exists or remote execution is unavailable.

## Instructions
1. Inspect `.github/workflows/` for workflows named or triggered as build, ci, test, package, or release.
2. If a matching workflow exists, run it remotely first. If multiple matching workflows exist, run all relevant ones that cover the requested build/test surface.
3. Use `gh workflow list`, `gh workflow view`, `gh workflow run`, `gh run list`, `gh run watch`, and `gh run view` to trigger and inspect runs.
4. Prefer the repository's normal trigger if the workflow is not manually dispatchable.
5. Do not duplicate the build locally unless remote execution is unavailable or the repo lacks a matching workflow.
6. Report the workflow name, run URL or ID, and final result.
