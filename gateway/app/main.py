# gateway/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from app.router.auth_router import auth_router

load_dotenv()

app = FastAPI()

# --- 설정값 로드 ---
# 환경 변수에서 콤마(,)로 구분된 여러 URL을 하나의 문자열로 가져옵니다.
# 변수 이름도 복수형인 FRONTEND_URLS로 변경하여 명확하게 합니다.
FRONTEND_URLS_STR = os.getenv("FRONTEND_URLS", "http://localhost:3000")

# 가져온 문자열을 콤마(,) 기준으로 잘라서 파이썬 리스트로 만듭니다.
# 이렇게 하면 여러 개의 출처(origin)를 동적으로 관리할 수 있습니다.
ALLOWED_ORIGINS = [url.strip() for url in FRONTEND_URLS_STR.split(',')]

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "your-secret-key")

# 현재 환경이 프로덕션(배포) 환경인지 확인합니다.
IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") == "production"


# --- 미들웨어 설정 ---

# CORS 설정: 위에서 만든 리스트(ALLOWED_ORIGINS)를 사용합니다.
# 이제 여기에 포함된 모든 주소에서의 요청을 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 추가 (기존과 동일)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    session_cookie="session",
    max_age=86400,  # 24시간
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