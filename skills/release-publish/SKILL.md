---
name: release-publish
description: Use when preparing, validating, and publishing a release or package version bump with explicit safety checks.
---

# Release Publish

## When to use
- A release, publish, or version-bump task is requested.
- You need to validate the release surface before mutation.

## Inputs
- Repository and target branch/tag.
- Release objective and expected version.
- Publish mechanism, if known.

## Outputs
- Objective.
- Files changed.
- Validation.
- Publish result.
- Rollback note.

## Tool dependencies
- `gh`
- Package manager / release tooling for the repo

## Stop conditions
- The release is validated and either published or deferred.
- The required release surface is missing.

## Instructions
1. Inspect release metadata, workflow files, and changelog state first.
2. Prefer dry-run and validation before publish.
3. Keep mutation steps explicit and limited.
4. Include rollback guidance whenever mutation occurs.
