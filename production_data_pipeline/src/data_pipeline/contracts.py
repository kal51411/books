from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ValidationIssue:
    row_number: int
    field: str
    code: str
    message: str


REQUIRED_COLUMNS = {
    "user_id",
    "email",
    "country",
    "signup_ts",
    "is_active",
}


COUNTRY_LENGTH = 2


def _parse_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return None


def _parse_iso_ts(value: Any) -> Optional[datetime]:
    text = str(value).strip()
    if not text:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def validate_contract(row: Dict[str, Any], row_number: int) -> Tuple[Dict[str, Any], List[ValidationIssue]]:
    """Validate and coerce one row into a normalized contract shape."""
    issues: List[ValidationIssue] = []

    normalized = {
        "user_id": str(row.get("user_id", "")).strip(),
        "email": str(row.get("email", "")).strip().lower(),
        "country": str(row.get("country", "")).strip().upper(),
        "signup_ts": _parse_iso_ts(row.get("signup_ts")),
        "age": None,
        "is_active": _parse_bool(row.get("is_active")),
    }

    raw_age = row.get("age")
    if raw_age not in (None, ""):
        try:
            normalized["age"] = int(raw_age)
        except (TypeError, ValueError):
            issues.append(
                ValidationIssue(
                    row_number=row_number,
                    field="age",
                    code="invalid_integer",
                    message=f"age must be an integer, got {raw_age!r}",
                )
            )

    if not normalized["user_id"]:
        issues.append(ValidationIssue(row_number, "user_id", "required", "user_id is required"))

    if "@" not in normalized["email"]:
        issues.append(ValidationIssue(row_number, "email", "invalid_email", "email format is invalid"))

    if len(normalized["country"]) != COUNTRY_LENGTH:
        issues.append(
            ValidationIssue(
                row_number,
                "country",
                "invalid_country_code",
                "country must be a 2-letter ISO code",
            )
        )

    if normalized["signup_ts"] is None:
        issues.append(
            ValidationIssue(
                row_number,
                "signup_ts",
                "invalid_datetime",
                "signup_ts must be an ISO datetime",
            )
        )

    if normalized["is_active"] is None:
        issues.append(
            ValidationIssue(
                row_number,
                "is_active",
                "invalid_boolean",
                "is_active must be boolean-like",
            )
        )

    age = normalized["age"]
    if age is not None and not (0 <= age <= 120):
        issues.append(
            ValidationIssue(
                row_number,
                "age",
                "out_of_range",
                "age must be in [0, 120]",
            )
        )

    return normalized, issues


def validate_columns(columns: List[str]) -> List[str]:
    present = {c.strip() for c in columns}
    return sorted(REQUIRED_COLUMNS - present)
