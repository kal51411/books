"""Domain models for traceable Indian legal AI responses."""

from __future__ import annotations

import importlib
import importlib.util
from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

if importlib.util.find_spec("pydantic"):
    _pydantic = importlib.import_module("pydantic")
    BaseModel = _pydantic.BaseModel
    Field = _pydantic.Field
    HttpUrl = _pydantic.HttpUrl
    field_validator = _pydantic.field_validator
else:
    class _Field:
        def __init__(self, default=None, default_factory=None, **_: Any) -> None:
            self.default = default
            self.default_factory = default_factory

    def Field(default=None, default_factory=None, **kwargs: Any):
        return _Field(default=default, default_factory=default_factory, **kwargs)

    HttpUrl = str

    def field_validator(*_: Any, **__: Any):
        def decorator(func):
            return func
        return decorator

    class BaseModel:
        def __init__(self, **data: Any) -> None:
            annotations: dict[str, Any] = {}
            for cls in reversed(type(self).mro()):
                annotations.update(getattr(cls, "__annotations__", {}))
            for name in annotations:
                default = getattr(type(self), name, None)
                if name in data:
                    value = data[name]
                elif isinstance(default, _Field):
                    value = default.default_factory() if default.default_factory else default.default
                elif default is not None:
                    value = default
                else:
                    value = None
                setattr(self, name, value)

        def model_copy(self, *, update: dict[str, Any] | None = None):
            data = dict(self.__dict__)
            if update:
                data.update(update)
            return type(self)(**data)

        def model_dump(self) -> dict[str, Any]:
            return dict(self.__dict__)


class SourceType(StrEnum):
    INDIA_CODE = "india_code"
    SUPREME_COURT = "supreme_court"
    HIGH_COURT = "high_court"
    CONSTITUTION = "constitution"
    RULE = "rule"
    REGULATION = "regulation"
    GAZETTE = "gazette"
    COMMENTARY = "commentary"


class Jurisdiction(StrEnum):
    UNION = "union"
    ANDHRA_PRADESH = "andhra_pradesh"
    DELHI = "delhi"
    KARNATAKA = "karnataka"
    MAHARASHTRA = "maharashtra"
    TAMIL_NADU = "tamil_nadu"
    WEST_BENGAL = "west_bengal"
    UNKNOWN = "unknown"


class LegalDocument(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_type: SourceType
    title: str
    text: str
    source_url: HttpUrl | None = None
    act_name: str | None = None
    section: str | None = None
    subsection: str | None = None
    court: str | None = None
    judges: list[str] = Field(default_factory=list)
    citation: str | None = None
    year: int | None = None
    state: str | None = None
    jurisdiction: Jurisdiction = Jurisdiction.UNKNOWN
    enactment_date: date | None = None
    amendment_date: date | None = None
    effective_date: date | None = None
    repeal_status: str | None = None
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)


class LegalChunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    chunk_index: int
    text: str
    paragraph: int | None = None
    section: str | None = None
    parent_id: UUID | None = None
    embedding: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def text_must_be_grounding_ready(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("legal chunks cannot be empty")
        return value


class Evidence(BaseModel):
    document_id: UUID
    chunk_id: UUID
    title: str
    excerpt: str
    source_url: HttpUrl | None = None
    citation: str | None = None
    section: str | None = None
    paragraph: int | None = None
    score: float = Field(ge=0)
    rerank_score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    document_id: UUID
    chunk_id: UUID
    paragraph: int | None = None
    label: str
    source_url: HttpUrl | None = None


class QueryUnderstanding(BaseModel):
    raw_query: str
    rewritten_query: str
    legal_intents: list[str]
    acts: list[str]
    sections: list[str]
    jurisdiction: Jurisdiction
    temporal_as_of: date | None = None
    needs_case_law: bool = False
    confidence: float = Field(ge=0, le=1)


class LegalAnswer(BaseModel):
    answer: str
    confidence: float = Field(ge=0, le=1)
    citations: list[Citation]
    evidence: list[Evidence]
    caveats: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TimelineEvent(BaseModel):
    date: date
    title: str
    description: str
    citations: list[Citation]
