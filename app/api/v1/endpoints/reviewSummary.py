import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import get_secret
import re

router = APIRouter()

# 환경 변수 로드
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# GOOGLE_API_KEY = get_secret()

if not GOOGLE_API_KEY:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Generative AI 구성
genai.configure(api_key=GOOGLE_API_KEY)

# 모델 초기화
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction="""
    너는 리뷰글들을 받아서 요약해줘:

    - 리뷰 : 리뷰글들을 분석하여 만족스러운지 아닌지 판단하고 (대부분 만족하는지 아니지만 써줘) 추천하는 이유와 비추천하는 이유를 뽑아줘. (해당 내용이 없으면 그냥 비워도 돼.)

    예시 형식:
    리뷰요약: 전반적으로 매우 만족스러웠습니다. 
    추천-지역 관광지들은 풍경이 아름다웠고, 다양한 액티비티들이 있어 즐거운 시간을 보낼 수 있었습니다. 
    비추천-교통이 조금 불편하다는 점과 몇몇 인기 있는 장소에서는 사람이 많아 혼잡함이 있었습니다. 
    """
)

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def reviewSummary(request: ChatRequest):
    try:
        user_prompt = request.prompt

        # 모델 응답
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0.7
            )
        )

        if not response.candidates or not response.candidates[0].content.parts:
            raise HTTPException(status_code=500, detail="모델 응답이 없습니다.")

        generated_text = ''.join([part.text for part in response.candidates[0].content.parts])

        # 파싱 로직
        def parse_output(text: str):
            summary_match = re.search(r"리뷰요약[:：]\s*(.+)", text, re.DOTALL)

            # 에티켓
            summary_text = ""
            if summary_match:
                summary_text = summary_match.group(1).strip()

            return {
                "content": summary_text
            }

        result = parse_output(generated_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")