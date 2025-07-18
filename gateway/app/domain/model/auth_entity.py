from sqlalchemy import Column, String, DateTime, Integer, Text, func, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# SQLAlchemy Base 클래스
Base = declarative_base()

# SQLAlchemy 모델
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    picture = Column(Text, nullable=True)
    google_id = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계 설정
    oauth_sessions = relationship("OAuthSession", back_populates="user")


class OAuthSession(Base):
    __tablename__ = "oauth_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_type = Column(String(50), default="Bearer")
    expires_in = Column(Integer, nullable=True)
    scope = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계 설정
    user = relationship("User", back_populates="oauth_sessions")
