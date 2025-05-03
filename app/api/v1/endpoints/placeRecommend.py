# import os
# from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, HTTPException
from app.config import get_geocodingAPI  

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("API 키를 불러올 수 없습니다.")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# 입력한 지역 → 위도, 경도 변환
async def get_coordinates(location: str):
    params = {"address": location, "key": GOOGLE_PLACES_API}
    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)
        data = response.json()

    if data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    else:
        raise Exception("위치를 찾을 수 없습니다.")

# 주변 장소(POI) 검색 후 평점/리뷰 수 적은 순 정렬
async def get_less_crowded_places(lat: float, lng: float):
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # 반경 10km
        "type": "tourist_attraction",  # 관광지, 필요 시 restaurant 등 변경 가능
        "key": GOOGLE_PLACES_API
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(PLACES_URL, params=params)
        data = response.json()

    results = data.get("results", [])
    print("검색 위치:", lat, lng)
    print("API 상태:", data.get("status"))
    print("Google Places API 응답 수:", len(results))

    # 평점과 리뷰 수 기준으로 적게 알려진 장소 정렬
    sorted_places = sorted(
        results,
        key=lambda x: (x.get("user_ratings_total", 0), -x.get("rating", 0))
    )

    # 상위 5개만 추천
    recommendations = [
        {
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "rating": place.get("rating"),
            "reviews": place.get("user_ratings_total")
        }
        for place in sorted_places[:5]
    ]

    return recommendations

@router.get("/")
async def recommend_quiet_places(prompt: str):
    try:
        lat, lng = await get_coordinates(prompt)
        places = await get_less_crowded_places(lat, lng)

        return {
            "region": prompt,
            "recommendations": places
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))