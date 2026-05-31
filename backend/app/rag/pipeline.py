"""End-to-end legal RAG pipeline with mandatory evidence and citations."""

from __future__ import annotations

from backend.app.domain.legal import Citation, LegalAnswer
from backend.app.rag.citation_validator import CitationValidator
from backend.app.rag.query_understanding import QueryUnderstandingService
from backend.app.rag.retrievers import ContextBuilder, CrossEncoderReranker, HybridRetriever
from backend.app.repositories.in_memory import InMemoryLegalRepository
from backend.app.security.prompt_injection import PromptInjectionGuard
from backend.app.services.llm import LLMRequest, LLMRouter


class LegalRAGPipeline:
    def __init__(self, repository: InMemoryLegalRepository) -> None:
        self.repository = repository
        self.query_understanding = QueryUnderstandingService()
        self.retriever = HybridRetriever(repository)
        self.reranker = CrossEncoderReranker()
        self.context_builder = ContextBuilder()
        self.llm = LLMRouter()
        self.validator = CitationValidator(repository)
        self.guard = PromptInjectionGuard()

    async def answer(self, query: str) -> LegalAnswer:
        finding = self.guard.inspect(query)
        if finding.blocked:
            raise ValueError(f"unsafe prompt rejected: {', '.join(finding.reasons)}")
        understanding = self.query_understanding.understand(query)
        evidence = await self.retriever.retrieve(understanding)
        if not evidence:
            raise ValueError("cannot answer without retrieved legal evidence")
        reranked = await self.reranker.rerank(understanding.rewritten_query, evidence)
        context = self.context_builder.build(reranked)
        response = await self.llm.generate(
            LLMRequest(
                system="You are NyayaGPT. Answer only from evidence and cite every legal claim.",
                prompt=f"Question: {query}\n\nEvidence:\n{context}",
                model="nyayagpt-deterministic",
            )
        )
        citations = [
            Citation(
                document_id=item.document_id,
                chunk_id=item.chunk_id,
                paragraph=item.paragraph,
                label=item.citation or item.title,
                source_url=item.source_url,
            )
            for item in reranked[: min(3, len(reranked))]
        ]
        await self.validator.validate(citations, reranked)
        confidence = min(0.95, 0.55 + sum(item.score for item in reranked[:3]) / 3)
        return LegalAnswer(
            answer=response.text,
            confidence=confidence,
            citations=citations,
            evidence=reranked,
            caveats=["This is legal information, not a substitute for advice from an Indian advocate."],
        )
