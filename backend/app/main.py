# ==============================================================================
# 파일: backend/app/main.py
# 역할: FastAPI 애플리케이션의 메인 파일입니다.
#       CORS 미들웨어가 로드되었는지 확인하기 위한 디버깅 코드를 추가했습니다.
# ==============================================================================
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import get_api_key
from .models import DraftRequest, DraftResponse
from .services.rag_service import generate_draft_from_topic

# =================================================================
# ✅ 최종 디버깅: 이 메시지가 서버 시작 로그에 반드시 보여야 합니다.
# 만약 이 메시지가 보이지 않는다면, Uvicorn이 이 파일을 실행하고 있지 않은 것입니다.
print("✅✅✅ Loading main.py with CORS Middleware ENABLED! ✅✅✅")
# =================================================================

# FastAPI 앱 인스턴스를 생성합니다.
app = FastAPI(
    title="P.A.G.E. Backend API",
    description="AI 블로그 초안 생성기 P.A.G.E.의 백엔드 API입니다.",
    version="0.1.0",
)

# --- [CORS 설정] ---
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------


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
    
    generated_draft = await generate_draft_from_topic(request.topic)
    
    return DraftResponse(draft=generated_draft)
