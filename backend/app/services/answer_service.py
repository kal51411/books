"""Application service layer for legal answers."""

from backend.app.domain.legal import LegalAnswer
from backend.app.rag.pipeline import LegalRAGPipeline


class AnswerService:
    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.pipeline = pipeline

    async def answer_question(self, query: str) -> LegalAnswer:
        return await self.pipeline.answer(query)
