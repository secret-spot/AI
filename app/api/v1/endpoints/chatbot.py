# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import get_geminiAPI
import re

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = get_geminiAPI()

if not GOOGLE_API_KEY:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Generative AI 구성
genai.configure(api_key=GOOGLE_API_KEY)

# 모델 초기화
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction="""
    너는 여행을 도와주는 친구야. 질문을 받으면 친구처럼 친절하게 대답해줘.
    """
)

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def chatbot(request: ChatRequest):
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
            return {
                "content": text.strip()
            }

        result = parse_output(generated_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")