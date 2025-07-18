import os
import secrets
import httpx
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from ..model.auth_entity import User, OAuthSession
from ..model.auth_schema import LoginResponse, CallbackResponse, UserResponse, OAuthToken, GoogleUserInfo, AuthResponse

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key")
        self.jwt_algorithm = "HS256"
        self.jwt_expiration_hours = 24
        
        # 환경 변수 로깅 (보안을 위해 일부만 표시)
        logger.info(f"Google Client ID: {self.google_client_id[:10] if self.google_client_id else 'None'}...")
        logger.info(f"Google Client Secret configured: {bool(self.google_client_secret)}")
        
        if not self.google_client_id or not self.google_client_secret:
            logger.error("Google OAuth credentials not configured")
            raise ValueError("Google OAuth credentials not configured")
        
        # 구글 OAuth 엔드포인트
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def generate_state(self) -> str:
        """OAuth state 파라미터 생성"""
        return secrets.token_urlsafe(32)
    
    def get_google_auth_url(self, redirect_uri: str, state: str) -> str:
        """구글 OAuth 인증 URL 생성"""
        try:
            params = {
                "client_id": self.google_client_id,
                "redirect_uri": redirect_uri,
                "scope": "openid email profile",
                "response_type": "code",
                "state": state,
                "access_type": "offline",
                "prompt": "consent"
            }
            
            auth_url = f"{self.google_auth_url}?{urlencode(params)}"
            logger.info(f"Generated Google auth URL: {auth_url}")
            return auth_url
        except Exception as e:
            logger.error(f"Failed to generate auth URL: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate auth URL: {str(e)}")
    
    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """인증 코드를 액세스 토큰으로 교환"""
        token_data = {
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.google_token_url, 
                    data=token_data,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Token exchange HTTP error: {e.response.status_code} - {e.response.text}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Token exchange failed: {e.response.status_code} - {e.response.text}"
                )
            except httpx.RequestError as e:
                logger.error(f"Token exchange request error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Token exchange request failed: {str(e)}")
    
    async def get_google_user_info(self, access_token: str) -> GoogleUserInfo:
        """구글 사용자 정보 조회"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(self.google_userinfo_url, headers=headers)
                response.raise_for_status()
                user_data = response.json()
                return GoogleUserInfo(**user_data)
            except httpx.HTTPStatusError as e:
                logger.error(f"User info HTTP error: {e.response.status_code} - {e.response.text}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to get user info: {e.response.status_code} - {e.response.text}"
                )
            except httpx.RequestError as e:
                logger.error(f"User info request error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"User info request failed: {str(e)}")
            except Exception as e:
                logger.error(f"User info parsing error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to parse user info: {str(e)}")
    
    def create_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """JWT 토큰 생성"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(hours=self.jwt_expiration_hours)
        payload = {
            "sub": user_data["email"],
            "name": user_data["name"],
            "email": user_data["email"],
            "picture": user_data.get("picture"),
            "google_id": user_data.get("google_id"),
            "exp": expire,
            "iat": now
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    async def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=[self.jwt_algorithm],
                options={"verify_exp": True, "verify_iat": True}
            )
            
            # 토큰 만료 시간 추가 검증
            exp = payload.get("exp")
            if exp:
                exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
                if exp_datetime < datetime.now(timezone.utc):
                    raise HTTPException(status_code=401, detail="Token has expired")
            
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            raise HTTPException(status_code=401, detail="Token verification failed")
    
    async def process_google_callback(self, code: str, state: str, redirect_uri: str) -> AuthResponse:
        """구글 OAuth 콜백 처리"""
        try:
            logger.info(f"Processing Google OAuth callback for code: {code[:10]}...")
            
            # 1. 코드를 토큰으로 교환
            token_data = await self.exchange_code_for_token(code, redirect_uri)
            
            if not token_data.get("access_token"):
                logger.error("No access token received from Google")
                raise HTTPException(status_code=400, detail="No access token received from Google")
            
            # 2. 사용자 정보 조회
            google_user_info = await self.get_google_user_info(token_data["access_token"])
            
            # 3. 사용자 응답 객체 생성 (실제 DB 저장은 repository에서 처리)
            now = datetime.now(timezone.utc)
            user_response = UserResponse(
                email=google_user_info.email,
                name=google_user_info.name,
                picture=google_user_info.picture,
                google_id=google_user_info.id,
                created_at=now,
                updated_at=now
            )
            
            # 4. JWT 토큰 생성
            jwt_token = self.create_jwt_token({
                "email": user_response.email,
                "name": user_response.name,
                "picture": user_response.picture,
                "google_id": user_response.google_id
            })
            
            # 5. OAuth 토큰 객체 생성
            oauth_token = OAuthToken(
                access_token=jwt_token,
                token_type="Bearer",
                expires_in=self.jwt_expiration_hours * 3600
            )
            
            logger.info(f"Google OAuth authentication successful for user: {user_response.email}")
            
            return AuthResponse(
                user=user_response,
                token=oauth_token,
                message="Google OAuth authentication successful"
            )
            
        except HTTPException:
            # HTTPException은 그대로 전달
            raise
        except Exception as e:
            logger.error(f"OAuth callback processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"OAuth callback processing failed: {str(e)}")
