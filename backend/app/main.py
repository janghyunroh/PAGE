# ==============================================================================
# 파일: backend/app/main.py
# 역할: FastAPI 애플리케이션의 메인 파일입니다. API 엔드포인트를 정의합니다.
#       (순환 참조를 유발할 수 있는 불필요한 import를 제거했습니다.)
# ==============================================================================
from fastapi import FastAPI, Depends
from .dependencies import get_api_key
from .models import DraftRequest, DraftResponse

# FastAPI 앱 인스턴스를 생성합니다.
app = FastAPI(
    title="P.A.G.E. Backend API",
    description="AI 블로그 초안 생성기 P.A.G.E.의 백엔드 API입니다.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    서버가 정상적으로 실행 중인지 확인하기 위한 루트 엔드포인트입니다.
    """
    return {"message": "Welcome to P.A.G.E. Backend API!"}


@app.post("/generate-draft", 
          response_model=DraftResponse,
          dependencies=[Depends(get_api_key)])
async def generate_draft(request: DraftRequest):
    """
    블로그 초안 생성을 요청받는 메인 API 엔드포인트입니다.
    API 키 인증이 필요합니다.
    """
    print(f"Received topic: {request.topic}")
    
    # --- TODO: 여기에 RAG 및 LLM 호출 로직을 추가할 예정입니다. ---
    
    # 현재는 더미 데이터를 반환합니다.
    dummy_draft = f"""---
title: {request.topic}
description: This is a draft about {request.topic}.
author: janghyunroh
date: 2025-08-25 10:30 +0900
categories: [New]
tags: [Draft]
---

# {request.topic}에 대한 초안

이것은 **{request.topic}**에 대해 AI가 생성한 블로그 포스트 초안의 시작입니다.
여기에 RAG를 통해 검색된 내용과 LLM이 생성한 본문이 채워질 예정입니다.
"""
    
    return DraftResponse(draft=dummy_draft)
