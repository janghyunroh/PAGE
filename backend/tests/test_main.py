# ==============================================================================
# 파일: backend/tests/test_main.py
# 역할: app/main.py의 API 엔드포인트들을 테스트합니다.
# ==============================================================================
import pytest
import os
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv

# 테스트 환경에서도 .env 파일을 로드하여 API 키를 사용할 수 있도록 합니다.
load_dotenv()

# FastAPI 앱을 import 합니다.
from app.main import app

# 테스트에 사용할 API 키를 환경 변수에서 가져옵니다.
SECRET_API_KEY = os.getenv("MY_SECRET_API_KEY")

@pytest.mark.asyncio
async def test_read_root():
    """
    루트 엔드포인트('/')가 정상적으로 응답하는지 테스트합니다.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to P.A.G.E. Backend API!"}

@pytest.mark.asyncio
async def test_generate_draft_no_api_key():
    """
    API 키 없이 /generate-draft에 접근 시 403 Forbidden 에러가 발생하는지 테스트합니다.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/generate-draft", json={"topic": "Test Topic"})
    # 수정: FastAPI의 기본 동작인 403을 기대하도록 변경
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_generate_draft_wrong_api_key():
    """
    잘못된 API 키로 /generate-draft에 접근 시 401 Unauthorized 에러가 발생하는지 테스트합니다.
    """
    headers = {"Authorization": "Bearer wrong-key"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/generate-draft", json={"topic": "Test Topic"}, headers=headers)
    # 이 경우는 우리가 직접 401을 발생시키므로 그대로 둡니다.
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_generate_draft_success():
    """
    올바른 API 키로 /generate-draft에 접근 시 200 OK와 함께 정상적인 응답을 받는지 테스트합니다.
    """
    headers = {"Authorization": f"Bearer {SECRET_API_KEY}"}
    topic = "Testing with Pytest"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/generate-draft", json={"topic": topic}, headers=headers)
    
    assert response.status_code == 200
    response_data = response.json()
    assert "draft" in response_data
    assert topic in response_data["draft"]
