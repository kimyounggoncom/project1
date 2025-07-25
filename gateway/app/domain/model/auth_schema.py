# gateway/app/domain/model/auth_schema.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime

class OAuthLoginRequest(BaseModel):
    redirect_uri: Optional[HttpUrl] = None
    state: Optional[str] = None

class OAuthCallbackRequest(BaseModel):
    code: str
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool = Field(..., description="요청 성공 여부")
    message: str = Field(..., description="응답 메시지")
    auth_url: Optional[str] = Field(None, description="Google OAuth 인증 URL")

class CallbackResponse(BaseModel):
    success: bool
    message: str
    user: Optional[Dict[str, Any]] = None
    token: Optional[Dict[str, Any]] = None
    redirect_url: Optional[str] = None

class UserResponse(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OAuthToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

class GoogleUserInfo(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: Optional[str] = None

class AuthResponse(BaseModel):
    user: UserResponse
    token: OAuthToken
    message: str = "Authentication successful"