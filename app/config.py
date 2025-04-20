from google.auth import default
from google.cloud import secretmanager


def get_secret():
    credentials, _ = default()
    # Secret Manager 클라이언트 생성
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = "projects/736744382613/secrets/GOOGLE_API_KEY/versions/latest"
    try:
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise Exception(f"비밀 키를 가져오는 데 실패했습니다: {str(e)}")
