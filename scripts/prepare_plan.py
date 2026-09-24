#!/usr/bin/env python3
"""Create a deterministic per-ID analysis plan from a tracking CSV."""
import argparse, csv, json, re, sys
from datetime import datetime
from pathlib import Path

DATE_FORMATS = ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d")


def parse_date(value):
    value=(value or "").strip()
    for fmt in DATE_FORMATS:
        try: return datetime.strptime(value, fmt).date()
        except ValueError: pass
    return None


def truthy(value):
    return (value or "").strip().lower() in {"x","✓","1","true","yes","có","co"}


def norm(value):
    return re.sub(r"\s+", " ", (value or "").strip()).casefold()


def main():
    p=argparse.ArgumentParser(
        description="Build a JSON analysis plan grouped by ID. Data goes to stdout or --output; diagnostics go to stderr.",
        epilog="Example: python scripts/prepare_plan.py tracking.csv --output plan.json"
    )
    p.add_argument("input", help="UTF-8 or UTF-8-BOM CSV input")
    p.add_argument("--output", "-o", help="Write JSON to this file; default is stdout")
    p.add_argument("--latest-only", action="store_true", help="Omit full history rows from the JSON plan")
    args=p.parse_args()
    path=Path(args.input)
    if not path.exists():
        print(f"ERROR input_not_found: {path}", file=sys.stderr); return 3
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows=list(csv.DictReader(f))
    if not rows:
        print("ERROR empty_input: CSV has no data rows", file=sys.stderr); return 4
    required={"Snapshot","ID","Tóm tắt nội dung chỉ đạo","Kết quả/tiến độ đến thời điểm báo cáo"}
    missing=sorted(required-set(rows[0]))
    if missing:
        print("ERROR missing_columns: "+", ".join(missing), file=sys.stderr); return 5
    groups={}
    for idx,row in enumerate(rows,start=2):
        key=(row.get("ID") or "").strip()
        if not key:
            print(f"ERROR blank_id: CSV row {idx}", file=sys.stderr); return 6
        snapshot=parse_date(row.get("Snapshot"))
        if not snapshot:
            print(f"ERROR invalid_snapshot: ID={key} value={row.get('Snapshot')!r}", file=sys.stderr); return 7
        row["_snapshot_iso"]=snapshot.isoformat()
        row["_source_row"]=idx
        groups.setdefault(key,[]).append(row)
    items=[]
    for key,hist in sorted(groups.items()):
        hist.sort(key=lambda r:r["_snapshot_iso"])
        cur=hist[-1]; prev=hist[-2] if len(hist)>1 else None
        statuses=[c for c in ("Hoàn Thành","Thực hiện đúng tiến độ","Chưa hoàn thành") if truthy(cur.get(c))]
        signals=[]
        days=cur.get("Số ngày còn lại","")
        if "trễ hạn" in norm(days) or re.fullmatch(r"-\d+(?:\.0+)?", (days or "").strip()): signals.append("overdue")
        if "không giao thời hạn" in norm(days) or not any((cur.get("Thời hạn mới nhất (Date)"),cur.get("Thời hạn (RAW)"),days)): signals.append("no_deadline")
        if len(statuses)>1: signals.append("status_conflict")
        progress=cur.get("Kết quả/tiến độ đến thời điểm báo cáo","")
        if truthy(cur.get("Hoàn Thành")) and re.search(r"đang |đã chuyển|đề xuất ngừng|chờ ", norm(progress)): signals.append("unsupported_completion")
        same_progress = bool(prev and norm(progress)==norm(prev.get("Kết quả/tiến độ đến thời điểm báo cáo")))
        if same_progress: signals.append("no_substantive_progress")
        diff=(cur.get("Chênh lệch dự kiến so với thời hạn (Ngày)") or "").strip()
        try:
            if float(diff)>0: signals.append("forecast_after_deadline")
        except ValueError: pass
        material_fields = [
            "Tóm tắt nội dung chỉ đạo", "Kết quả/tiến độ đến thời điểm báo cáo",
            "Hoàn Thành", "Thực hiện đúng tiến độ", "Chưa hoàn thành",
            "Thời hạn mới nhất (Date)", "Thời hạn (RAW)",
            "Dự kiến mới nhất (Date)", "Dự kiến thời gian hoàn thành (RAW)",
            "Chịu trách nhiệm (PIC)", "Chịu trách nhiệm", "KHỐI"
        ]
        time_fields = ["Snapshot", "Số ngày còn lại"]
        if prev:
            non_time_changed=[f for f in material_fields if norm(cur.get(f)) != norm(prev.get(f))]
            time_changed=[f for f in time_fields if norm(cur.get(f)) != norm(prev.get(f))]
            if non_time_changed:
                wording_mode="rewrite"
            elif time_changed:
                wording_mode="preserve_core_update_facts"
            else:
                wording_mode="identical_allowed"
        else:
            non_time_changed=[]; time_changed=[]; wording_mode="rewrite"
        item={
            "id":key,
            "latest_snapshot":cur["_snapshot_iso"],
            "snapshot_wording_mode":wording_mode,
            "changed_material_fields":non_time_changed,
            "changed_time_fields":time_changed,
            "snapshot_count":len(hist),
            "source_rows":[r["_source_row"] for r in hist],
            "status_marks":statuses,
            "candidate_signals":sorted(set(signals)),
            "current":{k:v for k,v in cur.items() if not k.startswith("_")}
        }
        if not args.latest_only:
            item["history"]=[{k:v for k,v in r.items() if not k.startswith("_")} for r in hist]
        items.append(item)
    payload={"schema_version":"1.0","row_count":len(rows),"unique_id_count":len(items),"items":items}
    text=json.dumps(payload,ensure_ascii=False,indent=2)
    if args.output:
        Path(args.output).write_text(text+"\n",encoding="utf-8")
        print(json.dumps({"status":"ok","output":args.output,"row_count":len(rows),"unique_id_count":len(items)},ensure_ascii=False))
    else:
        print(text)
    return 0

if __name__=="__main__": raise SystemExit(main())
