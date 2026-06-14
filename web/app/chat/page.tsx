'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ChatContainer } from '@/components/chat';
import { Button, Icon, GlassCard } from '@/components/ui';
import { useSajuStore, useChatStore } from '@/stores/sajuStore';

export default function ChatPage() {
  const router = useRouter();
  const { result } = useSajuStore();
  const { clearChat } = useChatStore();

  // Redirect if no saju result
  useEffect(() => {
    if (!result) {
      router.push('/');
    }
  }, [result, router]);

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <GlassCard className="max-w-md p-8 text-center">
          <Icon
            name="solar:chat-round-dots-bold"
            size={48}
            className="text-gray-400 mx-auto mb-4"
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
