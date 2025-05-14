# import os
# from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, HTTPException
from app.config import get_geocodingAPI  
from pydantic import BaseModel

router = APIRouter()

# Load environment variables
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("Failed to load the API key.")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

async def get_coordinates(place_name: str):
    params = {
        "address": place_name,
        "key": GOOGLE_PLACES_API,
        "language": "ko"  # Return search results in Korean
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)
        data = response.json()

    if data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    else:
        raise Exception("Could not find the location for the given place.")

# Search for nearby places (POIs) and sort by lowest ratings/reviews
async def get_less_crowded_places(lat: float, lng: float):
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # Radius of 5km
        "type": "tourist_attraction",  # Change to 'restaurant' or others if needed
        "key": GOOGLE_PLACES_API,
        "language": "ko"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(PLACES_URL, params=params)
        data = response.json()

    results = data.get("results", [])

    # Filter only places with at least 1 review
    filtered_results = [
        place for place in results
        if place.get("user_ratings_total", 0) > 0
    ]

    # Sort by number of reviews (ascending) and rating (descending)
    sorted_places = sorted(
        filtered_results,
        key=lambda x: (x.get("user_ratings_total", 0), -x.get("rating", 0))
    )

    # Recommend top 3 places
    recommendations = [
        {
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "rating": place.get("rating"),
            "reviews": place.get("user_ratings_total")
        }
        for place in sorted_places[:3]
    ]

    return recommendations

# Request model
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def recommend_quiet_places(request: ChatRequest):
    try:
        body = request.prompt
        
        lat, lng = await get_coordinates(body)
        places = await get_less_crowded_places(lat, lng)

        return {
            "region": body,
            "recommendations": places
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))