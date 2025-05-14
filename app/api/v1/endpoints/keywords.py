import anyio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import models
import re

router = APIRouter()

# Request
class ChatRequest(BaseModel):
    prompt: str

def call_gemini_sync(prompt: str) -> str:
    model_name = "keyword"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("No Response")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.post("/")
async def keyword(request: ChatRequest):
    try:
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, request.prompt)

        def parse_output(text: str):
            location_match = re.search(r"Location[:：]\s*([^\n]+)", text)
            companion_match = re.search(r"Companion[:：]\s*([^\n]+)", text)
            activity_match = re.search(r"Activity[:：]\s*([^\n]+)", text)

            # 장소 파싱
            cities = []
            if location_match:
                city_list = [c.strip() for c in location_match.group(1).split(",")]
                cities = [{"key": "Korea", "value": city} for city in city_list]

            # 키워드 파싱
            keywords = []
            if companion_match:
                keywords.append(companion_match.group(1).strip())
            if activity_match:
                activities = [a.strip() for a in activity_match.group(1).split(",")]
                keywords.extend(activities)

            return {
                "keywords": keywords,
                "regions": cities
            }

        result = parse_output(generated_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
