# import os
# from dotenv import load_dotenv
from google.auth import default
from google.cloud import secretmanager
import google.generativeai as genai


def get_geminiAPI():
    credentials, _ = default()
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = "projects/1036716270240/secrets/GOOGLE_API_KEY/versions/latest"
    try:
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise Exception(f"비밀 키를 가져오는 데 실패했습니다: {str(e)}")

def get_geocodingAPI():
    credentials, _ = default()
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = "projects/1036716270240/secrets/GOOGLE_PLACES_API/versions/latest"
    try:
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise Exception(f"비밀 키를 가져오는 데 실패했습니다: {str(e)}")

# 환경 변수 로드
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = get_geminiAPI()

if not GOOGLE_API_KEY:
    raise Exception("API 키를 불러올 수 없습니다.")

# Google Generative AI 구성
genai.configure(api_key=GOOGLE_API_KEY)

models = {
    # 챗봇 기능
    "chatbot": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
        너는 여행을 도와주는 친구야. 질문을 받으면 친구처럼 친절하게 대답해줘. 만약에 여행지 추천을 받는다면 사람들이 많이 몰리지 않는 소도시 중심으로 추천해줘.
        그리고 답변은 150자 이내로 해줘.
        """
    ),
    # 소도시 추천 기능 
    "recommend": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
        너는 여행 가이드야. 해당 검색어 주변 소도시를 추천하면서 소도시를 소개하는 한줄평을 남겨줘:

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
    ),
    # 에티켓 출력 기능 
    "etiquette": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
        너는 지역명을 입력받아 해당 지역에 맞는 에티켓 문구를 출력해줘:

        - 에티켓 : 지역명이면 해당 지역에 맞는 에티켓 내용 간단하게 요약해서 3줄 출력해줘 (대중교통, 공공장소 이런식으로 구분 안해줘도 돼.)

        예시 형식:
        에티켓: 교토 여행 에티켓 요약
        사찰·신사에서는 조용히 하고, 사진 촬영 금지 구역을 확인해요.
        왼쪽 통행을 지키고, 길에서 현지인에게 방해되지 않게 해요.
        쓰레기는 직접 챙겨서 버려요.
        """
    ),
    # 리뷰 요약 기능 
    "reviewSummary": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
        너는 리뷰글들을 받아서 요약해줘:

        - 리뷰 : 리뷰글들을 분석하여 만족스러운지 아닌지 판단하고 (대부분 만족하는지 아니지만 써줘) 추천하는 이유와 비추천하는 이유를 뽑아줘. (해당 내용이 없으면 그냥 비워도 돼.)

        예시 형식:
        리뷰요약: 전반적으로 매우 만족스러웠습니다. 
        추천-지역 관광지들은 풍경이 아름다웠고, 다양한 액티비티들이 있어 즐거운 시간을 보낼 수 있었습니다. 
        비추천-교통이 조금 불편하다는 점과 몇몇 인기 있는 장소에서는 사람이 많아 혼잡함이 있었습니다. 
        """
    ),
    # 키워드 추출 기능 
    "keyword": genai.GenerativeModel(
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
}


