# 📝 배포 및 개발 노트

## 🔑 현재 사용 중인 실제 환경 변수 값들

### Frontend (.env.local)
```bash
# 실제 값들을 여기에 기록 (보안상 중요!)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=실제_구글_클라이언트_ID
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_ENVIRONMENT=development
```

### Gateway (.env)
```bash
# 실제 값들을 여기에 기록 (보안상 중요!)
GOOGLE_CLIENT_ID=실제_구글_클라이언트_ID
GOOGLE_CLIENT_SECRET=실제_구글_클라이언트_시크릿
JWT_SECRET=실제_JWT_시크릿_키
SESSION_SECRET_KEY=실제_세션_시크릿_키
FRONTEND_URL=http://localhost:3000
GATEWAY_URL=http://localhost:8080
AUTH_SERVICE_URL=http://localhost:8001
SUPABASE_URL=실제_수파베이스_URL
SUPABASE_KEY=실제_수파베이스_키
SUPABASE_JWT_SECRET=실제_수파베이스_JWT_시크릿
ENVIRONMENT=development
```

## 🐛 현재 발생한 에러들

### 1. API 호출 에러
- **증상**: 브라우저 콘솔에서 "API 호출 에러" 발생
- **원인**: 환경 변수 설정 문제 또는 서버 연결 실패
- **해결책**: 
  - 환경 변수 파일 생성 확인
  - 서버 포트 설정 확인
  - CORS 설정 확인

### 2. 포트 충돌 문제
- **현재 설정**: Frontend(3000), Gateway(8080), Auth Service(8001)
- **주의사항**: 다른 서비스와 포트 충돌 가능성

## 🔧 개발 환경 설정

### 현재 시스템 정보
- **OS**: Windows 10 (10.0.26100)
- **Shell**: PowerShell
- **Node.js**: v22.16.0
- **Python**: 3.10.18
- **Docker**: 28.3.2

### IDE 설정
- **에디터**: VS Code 권장
- **확장 프로그램**: 
  - Python
  - TypeScript
  - Docker
  - Tailwind CSS IntelliSense

## 📦 패키지 매니저 설정

### Frontend
```bash
# pnpm 사용 권장
npm install -g pnpm
cd frontend
pnpm install
```

### Gateway
```bash
# Python 가상환경 권장
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 실행 순서

### 1. 환경 변수 설정
```bash
# Frontend
cp frontend/env_example.txt frontend/.env.local
# .env.local 파일 편집

# Gateway
cp gateway/env_example.txt gateway/.env
# .env 파일 편집
```

### 2. Docker 실행
```bash
docker-compose up -d
```

### 3. 개발 모드 실행
```bash
# Frontend
cd frontend
pnpm dev

# Gateway
cd gateway
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## 🔍 디버깅 도구

### 로그 확인
```bash
# Docker 로그
docker-compose logs -f [service-name]

# Frontend 로그
# 브라우저 개발자 도구 콘솔

# Gateway 로그
# 터미널에서 직접 확인
```

### 헬스체크
```bash
# Frontend
curl http://localhost:3000

# Gateway
curl http://localhost:8080/health

# Auth Service
curl http://localhost:8001/health
```

## 📋 TODO 리스트

### 현재 작업 중인 기능
- [ ] Google OAuth 로그인 구현 완료
- [ ] JWT 토큰 기반 인증 시스템
- [ ] 사용자 대시보드 구현
- [ ] API Gateway 설정

### 향후 개발 예정
- [ ] 사용자 프로필 관리
- [ ] 로그아웃 기능
- [ ] 에러 처리 개선
- [ ] 테스트 코드 작성
- [ ] CI/CD 파이프라인 구축

## 🔐 보안 주의사항

### 절대 Git에 커밋하지 말 것
- `.env` 파일들
- 실제 API 키들
- 시크릿 키들
- 개인 정보

### 운영 환경에서 변경해야 할 것
- 모든 기본 시크릿 키
- 데이터베이스 비밀번호
- API 키들
- CORS 설정

## 📞 문제 발생 시 연락처
- 개발자: [이름]
- 이메일: [이메일]
- 프로젝트 URL: [GitHub 저장소 URL] 