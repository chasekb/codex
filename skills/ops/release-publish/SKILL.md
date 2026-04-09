---
name: release-publish
description: Use when preparing, validating, and publishing a release or package version bump with explicit safety checks.
---

# Release Publish

## When to use
- A release, publish, or version-bump task is requested.
- You need to validate the release surface before mutation.
- The repo has package metadata, changelog, or release workflow files.

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

## Instructions
1. Inspect release metadata, workflow files, and changelog state first.
2. Prefer dry-run and validation before publish.
3. Keep mutation steps explicit and limited.
4. If a publish target exists, verify the artifact or workflow result after dispatch.
5. Include rollback guidance whenever mutation occurs.

## Stop conditions
- The release is validated and either published or deferred.
- The required release surface is missing.
