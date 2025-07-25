'use client';

// ▼▼▼▼▼ 올바른 경로로 수정합니다. ('../../') ▼▼▼▼▼
import { useAuthStore } from '../../stores/authStore';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '../../utils/axios';
// ▲▲▲▲▲ 경로 수정 끝 ▲▲▲▲▲

export default function DashboardPage() {
  // ▼▼▼▼▼ Zustand의 올바른 사용법으로 수정합니다. ▼▼▼▼▼
  // 스토어에서 필요한 상태와 함수들을 객체 분해 할당으로 한 번에 가져옵니다.
  const { user, isLoading, clearUser } = useAuthStore();
  // ▲▲▲▲▲ 사용법 수정 끝 ▲▲▲▲▲

  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
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

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

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
              {user.picture ? (
                <img
                  src={user.picture}
                  alt="Profile"
                  className="w-8 h-8 rounded-full"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                  {user.name[0].toUpperCase()}
                </div>
              )}
              <span className="text-gray-700 font-medium">{user.name}</span>
              <button
                onClick={handleLogout}
                className="px-3 py-2 text-sm text-red-600 hover:text-red-800 font-medium"
              >
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 메인 콘텐츠 */}
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* 탭 네비게이션 */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('overview')}
              className={`${
                activeTab === 'overview'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              개요
            </button>
            <button
              onClick={() => setActiveTab('profile')}
              className={`${
                activeTab === 'profile'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              프로필
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`${
                activeTab === 'settings'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              설정
            </button>
          </nav>
        </div>

        {/* 탭 콘텐츠 */}
        <div className="bg-white shadow rounded-lg">
          {activeTab === 'overview' && (
            <div className="p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">시스템 개요</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">사용자 프로필</h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  {user.picture ? (
                    <img
                      src={user.picture}
                      alt="Profile"
                      className="w-20 h-20 rounded-full"
                    />
                  ) : (
                    <div className="w-20 h-20 rounded-full bg-blue-500 flex items-center justify-center text-white text-2xl font-bold">
                      {user.name[0].toUpperCase()}
                    </div>
                  )}
                  <div>
                    <h3 className="text-xl font-medium text-gray-900">{user.name}</h3>
                    <p className="text-gray-500">{user.email}</p>
                  </div>
                </div>
                <div className="mt-6 border-t border-gray-200 pt-4">
                  <dl className="grid grid-cols-1 gap-4">
                    <div>
                      <dt className="text-sm font-medium text-gray-500">이름</dt>
                      <dd className="mt-1 text-sm text-gray-900">{user.name}</dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">이메일</dt>
                      <dd className="mt-1 text-sm text-gray-900">{user.email}</dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">인증 방식</dt>
                      <dd className="mt-1 text-sm text-gray-900">Google OAuth</dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">설정</h2>
              <p>설정 페이지입니다.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}