'use client';

import { useEffect } from 'react';
// 정확한 상대 경로('../')로 수정했습니다.
import { useAuthStore } from '../stores/authStore';
import api from '../utils/axios';
import axios from 'axios';

// API 응답과 유저 데이터의 타입을 명확하게 정의합니다.
interface User {
  email: string;
  name: string;
  picture: string;
  google_id: string;
}

interface VerifyApiResponse {
  success: boolean;
  user: User;
}

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  // Zustand의 올바른 사용법으로 스토어에서 값을 한번에 가져옵니다.
  const { setUser, clearUser, setLoading } = useAuthStore();
  
  useEffect(() => {
    const verifyUser = async () => {
      setLoading(true);
      try {
        const response = await api.get<VerifyApiResponse>('/auth/verify');
        if (response.data.success) {
          setUser(response.data.user);
        } else {
          clearUser();
        }
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          console.log("User not logged in.");
          clearUser();
        } else {
          console.error("An unexpected error occurred during auth check:", err);
          clearUser();
        }
      }
    };

    verifyUser();
  }, [setUser, clearUser, setLoading]);

  return <>{children}</>;
}