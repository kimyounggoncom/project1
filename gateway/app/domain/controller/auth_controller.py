# gateway/app/domain/controller/auth_controller.py

import os
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
import logging

from ..service.auth_service import AuthService
from ..model.auth_schema import LoginResponse, CallbackResponse, OAuthLoginRequest, OAuthCallbackRequest

logger = logging.getLogger(__name__)

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self.gateway_url = os.getenv("GATEWAY_URL", "http://localhost:8080")
        # frontend_url을 여기서 고정하지 않고, 각 요청마다 동적으로 결정합니다.

    def get_frontend_url(self, request: Request) -> str:
        """
        요청 헤더의 Origin을 기반으로 동적으로 프론트엔드 URL을 결정합니다.
        CORS 설정에서 허용된 Origin만 신뢰하여 보안을 유지합니다.
        """
        origin = request.headers.get("origin")
        allowed_origins_str = os.getenv("FRONTEND_URLS", "http://localhost:3000")
        allowed_origins = [url.strip() for url in allowed_origins_str.split(',')]

        # 요청의 Origin이 허용된 목록에 있으면 해당 Origin을 사용합니다.
        if origin and origin in allowed_origins:
            logger.debug(f"Dynamic frontend URL detected from origin: {origin}")
            return origin
        
        # Origin 헤더가 없거나 허용되지 않은 경우, 목록의 첫 번째 URL을 안전한 기본값으로 사용합니다.
        default_url = allowed_origins[0]
        logger.warning(f"Origin '{origin}' not in allowed list or not present. Falling back to default: {default_url}")
        return default_url

    async def google_login(self, request: Request, login_request: Optional[OAuthLoginRequest] = None) -> LoginResponse:
        """구글 OAuth 로그인 시작"""
        try:
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            
            state = self.auth_service.generate_state()
            request.session["oauth_state"] = state
            
            auth_url = self.auth_service.get_google_auth_url(redirect_uri, state)
            
            return LoginResponse(
                success=True,
                message="Google OAuth URL generated successfully",
                auth_url=auth_url
            )
        except Exception as e:
            logger.error(f"Google login failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Google login failed")
    
    async def google_login_redirect(self, request: Request) -> RedirectResponse:
        """구글 OAuth 로그인 페이지로 직접 리디렉션"""
        try:
            login_response = await self.google_login(request)
            if login_response.auth_url:
                return RedirectResponse(url=login_response.auth_url)
            else:
                raise HTTPException(status_code=500, detail="Failed to generate auth URL")
        except Exception as e:
            logger.error(f"Google login redirect failed: {str(e)}")
            frontend_url = self.get_frontend_url(request)
            error_url = f"{frontend_url}/login?error=oauth_failed"
            return RedirectResponse(url=error_url)
    
    async def google_callback(self, request: Request, callback_request: OAuthCallbackRequest) -> CallbackResponse:
        """구글 OAuth 콜백 처리 (API용, JSON 반환)"""
        try:
            if callback_request.error:
                return CallbackResponse(success=False, message=f"OAuth error: {callback_request.error_description or callback_request.error}")
            
            stored_state = request.session.get("oauth_state")
            if not stored_state or stored_state != callback_request.state:
                return CallbackResponse(success=False, message="Invalid OAuth state")
            
            request.session.pop("oauth_state", None)
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            
            auth_response = await self.auth_service.process_google_callback(
                callback_request.code,
                callback_request.state,
                redirect_uri
            )
            
            frontend_url = self.get_frontend_url(request)
            
            return CallbackResponse(
                success=True,
                message="Google OAuth authentication successful",
                user=auth_response.user.dict(),
                token=auth_response.token.dict(),
                redirect_url=f"{frontend_url}/dashboard"
            )
        except Exception as e:
            logger.error(f"Google callback failed: {str(e)}")
            return CallbackResponse(success=False, message="Google callback failed")

    async def google_callback_redirect(self, request: Request, code: str, state: str, error: Optional[str] = None) -> RedirectResponse:
        """구글 OAuth 콜백 후 프론트엔드로 최종 리디렉션"""
        try:
            callback_request = OAuthCallbackRequest(code=code, state=state, error=error)
            callback_response = await self.google_callback(request, callback_request)
            
            frontend_url = self.get_frontend_url(request)
            
            if callback_response.success and callback_response.token:
                dashboard_url = f"{frontend_url}/dashboard?auth=success"
                response = RedirectResponse(url=dashboard_url)
                
                token_value = callback_response.token['access_token']
                
                IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") == "production"
                
                cookie_domain = None
                if IS_PRODUCTION:
                    # 'kimyounggon.com'이 포함된 경우에만 도메인을 설정하여 보안 강화
                    if "kimyounggon.com" in frontend_url:
                        cookie_domain = ".kimyounggon.com"
                
                response.set_cookie(
                    key="session_token",
                    value=token_value,
                    httponly=True,
                    max_age=86400, # 24시간
                    path="/",
                    secure=IS_PRODUCTION,
                    samesite="none" if IS_PRODUCTION else "lax",
                    domain=cookie_domain
                )
                return response
            else:
                error_message = callback_response.message or "unknown_error"
                error_url = f"{frontend_url}/login?error={error_message}"
                return RedirectResponse(url=error_url)
                
        except Exception as e:
            logger.error(f"Callback redirect failed catastrophically: {str(e)}")
            frontend_url = self.get_frontend_url(request)
            error_url = f"{frontend_url}/login?error=callback_failed_unexpectedly"
            return RedirectResponse(url=error_url)
    
    async def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰을 검증하여 유저 정보를 반환"""
        try:
            payload = await self.auth_service.verify_jwt_token(token)
            return {
                "success": True,
                "user": {
                    "email": payload.get("email"),
                    "name": payload.get("name"),
                    "picture": payload.get("picture"),
                    "google_id": payload.get("google_id")
                }
            }
        except Exception as e:
            logger.error(f"JWT token verification failed: {str(e)}")
            # 401 에러는 의도된 동작일 수 있으므로, 명확한 메시지를 반환
            raise HTTPException(status_code=401, detail="Invalid or expired token")