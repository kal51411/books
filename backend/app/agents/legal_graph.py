"""LangGraph-compatible multi-agent orchestration contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from backend.app.domain.legal import Evidence, LegalAnswer
from backend.app.rag.pipeline import LegalRAGPipeline


@dataclass
class LegalAgentState:
    query: str
    evidence: list[Evidence] = field(default_factory=list)
    answer: LegalAnswer | None = None
    safety_findings: list[str] = field(default_factory=list)


class AgentNode(Protocol):
    async def __call__(self, state: LegalAgentState) -> LegalAgentState: ...


class RetrievalAgent:
    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.pipeline = pipeline

    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        understanding = self.pipeline.query_understanding.understand(state.query)
        state.evidence = await self.pipeline.retriever.retrieve(understanding)
        return state


class LegalResearchAgent:
    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        return state


class CaseLawAgent:
    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        return state


class CitationVerificationAgent:
    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.pipeline = pipeline

    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        if state.answer:
            await self.pipeline.validator.validate(state.answer.citations, state.answer.evidence)
        return state


class SafetyAgent:
    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.pipeline = pipeline

    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        finding = self.pipeline.guard.inspect(state.query)
        state.safety_findings.extend(finding.reasons)
        return state


class FinalAnswerAgent:
    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.pipeline = pipeline

    async def __call__(self, state: LegalAgentState) -> LegalAgentState:
        state.answer = await self.pipeline.answer(state.query)
        return state


class LegalAgentGraph:
    """Small executable graph; production can swap in LangGraph StateGraph wiring."""

    def __init__(self, pipeline: LegalRAGPipeline) -> None:
        self.nodes: list[AgentNode] = [
            SafetyAgent(pipeline),
            RetrievalAgent(pipeline),
            LegalResearchAgent(),
            CaseLawAgent(),
            FinalAnswerAgent(pipeline),
            CitationVerificationAgent(pipeline),
        ]

    async def run(self, query: str) -> LegalAnswer:
        state = LegalAgentState(query=query)
        for node in self.nodes:
            state = await node(state)
        if state.answer is None:
            raise RuntimeError("legal agent graph completed without answer")
        return state.answer
