import pandas as pd
import numpy as np
from datetime import datetime

# ── 1. CONFIGURATION ──────────────────────────────────────────────
INPUT_FILE  = "messy_data.csv"
OUTPUT_FILE = "cleaned_data.xlsx"

# ── 2. LOAD THE DATA ──────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(INPUT_FILE)

# Track changes for summary report
changes = []

original_rows = len(df)
print(f"  ✓ Loaded {original_rows} rows, {len(df.columns)} columns")

# ── 3. CLEAN COLUMN NAMES ─────────────────────────────────────────
print("Cleaning column names...")
original_columns = df.columns.tolist()

df.columns = (
    df.columns
    .str.strip()           # remove leading/trailing spaces
    .str.lower()           # lowercase
    .str.replace(" ", "_") # spaces to underscores
)

for old, new in zip(original_columns, df.columns.tolist()):
    if old.strip().lower().replace(" ", "_") != new:
        changes.append(["Column Rename", old, new, "Standardized column name"])
    elif old != new:
        changes.append(["Column Rename", old, new, "Trimmed whitespace from column name"])

print(f"  ✓ Columns standardized: {df.columns.tolist()}")

# ── 4. TRIM WHITESPACE FROM ALL TEXT CELLS ────────────────────────
print("Trimming whitespace...")
whitespace_count = 0

for col in df.select_dtypes(include="object").columns:
    before = df[col].copy()
    df[col] = df[col].str.strip()
    fixed = (before != df[col]).sum()
    if fixed > 0:
        whitespace_count += fixed
        changes.append(["Whitespace", col, f"{fixed} cells", "Trimmed leading/trailing spaces"])

print(f"  ✓ Trimmed whitespace in {whitespace_count} cells")

# ── 5. STANDARDIZE TEXT CASING ────────────────────────────────────
print("Standardizing text casing...")

text_columns = ["first_name", "last_name", "state"]
for col in text_columns:
    if col in df.columns:
        before = df[col].copy()
        df[col] = df[col].str.title()  # Title Case
        fixed = (before != df[col]).dropna().sum()
        if fixed > 0:
            changes.append(["Casing", col, f"{fixed} cells", "Converted to Title Case"])

print(f"  ✓ Text casing standardized")

# ── 6. REMOVE DUPLICATE ROWS ──────────────────────────────────────
print("Checking for duplicates...")
duplicate_count = df.duplicated().sum()

if duplicate_count > 0:
    df = df.drop_duplicates()
    changes.append(["Duplicates", "All columns", f"{duplicate_count} rows removed", "Exact duplicate rows dropped"])
    print(f"  ✓ Removed {duplicate_count} duplicate rows")
else:
    print("  ✓ No duplicates found")

# ── 7. FIX NUMBERS STORED AS TEXT ────────────────────────────────
print("Converting numeric columns...")

numeric_columns = ["income", "home_value"]
for col in numeric_columns:
    if col in df.columns:
        before_nulls = df[col].isna().sum()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        after_nulls  = df[col].isna().sum()
        new_nulls    = after_nulls - before_nulls

        if new_nulls > 0:
            changes.append(["Numeric Conversion", col,
                           f"{new_nulls} non-numeric values",
                           "Converted to NaN (could not parse as number)"])

print(f"  ✓ Numeric columns converted")

# ── 8. HANDLE MISSING VALUES ──────────────────────────────────────
print("Handling missing values...")
missing_before = df.isna().sum()

for col in df.columns:
    missing = df[col].isna().sum()
    if missing > 0:
        if df[col].dtype in ["float64", "int64"]:
            # Fill numeric nulls with column median
            median_val = df[col].median()
            df[col]    = df[col].fillna(median_val)
            changes.append(["Missing Values", col,
                           f"{missing} nulls filled with median ({median_val:,.0f})",
                           "Numeric null filled with median"])
        else:
            # Fill text nulls with "Unknown"
            df[col] = df[col].fillna("Unknown")
            changes.append(["Missing Values", col,
                           f"{missing} nulls filled with 'Unknown'",
                           "Text null filled with placeholder"])

print(f"  ✓ Missing values handled")

# ── 9. BUILD SUMMARY REPORT ───────────────────────────────────────
summary = pd.DataFrame(changes, columns=["Issue Type", "Column", "Detail", "Action Taken"])

stats = pd.DataFrame([
    ["Original Row Count",  original_rows],
    ["Final Row Count",     len(df)],
    ["Rows Removed",        original_rows - len(df)],
    ["Total Issues Fixed",  len(changes)],
    ["Run Date",            datetime.now().strftime("%Y-%m-%d %H:%M")],
], columns=["Metric", "Value"])

# ── 10. SAVE TO EXCEL WITH MULTIPLE TABS ──────────────────────────
print("Saving output...")

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer,     sheet_name="Cleaned Data",    index=False)
    summary.to_excel(writer, sheet_name="Changes Made",   index=False)
    stats.to_excel(writer,   sheet_name="Summary Stats",  index=False)

print(f"\n✓ Done! Output saved to '{OUTPUT_FILE}'")
print(f"  - Cleaned Data tab:  {len(df)} rows")
print(f"  - Changes Made tab:  {len(changes)} issues fixed")
print(f"\nOpen '{OUTPUT_FILE}' in Excel to review.")