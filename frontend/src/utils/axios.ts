// 파일 경로: frontend/src/utils/axios.ts

import axios from 'axios';

// ▼▼▼ 이 부분이 가장 중요합니다! || 'http://localhost:8080' 부분을 완전히 삭제합니다. ▼▼▼
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// 만약 API_BASE_URL이 없다면 에러를 발생시켜서 문제를 즉시 알 수 있게 합니다. (강력 추천)
if (!API_BASE_URL) {
  console.error("치명적 에러: NEXT_PUBLIC_API_URL 환경 변수가 설정되지 않았습니다.");
  // 로컬 개발 환경을 위한 임시 경고
  if (typeof window !== 'undefined') {
    alert("API 서버 주소가 설정되지 않았습니다. .env.local 파일을 확인해주세요.");
  }
}

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 응답 인터셉터 (기존 코드와 동일)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default api;