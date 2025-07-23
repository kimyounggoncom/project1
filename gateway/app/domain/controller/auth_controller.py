# gateway/app/domain/controller/auth_controller.py

import os
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
import logging

from ..service.auth_service import AuthService
from ..model.auth_schema import LoginResponse, CallbackResponse, OAuthLoginRequest, OAuthCallbackRequest

logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        # CORS 설정과 일관성을 위해 FRONTEND_URLS에서 첫 번째 URL을 기본값으로 사용
        self.frontend_url = os.getenv("FRONTEND_URLS", "http://localhost:3000").split(',')[0]
        self.gateway_url = os.getenv("GATEWAY_URL", "http://localhost:8080")
    
    async def google_login(self, request: Request, login_request: Optional[OAuthLoginRequest] = None) -> LoginResponse:
        """구글 OAuth 로그인 시작"""
        try:
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            if login_request and login_request.redirect_uri:
                redirect_uri = str(login_request.redirect_uri)
            
            state = self.auth_service.generate_state()
            request.session["oauth_state"] = state
            
            auth_url = self.auth_service.get_google_auth_url(redirect_uri, state)
            logger.info(f"Generated Google OAuth URL: {auth_url}")
            
            return LoginResponse(
                success=True,
                message="Google OAuth URL generated successfully",
                auth_url=auth_url
            )
        except Exception as e:
            logger.error(f"Google login failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Google login failed: {str(e)}")
    
    async def google_login_redirect(self, request: Request) -> RedirectResponse:
        """구글 OAuth 로그인 리디렉션"""
        try:
            login_response = await self.google_login(request)
            if login_response.auth_url:
                return RedirectResponse(url=login_response.auth_url)
            else:
                raise HTTPException(status_code=500, detail="Failed to generate auth URL")
        except Exception as e:
            logger.error(f"Google login redirect failed: {str(e)}")
            error_url = f"{self.frontend_url}/login?error=oauth_failed"
            return RedirectResponse(url=error_url)
    
    async def google_callback(self, request: Request, callback_request: OAuthCallbackRequest) -> CallbackResponse:
        """구글 OAuth 콜백 처리"""
        try:
            if callback_request.error:
                logger.error(f"OAuth error: {callback_request.error} - {callback_request.error_description}")
                return CallbackResponse(success=False, message=f"OAuth error: {callback_request.error_description or callback_request.error}")
            
            stored_state = request.session.get("oauth_state")
            if not stored_state or stored_state != callback_request.state:
                logger.error("Invalid OAuth state")
                return CallbackResponse(success=False, message="Invalid OAuth state")
            
            request.session.pop("oauth_state", None)
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            
            auth_response = await self.auth_service.process_google_callback(
                callback_request.code,
                callback_request.state,
                redirect_uri
            )
            
            logger.info(f"Google OAuth successful for user: {auth_response.user.email}")
            
            return CallbackResponse(
                success=True,
                message="Google OAuth authentication successful",
                user=auth_response.user.dict(),
                token=auth_response.token.dict(),
                redirect_url=f"{self.frontend_url}/dashboard"
            )
        except Exception as e:
            logger.error(f"Google callback failed: {str(e)}")
            return CallbackResponse(success=False, message=f"Google callback failed: {str(e)}")

    async def google_callback_redirect(self, request: Request, code: str, state: str, error: Optional[str] = None) -> RedirectResponse:
        """구글 OAuth 콜백 리디렉션. 쿠키 설정을 환경에 따라 동적으로 변경합니다."""
        try:
            callback_request = OAuthCallbackRequest(code=code, state=state, error=error)
            callback_response = await self.google_callback(request, callback_request)
            
            if callback_response.success:
                dashboard_url = f"{self.frontend_url}/dashboard?auth=success"
                response = RedirectResponse(url=dashboard_url)
                
                token_value = callback_response.token['access_token']
                
                # --- 환경에 따른 쿠키 설정 (핵심 수정 부분) ---
                IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") == "production"
                
                # 프로덕션 환경에서는 '.kimyounggon.com' 도메인으로 설정하고, 로컬에서는 설정하지 않음(None)
                cookie_domain = ".kimyounggon.com" if IS_PRODUCTION else None
                cookie_secure = True if IS_PRODUCTION else False
                cookie_samesite = "none" if IS_PRODUCTION else "lax"
                
                logger.info(f"Cookie settings | Production: {IS_PRODUCTION}, Domain: {cookie_domain}, Secure: {cookie_secure}, SameSite: {cookie_samesite}")

                response.set_cookie(
                    key="session_token",
                    value=token_value,
                    httponly=True,
                    max_age=86400,  # 24시간
                    path="/",
                    secure=cookie_secure,
                    samesite=cookie_samesite,
                    domain=cookie_domain
                )
                logger.info("Cookie set successfully with dynamic settings.")
                return response
            else:
                error_url = f"{self.frontend_url}/login?error={callback_response.message}"
                logger.error(f"Callback failed, redirecting to: {error_url}")
                return RedirectResponse(url=error_url)
                
        except Exception as e:
            logger.error(f"Callback redirect failed catastrophically: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            error_url = f"{self.frontend_url}/login?error=callback_failed_unexpectedly"
            return RedirectResponse(url=error_url)
    
    async def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰 검증"""
        try:
            payload = await self.auth_service.verify_jwt_token(token)
            return {
                "success": True,
                "user": {
                    "email": payload.get("email"),
                    "name": payload.get("name"),
                    "picture": payload.get("picture"),
                    "google_id": payload.get("google_id")
                },
                "email": payload.get("email"),
                "name": payload.get("name")
            }
        except Exception as e:
            logger.error(f"JWT token verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")