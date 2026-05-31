"""Citation enforcement engine."""

from __future__ import annotations

from backend.app.domain.legal import Citation, Evidence
from backend.app.repositories.in_memory import InMemoryLegalRepository


class CitationValidationError(ValueError):
    pass


class CitationValidator:
    def __init__(self, repository: InMemoryLegalRepository) -> None:
        self.repository = repository

    async def validate(self, citations: list[Citation], evidence: list[Evidence]) -> None:
        if not citations:
            raise CitationValidationError("answer rejected: at least one citation is required")
        evidence_keys = {(item.document_id, item.chunk_id, item.paragraph) for item in evidence}
        for citation in citations:
            document = await self.repository.get_document(citation.document_id)
            chunk = await self.repository.get_chunk(citation.chunk_id)
            if document is None or chunk is None:
                raise CitationValidationError(f"answer rejected: missing citation {citation.label}")
            if chunk.document_id != document.id:
                raise CitationValidationError(f"answer rejected: mismatched citation {citation.label}")
            key = (citation.document_id, citation.chunk_id, citation.paragraph)
            if key not in evidence_keys:
                raise CitationValidationError(f"answer rejected: citation not present in evidence {citation.label}")
