import anyio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import models
import re

router = APIRouter()

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

def call_gemini_sync(prompt: str) -> str:
    model_name = "reviewSummary"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("모델 응답 없음")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.post("/")
async def reviewSummary(request: ChatRequest):
    try:
        # Gemini 호출을 별도 쓰레드에서 실행 (FastAPI 비동기 유지)
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, request.prompt)

        summary_match = re.search(r"리뷰요약[:：]\s*(.+)", generated_text, re.DOTALL)
        summary_text = summary_match.group(1).strip() if summary_match else ""

        return {"content": summary_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")