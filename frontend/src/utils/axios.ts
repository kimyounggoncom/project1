// 파일 경로: frontend/src/utils/axios.ts

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_BASE_URL) {
  console.error("치명적 에러: NEXT_PUBLIC_API_URL 환경 변수가 설정되지 않았습니다.");
  if (typeof window !== 'undefined') {
    alert("API 서버 주소가 설정되지 않았습니다. .env.local 파일을 확인해주세요.");
  }
}

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // 다른 도메인으로 쿠키를 전송하기 위해 필수!
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// ▼▼▼▼▼ 여기가 최종적으로 수정된 응답 인터셉터입니다 ▼▼▼▼▼
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 401 에러가 발생했는지 확인합니다.
    if (error.response?.status === 401) {
      // 하지만, 그 에러가 '/auth/verify' 경로에서 발생한 것은 아닌지 추가로 확인합니다.
      // '/auth/verify'에서 발생한 401은 의도된 동작일 수 있으므로, 페이지를 강제로 이동시키지 않습니다.
      if (error.config.url !== '/auth/verify') {
        // '/auth/verify' 가 아닌 다른 API에서 401 에러가 발생하면, 그때 홈페이지로 보냅니다.
        window.location.href = '/';
      }
    }
    // 다른 모든 에러는 그대로 반환하여, 각 컴포넌트가 처리할 수 있도록 합니다.
    return Promise.reject(error);
  }
);
// ▲▲▲▲▲ 여기까지가 수정된 부분입니다 ▲▲▲▲▲

export default api;