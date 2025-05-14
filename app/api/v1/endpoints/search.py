# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from app.config import get_geocodingAPI
import httpx
from pydantic import BaseModel

router = APIRouter()

# Load environment variables
# load_dotenv()
# GOOGLE_PLACES_API = os.getenv("GOOGLE_PLACES_API")

GOOGLE_PLACES_API = get_geocodingAPI()

if not GOOGLE_PLACES_API:
    raise Exception("Failed to load the API key.")

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

    # Administrative region
    region_keywords = {
        "administrative_area_level_1",  # Province/Metropolitan city
        "administrative_area_level_2",  # City/County/District
        "locality",                     # City
        "sublocality",                  # Town/Village/Neighborhood
        "country"
    }

    # Point of interest (POI)
    place_keywords = {
        "point_of_interest", "establishment", "premise", "park", "museum"
    }

    isRegion = any(t in types for t in region_keywords)
    isPlace = any(t in types for t in place_keywords)

    return {
        "isRegion": isRegion,
        "isPlace": isPlace
    }

# Request model
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
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")