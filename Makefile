# MSA 프로젝트 관리 Makefile

.PHONY: help build up down restart logs clean dev test

# 기본 타겟
help:
	@echo "사용 가능한 명령어:"
	@echo "  build     - 모든 서비스 빌드"
	@echo "  up        - 모든 서비스 시작"
	@echo "  down      - 모든 서비스 중지"
	@echo "  restart   - 모든 서비스 재시작"
	@echo "  logs      - 모든 서비스 로그 확인"
	@echo "  clean     - 모든 컨테이너, 이미지, 볼륨 삭제"
	@echo "  dev       - 개발 모드로 서비스 시작"
	@echo "  test      - 테스트 실행"
	@echo "  frontend  - 프론트엔드만 시작"
	@echo "  backend   - 백엔드 서비스들만 시작"

# 모든 서비스 빌드
build:
	@echo "🔨 모든 서비스 빌드 중..."
	docker-compose build --no-cache

# 모든 서비스 시작
up:
	@echo "🚀 모든 서비스 시작 중..."
	docker-compose up -d

# 모든 서비스 중지
down:
	@echo "🛑 모든 서비스 중지 중..."
	docker-compose down

# 모든 서비스 재시작
restart:
	@echo "🔄 모든 서비스 재시작 중..."
	docker-compose restart

# 로그 확인
logs:
	@echo "📋 서비스 로그 확인 중..."
	docker-compose logs -f

# 특정 서비스 로그 확인
logs-frontend:
	docker-compose logs -f frontend

logs-gateway:
	docker-compose logs -f gateway

logs-auth:
	docker-compose logs -f auth-service

# 개발 모드 (로그와 함께 실행)
dev:
	@echo "🔧 개발 모드로 시작 중..."
	docker-compose up --build

# 프론트엔드만 시작
frontend:
	@echo "🎨 프론트엔드 서비스 시작 중..."
	docker-compose up -d frontend

# 백엔드 서비스들만 시작
backend:
	@echo "⚙️ 백엔드 서비스들 시작 중..."
	docker-compose up -d gateway auth-service redis postgres

# 특정 서비스 빌드 및 시작
build-frontend:
	docker-compose build frontend
	docker-compose up -d frontend

build-gateway:
	docker-compose build gateway
	docker-compose up -d gateway

build-auth:
	docker-compose build auth-service
	docker-compose up -d auth-service

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	@echo "프론트엔드 테스트..."
	cd frontend && pnpm test
	@echo "백엔드 테스트..."
	# 추후 pytest 등으로 테스트 추가

# 시스템 정리
clean:
	@echo "🧹 시스템 정리 중..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	docker volume prune -f

# 완전 정리 (이미지까지 삭제)
clean-all:
	@echo "🗑️ 모든 리소스 삭제 중..."
	docker-compose down -v --remove-orphans --rmi all
	docker system prune -af
	docker volume prune -f

# 헬스체크
health:
	@echo "🏥 서비스 상태 확인 중..."
	@echo "Gateway Health:"
	@curl -f http://localhost:8080/health || echo "Gateway 서비스가 실행되지 않음"
	@echo "\nAuth Service Health:"
	@curl -f http://localhost:8001/health || echo "Auth 서비스가 실행되지 않음"
	@echo "\nFrontend Health:"
	@curl -f http://localhost:3000 || echo "Frontend 서비스가 실행되지 않음"

# 서비스 상태 확인
status:
	@echo "📊 서비스 상태:"
	docker-compose ps

# 개발 환경 설정
setup-dev:
	@echo "🛠️ 개발 환경 설정 중..."
	cd frontend && pnpm install
	@echo "개발 환경 설정 완료!"

# 프로덕션 배포
deploy:
	@echo "🚀 프로덕션 배포 중..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# 백업
backup:
	@echo "💾 데이터 백업 중..."
	docker-compose exec postgres pg_dump -U msa_user msa_db > backup_$(shell date +%Y%m%d_%H%M%S).sql 