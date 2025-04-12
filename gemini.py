from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

# Google Generative AI 구성
genai.configure(api_key=GOOGLE_API_KEY)

# GenerativeModel 초기화
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    #AI 모델의 역할 부여 
    system_instruction="""
    넌 내가 주는 여행 후기글을 요약해주고, 다음 키워드를 추출해주는 친구야.
    1. 장소: 한국 기준 어느 '시'에서의 이야기인지
    2. 동행: 혼자, 가족, 친구, 연인 중 무엇인지
    3. 활동: 예술, 익스트림, 사진촬영, 음식, 힐링, 역사, 쇼핑, 체험 중 해당되는 활동 키워드를 모두 뽑아줘.

    키워드는 항목별로 정리해줘.
    """
)

# FastAPI 애플리케이션 생성
app = FastAPI(title="Gemini Keyword")

# 요청 모델 정의
class ChatRequest(BaseModel):
    prompt: str

@app.post("/keyword/")
async def keyword(request: ChatRequest):
    try:
        # 사용자 프롬프트 추출
        user_prompt = request.prompt

        # 모델을 사용하여 응답 생성
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0.7
            )
        )

        # 응답 처리
        if response.candidates and response.candidates[0].content.parts:
            generated_text = ''.join([part.text for part in response.candidates[0].content.parts])
        else:
            raise HTTPException(status_code=500, detail="유효한 응답 내용을 찾을 수 없습니다.")

        # 키워드 파싱
        import re

        def extract_keyword_section(text: str):
            location = re.search(r"\*\*장소:\*\* ?([^\n]+)", text)
            companion = re.search(r"\*\*동행:\*\* ?([^\n]+)", text)
            activities = re.search(r"\*\*활동:\*\* ?([^\n]+)", text)

            return {
                "request": request.prompt.strip(),
                "keyword": {
                    "장소": location.group(1).strip() if location else None,
                    "동행": companion.group(1).strip() if companion else None,
                    "활동": [a.strip() for a in activities.group(1).split(',')] if activities else []
                }
            }

        result = extract_keyword_section(generated_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")