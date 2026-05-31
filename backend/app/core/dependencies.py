"""Dependency assembly for FastAPI routes."""

from functools import lru_cache

from backend.app.rag.pipeline import LegalRAGPipeline
from backend.app.repositories.in_memory import InMemoryLegalRepository
from backend.app.services.answer_service import AnswerService


@lru_cache
def get_repository() -> InMemoryLegalRepository:
    return InMemoryLegalRepository.with_seed_data()


@lru_cache
def get_rag_pipeline() -> LegalRAGPipeline:
    return LegalRAGPipeline(repository=get_repository())


def get_answer_service() -> AnswerService:
    return AnswerService(pipeline=get_rag_pipeline())
