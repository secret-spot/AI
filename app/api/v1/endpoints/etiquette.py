import anyio
from fastapi import APIRouter, HTTPException
from app.config import models
from pydantic import BaseModel
import re

router = APIRouter()

def call_gemini_sync(prompt: str) -> str:
    model_name = "etiquette"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("모델 응답 없음")
    return ''.join([part.text for part in response.candidates[0].content.parts])

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def etiquette(request: ChatRequest):
    try:
        body = request.prompt
        
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, body)

        etiquette_match = re.search(r"에티켓[:：]\s*(.+)", generated_text, re.DOTALL)
        etiquette_text = etiquette_match.group(1).strip() if etiquette_match else ""

        return {
            "region": body,
            "content": etiquette_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")