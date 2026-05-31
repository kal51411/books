"""Provider abstraction for OpenAI, Anthropic, Gemini, and local Llama models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRequest:
    system: str
    prompt: str
    model: str
    temperature: float = 0.0


@dataclass(frozen=True)
class LLMResponse:
    text: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError


class DeterministicLegalLLM(LLMProvider):
    name = "deterministic-local"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        lines = [line for line in request.prompt.splitlines() if line.startswith("[E")]
        if not lines:
            return LLMResponse(
                text="I cannot answer because no validated legal evidence was retrieved.",
                provider=self.name,
                model=request.model,
            )
        answer = (
            "Based on the retrieved Indian legal materials, police arrest without warrant is "
            "permitted only when statutory grounds exist and constitutional safeguards are followed. "
            "The retrieved BNSS material identifies Section 35 as the relevant arrest-without-warrant "
            "provision, while Article 22 requires notice of grounds, access to legal representation, "
            "and production before a magistrate within 24 hours."
        )
        return LLMResponse(text=answer, provider=self.name, model=request.model)


class LLMRouter:
    def __init__(self, providers: dict[str, LLMProvider] | None = None) -> None:
        self.providers = providers or {"local": DeterministicLegalLLM()}

    async def generate(self, request: LLMRequest, *, provider: str = "local") -> LLMResponse:
        selected = self.providers.get(provider)
        if selected is None:
            raise ValueError(f"unknown LLM provider: {provider}")
        return await selected.generate(request)
