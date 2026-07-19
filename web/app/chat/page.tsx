'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ChatContainer } from '@/components/chat';
import { Button, Icon, GlassCard } from '@/components/ui';
import { useSajuStore, useChatStore } from '@/stores/sajuStore';

export default function ChatPage() {
  const { result, hasHydrated } = useSajuStore();
  const { clearChat } = useChatStore();

  // 저장된 결과 복원 전에는 판단을 보류한다 (자동 리다이렉트 없음 — 사용자가 직접 선택한다).
  if (!hasHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Icon
          name="solar:refresh-bold"
          size={32}
          className="text-muted-foreground animate-spin"
          aria-label="불러오는 중"
        />
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <GlassCard className="max-w-md p-8 text-center">
          <Icon
            name="solar:chat-round-dots-bold"
            size={48}
            className="text-muted-foreground mx-auto mb-4"
          />
          <h2 className="text-xl font-bold text-foreground mb-2">
            사주 분석이 필요합니다
          </h2>
          <p className="text-muted-foreground mb-6">
            AI 상담을 시작하려면 먼저 사주 분석을 진행해주세요.
          </p>
          <Link href="/">
            <Button>
              <Icon name="solar:home-2-bold" size={20} className="mr-2" />
              홈으로 가기
            </Button>
          </Link>
        </GlassCard>
      </div>
    );
  }

  return (
    <main className="min-h-screen py-6 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-6"
        >
          <div>
            <h1 className="text-2xl font-bold text-foreground">AI 사주 상담</h1>
            <p className="text-muted-foreground text-sm">
              {result.birth_info.name}님의 사주를 바탕으로 상담합니다
            </p>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={clearChat}
            >
              <Icon name="solar:refresh-bold" size={16} className="mr-1" />
              대화 초기화
            </Button>
            <Link href="/result">
              <Button variant="outline" size="sm">
                <Icon name="solar:chart-2-bold" size={16} className="mr-1" />
                분석 결과
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Chat Container */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <ChatContainer />
        </motion.div>
      </div>
    </main>
  );
}
