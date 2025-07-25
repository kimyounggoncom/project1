'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
// 정확한 상대 경로('../')로 수정했습니다.
import api from '../utils/axios';
import axios from 'axios';

export default function Home() {
  const [isLoading, setIsLoading] = = useState(false);
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
      setMessage('❌ 구글 로그인 중 네트워크 오류가 발생했습니다. 개발자 콘솔을 확인해주세요.');
      console.error('--- DETAILED LOGIN ERROR ---');
      if (axios.isAxiosError(err)) {
        if (err.response) {
          console.error('Response Data:', err.response.data);
          console.error('Response Status:', err.response.status);
        } else if (err.request) {
          console.error('No Response Received. This is often a CORS or Network issue.');
        } else {
          console.error('Error setting up request:', err.message);
        }
      } else {
        console.error('An unexpected non-Axios error occurred:', err);
      }
      console.error('--- END OF DETAILED ERROR ---');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-800">MSA Dashboard</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleGoogleLogin}
                disabled={isLoading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? '로그인 중...' : 'Google로 로그인'}
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0 text-center">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              MSA 인증 시스템에 오신 것을 환영합니다
            </h2>
            <p className="text-lg text-gray-600">
              안전하고 효율적인 인증 시스템으로 시작하세요
            </p>
            {message && <p className="mt-4 text-red-500">{message}</p>}
          </div>
        </div>
      </main>
    </div>
  );
}