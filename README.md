# nhan-dinh-kien-nghi-dau-hieu v4

Copy `.agents/skills/nhan-dinh-kien-nghi-dau-hieu/` into the project root.

V4 replaces earlier snapshot wording instructions with one definitive three-mode rule:

- `rewrite`
- `preserve_core_update_facts`
- `identical_allowed`

Default batch flow:

```bash
python scripts/prepare_plan.py input.csv --output plan.json
python scripts/validate_output.py output.csv --report validation.json
```
