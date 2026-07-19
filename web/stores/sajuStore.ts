// Zustand 상태 관리

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { SajuResultDisplay, ChatMessage } from '@/types/saju';

interface SajuState {
  result: SajuResultDisplay | null;
  isLoading: boolean;
  error: string | null;
  /**
   * localStorage 복원이 끝났는지 여부. 첫 렌더에는 항상 false다.
   * 이 값이 false인 동안 `result === null`은 "결과 없음"이 아니라 "아직 모름"이므로,
   * 소비하는 화면은 빈 상태를 보여주거나 리다이렉트해서는 안 된다.
   */
  hasHydrated: boolean;
  setResult: (result: SajuResultDisplay) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearResult: () => void;
  setHasHydrated: (hydrated: boolean) => void;
}

export const useSajuStore = create<SajuState>()(
  persist(
    (set) => ({
      result: null,
      isLoading: false,
      error: null,
      hasHydrated: false,
      setResult: (result) => set({ result, error: null }),
      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error, isLoading: false }),
      clearResult: () => set({ result: null, error: null }),
      setHasHydrated: (hasHydrated) => set({ hasHydrated }),
    }),
    {
      name: 'saju-storage',
      partialize: (state) => ({ result: state.result }),
      // 복원 성공/실패(저장값 없음·JSON 파손 포함) 어느 쪽이든 게이트를 열어야
      // 화면이 로딩 상태에 영구히 갇히지 않는다.
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true);
      },
    }
  )
);

interface ChatState {
  sessionId: string | null;
  messages: ChatMessage[];
  setSessionId: (id: string) => void;
  addMessage: (message: ChatMessage) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  sessionId: null,
  messages: [],
  setSessionId: (sessionId) => set({ sessionId }),
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  clearChat: () => set({ messages: [], sessionId: null }),
}));
