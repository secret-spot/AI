from fastapi import FastAPI
import os
from app.api.v1.routers import api_router

app = FastAPI(
    title="Gemini",
    description="API documentation",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)


app.include_router(api_router, prefix="/api/v1")

# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Hello, world!"}