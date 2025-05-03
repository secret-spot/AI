import anyio
from fastapi import APIRouter, HTTPException
import google.generativeai as genai
from app.config import models
import re

router = APIRouter()

def call_gemini_sync(prompt: str) -> str:
    model_name = "recommend"
    model = models.get(model_name)
    response = model.generate_content(prompt)
    if not response.candidates or not response.candidates[0].content.parts:
        raise Exception("모델 응답 없음")
    return ''.join([part.text for part in response.candidates[0].content.parts])

@router.get("/")
async def recommend(prompt: str):
    try:
        generated_text = await anyio.to_thread.run_sync(call_gemini_sync, prompt)

        # 소도시와 한줄평을 3개씩 추출
        smallcities = []
        shortreviews = []
        for i in range(3):
            smallcities.append(re.search(fr"소도시{i+1}[:：]\s*(.+)", generated_text))
            shortreviews.append(re.search(fr"한줄평{i+1}[:：]\s*(.+)", generated_text))

        # 추출된 텍스트를 바로 리스트에 넣기 전에, 매칭된 결과가 있는지 체크
        smallcities_text = [match.group(1).strip() if match else "" for match in smallcities]
        shortreviews_text = [match.group(1).strip() if match else "" for match in shortreviews]

        # 결과 리스트로 구성
        result = []
        for i in range(3):
            smallCity = smallcities_text[i]
            shortReview = shortreviews_text[i]
            result.append({
                "smallCity": smallCity,
                "shortReview": shortReview
            })

        return {
            "region":prompt,
            "recommendations": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
