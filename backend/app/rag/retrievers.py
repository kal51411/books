"""Hybrid retrieval primitives: BM25-style lexical, vector hook, metadata filters, reranking."""

from __future__ import annotations

from backend.app.domain.legal import Evidence, QueryUnderstanding
from backend.app.repositories.in_memory import InMemoryLegalRepository


class HybridRetriever:
    def __init__(self, repository: InMemoryLegalRepository) -> None:
        self.repository = repository

    async def retrieve(self, understanding: QueryUnderstanding, *, top_k: int = 20) -> list[Evidence]:
        filters = {"as_of": understanding.temporal_as_of} if understanding.temporal_as_of else {}
        lexical = await self.repository.search(understanding.rewritten_query, top_k=top_k, filters=filters)
        # Production adapters plug Qdrant vector search and PostgreSQL ts_rank_cd BM25 here.
        return self._deduplicate(lexical)

    def _deduplicate(self, evidence: list[Evidence]) -> list[Evidence]:
        seen = set()
        output: list[Evidence] = []
        for item in evidence:
            key = (item.document_id, item.chunk_id)
            if key in seen:
                continue
            seen.add(key)
            output.append(item)
        return output


class CrossEncoderReranker:
    async def rerank(self, query: str, evidence: list[Evidence]) -> list[Evidence]:
        for item in evidence:
            overlap = len(set(query.lower().split()) & set(item.excerpt.lower().split()))
            item.rerank_score = item.score + overlap / 100
        return sorted(evidence, key=lambda item: item.rerank_score or item.score, reverse=True)


class ContextBuilder:
    def build(self, evidence: list[Evidence], *, max_chunks: int = 12) -> str:
        blocks = []
        for index, item in enumerate(evidence[:max_chunks], start=1):
            blocks.append(
                f"[E{index}] doc={item.document_id} chunk={item.chunk_id} "
                f"section={item.section} paragraph={item.paragraph}: {item.excerpt}"
            )
        return "\n".join(blocks)
