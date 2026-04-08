# Step Library (Reusable Macros)

## inspect
- list target files
- read only relevant sections

## plan
- define objective and success criteria
- map impact surface and phased steps
- define verification before mutation

## skill_select
- choose skill by task class, confidence, and keywords
- fallback to context-compaction when confidence is low

## skill_load
- load metadata-only skill content by default
- cap loaded skill chars per budget

## memory_load
- read top relevant memory records first
- cap memory payload by workflow budget

## patch
- apply minimal change
- avoid unrelated edits

## verify
- run smallest relevant gate
- capture pass/fail summary only

## report
- changed files
- verification evidence
- final status

## memory_commit
- write only verified high-signal facts/decisions
- enforce compact one-line record format
