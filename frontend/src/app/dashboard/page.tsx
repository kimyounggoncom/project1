'use client';

// 정확한 상대 경로('../../')로 수정했습니다.
import { useAuthStore } from '../../stores/authStore';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '../../utils/axios';

export default function DashboardPage() {
  // Zustand의 올바른 사용법으로 스토어에서 값을 한번에 가져옵니다.
  const { user, isLoading, clearUser } = useAuthStore();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // 인증 확인이 끝났고(isLoading === false), 유저 정보가 없으면 홈페이지로 리디렉션합니다.
    if (!isLoading && !user) {
      router.replace('/');
    }
  }, [user, isLoading, router]);
  
  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Failed to logout from server, but proceeding with client-side logout:', error);
    } finally {
      clearUser();
      router.push('/');
    }
  };

  // isLoading 상태이거나, 아직 user 정보가 설정되지 않았을 때 로딩 화면을 보여줍니다.
  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // 유저 정보가 있으면, 대시보드 내용을 보여줍니다.
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-800">MSA Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              {user.picture ? (
                <img src={user.picture} alt="Profile" className="w-8 h-8 rounded-full" />
              ) : (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                  {user.name[0].toUpperCase()}
                </div>
              )}
              <span className="text-gray-700 font-medium">{user.name}</span>
              <button onClick={handleLogout} className="px-3 py-2 text-sm text-red-600 hover:text-red-800 font-medium">
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </nav>
      {/* ... 이하 대시보드 UI ... */}
    </div>
  );
}