"""Legal query understanding for Indian law."""

from __future__ import annotations

import re
from datetime import date

from backend.app.domain.legal import Jurisdiction, QueryUnderstanding


class QueryUnderstandingService:
    ACT_ALIASES = {
        "bnss": "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "crpc": "Code of Criminal Procedure, 1973",
        "ipc": "Indian Penal Code, 1860",
        "bns": "Bharatiya Nyaya Sanhita, 2023",
        "constitution": "Constitution of India",
        "aadhaar": "Aadhaar Act and Aadhaar judgments",
    }

    def understand(self, query: str) -> QueryUnderstanding:
        lowered = query.lower()
        intents: list[str] = []
        if any(token in lowered for token in ["arrest", "bail", "warrant", "police"]):
            intents.append("criminal_procedure")
        if any(token in lowered for token in ["case", "judgment", "precedent", "aadhaar"]):
            intents.append("case_law_research")
        if any(token in lowered for token in ["section", "article", "act"]):
            intents.append("statutory_interpretation")
        if not intents:
            intents.append("general_legal_research")

        acts = [name for alias, name in self.ACT_ALIASES.items() if alias in lowered]
        if "arrest" in lowered and "warrant" in lowered and not acts:
            acts.append("Bharatiya Nagarik Suraksha Sanhita, 2023")

        sections = re.findall(r"(?:section|sec\.?|article)\s+([0-9A-Za-z().-]+)", query, re.I)
        temporal_as_of = self._extract_temporal_date(lowered)
        rewritten = " ".join([query, *acts, *sections]).strip()
        return QueryUnderstanding(
            raw_query=query,
            rewritten_query=rewritten,
            legal_intents=intents,
            acts=acts,
            sections=sections,
            jurisdiction=Jurisdiction.UNION,
            temporal_as_of=temporal_as_of,
            needs_case_law="case_law_research" in intents,
            confidence=0.84 if acts or sections else 0.66,
        )

    def _extract_temporal_date(self, lowered: str) -> date | None:
        year_match = re.search(r"\b(19|20)\d{2}\b", lowered)
        if "today" in lowered or "current" in lowered:
            return date.today()
        if year_match:
            return date(int(year_match.group()), 12, 31)
        return None
