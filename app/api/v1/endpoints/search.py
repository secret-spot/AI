# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from app.config import get_geocodingAPI
import httpx
from pydantic import BaseModel

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Geocoding API URL
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

async def classify_location(query):
    params = {
        'address': query,
        'key': GOOGLE_PLACES_API
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(geocode_url, params=params)
        data = response.json()

    if 'results' not in data or not data['results']:
        return {
            "isRegion": False,
            "isPlace": False
        }
    
    result = data['results'][0]
    types = result.get("types", [])

    # 행정 구역
    region_keywords = {
        "administrative_area_level_1",  # 도/광역시
        "administrative_area_level_2",  # 시/군/구
        "locality",                     # 도시
        "sublocality",                 # 동/읍/면
        "country"
    }

    # 장소(POI)
    place_keywords = {
        "point_of_interest", "establishment", "premise", "park", "museum"
    }

    isRegion = any(t in types for t in region_keywords)
    isPlace = any(t in types for t in place_keywords)

    return {
        "isRegion": isRegion,
        "isPlace": isPlace
    }

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str
    
@router.post("/")
async def search(request: ChatRequest):
    try:
        body = request.prompt
        
        result = await classify_location(body)  

        return {
            "prompt": body,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")