---
name: podman-compose-test-runner
description: Use when a repository has a compose test file and you should run tests with podman-compose instead of ad hoc local commands.
---

# Podman Compose Test Runner

## When to use
- The repository contains a dedicated compose file for tests or integration checks.
- The repo uses `podman-compose` for containerized test execution.

## Inputs
- Repo path or checkout.
- Compose test file candidates such as `compose.test.yaml`, `docker-compose.test.yml`, or similar.
- Test service names if the stack has a dedicated test container.

## Outputs
- Compose file used.
- Test command executed.
- Exit status and relevant logs.

## Tool dependencies
- `podman-compose`
- Compose test file in the repository

## Stop conditions
- The compose test stack has run and the outcome is known.
- No matching compose file exists or `podman-compose` is unavailable.

## Instructions
1. Find the test-specific compose file.
2. Validate it with `podman-compose config`.
3. Run the stack with `podman-compose up --build --abort-on-container-exit`.
4. Inspect logs on failure.
