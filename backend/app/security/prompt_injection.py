"""Prompt-injection and unsafe instruction detection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptInjectionFinding:
    blocked: bool
    reasons: list[str]


class PromptInjectionGuard:
    BLOCKLIST = {
        "ignore previous instructions": "instruction override",
        "reveal system prompt": "system prompt exfiltration",
        "make up an answer": "hallucination request",
        "fabricate citation": "citation fabrication request",
        "developer message": "privileged instruction request",
    }

    def inspect(self, text: str) -> PromptInjectionFinding:
        lowered = text.lower()
        reasons = [reason for phrase, reason in self.BLOCKLIST.items() if phrase in lowered]
        return PromptInjectionFinding(blocked=bool(reasons), reasons=reasons)
