'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AuthCallbackPage() {
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('로그인 처리 중...');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        const userEmail = urlParams.get('user');
        const error = urlParams.get('error');
        console.log('00000', token, userEmail, error);
        if (error) {
          setStatus('error');
          setMessage(`로그인 실패: ${decodeURIComponent(error)}`);
          return;
        }
        console.log('11111', token);
        if (token && userEmail) {
          // httpOnly 쿠키 방식에서는 토큰이 자동으로 설정됨
          // 더 이상 localStorage에 저장하지 않음
          
          setStatus('success');
          setMessage('로그인 성공! 대시보드로 이동합니다...');
          console.log('22222', token);
          // 2초 후 대시보드로 리디렉션
          setTimeout(() => {
            router.push('/dashboard');
          }, 2000);
        } else {
          // 새로운 OAuth 방식에서는 바로 메인 페이지로 리디렉션됨
          setStatus('success');
          setMessage('로그인 처리 중...');
          console.log('33333', token);
          router.push('/');
        }
      } catch (err) {
        console.error('Callback processing error:', err);
        setStatus('error');
        setMessage('로그인 처리 중 오류가 발생했습니다.');
        console.log('44444', err);
      }
    };

    handleCallback();
  }, [router]);

  const handleRetry = () => {
    router.push('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          {status === 'loading' && (
            <div>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <h2 className="mt-6 text-2xl font-bold text-gray-900">로그인 처리 중</h2>
              <p className="mt-2 text-gray-600">{message}</p>
            </div>
          )}

          {status === 'success' && (
            <div>
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="mt-6 text-2xl font-bold text-gray-900">로그인 성공!</h2>
              <p className="mt-2 text-gray-600">{message}</p>
            </div>
          )}

          {status === 'error' && (
            <div>
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
              <h2 className="mt-6 text-2xl font-bold text-gray-900">로그인 실패</h2>
              <p className="mt-2 text-gray-600">{message}</p>
              <button
                onClick={handleRetry}
                className="mt-4 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                다시 로그인하기
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 