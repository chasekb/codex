# Rules Index & Precedence

Order of application (highest to lowest):
1. `03-no-absolute-right.md`
2. `02-concise.md`
3. `06-token-budgeting.md`
4. `07-verbosity-contract.md`
5. `08-routing-discipline.md`
6. `09-reuse-over-repeat.md`
7. Domain policy rules (`01-core.md`, `04-online.md`, `05-git.md`)

Composition rules:
- Prefer references to shared clauses over duplicated long text.
- Resolve conflicts by choosing lower-token compliant behavior.
- Default output format: structured bullets/checklists.
- Procedural behavior should live in `workflows/*` and `hooks/*`; rules remain policy-first.
