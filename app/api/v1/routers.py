from fastapi import APIRouter
from app.api.v1.endpoints import keywords
from app.api.v1.endpoints import search
from app.api.v1.endpoints import etiquette
from app.api.v1.endpoints import reviewSummary
from app.api.v1.endpoints import chatbot

api_router = APIRouter()
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(etiquette.router, prefix="/etiquette", tags=["etiquette"])
api_router.include_router(reviewSummary.router, prefix="/summary", tags=["reviewSummary"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])