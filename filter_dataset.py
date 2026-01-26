import pandas as pd
import re
from pathlib import Path

in_path = Path("training_data/AACDB_dataset_original.txt")
out_path = Path("training_data/AACDB_pdb_codes.txt")
out_unique_path = Path("training_data/AACDB_pdb_codes.txt")

# Read as TSV (tab-delimited). Handle potential weird lines by engine='python'
df = pd.read_csv(in_path, sep="\t", dtype=str, engine="python")

# Extract pdb column
pdb_raw = df["pdb"].astype(str).str.strip().str.upper().tolist()

# Filter to valid 4-char PDB codes (alnum), keep order
pdb_codes = [p for p in pdb_raw if re.fullmatch(r"[A-Z0-9]{4}", p or "")]

# Write all (including repeats)
out_path.write_text("\n".join(pdb_codes) + ("\n" if pdb_codes else ""))

# Unique preserving order
seen = set()
pdb_unique = []
for p in pdb_codes:
    if p not in seen:
        seen.add(p)
        pdb_unique.append(p)
out_unique_path.write_text("\n".join(pdb_unique) + ("\n" if pdb_unique else ""))

# Duplicates summary
from collections import Counter
counts = Counter(pdb_codes)
dups = {k:v for k,v in counts.items() if v>1}
top_dups = sorted(dups.items(), key=lambda x:(-x[1], x[0]))[:20]

summary = {
    "rows_in_file": len(df),
    "pdb_entries_found": len(pdb_raw),
    "valid_pdb_codes": len(pdb_codes),
    "unique_valid_pdb_codes": len(pdb_unique),
    "num_duplicate_codes": len(dups),
    "top_duplicates": top_dups
}
