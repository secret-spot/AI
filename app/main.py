from fastapi import FastAPI
from routes.keywords import router as keyword_router

app = FastAPI(title="Gemini")

# 라우터 등
app.include_router(keyword_router)
