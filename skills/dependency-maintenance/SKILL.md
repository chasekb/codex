---
name: dependency-maintenance
description: Use when inspecting, planning, or executing dependency updates, audits, and compatibility checks.
---

# Dependency Maintenance

## When to use
- A repo needs package/version inspection or dependency updates.
- You are checking stale, vulnerable, or incompatible dependencies.

## Inputs
- Repository and package ecosystem.
- Update scope or package names if known.
- Lockfile or manifest files.

## Outputs
- Current state.
- Candidate updates.
- Risk assessment.
- Validation plan.
- Status.

## Tool dependencies
- Package-manager inspection tools
- Repo manifests / lockfiles

## Stop conditions
- The update plan is validated or the repo is already current.
- Required manifests or lockfiles are missing.

## Instructions
1. Inspect current versions and lockfiles before proposing updates.
2. Prefer the smallest safe upgrade surface.
3. Record compatibility or migration risks explicitly.
4. Validate after changes and keep the result concise.
