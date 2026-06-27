import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers.document_router import router
from src.api.health import router as health_router
from src.config.settings import Settings
from src.api.routers.chat_router import router as chat_router

def get_settings() -> Settings:
    return Settings()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Enterprise Knowledge Assistant API",
    )

    app.include_router(
        router,
        prefix="/api/documents",
        tags=["Documents"]
    )

    app.include_router(
        chat_router,
        prefix="/api/chat",
        tags=["Chat"]
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/health")

    @app.on_event("startup")
    async def startup_event():
        logging.info("Starting Enterprise Knowledge Assistant...")
        # TODO: initialize database, embeddings, retriever, and other services here.

    @app.on_event("shutdown")
    async def shutdown_event():
        logging.info("Shutting down Enterprise Knowledge Assistant...")
        # TODO: clean up resources here.

    return app


app = create_app()
