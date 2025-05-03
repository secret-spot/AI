# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from app.config import get_geocodingAPI
import httpx

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Geocoding API URL
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

async def is_location(query):
    params = {
        'address': query,
        'key': GOOGLE_PLACES_API
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(geocode_url, params=params)
        print(response.url)
        data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return True
    else:
        return False
    
@router.get("/")
async def search(prompt: str):
    try:
        isRegion = await is_location(prompt)  
        print(isRegion)

        return {
            "prompt": prompt,
            "isRegion": isRegion
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")