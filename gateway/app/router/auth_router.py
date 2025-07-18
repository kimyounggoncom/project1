from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from typing import Optional, Dict, Any
import logging

from ..domain.controller.auth_controller import AuthController
from ..domain.model.auth_schema import LoginResponse, CallbackResponse, OAuthLoginRequest

logger = logging.getLogger(__name__)

# 라우터 생성
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

# AuthController 인스턴스 생성
auth_controller = AuthController()


@auth_router.get("/google/login", response_model=LoginResponse)
async def google_login_api(
    request: Request,
    redirect_uri: Optional[str] = Query(None, description="Custom redirect URI")
) -> LoginResponse:
    """
    구글 OAuth 로그인 API
    
    - **redirect_uri**: 선택적 리디렉션 URI
    - 반환값: 구글 OAuth 인증 URL
    """
    try:
        login_request = None
        if redirect_uri:
            login_request = OAuthLoginRequest(redirect_uri=redirect_uri)
        
        return await auth_controller.google_login(request, login_request)
    except Exception as e:
        logger.error(f"Google login API failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/google/login/redirect")
async def google_login_redirect(request: Request) -> RedirectResponse:
    """
    구글 OAuth 로그인 리디렉션
    
    브라우저에서 직접 접근할 수 있는 엔드포인트
    구글 OAuth 페이지로 자동 리디렉션됩니다.
    """
    return await auth_controller.google_login_redirect(request)


@auth_router.get("/google/callback", response_model=CallbackResponse)
async def google_callback_api(
    request: Request,
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    error: Optional[str] = Query(None, description="Error from Google OAuth")
) -> CallbackResponse:
    """
    구글 OAuth 콜백 API
    
    - **code**: 구글에서 받은 인증 코드
    - **state**: CSRF 보호를 위한 state 파라미터
    - **error**: 구글 OAuth 에러 (선택적)
    """
    try:
        from ..domain.model.auth_schema import OAuthCallbackRequest
        
        callback_request = OAuthCallbackRequest(
            code=code,
            state=state,
            error=error
        )
        
        return await auth_controller.google_callback(request, callback_request)
    except Exception as e:
        logger.error(f"Google callback API failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/google/callback/redirect")
async def google_callback_redirect(
    request: Request,
    code: str = Query(..., description="Authorization code from Google"),
    state: str = Query(..., description="State parameter for CSRF protection"),
    error: Optional[str] = Query(None, description="Error from Google OAuth")
) -> RedirectResponse:
    """
    구글 OAuth 콜백 리디렉션
    
    구글에서 리디렉션되는 실제 엔드포인트
    처리 후 프론트엔드로 자동 리디렉션됩니다.
    """
    return await auth_controller.google_callback_redirect(request, code, state, error)


@auth_router.get("/verify")
async def verify_token(request: Request) -> Dict[str, Any]:
    """
    JWT 토큰 검증
    
    httpOnly 쿠키에서 토큰을 읽어서 검증합니다.
    """
    try:
        # 쿠키에서 토큰 가져오기
        token = request.cookies.get("session_token")
        if not token:
            raise HTTPException(status_code=401, detail="No token provided")
        
        # 토큰 검증 (await 추가)
        return await auth_controller.verify_jwt_token(token)
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")





# 헬스 체크 엔드포인트
@auth_router.get("/health")
async def auth_health_check():
    """인증 서비스 헬스 체크"""
    return {
        "status": "healthy",
        "service": "auth",
        "endpoints": {
            "google_login": "/auth/google/login",
            "google_callback": "/auth/google/callback",
            "verify_token": "/auth/verify",
            "current_user": "/auth/me"
        }
    }


@auth_router.get("/debug/config")
async def debug_config():
    """디버깅용 설정 확인"""
    import os
    return {
        "google_client_id_configured": bool(os.getenv("GOOGLE_CLIENT_ID")),
        "google_client_secret_configured": bool(os.getenv("GOOGLE_CLIENT_SECRET")),
        "google_client_id_prefix": os.getenv("GOOGLE_CLIENT_ID", "")[:10] if os.getenv("GOOGLE_CLIENT_ID") else "None",
        "gateway_url": os.getenv("GATEWAY_URL", "http://localhost:8080"),
        "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "environment_variables": {
            "GOOGLE_CLIENT_ID": "✓" if os.getenv("GOOGLE_CLIENT_ID") else "✗",
            "GOOGLE_CLIENT_SECRET": "✓" if os.getenv("GOOGLE_CLIENT_SECRET") else "✗",
            "JWT_SECRET": "✓" if os.getenv("JWT_SECRET") else "✗",
            "SESSION_SECRET_KEY": "✓" if os.getenv("SESSION_SECRET_KEY") else "✗",
        }
    }
