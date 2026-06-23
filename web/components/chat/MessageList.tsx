'use client';

import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { MessageBubble } from './MessageBubble';
import { ReasoningDisplay } from './ReasoningDisplay';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Mascot } from '@/components/ui';
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
  const containerRef = useRef<HTMLDivElement>(null);
  // 사용자가 답변 생성 영역(스크롤 하단)에 있는지 추적
  const isAtBottomRef = useRef(true);

  const handleScroll = () => {
    const container = containerRef.current;
    if (!container) return;
    isAtBottomRef.current =
      container.scrollHeight - container.scrollTop - container.clientHeight < 80;
  };

  // 메시지/reasoning/streamingOutput 변경 시, 사용자가 생성 영역(하단)에 있을 때만 컨테이너 내부만 스크롤
  // (scrollIntoView는 페이지 전체 등 모든 스크롤 조상을 함께 움직여 다른 창까지 끌려 내려감)
  useEffect(() => {
    if (!isAtBottomRef.current) return;
    const container = containerRef.current;
    if (container) container.scrollTop = container.scrollHeight;
  }, [messages, reasoning, streamingOutput]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="text-center">
          <Mascot mood="happy" size="xl" floating className="mx-auto mb-4" />
          <p className="font-bold text-foreground">별이에게 사주에 대해 물어보세요</p>
          <p className="text-sm mt-2 text-muted-foreground">예: "제 성격은 어떤가요?" "직업운은 어떤가요?"</p>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto p-4 space-y-4"
    >
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
          <div className="w-10 h-10 flex items-center justify-center flex-shrink-0">
            <Mascot mood="talking" size="sm" />
          </div>
          <div className="max-w-[75%] p-4 rounded-xl rounded-tl-sm bg-surface border-[1.5px] border-border shadow-block-sm">
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
          <div className="w-10 h-10 flex items-center justify-center">
            <Mascot mood="thinking" size="sm" />
          </div>
          <div className="bg-surface border-[1.5px] border-border rounded-xl rounded-tl-sm shadow-block-sm p-4">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
