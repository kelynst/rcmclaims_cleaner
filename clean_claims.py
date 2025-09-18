#!/usr/bin/env python3
"""
claims_cleaner.py
- Load claims from CSV or Excel
- Clean:
  * trim whitespace
  * drop fully-empty rows/columns
  * normalize date columns to YYYY-MM-DD
  * drop duplicate rows
- Save to cleaned_<filename>.csv (or --out)
"""

from __future__ import annotations
import argparse
from pathlib import Path
import sys

import pandas as pd


def load_table(path: Path, sheet: str | None = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xls", ".xlsx"}:
        # openpyxl must be installed for .xlsx
        return pd.read_excel(path, sheet_name=sheet)
    elif suffix == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use CSV or XLSX.")


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    # Strip leading/trailing spaces from string cells and column names
    df = df.rename(columns=lambda c: c.strip() if isinstance(c, str) else c)
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


def guess_date_columns(columns: list[str]) -> list[str]:
    """Heuristic: any column whose name contains these tokens."""
    tokens = ("date", "dob", "dos", "dt")
    found = []
    for c in columns:
        name = str(c).lower()
        if any(tok in name for tok in tokens):
            found.append(c)
    return found


def normalize_dates(df: pd.DataFrame, date_cols: list[str] | None) -> pd.DataFrame:
    if date_cols is None or len(date_cols) == 0:
        date_cols = guess_date_columns(list(df.columns))

    for col in date_cols:
        if col in df.columns:
            s = pd.to_datetime(df[col], errors="coerce", utc=False)
            # Keep only date component in ISO format
            df[col] = s.dt.strftime("%Y-%m-%d")
    return df


def clean_claims(
    df: pd.DataFrame, date_cols: list[str] | None = None
) -> tuple[pd.DataFrame, dict]:
    original_shape = df.shape

    df = trim_whitespace(df)
    df = df.dropna(how="all")              # drop fully empty rows
    df = df.dropna(axis=1, how="all")      # drop fully empty columns
    df = normalize_dates(df, date_cols)

    before_dupes = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    after_dupes = len(df)

    stats = {
        "original_rows": original_shape[0],
        "original_cols": original_shape[1],
        "rows_after_dropna": before_dupes,
        "rows_after_dedup": after_dupes,
        "final_cols": df.shape[1],
        "date_cols_used": date_cols or guess_date_columns(list(df.columns)),
    }
    return df, stats


def build_output_path(in_path: Path, out_arg: str | None) -> Path:
    if out_arg:
        return Path(out_arg)
    return in_path.with_name(f"cleaned_{in_path.stem}.csv")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Clean healthcare claims (CSV/XLSX) and write a clean CSV."
    )
    ap.add_argument(
        "input",
        help="Path to CSV or XLSX file (e.g., sample_claims.xlsx or claims.csv)",
    )
    ap.add_argument(
        "--sheet",
        help="Excel sheet name (if using .xlsx).",
        default=None,
    )
    ap.add_argument(
        "--date-cols",
        help="Comma-separated list of date column names to normalize "
             "(e.g., 'DOB,DOS,ServiceDate'). If omitted, columns are guessed.",
        default="",
    )
    ap.add_argument(
        "--out",
        help="Output CSV path. Default: cleaned_<input>.csv",
        default=None,
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    in_path = Path(args.input)

    if not in_path.exists():
        print(f"ERROR: File not found: {in_path}", file=sys.stderr)
        return 1

    date_cols = [c.strip() for c in args.date_cols.split(",") if c.strip()] or None

    try:
        df = load_table(in_path, sheet=args.sheet)
    except Exception as e:
        print(f"ERROR reading file: {e}", file=sys.stderr)
        return 1

    cleaned, stats = clean_claims(df, date_cols=date_cols)

    out_path = build_output_path(in_path, args.out)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned.to_csv(out_path, index=False)
    except Exception as e:
        print(f"ERROR writing output: {e}", file=sys.stderr)
        return 1

    print("✅ Clean complete")
    print(f"• Input:  {in_path}")
    print(f"• Output: {out_path}")
    print(
        f"• Rows: {stats['original_rows']} → "
        f"{stats['rows_after_dropna']} (after empty-row drop) → "
        f"{stats['rows_after_dedup']} (after dedup)"
    )
    print(f"• Cols: {stats['original_cols']} → {stats['final_cols']}")
    print(f"• Date columns normalized: {', '.join(stats['date_cols_used']) or 'None'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())