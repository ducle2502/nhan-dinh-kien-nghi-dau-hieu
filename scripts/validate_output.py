#!/usr/bin/env python3
"""Validate generated oversight columns in CSV form."""
import argparse, csv, json, re, sys
from pathlib import Path

REQUIRED=("Nhận định và kiến nghị","Dấu hiệu")
REVIEW="Cần rà soát thủ công"
RISK=re.compile(r"\b(xóa|xoá|đóng|ngừng theo dõi|chuyển.*theo dõi|gian lận|che giấu|kỷ luật)\b",re.I)
VAGUE=re.compile(r"\b(cần đẩy nhanh|cần quan tâm|sớm xử lý)\b",re.I)
RECOMMENDATION_IN_SIGNAL=re.compile(r"\b(cần|yêu cầu|kiến nghị|đề nghị)\b",re.I)
TRUE={"có","co","yes","true","1"}


def main():
    p=argparse.ArgumentParser(
        description="Validate the two generated Vietnamese oversight fields. JSON summary is written to stdout; diagnostics to stderr.",
        epilog="Example: python scripts/validate_output.py output.csv --report validation.json"
    )
    p.add_argument("input",help="Generated UTF-8 or UTF-8-BOM CSV")
    p.add_argument("--report",help="Optional JSON report file")
    args=p.parse_args(); path=Path(args.input)
    if not path.exists():
        print(f"ERROR input_not_found: {path}",file=sys.stderr); return 3
    with path.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    if not rows:
        print("ERROR empty_input: CSV has no data rows",file=sys.stderr); return 4
    missing=[c for c in REQUIRED if c not in rows[0]]
    if missing:
        print("ERROR missing_columns: "+", ".join(missing),file=sys.stderr); return 5
    issues=[]
    for n,row in enumerate(rows,start=2):
        key=(row.get("ID") or f"row-{n}").strip(); rec=row[REQUIRED[0]].strip(); sig=row[REQUIRED[1]].strip()
        def add(code,message): issues.append({"row":n,"id":key,"code":code,"message":message})
        if not rec: add("blank_recommendation","Required field is blank")
        if not sig: add("blank_signal","Required field is blank")
        if "?" in rec+sig: add("question_mark","Contains a rhetorical or unresolved question")
        if VAGUE.search(rec): add("vague_recommendation","Uses vague action language without an explicit deliverable")
        if RECOMMENDATION_IN_SIGNAL.search(sig): add("recommendation_in_signal","Dấu hiệu appears to contain a recommendation")
        if rec==sig or (len(sig)>30 and sig in rec): add("duplicated_fields","The two fields duplicate content")
        if RISK.search(rec+sig) and row.get(REVIEW,"").strip().lower() not in TRUE: add("missing_human_review","Sensitive closure or allegation term lacks human-review flag")
    result={"status":"pass" if not issues else "fail","rows_checked":len(rows),"error_count":len(issues),"issues":issues}
    text=json.dumps(result,ensure_ascii=False,indent=2)
    print(text)
    if args.report: Path(args.report).write_text(text+"\n",encoding="utf-8")
    for x in issues: print(f"ERROR {x['code']}: row={x['row']} id={x['id']} {x['message']}",file=sys.stderr)
    return 0 if not issues else 2

if __name__=="__main__": raise SystemExit(main())
