# 🚀 MSA 인증 시스템 설정 가이드

## 📋 필수 환경 변수 설정

### Frontend (.env.local)
```bash
# 구글 OAuth 설정
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id_here

# API 서버 URL
NEXT_PUBLIC_API_URL=http://localhost:8080

# 기타 설정
NEXT_PUBLIC_ENVIRONMENT=development
```

### Gateway (.env)
```bash
# Google OAuth 설정
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# JWT 설정
JWT_SECRET=your_jwt_secret_key_here

# 세션 설정
SESSION_SECRET_KEY=your_session_secret_key_here

# 서비스 URL 설정
FRONTEND_URL=http://localhost:3000
GATEWAY_URL=http://localhost:8080
AUTH_SERVICE_URL=http://localhost:8001

# Supabase 설정 (선택사항)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
SUPABASE_JWT_SECRET=your_supabase_jwt_secret_here

# 기타 설정
ENVIRONMENT=development
```

## 🛠️ 개발 환경 요구사항

### 필수 도구 및 버전
- **Node.js**: v22.16.0
- **Python**: 3.10.18
- **Docker**: 28.3.2
- **pnpm**: (권장 패키지 매니저)

### 주요 의존성 버전
#### Frontend (Next.js)
- Next.js: 15.3.5
- React: 19.0.0
- TypeScript: 5.x
- Tailwind CSS: 4.x
- Axios: 1.10.0
- Zustand: 5.0.6

#### Gateway (FastAPI)
- FastAPI: 0.104.1
- Uvicorn: 0.24.0
- Python-Jose: 3.3.0
- Pydantic: 2.5.0
- SQLAlchemy: 2.0.23

## 🚀 실행 방법

### 1. 환경 변수 설정
```bash
# Frontend 환경 변수 설정
cp frontend/env_example.txt frontend/.env.local
# .env.local 파일을 편집하여 실제 값 입력

# Gateway 환경 변수 설정
cp gateway/env_example.txt gateway/.env
# .env 파일을 편집하여 실제 값 입력
```

### 2. Docker Compose로 실행
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker-compose ps
```

### 3. 개발 모드 실행
```bash
# Frontend 개발 서버
cd frontend
pnpm install
pnpm dev

# Gateway 개발 서버
cd gateway
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## 🔧 포트 설정
- **Frontend**: http://localhost:3000
- **Gateway**: http://localhost:8080
- **Auth Service**: http://localhost:8001

## 🔐 Google OAuth 설정
1. Google Cloud Console에서 프로젝트 생성
2. OAuth 2.0 클라이언트 ID 생성
3. 승인된 리디렉션 URI 설정:
   - `http://localhost:8080/auth/google/callback/redirect`
   - `http://localhost:3000/auth/callback`

## 📝 주의사항
- `.env` 파일들은 절대 Git에 커밋하지 마세요!
- 실제 운영 환경에서는 모든 시크릿 키를 변경하세요
- CORS 설정이 올바른지 확인하세요

## 🐛 문제 해결
- API 호출 에러 발생 시 환경 변수 설정 확인
- 포트 충돌 시 다른 포트로 변경
- Docker 컨테이너 로그 확인: `docker-compose logs [service-name]` 