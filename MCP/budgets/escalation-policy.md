# Token Escalation Policy

Escalate only when all are true:
1. Primary tool produced insufficient evidence.
2. Output contract cannot be satisfied with current cap.
3. At least one compression attempt already applied.

Escalation limits:
- First escalation: +20% for current step only.
- Second escalation: +20% and require explicit justification field.
- No third escalation; fail fast and request narrower scope.
