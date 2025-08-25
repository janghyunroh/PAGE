# ==============================================================================
# 파일: backend/app/dependencies.py
# 역할: API 보안과 같이 여러 곳에서 공통으로 사용될 의존성을 정의합니다.
# ==============================================================================
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

API_KEY = os.getenv("MY_SECRET_API_KEY")
API_KEY_NAME = "Authorization" # HTTP 헤더 이름

# HTTP 헤더에서 API 키를 읽어오는 객체를 생성합니다.
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Depends(api_key_header)):
    """
    요청 헤더에 포함된 API 키가 유효한지 검증하는 함수입니다.
    Bearer 토큰 형식을 사용합니다. (예: "Bearer YOUR_SECRET_KEY")
    """
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key or format. Expected: Bearer YOUR_SECRET_KEY",
        )
    return api_key
