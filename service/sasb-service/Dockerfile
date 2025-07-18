# 1. 베이스 이미지 설정
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /usr/src/app

# 3. KoNLPy 설치에 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    default-jdk \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY ./app ./app
COPY ./data ./data

# 6. 결과물 폴더 생성
RUN mkdir -p /usr/src/app/output

# 7. 스크립트 실행
CMD ["python", "-u", "app/main.py"]