from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx
import os
from typing import Dict, Any, List
import logging
from datetime import datetime
import asyncio

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 설정
SASB_SERVICE_PORT = int(os.getenv("SASB_SERVICE_PORT", "8002"))
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend
    "http://localhost:8000",  # Gateway
    "http://localhost:8080",  # Gateway (Docker)
]

# Gateway 서비스에 등록 (최신 방식)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    try:
        async with httpx.AsyncClient() as client:
            # Gateway에 서비스 등록 (실제 구현에서는 서비스 디스커버리 사용)
            logger.info(f"SASB 서비스가 포트 {SASB_SERVICE_PORT}에서 시작됨")
            
    except Exception as e:
        logger.warning(f"Gateway 등록 실패: {e}")
    
    yield  # 애플리케이션 실행
    
    # 종료 시 실행
    logger.info("SASB 서비스 종료")

app = FastAPI(
    title="SASB Analysis Service",
    description="SASB (Sustainability Accounting Standards Board) 분석 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 상태 관리
service_status = {
    "status": "healthy",
    "last_analysis": None,
    "total_analyses": 0,
    "service_start_time": datetime.now().isoformat()
}

@app.get("/")
async def root():
    """SASB 서비스 루트 엔드포인트"""
    return {
        "message": "SASB Analysis Service is running",
        "version": "1.0.0",
        "service": "sasb-service",
        "port": SASB_SERVICE_PORT,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "sasb-service",
        "port": SASB_SERVICE_PORT,
        "timestamp": datetime.now().isoformat(),
        "uptime": service_status["service_start_time"]
    }

@app.get("/status")
async def get_service_status():
    """서비스 상태 정보"""
    return service_status

@app.post("/analyze")
async def analyze_sasb_data(
    data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """SASB 분석 실행"""
    try:
        logger.info(f"SASB 분석 요청 받음: {data}")
        
        # 분석 데이터 검증
        if not data.get("text_data"):
            raise HTTPException(
                status_code=400, 
                detail="분석할 텍스트 데이터가 필요합니다"
            )
        
        # 백그라운드에서 분석 실행
        background_tasks.add_task(run_sasb_analysis, data)
        
        # 즉시 응답 반환
        analysis_id = f"sasb_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "message": "SASB 분석이 시작되었습니다",
            "analysis_id": analysis_id,
            "status": "processing",
            "estimated_time": "5-10분"
        }
        
    except Exception as e:
        logger.error(f"SASB 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")

@app.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """분석 결과 조회"""
    try:
        # 실제 구현에서는 데이터베이스나 파일 시스템에서 결과 조회
        # 여기서는 샘플 응답
        return {
            "analysis_id": analysis_id,
            "status": "completed",
            "results": {
                "sasb_topics": [
                    "GHG Emissions",
                    "Energy Management", 
                    "Water Management",
                    "Waste Management"
                ],
                "materiality_scores": {
                    "GHG Emissions": 8.5,
                    "Energy Management": 7.2,
                    "Water Management": 6.8,
                    "Waste Management": 5.9
                },
                "recommendations": [
                    "온실가스 배출량 감축 계획 수립 필요",
                    "에너지 효율성 개선 방안 검토",
                    "물 사용량 최적화 전략 개발"
                ]
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"분석 결과 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=f"결과 조회 중 오류 발생: {str(e)}")

@app.get("/sasb-topics")
async def get_sasb_topics():
    """SASB 주제 목록 조회"""
    sasb_topics = [
        {
            "code": "GHG",
            "name": "GHG Emissions",
            "description": "온실가스 배출량 관리"
        },
        {
            "code": "ENERGY",
            "name": "Energy Management",
            "description": "에너지 관리 및 효율성"
        },
        {
            "code": "WATER",
            "name": "Water Management", 
            "description": "물 자원 관리"
        },
        {
            "code": "WASTE",
            "name": "Waste Management",
            "description": "폐기물 관리"
        },
        {
            "code": "LABOR",
            "name": "Labor Practices",
            "description": "노동 관행 및 인권"
        }
    ]
    
    return {
        "sasb_topics": sasb_topics,
        "total_count": len(sasb_topics)
    }

async def run_sasb_analysis(data: Dict[str, Any]):
    """백그라운드에서 실행되는 SASB 분석 함수"""
    try:
        logger.info("SASB 분석 백그라운드 작업 시작")
        
        # 실제 분석 로직 (시뮬레이션)
        await asyncio.sleep(2)  # 분석 시뮬레이션
        
        # 분석 완료 후 상태 업데이트
        service_status["last_analysis"] = datetime.now().isoformat()
        service_status["total_analyses"] += 1
        
        logger.info("SASB 분석 완료")
        
    except Exception as e:
        logger.error(f"SASB 분석 백그라운드 작업 오류: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=SASB_SERVICE_PORT,
        log_level="info"
    )
