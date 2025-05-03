import anyio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import models
import re

router = APIRouter()

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

def call_gemini_sync(prompt: str) -> str:
    model_name = "keyword"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("모델 응답 없음")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.post("/")
async def keyword(request: ChatRequest):
    try:
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, request.prompt)

        def parse_output(text: str):
            location_match = re.search(r"장소[:：]\s*([^\n]+)", text)
            companion_match = re.search(r"동행[:：]\s*([^\n]+)", text)
            activity_match = re.search(r"활동[:：]\s*([^\n]+)", text)

            # 장소 파싱
            cities = []
            if location_match:
                city_list = [c.strip() for c in location_match.group(1).split(",")]
                cities = [{"key": "대한민국", "value": city} for city in city_list]

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
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
