# Decision rules

Read this file when classifying a row or ID history.

## Evidence hierarchy

1. Verifiable document, decision, minutes, approved deliverable, evidence link, or operational result.
2. Quantified output with completion date and scope.
3. Completed action naming its output.
4. Narrative status such as reviewing, coordinating, drafting, awaiting, or handing off.
5. Status mark without evidence.

A lower level cannot by itself prove completion when the directive requires a higher-level output.

## Signal classification

### Overdue
Use when `Snapshot > Thời hạn mới nhất` or the source states `Trễ hạn N ngày`.
Include, where available: overdue days, expired forecast, missing deliverable, missing revised date, and unchanged number of snapshots.

### At risk before deadline
Use when time remains but a required intermediate output is absent, the forecast exceeds the deadline, or an unresolved dependency could prevent delivery. State `Còn N ngày`; do not invent a universal threshold.

### Slippage
Use when a deadline or forecast changed, or when the latest forecast is later than the latest deadline. Require reason, approval, impact, and revised plan if absent.

### Unsupported completion
Use when completion is marked but scope is partial, evidence is missing, the item was only handed off, or the reported result does not satisfy the directive's deliverables.

### Missing management information
Distinguish the exact gap: no deadline, no forecast, no progress, no output definition, no accountable unit, no approval level, no evidence, no effective date, or no application result.

### Status conflict
Use when status marks and narrative disagree, different units report materially different states, or the same directive appears with conflicting owners or outcomes.

### Snapshot wording decision

Compare the current snapshot with the immediately preceding snapshot using these material inputs:

- required deliverables;
- progress and evidence;
- completion status;
- deadline and forecast;
- accountable unit and owner;
- dependency or blocking issue;
- approved decision;
- risk implication;
- required management action;
- time-sensitive facts such as overdue or remaining days.

Assign exactly one mode:

1. `rewrite`
   - Use when any non-time material input changes.
   - Rewrite both fields to reflect what is new, what remains, and whether the previous management action is still appropriate.

2. `preserve_core_update_facts`
   - Use when progress, evidence, and required management action remain substantively unchanged, but time-sensitive facts change.
   - Keep the same core conclusion and action.
   - Update dates, overdue days, remaining days, and expired forecasts.
   - State `không có tiến triển thực chất so với kỳ [previous snapshot]` when supported.
   - Do not copy the previous wording verbatim.

3. `identical_allowed`
   - Use only when every material input, including time-sensitive facts, is unchanged.
   - Identical wording is permitted but not required.
   - Do not create cosmetic differences merely to make snapshots look different.

A wording change alone is not substantive progress. A changed day count is a factual change but does not by itself change the core conclusion.

### Closure or tracker transfer
Recommend `giữ mở để làm rõ` unless there is closure evidence or all transfer controls exist: destination, reference ID, accountable unit, transfer date, and reporting route.

### Suspension for another priority
Do not declare it improper without evidence. State that alignment with the directive is unsubstantiated, then request approved scope, impact assessment, resource decision, items continuing or paused, and restart date.

## Human review triggers

Always set `Cần rà soát thủ công = Có` for:

- close, delete, discontinue, archive, or transfer decisions;
- severity or board-report escalation;
- conflicting sources or units;
- fraud, concealment, misconduct, discipline, or personal responsibility;
- insufficient evidence where the conclusion could change a governance decision.
