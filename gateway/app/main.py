from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import httpx
import os
from typing import Dict, Any
import logging
from dotenv import load_dotenv
from app.router.auth_router import auth_router

load_dotenv()

app = FastAPI()

# 환경 변수에서 설정 가져오기
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "your-secret-key")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Set-Cookie", "Authorization"],
    max_age=3600,
)

# 세션 미들웨어 추가
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    session_cookie="session",
    max_age=86400,  # 24시간
    same_site="lax",
    https_only=False,  # 개발환경에서는 False, 프로덕션에서는 True
)

# 라우터 등록
app.include_router(auth_router, tags=["auth"])

@app.get("/health")
async def health_check():
    """Gateway 서비스 헬스 체크"""
    return {
        "status": "healthy",
        "service": "gateway"
    }

@app.get("/")
async def root():
    return {"message": "Gateway Service"} 