# import os
# from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import get_secret
import re

router = APIRouter()

# 환경 변수 로드
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = get_secret()

if not GOOGLE_API_KEY:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Generative AI 구성
genai.configure(api_key=GOOGLE_API_KEY)

# 모델 초기화
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction="""
    너는 여행 후기글을 받아서 요약하고, 다음 정보를 핵심 키워드로 정리해줘:

    - 장소: 한국 기준 어느 '시'에서의 이야기인지 (여러 장소가 나오면 모두)
    - 동행: 혼자, 가족, 친구, 연인 중 무엇인지
    - 활동: 예술, 익스트림, 사진촬영, 음식, 힐링, 역사, 쇼핑, 체험 중 후기와 관련 있는 활동

    예시 형식:
    장소: 강릉, 속초
    동행: 연인
    활동: 익스트림, 힐링
    """
)

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def keyword(request: ChatRequest):
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
