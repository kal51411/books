"""HTTP API routes."""

import importlib
import importlib.util
from typing import Annotated, Any

if importlib.util.find_spec("fastapi"):
    _fastapi = importlib.import_module("fastapi")
    APIRouter = _fastapi.APIRouter
    Depends = _fastapi.Depends
    HTTPException = _fastapi.HTTPException
else:
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str) -> None:
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)

    class APIRouter:
        def __init__(self, *_: Any, **__: Any) -> None: pass
        def post(self, *_: Any, **__: Any):
            def decorator(func): return func
            return decorator
        def get(self, *_: Any, **__: Any):
            def decorator(func): return func
            return decorator

    def Depends(value): return value

if importlib.util.find_spec("pydantic"):
    _pydantic = importlib.import_module("pydantic")
    BaseModel = _pydantic.BaseModel
    Field = _pydantic.Field
else:
    from backend.app.domain.legal import BaseModel, Field

from backend.app.core.dependencies import get_answer_service
from backend.app.domain.legal import LegalAnswer
from backend.app.services.answer_service import AnswerService

router = APIRouter(prefix="/api/v1", tags=["legal-research"])


class AskRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000)
    mode: str = Field(default="research", pattern="^(research|memo|timeline|comparison)$")


@router.post("/ask", response_model=LegalAnswer)
async def ask(
    request: AskRequest,
    service: Annotated[AnswerService, Depends(get_answer_service)],
) -> LegalAnswer:
    try:
        return await service.answer_question(request.query)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "nyayagpt"}
