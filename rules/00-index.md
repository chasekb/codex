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
- Shared behavior libraries such as Superpowers may own reusable skill content, but they do not own routing or enforcement policy.
- Use core runtime skills for policy-owned decisions; use Superpowers skills for behavior-shaping tasks and authoring patterns.
- Use `skill-promotion` for reusable skill creation/update; use `skill-maintenance` for external discovery/install.
- The backlog store in `MCP/backlog/backlog.json` is the canonical source of truth; mirrors must not become alternate backlog authorities.
- Separate backlog recommendations from implementation tasks in the canonical store; source recommendations only close after derived tasks are committed, verified, and reviewed.
- Prefer metadata-only skill loads in default runtime paths; request full skill bodies only in workflows that explicitly need them.
