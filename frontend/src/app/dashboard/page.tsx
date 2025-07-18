'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../../utils/axios';

interface UserInfo {
  email: string;
  name: string;
  picture?: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const getUserInfo = async () => {
      console.log('=== getUserInfo 함수 시작 ===');
      try {
        const response = await api.get('/auth/verify');
        console.log('API 응답:', response.data);
        
        if (response.status === 200) {
          setUserInfo({
            email: response.data.email || response.data.user?.email,
            name: response.data.name || response.data.user?.name || response.data.email?.split('@')[0],
            picture: response.data.picture || response.data.user?.picture
          });
          console.log('사용자 정보 설정 완료');
        }
      } catch (error) {
        console.error('API 호출 에러:', error);
        router.push('/');
      } finally {
        setIsLoading(false);
      }
    };

    getUserInfo();
  }, []);

  const handleLogout = async () => {
    try {
      // 로그아웃 처리 (쿠키 삭제 등)
      router.push('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!userInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-600">사용자 정보를 찾을 수 없습니다</h2>
          <button
            onClick={() => router.push('/')}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            홈으로 돌아가기
          </button>
        </div>
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
              {userInfo.picture ? (
                <img
                  src={userInfo.picture}
                  alt="Profile"
                  className="w-8 h-8 rounded-full"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
                  {userInfo.name[0].toUpperCase()}
                </div>
              )}
              <span className="text-gray-700">{userInfo.name}</span>
              <button
                onClick={handleLogout}
                className="px-3 py-2 text-sm text-red-600 hover:text-red-800"
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
                  {userInfo.picture ? (
                    <img
                      src={userInfo.picture}
                      alt="Profile"
                      className="w-20 h-20 rounded-full"
                    />
                  ) : (
                    <div className="w-20 h-20 rounded-full bg-blue-500 flex items-center justify-center text-white text-2xl">
                      {userInfo.name[0].toUpperCase()}
                    </div>
                  )}
                  <div>
                    <h3 className="text-xl font-medium text-gray-900">{userInfo.name}</h3>
                    <p className="text-gray-500">{userInfo.email}</p>
                  </div>
                </div>
                <div className="mt-6 border-t border-gray-200 pt-4">
                  <dl className="grid grid-cols-1 gap-4">
                    <div>
                      <dt className="text-sm font-medium text-gray-500">이름</dt>
                      <dd className="mt-1 text-sm text-gray-900">{userInfo.name}</dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">이메일</dt>
                      <dd className="mt-1 text-sm text-gray-900">{userInfo.email}</dd>
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
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">이메일 알림</h3>
                    <p className="text-sm text-gray-500">시스템 알림을 이메일로 받습니다</p>
                  </div>
                  <button className="px-3 py-2 bg-gray-200 text-gray-700 rounded-md text-sm">
                    설정 변경
                  </button>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">보안 설정</h3>
                    <p className="text-sm text-gray-500">2단계 인증 및 보안 옵션을 관리합니다</p>
                  </div>
                  <button className="px-3 py-2 bg-gray-200 text-gray-700 rounded-md text-sm">
                    설정 변경
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 