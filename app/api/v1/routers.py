from fastapi import APIRouter
from app.api.v1.endpoints import keywords
from app.api.v1.endpoints import search
from app.api.v1.endpoints import etiquette
from app.api.v1.endpoints import reviewSummary
from app.api.v1.endpoints import recommend
from app.api.v1.endpoints import placeRecommend
from app.api.v1.endpoints import chatbot

api_router = APIRouter()
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])               # Keyword extraction 
api_router.include_router(search.router, prefix="/search", tags=["search"])                     # Location type classification 
api_router.include_router(etiquette.router, prefix="/etiquette", tags=["etiquette"])            # Etiquette generation 
api_router.include_router(reviewSummary.router, prefix="/summary", tags=["reviewSummary"])      # Review summarization 
api_router.include_router(recommend.router, prefix="/recommend", tags=["recommend"])            # Small city recommendation 
api_router.include_router(placeRecommend.router, prefix="/recommend/place", tags=["recommend"]) # Places with fewer reviews but high ratings recommendation 
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])                  # Chatbot 