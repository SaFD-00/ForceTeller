// Zustand 상태 관리

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { SajuResultDisplay, ChatMessage } from '@/types/saju';

interface SajuState {
  result: SajuResultDisplay | null;
  isLoading: boolean;
  error: string | null;
  setResult: (result: SajuResultDisplay) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearResult: () => void;
}

export const useSajuStore = create<SajuState>()(
  persist(
    (set) => ({
      result: null,
      isLoading: false,
      error: null,
      setResult: (result) => set({ result, error: null }),
      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error, isLoading: false }),
      clearResult: () => set({ result: null, error: null }),
    }),
    {
      name: 'saju-storage',
      partialize: (state) => ({ result: state.result }),
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
