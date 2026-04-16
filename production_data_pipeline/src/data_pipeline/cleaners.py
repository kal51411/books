from __future__ import annotations

from datetime import datetime
from typing import Dict, List


def deduplicate_latest(rows: List[Dict]) -> List[Dict]:
    """Keep only the latest signup row for each user_id."""
    by_user: Dict[str, Dict] = {}
    for row in rows:
        existing = by_user.get(row["user_id"])
        if existing is None:
            by_user[row["user_id"]] = row
            continue
        if row["signup_ts"] >= existing["signup_ts"]:
            by_user[row["user_id"]] = row
    return list(by_user.values())


def to_serializable(rows: List[Dict]) -> List[Dict]:
    output: List[Dict] = []
    for row in rows:
        clean = dict(row)
        ts = clean.get("signup_ts")
        if isinstance(ts, datetime):
            clean["signup_ts"] = ts.isoformat()
        output.append(clean)
    return output
