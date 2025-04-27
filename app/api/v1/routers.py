from fastapi import APIRouter
from app.api.v1.endpoints import keywords
from app.api.v1.endpoints import search
from app.api.v1.endpoints import etiquette

api_router = APIRouter()
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(etiquette.router, prefix="/etiquette", tags=["etiquette"])