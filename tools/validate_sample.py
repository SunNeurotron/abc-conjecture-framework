# tools/validate_sample.py (skeleton)
import csv, subprocess, sys, datetime

SAMPLE = "data/samples/sample_100k.csv"
OUT = "data/validation_results.csv"
GP_COMMAND = "gp"   # path to gp binary

def factor_via_pari(n):
    # ejemplo: gp -q 'factorint(123456789);'
    cmd = [GP_COMMAND, "-q", f"factorint({n})"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

with open(SAMPLE) as fin, open(OUT, "w", newline='') as fout:
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames + ["factor_out","factor_method","validated","date"]
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        c = int(row["c"])
        try:
            fout_str = factor_via_pari(c)
            row["factor_out"] = fout_str
            row["factor_method"] = "PARI/GP"
            row["validated"] = "yes"
        except Exception as e:
            row["factor_out"] = str(e)
            row["factor_method"] = "error"
            row["validated"] = "no"
        row["date"] = datetime.datetime.utcnow().isoformat()
        writer.writerow(row)
print("Validation results written to", OUT)
