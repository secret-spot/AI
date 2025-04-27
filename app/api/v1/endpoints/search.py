# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import get_geocodingAPI
import requests

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Geocoding API URL
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

def is_location(query):
    # API 요청 파라미터
    params = {
        'address': query,  # 사용자가 입력한 검색어
        'key': GOOGLE_PLACES_API    # API 키
    }
    
    # 요청 보내기
    response = requests.get(geocode_url, params=params)
    print(response.url)
    data = response.json()
    
    # 검색 결과가 있으면 지역명으로 판단
    if 'results' in data and len(data['results']) > 0:
        return True  # 지역명
    else:
        return False  # 결과 없음

@router.get("/")
async def search(prompt: str):
    try:
        isRegion=is_location(prompt)
        print(isRegion)

        return {
            "region": prompt,
            "isRegion": isRegion
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")