---
name: podman-compose-test-runner
description: Use when a repository has a compose test file and you should run tests with podman-compose instead of ad hoc local commands.
---

# Podman Compose Test Runner

## When to use
- The repository contains a dedicated compose file for tests or integration checks.
- The repo uses `podman-compose` for containerized test execution.
- The user wants the test stack run in containers instead of locally.

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
1. Find `compose.test.yaml`, `compose.test.yml`, `docker-compose.test.yaml`, `docker-compose.test.yml`, `compose-test.yaml`, `compose-test.yml`, or the repo's equivalent test compose file.
2. Prefer test-specific compose files over generic `compose.yaml` or `docker-compose.yaml` files.
3. Validate the file first with `podman-compose -f FILE config`.
4. Run the test stack with `podman-compose -f FILE up --build --abort-on-container-exit`.
5. If a dedicated test service is obvious, add `--exit-code-from SERVICE`.
6. On failure, inspect logs with `podman-compose -f FILE logs --no-color`.
7. Tear down with `podman-compose -f FILE down -v`.
8. Fall back to non-container tests only if no test compose file exists or `podman-compose` is unavailable.
