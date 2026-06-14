'use client';

import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { MessageBubble } from './MessageBubble';
import { ReasoningDisplay } from './ReasoningDisplay';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Icon } from '@/components/ui';
import type { ChatMessage } from '@/types/saju';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  reasoning?: string;
  streamingOutput?: string;
  isReasoningComplete?: boolean;
  onSuggestedQuestionClick?: (question: string) => void;
}

export function MessageList({
  messages,
  isLoading = false,
  reasoning = '',
  streamingOutput = '',
  isReasoningComplete = false,
  onSuggestedQuestionClick,
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // 메시지, reasoning, 또는 streamingOutput 변경 시 스크롤
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, reasoning, streamingOutput]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center text-gray-400">
          <Icon name="solar:chat-round-dots-bold" size={48} className="mx-auto mb-4" />
          <p>AI 상담사에게 사주에 대해 질문해보세요</p>
          <p className="text-sm mt-2">예: "제 성격은 어떤가요?" "직업운은 어떤가요?"</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <MessageBubble
          key={index}
          message={message}
          onSuggestedQuestionClick={onSuggestedQuestionClick}
        />
      ))}

      {/* 로딩 중: Reasoning 표시 */}
      {isLoading && reasoning && (
        <ReasoningDisplay
          reasoning={reasoning}
          isComplete={isReasoningComplete}
        />
      )}

      {/* 로딩 중: 스트리밍 응답 표시 */}
      {isLoading && streamingOutput && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex gap-3"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/30 to-blue-500/30 flex items-center justify-center flex-shrink-0">
            <Icon name="solar:magic-stick-3-bold" size={20} className="text-foreground" />
          </div>
          <div className="max-w-[75%] p-4 rounded-2xl rounded-tl-md bg-muted border border-border">
            <MarkdownRenderer content={streamingOutput} />
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className="inline-block ml-0.5 text-primary"
            >
              ▌
            </motion.span>
          </div>
        </motion.div>
      )}

      {/* 로딩 중이지만 아직 스트리밍 시작 전: 기본 로딩 인디케이터 */}
      {isLoading && !reasoning && !streamingOutput && (
        <div className="flex gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/30 to-blue-500/30 flex items-center justify-center">
            <Icon name="solar:magic-stick-3-bold" size={20} className="text-foreground" />
          </div>
          <div className="bg-muted border border-border rounded-2xl rounded-tl-md p-4">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
