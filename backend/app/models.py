# ==============================================================================
# 파일: backend/app/models.py
# 역할: API가 주고받을 데이터의 형식을 정의합니다. (Pydantic 모델)
# ==============================================================================
from pydantic import BaseModel

class DraftRequest(BaseModel):
    """
    초안 생성을 요청할 때 클라이언트(Flutter)가 보내는 데이터 모델입니다.
    """
    topic: str
    

class DraftResponse(BaseModel):
    """
    서버가 초안 생성을 완료하고 클라이언트에게 보내는 데이터 모델입니다.
    """
    draft: str