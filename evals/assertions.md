# Output assertions

Grade each eval against observable assertions.

## Common assertions

1. Uses the latest snapshot as current state and prior snapshots only as history.
2. Assigns the correct snapshot wording mode:
   - `rewrite` for material non-time changes;
   - `preserve_core_update_facts` for unchanged substance with changed time facts;
   - `identical_allowed` only when all material inputs remain unchanged.
3. Preserves the distinction between facts in `Dấu hiệu` and actions in `Nhận định và kiến nghị`.
4. Does not infer motive, employee capability, or misconduct.
5. Does not invent dates, owners, approvals, or evidence.
6. Flags closure, deletion, transfer, conflict, escalation, and sensitive allegations for human review.
7. Names a concrete required deliverable rather than using only `cần đẩy nhanh` or similar wording.

## Case-specific assertions

- `overdue-multi-snapshot`: selects `preserve_core_update_facts`, states 50 overdue days, recognizes the August forecast expired, and identifies unchanged progress across two snapshots.
- `unsupported-completion`: treats handoff as not completed and asks for the actual standardized output and approval evidence.
- `closure-transfer-edge`: does not approve deletion and requires closure evidence or destination tracker controls.
