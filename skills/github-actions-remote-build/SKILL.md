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
2. Run the matching remote workflow first.
3. Inspect run and job logs with `gh`.
4. Do not duplicate the build locally unless remote execution is unavailable.
