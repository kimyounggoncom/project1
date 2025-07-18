'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '../utils/axios';

interface ClientLayoutProps {
  children: React.ReactNode;
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        console.log('🔍 Checking authentication...');
        
        // 공개 페이지는 인증 체크 건너뛰기
        if (pathname === '/login' || pathname === '/') {
          console.log('✅ Skipping auth check for public page');
          setIsLoading(false);
          return;
        }

        console.log('📡 Calling /auth/verify endpoint...');
        const response = await api.get('/auth/verify');
        
        console.log('✅ Auth check response:', response.status);
        if (response.status === 200) {
          console.log('🎉 Authentication successful!');
          setIsAuthenticated(true);
        }
      } catch (error: any) {
        console.error('❌ Authentication failed:', error);
        setIsAuthenticated(false);
        
        // 보호된 페이지에서 인증 실패시 홈페이지로 리다이렉트
        if (pathname !== '/' && pathname !== '/login') {
          router.push('/');
        }
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [pathname]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // 보호된 페이지에 대한 접근 제어
  if (!isAuthenticated && pathname !== '/' && pathname !== '/login') {
    router.push('/');
    return null;
  }

  return <>{children}</>;
} 