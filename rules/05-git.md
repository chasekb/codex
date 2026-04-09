# Git Commit Policy

## Requirements
- Keep all work in git with explicit, intentional commits.
- Use one commit per document/file change whenever practical.
- Write commit messages that describe the exact file and change intent.
- Avoid mixed-scope commits that bundle unrelated files.

## Commit Message Format
- Subject: `<path>: <what changed>`
- Body (optional): `why`, `impact`, and follow-up notes.

## Examples
- `rules/00-index.md: update precedence after rule renumbering`
- `workflows/pipelines/retro.yaml: add retrospective workflow pipeline`
- `hooks/_internal/routing/select-workflow: route request/retro task classes`
