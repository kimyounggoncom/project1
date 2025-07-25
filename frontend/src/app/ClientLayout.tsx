// frontend/src/app/ClientLayout.tsx

'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '../stores/authStore';  // '../' 로 경로 수정
import api from '../utils/axios';          // '../' 로 경로 수정
import axios from 'axios';

// --- 타입 정의 (기존과 동일) ---
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
  const { setUser, clearUser } = useAuthStore();
  const [isAuthChecked, setIsAuthChecked] = useState(false);

  useEffect(() => {
    const verifyUser = async () => {
      console.log("Checking authentication...");
      try {
        const response = await api.get<VerifyApiResponse>('/auth/verify');
        
        if (response.data.success) {
          setUser(response.data.user);
        } else {
          clearUser();
        }
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          console.log("Skipping auth check for public page (user not logged in).");
          clearUser();
        } else {
          console.error("An unexpected error occurred during auth check:", err);
          clearUser();
        }
      } finally {
        setIsAuthChecked(true);
      }
    };

    verifyUser();
  }, [setUser, clearUser]);

  if (!isAuthChecked) {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <div>Loading application...</div>
        </div>
    );
  }

  return <>{children}</>;
}