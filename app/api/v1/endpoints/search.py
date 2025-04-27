from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import get_secret
import re
# import os
# from dotenv import load_dotenv

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
    너는 검색어를 입력받아 지역인지 아닌지 구분하고, 지역이면 해당 지역에 맞는 에티켓 문구를 출력해줘줘:

    - 지역: 지역명인지 아닌지 
    - 지역명 : 해당 지역명
    - 에티켓 : 지역명이면 해당 지역에 맞는 에티켓 내용 간단하게 요약해서 출력해줘 (지역이 false면 없어도도 돼)

    예시 형식:
    지역: true 
    에티켓: 교토 여행 에티켓 요약
    사찰·신사에서는 조용히 하고, 사진 촬영 금지 구역을 확인해요.
    왼쪽 통행을 지키고, 길에서 현지인에게 방해되지 않게 해요.
    쓰레기는 직접 챙겨서 버려요.
    가게에서는 트레이에 돈을 놓고 계산해요.
    게이샤(마이코)에게 다가가거나 무단 촬영하지 않기.
    자전거는 인도에서 끌고 걷기가 기본이에요.
    """
)

# 요청 모델
class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
async def search(request: ChatRequest):
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
            search_match = re.search(r"지역[:：]\s*(true|false)", text, re.IGNORECASE)
            etiquette_match = re.search(r"에티켓[:：]\s*(.+)", text, re.DOTALL)

            # 지역 여부 
            is_region = search_match.group(1).strip().lower() == "true" if search_match else False

            # 지역명
            region_name = ""
            if is_region:
                region_name = user_prompt

            # 에티켓
            etiquette_text = ""
            if etiquette_match:
                etiquette_text = etiquette_match.group(1).strip()

            return {
                "isRegion": is_region,
                "region": region_name,
                "content": etiquette_text
            }

        result = parse_output(generated_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")