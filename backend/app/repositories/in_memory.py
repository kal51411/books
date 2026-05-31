"""Repository contract and deterministic in-memory implementation for tests/local dev."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from backend.app.domain.legal import Evidence, Jurisdiction, LegalChunk, LegalDocument, SourceType


class InMemoryLegalRepository:
    def __init__(self) -> None:
        self.documents: dict[UUID, LegalDocument] = {}
        self.chunks: dict[UUID, LegalChunk] = {}

    @classmethod
    def with_seed_data(cls) -> InMemoryLegalRepository:
        repo = cls()
        doc = LegalDocument(
            source_type=SourceType.INDIA_CODE,
            title="Bharatiya Nagarik Suraksha Sanhita, 2023 - Arrest without warrant",
            text=(
                "Police powers of arrest without warrant are governed by statutory conditions. "
                "The officer must identify a cognizable offence or other statutory ground, record "
                "reasons where required, and comply with constitutional safeguards."
            ),
            source_url="https://www.indiacode.nic.in/",
            act_name="Bharatiya Nagarik Suraksha Sanhita, 2023",
            section="35",
            jurisdiction=Jurisdiction.UNION,
            effective_date=date(2024, 7, 1),
        )
        repo.add_document(doc)
        repo.add_chunk(
            LegalChunk(
                document_id=doc.id,
                chunk_index=0,
                paragraph=1,
                section="35",
                text=(
                    "Section 35 BNSS addresses arrest without warrant by police officers for "
                    "cognizable offences and listed statutory circumstances, subject to safeguards."
                ),
            )
        )
        const = LegalDocument(
            source_type=SourceType.CONSTITUTION,
            title="Constitution of India - Article 22 safeguards",
            text="Article 22 protects arrested persons through information, counsel, and magistrate production safeguards.",
            source_url="https://www.indiacode.nic.in/handle/123456789/15240",
            act_name="Constitution of India",
            section="Article 22",
            jurisdiction=Jurisdiction.UNION,
            effective_date=date(1950, 1, 26),
        )
        repo.add_document(const)
        repo.add_chunk(
            LegalChunk(
                document_id=const.id,
                chunk_index=0,
                paragraph=1,
                section="Article 22",
                text=(
                    "Article 22 requires that an arrested person be informed of grounds of arrest, "
                    "be allowed legal representation, and be produced before a magistrate within 24 hours."
                ),
            )
        )
        return repo

    def add_document(self, document: LegalDocument) -> None:
        self.documents[document.id] = document

    def add_chunk(self, chunk: LegalChunk) -> None:
        self.chunks[chunk.id] = chunk

    async def get_document(self, document_id: UUID) -> LegalDocument | None:
        return self.documents.get(document_id)

    async def get_chunk(self, chunk_id: UUID) -> LegalChunk | None:
        return self.chunks.get(chunk_id)

    async def search(self, query: str, *, top_k: int = 10, filters: dict | None = None) -> list[Evidence]:
        terms = {term.lower() for term in query.split() if len(term) > 2}
        scored: list[Evidence] = []
        as_of = filters.get("as_of") if filters else None
        for chunk in self.chunks.values():
            doc = self.documents[chunk.document_id]
            if as_of and doc.effective_date and doc.effective_date > as_of:
                continue
            text = f"{doc.title} {chunk.text}".lower()
            overlap = sum(1 for term in terms if term in text)
            if overlap == 0:
                continue
            scored.append(
                Evidence(
                    document_id=doc.id,
                    chunk_id=chunk.id,
                    title=doc.title,
                    excerpt=chunk.text,
                    source_url=doc.source_url,
                    citation=doc.citation or doc.section,
                    section=chunk.section or doc.section,
                    paragraph=chunk.paragraph,
                    score=overlap / max(len(terms), 1),
                    metadata={"source_type": doc.source_type, "act_name": doc.act_name},
                )
            )
        return sorted(scored, key=lambda evidence: evidence.score, reverse=True)[:top_k]
