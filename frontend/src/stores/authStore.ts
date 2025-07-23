// 파일 경로: frontend/src/stores/authStore.ts

import { create } from 'zustand';

// 1. 유저 데이터의 모양(타입)을 정의합니다.
// 이 타입은 ClientLayout.tsx에서도 사용한 것과 동일해야 합니다.
interface User {
  email: string;
  name: string;
  picture: string;
  google_id: string;
}

// 2. 스토어(Store)가 가질 상태와 함수들의 타입을 정의합니다.
interface AuthState {
  user: User | null; // 유저 정보는 있거나(User) 없거나(null) 둘 중 하나입니다.
  setUser: (user: User) => void; // 유저 정보를 저장하는 함수
  clearUser: () => void; // 유저 정보를 삭제(로그아웃)하는 함수
}

// 3. Zustand를 사용하여 스토어를 생성합니다.
export const useAuthStore = create<AuthState>((set) => ({
  // 초기 상태
  user: null,

  // 유저 정보를 상태에 저장하는 'setUser' 액션(함수)
  setUser: (user) => set({ user: user }),

  // 유저 정보를 null로 만들어 상태를 초기화하는 'clearUser' 액션(함수)
  clearUser: () => set({ user: null }),
}));