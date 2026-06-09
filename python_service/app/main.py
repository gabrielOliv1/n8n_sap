from fastapi import FastAPI

from app.api.routes import attachment, email, health


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Registers all API routers:
    - health: GET /health — liveness probe for Docker healthcheck.
    - attachment: POST /attachmentProcessingService — legacy multipart endpoint (deprecated).
    - email: POST /emailProcessingService — n8n JSON array processing (M2).

    Returns:
        Configured FastAPI application instance.
    """
    application = FastAPI(
        title="N8N Python Service",
        description="Serviço de processamento de anexos para integração n8n",
        version="0.4.0",
    )
    application.include_router(health.router)
    application.include_router(attachment.router)
    application.include_router(email.router)
    return application


app = create_app()
