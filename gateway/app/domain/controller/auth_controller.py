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
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        self.gateway_url = os.getenv("GATEWAY_URL", "http://localhost:8080")  # 8000에서 8080으로 변경
    
    async def google_login(self, request: Request, login_request: Optional[OAuthLoginRequest] = None) -> LoginResponse:
        """구글 OAuth 로그인 시작"""
        try:
            # 기본 redirect URI 설정
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            
            # 사용자 정의 redirect URI가 있다면 사용
            if login_request and login_request.redirect_uri:
                redirect_uri = str(login_request.redirect_uri)
            
            # state 생성 (CSRF 보호)
            state = self.auth_service.generate_state()
            
            # 세션에 state 저장 (실제 구현에서는 Redis 등 사용 권장)
            request.session["oauth_state"] = state
            
            # 구글 OAuth URL 생성
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
            # 에러 발생 시 프론트엔드로 리디렉션
            error_url = f"{self.frontend_url}/login?error=oauth_failed"
            return RedirectResponse(url=error_url)
    
    async def google_callback(self, request: Request, callback_request: OAuthCallbackRequest) -> CallbackResponse:
        """구글 OAuth 콜백 처리"""
        try:
            # 에러 체크
            if callback_request.error:
                logger.error(f"OAuth error: {callback_request.error} - {callback_request.error_description}")
                return CallbackResponse(
                    success=False,
                    message=f"OAuth error: {callback_request.error_description or callback_request.error}"
                )
            
            # state 검증
            stored_state = request.session.get("oauth_state")
            if not stored_state or stored_state != callback_request.state:
                logger.error("Invalid OAuth state")
                return CallbackResponse(
                    success=False,
                    message="Invalid OAuth state"
                )
            
            # 세션에서 state 제거
            request.session.pop("oauth_state", None)
            
            # redirect URI 설정
            redirect_uri = f"{self.gateway_url}/auth/google/callback/redirect"
            
            # OAuth 콜백 처리
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
            return CallbackResponse(
                success=False,
                message=f"Google callback failed: {str(e)}"
            )
    
    async def google_callback_redirect(self, request: Request, code: str, state: str, error: Optional[str] = None) -> RedirectResponse:
        """구글 OAuth 콜백 리디렉션"""
        try:
            logger.info(f"=== CALLBACK REDIRECT START ===")
            logger.info(f"Code: {code[:10]}..., State: {state[:10]}..., Error: {error}")
            
            callback_request = OAuthCallbackRequest(
                code=code,
                state=state,
                error=error
            )
            
            logger.info(f"Calling google_callback...")
            callback_response = await self.google_callback(request, callback_request)
            
            logger.info(f"Callback response success: {callback_response.success}")
            logger.info(f"Callback response: {callback_response}")
            
            if callback_response.success:
                # 성공 시 httpOnly 쿠키 설정하고 대시보드로 리디렉션
                dashboard_url = f"{self.frontend_url}/dashboard?auth=success"
                logger.info(f"=== SUCCESS: Redirecting to dashboard: {dashboard_url} ===")
                
                response = RedirectResponse(url=dashboard_url)
                
                # 토큰 안전하게 추출
                try:
                    logger.info(f"Token object type: {type(callback_response.token)}")
                    logger.info(f"Token object: {callback_response.token}")
                    
                    # 딕셔너리에서 access_token 추출
                    token_value = callback_response.token['access_token']
                    logger.info(f"Token extracted successfully: {token_value[:20]}...")
                    
                    response.set_cookie(
                        key="session_token",  # authToken에서 session_token으로 변경
                        value=token_value,
                        httponly=True,
                        secure=False,  # 개발환경에서는 False, 프로덕션에서는 True
                        samesite="lax",
                        max_age=86400,  # 24시간
                        path="/",
                        domain="localhost"  # 로컬 개발에서 도메인 통일
                    )
                    logger.info("=== Cookie set successfully ===")
                except Exception as token_error:
                    logger.error(f"=== Token extraction failed: {token_error} ===")
                    logger.error(f"Token object: {callback_response.token}")
                    # 토큰 추출에 실패해도 대시보드로 리디렉션은 계속 진행
                
                logger.info(f"=== Returning response to: {dashboard_url} ===")
                return response
            else:
                # 실패 시 에러와 함께 로그인 페이지로 리디렉션
                error_url = f"{self.frontend_url}/login?error={callback_response.message}"
                logger.error(f"Callback failed, redirecting to: {error_url}")
                return RedirectResponse(url=error_url)
                
        except Exception as e:
            logger.error(f"=== CALLBACK REDIRECT FAILED ===")
            logger.error(f"Exception: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            error_url = f"{self.frontend_url}/login?error=callback_failed"
            logger.error(f"=== Redirecting to error page: {error_url} ===")
            return RedirectResponse(url=error_url)
    
    async def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰 검증"""
        try:
            # AuthService를 통해 토큰 검증
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

