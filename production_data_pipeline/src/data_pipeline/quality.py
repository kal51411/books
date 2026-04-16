from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Dict, List

from .contracts import ValidationIssue


def summarize_issues(issues: List[ValidationIssue]) -> Dict[str, int]:
    counter = Counter(issue.code for issue in issues)
    return dict(sorted(counter.items()))


def issues_to_dicts(issues: List[ValidationIssue]) -> List[Dict]:
    return [asdict(issue) for issue in issues]


def build_report(total_rows: int, clean_rows: int, quarantine_rows: int, issues: List[ValidationIssue]) -> Dict:
    quarantine_rate = quarantine_rows / total_rows if total_rows else 0.0
    return {
        "rows_in": total_rows,
        "rows_clean": clean_rows,
        "rows_quarantine": quarantine_rows,
        "quarantine_rate": round(quarantine_rate, 4),
        "issue_counts": summarize_issues(issues),
    }
