"""JWT auth and RBAC primitives."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from jose import jwt

from backend.app.core.config import get_settings


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: set[str]


def create_access_token(subject: str, roles: set[str], *, minutes: int = 60) -> str:
    settings = get_settings()
    payload = {
        "sub": subject,
        "roles": sorted(roles),
        "exp": datetime.now(UTC) + timedelta(minutes=minutes),
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def require_role(principal: Principal, role: str) -> None:
    if role not in principal.roles and "admin" not in principal.roles:
        raise PermissionError(f"role required: {role}")
