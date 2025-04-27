from fastapi import APIRouter
from app.api.v1.endpoints import keywords
from app.api.v1.endpoints import search
from app.api.v1.endpoints import etiquette
from app.api.v1.endpoints import reviewSummary
from app.api.v1.endpoints import chatbot

api_router = APIRouter()
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])               # 키워드 추출 기능 
api_router.include_router(search.router, prefix="/search", tags=["search"])                     # 검색어 구분 기능
api_router.include_router(etiquette.router, prefix="/etiquette", tags=["etiquette"])            # 에티켓 출력 기능 
api_router.include_router(reviewSummary.router, prefix="/summary", tags=["reviewSummary"])      # 리뷰 요약 기능 
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])                  # 챗봇 기능 