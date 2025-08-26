#!/usr/bin/env python3
"""
validate_sample.py

Validate factorization results for a sample of triples.
Input: data/samples/sample_100k.csv (or any CSV with 'c' column)
Output: data/validation_results.csv
"""
import csv
import subprocess
import datetime
import argparse
import os

GP_CMD = "gp"   # change to full path if necessary, e.g. /usr/bin/gp

def factor_via_pari(n):
    # use gp's factorint and capture output
    cmd = [GP_CMD, "-q", f"factorint({n});"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"PARI error: {p.stderr.strip()}")
    return p.stdout.strip()

def validate(input_csv, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(input_csv, newline='') as fin, open(output_csv, "w", newline='') as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["factor_out","factor_method","validated","validation_date"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            c = row.get("c")
            try:
                c_int = int(c)
                out = factor_via_pari(c_int)
                row["factor_out"] = out
                row["factor_method"] = "PARI/GP"
                row["validated"] = "yes"
            except Exception as e:
                row["factor_out"] = str(e)
                row["factor_method"] = "error"
                row["validated"] = "no"
            row["validation_date"] = datetime.datetime.utcnow().isoformat()
            writer.writerow(row)
    print(f"Validation complete. Results written to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a sample of triples using PARI/GP.")
    parser.add_argument("--input", "-i", default="data/samples/sample_100k.csv", help="Input sample CSV")
    parser.add_argument("--output", "-o", default="data/validation_results.csv", help="Output CSV")
    args = parser.parse_args()
    validate(args.input, args.output)
