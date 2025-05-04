import anyio
from fastapi import APIRouter, HTTPException
import google.generativeai as genai
from app.config import models
import re

router = APIRouter()

def call_gemini_sync(prompt: str) -> str:
    model_name = "etiquette"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("모델 응답 없음")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.get("/")
async def etiquette(prompt: str):
    try:
        if not prompt or not prompt.strip():
            raise HTTPException(status_code=400, detail="입력된 prompt가 없거나 비어 있습니다. 다시 입력해 주세요.")
        
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, prompt)

        etiquette_match = re.search(r"에티켓[:：]\s*(.+)", generated_text, re.DOTALL)
        etiquette_text = etiquette_match.group(1).strip() if etiquette_match else ""

        return {
            "region": prompt,
            "content": etiquette_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")