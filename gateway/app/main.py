from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from app.router.auth_router import auth_router

load_dotenv()

app = FastAPI()

# --- 설정값 로드 ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "your-secret-key")

# ▼▼▼ 여기가 핵심적인 변경 부분입니다 ▼▼▼
# 현재 환경이 프로덕션(배포) 환경인지 확인합니다.
# Railway는 자동으로 'RAILWAY_ENVIRONMENT' 변수를 'production'으로 설정해줍니다.
IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") == "production"

# --- 미들웨어 설정 ---

# CORS 설정 (기존과 동일)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 추가 (환경에 따라 다르게 설정)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    session_cookie="session",
    max_age=86400,  # 24시간
    # 프로덕션 환경에서는 samesite='none'과 https_only=True로 설정합니다.
    # 이렇게 해야 다른 도메인(Vercel)과 쿠키를 주고받을 수 있습니다.
    same_site="none" if IS_PRODUCTION else "lax",
    https_only=IS_PRODUCTION,
)

# --- 라우터 및 엔드포인트 ---

# 라우터 등록 (기존과 동일)
app.include_router(auth_router, tags=["auth"])

@app.get("/health")
async def health_check():
    """Gateway 서비스 헬스 체크"""
    return {"status": "healthy", "service": "gateway"}

@app.get("/")
async def root():
    return {"message": "Gateway Service"}