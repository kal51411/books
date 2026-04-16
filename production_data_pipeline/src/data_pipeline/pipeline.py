from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from .cleaners import deduplicate_latest, to_serializable
from .contracts import validate_columns, validate_contract
from .io_utils import read_csv, write_csv, write_json
from .quality import build_report, issues_to_dicts


class ContractError(RuntimeError):
    pass


def run(raw_path: Path, clean_path: Path, quarantine_path: Path, report_path: Path) -> Dict:
    raw_rows = read_csv(raw_path)
    if not raw_rows:
        raise ContractError("Input CSV is empty.")

    missing_columns = validate_columns(list(raw_rows[0].keys()))
    if missing_columns:
        raise ContractError(f"Missing required columns: {', '.join(missing_columns)}")

    clean_rows: List[Dict] = []
    quarantine_rows: List[Dict] = []
    all_issues = []

    for i, row in enumerate(raw_rows, start=2):
        normalized, issues = validate_contract(row, row_number=i)
        all_issues.extend(issues)
        if issues:
            quarantine_rows.append({**normalized, "issues": ";".join(issue.code for issue in issues)})
        else:
            clean_rows.append(normalized)

    deduped = deduplicate_latest(clean_rows)
    report = build_report(
        total_rows=len(raw_rows),
        clean_rows=len(deduped),
        quarantine_rows=len(quarantine_rows),
        issues=all_issues,
    )

    write_csv(
        clean_path,
        to_serializable(deduped),
        fieldnames=["user_id", "email", "country", "signup_ts", "age", "is_active"],
    )
    write_csv(
        quarantine_path,
        to_serializable(quarantine_rows),
        fieldnames=["user_id", "email", "country", "signup_ts", "age", "is_active", "issues"],
    )
    write_json(report_path, {**report, "quarantine_examples": issues_to_dicts(all_issues[:20])})
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Production-style data cleaning pipeline")
    parser.add_argument("--raw", type=Path, required=True, help="Input raw CSV")
    parser.add_argument("--clean", type=Path, required=True, help="Output clean CSV")
    parser.add_argument("--quarantine", type=Path, required=True, help="Output quarantine CSV")
    parser.add_argument("--report", type=Path, required=True, help="Output JSON report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run(args.raw, args.clean, args.quarantine, args.report)
    print("Pipeline completed:", report)


if __name__ == "__main__":
    main()
