# tools/generate_provenance_template.py
import csv

# Input expected: dataset CSV with columns a,b,c,q,rho (or adapt)
INPUT = "data/all_triples_sample.csv"   # if full set too large, use sample
OUTPUT = "data/provenance.csv"

with open(INPUT, newline='') as fin, open(OUTPUT, 'w', newline='') as fout:
    reader = csv.DictReader(fin)
    fieldnames = ["triple_id","a","b","c","q","rho","factor_method","factor_tool","tool_version","date","notes"]
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for i,row in enumerate(reader,1):
        writer.writerow({
            "triple_id": f"{i:06d}",
            "a": row.get("a",""),
            "b": row.get("b",""),
            "c": row.get("c",""),
            "q": row.get("q",""),
            "rho": row.get("rho",""),
            "factor_method": "",      # to be filled: "exact" / "partial" / "heuristic"
            "factor_tool": "",        # e.g., PARI/GP, msieve, yafu, sympy
            "tool_version": "",
            "date": "",
            "notes": ""
        })
print("Wrote", OUTPUT)
