"""NyayaGPT FastAPI application."""

import importlib
import importlib.util
from typing import Any

if importlib.util.find_spec("fastapi"):
    _fastapi = importlib.import_module("fastapi")
    FastAPI = _fastapi.FastAPI
    CORSMiddleware = importlib.import_module("fastapi.middleware.cors").CORSMiddleware
else:
    class FastAPI:
        def __init__(self, *, title: str, description: str, version: str) -> None:
            self.title = title
            self.description = description
            self.version = version
        def add_middleware(self, *_: Any, **__: Any) -> None:
            return None

        def include_router(self, *_: Any, **__: Any) -> None:
            return None

        def mount(self, *_: Any, **__: Any) -> None:
            return None

    class CORSMiddleware:
        pass

if importlib.util.find_spec("prometheus_client"):
    make_asgi_app = importlib.import_module("prometheus_client").make_asgi_app
else:
    def make_asgi_app(): return object()

from backend.app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="NyayaGPT API",
        description="AI-Powered Indian Legal Research and Assistance Platform",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    app.mount("/metrics", make_asgi_app())
    return app


app = create_app()
