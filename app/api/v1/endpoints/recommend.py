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
    너는 여행 가이드야. 해당 검색어 주변 소도시를 추천하면서 소도시를 소개하는는 한줄평을 남겨줘:

    - 소도시 : 검색어 주변에 있는 사람들이 많이 가지 않는 소도시 세 곳을 추천해줘.
    - 한줄평 : 소도시를 소개하는 한줄평을 작성해줘.

    예시 형식:
    소도시1: 구리
    한줄평1: 한강을 따라 펼쳐진 자연과 도심이 조화를 이루는 매력적인 소도시
    소도시2: 아산
    한줄평2: 온천과 자연이 어우러진 조용한 휴식처
    소도시3: 남양주
    한줄평3: 산과 강이 함께하는 힐링 도시
    """
)

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def recommend(request: ChatRequest):
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
            # 소도시와 한줄평을 3개씩 추출
            smallcities = re.findall(r"소도시[:：]\s*(.+)", text)
            shortreviews = re.findall(r"한줄평[:：]\s*(.+)", text)

            # 결과 리스트로 구성
            result = []
            for i in range(3):
                smallCity = smallcities[i].strip() if i < len(smallcities) else ""
                shortReview = shortreviews[i].strip() if i < len(shortreviews) else ""
                result.append({
                    "smallCity": smallCity,
                    "shortReview": shortReview
                })

            return result

        result = parse_output(generated_text)

        return {"recommendations": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")