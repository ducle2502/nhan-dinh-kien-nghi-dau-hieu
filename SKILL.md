---
name: nhan-dinh-kien-nghi-dau-hieu
description: Use this skill when the user wants to draft, revise, validate, or batch-generate the Vietnamese columns "Nhận định và kiến nghị" and "Dấu hiệu" from a directive, action, project, audit, or management tracking table. Activate for overdue items, weak evidence, questionable completion, unchanged updates across snapshots, shifted deadlines, missing owners or deadlines, proposed closure or migration to another tracker, even if the user only asks to "nhận xét", "nêu dấu hiệu", "soát tiến độ", or "viết lại hai cột". Do not use for general prose editing, employee performance appraisal, or project scheduling without an oversight assessment.
compatibility: Requires Python 3.9+ only when validating CSV output with scripts/validate_output.py.
metadata:
  author: internal-audit
  version: "4.0"
---

# Objective

Produce evidence-bound Vietnamese oversight text for two fields:

- `Dấu hiệu`: observable facts and data-quality signals only.
- `Nhận định và kiến nghị`: the main oversight conclusion followed by a concrete governance action.

Assess the work item and its evidence, never a person's competence, attitude, intent, or performance.

# Default workflow

Use plan, validate, execute for tabular or batch work:

- [ ] **Plan:** Run `python scripts/prepare_plan.py <input.csv> --output plan.json`. Do not draft before the plan succeeds.
- [ ] **Inspect:** Review each ID history in `plan.json`; use `snapshot_wording_mode` to decide whether to preserve the core assessment, rewrite it, or permit identical wording. Treat all script classifications as prompts for analysis, not final conclusions.
- [ ] **Classify:** Read `references/decision-rules.md` when the plan shows overdue, completion, changed dates, missing fields, suspension, closure, deletion, transfer, or conflicts.
- [ ] **Draft:** Split the directive into verifiable deliverables, compare them with evidence, then follow `references/output-standard.md`.
- [ ] **Review gate:** Mark `Cần rà soát thủ công = Có` for closure, deletion, transfer, severity escalation, conflicting sources, sensitive allegations, or materially incomplete evidence.
- [ ] **Validate:** Run `python scripts/validate_output.py <output.csv> --report validation.json`.
- [ ] **Fix and repeat:** If validation exits with code 2, fix every reported issue and rerun. Deliver only after `status` is `pass`.

For a single row supplied directly in chat, perform the same logic without scripts.

# Available scripts

- `scripts/prepare_plan.py`: converts source CSV into a deterministic per-ID JSON plan. Run `python scripts/prepare_plan.py --help` for options.
- `scripts/validate_output.py`: validates final CSV and emits a JSON result. Run `python scripts/validate_output.py --help` for options.

Both scripts are non-interactive, idempotent, and use relative paths from the skill root. Structured data goes to stdout or a requested file; diagnostics go to stderr.

# Non-negotiable rules

- Preserve RAW fields, source file, sheet, row, evidence link, and snapshot history.
- Compare rows by `ID`. Similar wording alone does not prove duplication.
- Do not treat formatting changes or paraphrases as progress.
- Do not accept `X`, `đang thực hiện`, `đang phối hợp`, `đã chuyển`, or `theo tiến độ dự án` as completion evidence.
- Do not invent a deadline, approver, owner, document number, causal explanation, or missing evidence.
- When evidence is absent, say `chưa có bằng chứng trong dữ liệu được cung cấp`.
- Do not recommend deleting a row solely because the reporting unit requests it.
- Do not accuse anyone of concealment, negligence, misconduct, or poor capability without direct evidence and human review.
- If a deadline is absent, require the authorized owner to set and report one. Do not set it yourself.

# Gotchas from the tracking data

- `Snapshot` is the assessment date, not the directive date.
- `Thời hạn (RAW)` is provenance. Use the normalized Date field for calculations when available.
- `Không giao thời hạn` is a governance gap, not proof of lateness.
- `Hoàn Thành = X` can conflict with narrative progress. Narrative deliverables and evidence take precedence over the mark.
- `Dự kiến mới nhất` after `Thời hạn mới nhất` is a slippage signal even when `Số lần thay đổi dự kiến = 0`.
- `Đã phê duyệt ban hành` is insufficient if the required evidence includes document number, effective date, communication, or actual application.
- `Đã chuyển Ban dự án/đơn vị khác thực hiện` is handoff, not completion.
- `Đề xuất ngừng theo dõi` requires closure evidence or the destination tracker, reference ID, accountable unit, transfer date, and reporting route.
- Decide snapshot wording from material assessment inputs, not from a desire for either uniformity or variation:
  - `rewrite`: use when any deliverable, evidence, status, deadline, forecast, owner, dependency, decision, risk implication, or required management action changes.
  - `preserve_core_update_facts`: use when the issue and required action remain the same but time-sensitive facts change. Keep the core conclusion, update dates and day counts, and state the lack of substantive progress where supported.
  - `identical_allowed`: use only when every material input, including time-sensitive facts, is unchanged. Do not rewrite merely for stylistic variation.
- Never copy prior wording verbatim when the overdue or remaining-day count changed, even if progress did not.
- A broad suspension due to Core T24 requires the approved scope, impact assessment, resource decision, and restart date. Do not assume the suspension is authorized.

# Output contract

Default columns:

```text
Snapshot | ID | Nhận định và kiến nghị | Dấu hiệu | Cần rà soát thủ công | Lý do rà soát
```

If the user requests only the original two fields, return only those two fields but still perform the review gate internally.

# Final validation checklist

- [ ] Latest snapshot used as current state.
- [ ] All prior snapshots for the same ID reviewed.
- [ ] Snapshot wording follows exactly one mode: `rewrite`, `preserve_core_update_facts`, or `identical_allowed`.
- [ ] Every number is sourced or reproducible.
- [ ] Directive deliverables were compared with reported outputs.
- [ ] `Dấu hiệu` contains facts only and no recommendation.
- [ ] `Nhận định và kiến nghị` states the main conclusion first.
- [ ] Recommendation identifies role, action, deliverable, and deadline requirement.
- [ ] No unsupported completion, causation, allegation, or personal evaluation.
- [ ] Closure, deletion, transfer, escalation, conflict, and sensitive cases are flagged for human review.
- [ ] The two fields do not repeat the same sentence.
