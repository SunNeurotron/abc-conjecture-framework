#!/usr/bin/env python3
"""
generate_provenance_template.py

Create a provenance CSV template for triples dataset.
Usage:
    python tools/generate_provenance_template.py --input data/all_triples.csv --output data/provenance.csv
If --input is not provided, a small sample is created to demonstrate format.
"""
import csv
import argparse
import os
from datetime import datetime

FIELDNAMES = [
    "triple_id", "a", "b", "c", "q", "rho",
    "factor_method", "factor_tool", "tool_version", "date", "notes"
]

SAMPLE_ROWS = [
    {"a":"2","b":"3","c":"5","q":"1.2","rho":"1"},
    {"a":"3","b":"5","c":"8","q":"1.1","rho":"1"}
]

def generate_template(input_path, output_path, limit=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    if input_path and os.path.exists(input_path):
        with open(input_path, newline='') as fin:
            reader = csv.DictReader(fin)
            for i, r in enumerate(reader, start=1):
                if limit and i > limit:
                    break
                rows.append({
                    "triple_id": f"{i:06d}",
                    "a": r.get("a",""),
                    "b": r.get("b",""),
                    "c": r.get("c",""),
                    "q": r.get("q",""),
                    "rho": r.get("rho",""),
                    "factor_method": "",
                    "factor_tool": "",
                    "tool_version": "",
                    "date": "",
                    "notes": ""
                })
    else:
        # write a small sample template so Jules sees the format
        for i, r in enumerate(SAMPLE_ROWS, start=1):
            rows.append({
                "triple_id": f"{i:06d}",
                "a": r["a"],
                "b": r["b"],
                "c": r["c"],
                "q": r["q"],
                "rho": r["rho"],
                "factor_method": "exact",
                "factor_tool": "PARI/GP",
                "tool_version": "2.15",
                "date": datetime.utcnow().isoformat(),
                "notes": "sample row"
            })

    with open(output_path, "w", newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote provenance template to {output_path} ({len(rows)} rows)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate provenance CSV template.")
    parser.add_argument("--input", "-i", help="Input triples CSV (with columns a,b,c,q,rho).")
    parser.add_argument("--output", "-o", default="data/provenance.csv", help="Output provenance CSV path.")
    parser.add_argument("--limit", "-n", type=int, help="Limit number of rows read from input.")
    args = parser.parse_args()
    generate_template(args.input, args.output, args.limit)
