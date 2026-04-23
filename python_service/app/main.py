from fastapi import FastAPI
from app.api.routes import attachment, health

def create_app() -> FastAPI:
    application = FastAPI(
        title="N8N Python Service",
        description="Serviço de processamento de anexos para integração n8n",
        version="0.1.0",
    )
    application.include_router(attachment.router)
    application.include_router(health.router)
    return application

app = create_app()
