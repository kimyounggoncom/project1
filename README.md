# MSA 모노레포 프로젝트

Next.js 프론트엔드와 FastAPI 백엔드를 사용한 마이크로서비스 아키텍처(MSA) 프로젝트입니다.

## 🏗️ 프로젝트 구조

```
project1/
├── frontend/           # Next.js 프론트엔드
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── gateway/            # API Gateway (FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── auth-service/       # 인증 서비스 (FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml  # Docker Compose 설정
├── Dockerfile         # 루트 레벨 Dockerfile
├── Makefile          # 프로젝트 관리 스크립트
├── supervisord.conf  # Supervisor 설정
└── README.md         # 프로젝트 문서
```

## 🚀 빠른 시작

### 전체 시스템 실행

```bash
# 모든 서비스 빌드 및 실행
make build
make up

# 또는 한 번에
make dev
```

### 개별 서비스 실행

```bash
# 백엔드 서비스만 실행
make backend

# 프론트엔드만 실행
make frontend
```

## 🛠️ 개발 환경 설정

### 필요 조건

- Docker & Docker Compose
- Node.js 18+ (로컬 개발 시)
- pnpm (패키지 매니저)
- Python 3.12+ (로컬 개발 시)
- Make (선택사항)

### 로컬 개발 환경 설정

```bash
# 개발 환경 설정
make setup-dev

# 개발 모드로 실행 (로그와 함께)
make dev
```

## 📋 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `make help` | 사용 가능한 모든 명령어 확인 |
| `make build` | 모든 서비스 빌드 |
| `make up` | 모든 서비스 시작 |
| `make down` | 모든 서비스 중지 |
| `make restart` | 모든 서비스 재시작 |
| `make logs` | 모든 서비스 로그 확인 |
| `make health` | 서비스 상태 확인 |
| `make clean` | 컨테이너 및 볼륨 정리 |

## 🏛️ 서비스 아키텍처

### 서비스 구성

1. **Frontend (Next.js)** - Port 3000
   - 사용자 인터페이스
   - TypeScript + Tailwind CSS
   - API Gateway를 통한 백엔드 통신

2. **API Gateway (FastAPI)** - Port 8000
   - 모든 API 요청의 진입점
   - 라우팅 및 프록시 역할
   - CORS 설정

3. **Auth Service (FastAPI)** - Port 8001
   - 사용자 인증 및 권한 관리
   - JWT 토큰 기반 인증
   - 사용자 등록/로그인

4. **Redis** - Port 6379 (선택사항)
   - 캐싱 및 세션 스토리지

5. **PostgreSQL** - Port 5432 (선택사항)
   - 데이터베이스

### 네트워크 구성

```
Frontend (3000) → API Gateway (8000) → Auth Service (8001)
                                    ↓
                              Redis (6379)
                                    ↓
                            PostgreSQL (5432)
```

## 🔧 API 엔드포인트

### API Gateway (http://localhost:8000)

- `GET /` - 서비스 상태 확인
- `GET /health` - 헬스체크
- `POST /auth/register` - 사용자 등록
- `POST /auth/login` - 사용자 로그인
- `GET /auth/verify` - 토큰 검증

### Auth Service (http://localhost:8001)

- `GET /` - 서비스 상태 확인
- `GET /health` - 헬스체크
- `POST /register` - 사용자 등록
- `POST /login` - 사용자 로그인
- `GET /verify` - 토큰 검증
- `GET /users/me` - 현재 사용자 정보

## 🧪 테스트

```bash
# 모든 테스트 실행
make test

# 특정 서비스 테스트
cd frontend && pnpm test
cd gateway && pytest
cd auth-service && pytest
```

## 📊 모니터링

### 헬스체크

```bash
# 모든 서비스 상태 확인
make health

# 개별 서비스 상태 확인
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:3000
```

### 로그 확인

```bash
# 모든 서비스 로그
make logs

# 특정 서비스 로그
make logs-frontend
make logs-gateway
make logs-auth
```

## 🔒 보안 설정

### 환경 변수

프로덕션 환경에서는 다음 환경 변수를 설정하세요:

```bash
# Auth Service
SECRET_KEY=your-super-secret-key-here

# Database
POSTGRES_PASSWORD=secure-password
POSTGRES_USER=your-db-user
POSTGRES_DB=your-db-name

# Redis (필요시)
REDIS_PASSWORD=your-redis-password
```

## 🚀 배포

### 프로덕션 배포

```bash
# 프로덕션 환경으로 배포
make deploy
```

### 데이터 백업

```bash
# 데이터베이스 백업
make backup
```

## 🛠️ 개발 가이드

### 새로운 서비스 추가

1. 새 서비스 디렉토리 생성
2. Dockerfile 작성
3. docker-compose.yml에 서비스 추가
4. Makefile에 관련 명령어 추가
5. API Gateway에 프록시 라우트 추가

### 코드 스타일

- **Frontend**: ESLint + Prettier
- **Backend**: Black + isort + flake8

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 생성해주세요. 