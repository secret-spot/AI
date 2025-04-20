from fastapi import FastAPI
from app.api.v1.routers import api_router

app = FastAPI(
    title="Gemini",
    description="API documentation",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# 라우터 등
app.include_router(api_router, prefix="/api/v1")
