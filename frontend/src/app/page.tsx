'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../utils/axios';
// ▼▼▼ axios와 AxiosError 타입을 가져오는 import를 추가합니다. ▼▼▼
import axios, { AxiosError } from 'axios';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const router = useRouter();

  const handleGoogleLogin = async () => {
    setIsLoading(true);
    setMessage('🔄 Google 로그인을 시작합니다...');
    try {
      const response = await api.get('/auth/google/login');
      const data = response.data;
      if (data.success && data.auth_url) {
        window.location.href = data.auth_url;
      } else {
        setMessage(`❌ 구글 로그인 URL 생성에 실패했습니다: ${data.message || '알 수 없는 오류'}`);
      }
    } catch (err) {
      // ▼▼▼▼▼ 타입 에러를 해결한 최종 디버깅 코드입니다. ▼▼▼▼▼
      setMessage('❌ 구글 로그인 중 네트워크 오류가 발생했습니다. 개발자 콘솔을 확인해주세요.');
      console.error('--- DETAILED LOGIN ERROR ---');
      
      // err가 Axios 에러인지 확인하는 과정을 추가합니다.
      if (axios.isAxiosError(err)) {
        if (err.response) {
          // 서버가 응답했지만, 에러 상태 코드(4xx, 5xx)를 보낸 경우
          console.error('Response Data:', err.response.data);
          console.error('Response Status:', err.response.status);
          console.error('Response Headers:', err.response.headers);
        } else if (err.request) {
          // 요청은 보냈지만, 서버로부터 응답을 받지 못한 경우 (CORS, 네트워크 단절 등)
          console.error('No Response Received. This is often a CORS or Network issue.');
          console.error('Request Object:', err.request);
        } else {
          // 요청을 설정하는 단계에서 문제가 발생한 경우
          console.error('Error setting up request:', err.message);
        }
        console.error('Full Error Config:', err.config);
      } else {
        // Axios 에러가 아닌 다른 종류의 에러인 경우
        console.error('An unexpected non-Axios error occurred:', err);
      }
      
      console.error('--- END OF DETAILED ERROR ---');
      // ▲▲▲▲▲ 여기까지가 타입 에러를 해결한 부분입니다. ▲▲▲▲▲
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 상단 네비게이션 바 */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-800">MSA Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
              >
                시작하기
              </button>
              <button
                onClick={handleGoogleLogin}
                disabled={isLoading}
                className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    로그인 중...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                      <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                      <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                      <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Google로 로그인
                  </div>
                )}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 메인 콘텐츠 */}
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg">
            <div className="p-6">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  MSA 인증 시스템에 오신 것을 환영합니다
                </h2>
                <p className="text-lg text-gray-600">
                  안전하고 효율적인 인증 시스템으로 시작하세요
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-medium text-blue-800">Frontend</h3>
                  <p className="text-sm text-blue-600 mt-1">Next.js + React</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="font-medium text-green-800">Gateway</h3>
                  <p className="text-sm text-green-600 mt-1">FastAPI</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h3 className="font-medium text-purple-800">Auth Service</h3>
                  <p className="text-sm text-purple-600 mt-1">OAuth + JWT</p>
                </div>
              </div>

              {message && (
                <div className={`mt-6 p-4 rounded-lg ${
                  message.includes('❌') 
                    ? 'bg-red-50 text-red-700 border border-red-200' 
                    : 'bg-blue-50 text-blue-700 border border-blue-200'
                }`}>
                  <p className="text-sm text-center">{message}</p>
                </div>
              )}
            </div>
          </div>

          <div className="mt-6 bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">시스템 정보</h3>
            <div className="space-y-2 text-sm text-gray-600">
              <p>• Gateway: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}</p>
              <p>• Frontend → Gateway → Auth Service</p>
              <p>• 실시간 JWT 토큰 기반 인증</p>
            </div>
          </div>
        </div>
      </div>

      {/* 하단 정보 */}
      <footer className="bg-white shadow mt-8">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            로그인하면 서비스 이용약관 및 개인정보처리방침에 동의하게 됩니다.
          </p>
        </div>
      </footer>
    </div>
  );
}