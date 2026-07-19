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

  const isEmpty = messages.length === 0 && !isLoading;

  // 빈 상태에서도 같은 컨테이너를 유지한다 — 라이브 리전은 내용이 삽입되기 "전에"
  // 이미 DOM 에 있어야 스크린리더가 삽입을 감지한다. 빈 상태에서 조기 반환하면
  // 첫 메시지가 리전과 동시에 마운트되어 첫 대화가 통째로 낭독되지 않는다.
  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className={
        isEmpty
          ? 'flex-1 flex items-center justify-center'
          : 'flex-1 overflow-y-auto p-4 space-y-4'
      }
    >
      {isEmpty && (
        <div className="text-center text-muted-foreground">
          <Icon name="solar:chat-round-dots-bold" size={48} className="mx-auto mb-4" />
          <p>AI 상담사에게 사주에 대해 질문해보세요</p>
          <p className="text-sm mt-2">예: “제 성격은 어떤가요?” “직업운은 어떤가요?”</p>
        </div>
      )}

      {/*
        완료된 메시지만 라이브 리전에 둔다.
        스트리밍 중인 답변(아래 streamingOutput 블록)은 토큰마다 DOM이 갱신되므로
        여기 포함시키면 매 토큰 재낭독으로 사용 불가능해진다. 어시스턴트 답변은
        스트리밍이 끝난 뒤에야 messages 에 들어오므로, 이 리전은 완성된 메시지를 한 번만 알린다.
        aria-atomic=false: 새로 추가된 말풍선만 읽고 이전 대화 전체는 다시 읽지 않는다.
      */}
      <div aria-live="polite" aria-atomic="false" className={isEmpty ? undefined : 'space-y-4'}>
        {messages.map((message, index) => (
          <MessageBubble
            key={index}
            message={message}
            onSuggestedQuestionClick={onSuggestedQuestionClick}
          />
        ))}
      </div>

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
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent/25 to-info/25 flex items-center justify-center flex-shrink-0">
            <Icon name="solar:magic-stick-3-bold" size={20} className="text-foreground" />
          </div>
          <div className="max-w-[75%] p-4 rounded-2xl rounded-tl-md bg-muted border border-border">
            <MarkdownRenderer content={streamingOutput} />
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className="inline-block ml-0.5 text-accent"
            >
              ▌
            </motion.span>
          </div>
        </motion.div>
      )}

      {/* 로딩 중이지만 아직 스트리밍 시작 전: 기본 로딩 인디케이터 */}
      {isLoading && !reasoning && !streamingOutput && (
        <div className="flex gap-3" role="status">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent/25 to-info/25 flex items-center justify-center">
            <Icon name="solar:magic-stick-3-bold" size={20} className="text-foreground" />
          </div>
          <div className="bg-muted border border-border rounded-2xl rounded-tl-md p-4">
            {/* 점만으로는 SR 에 아무 의미가 없다 — 상태를 텍스트로 제공한다 */}
            <span className="sr-only">답변 생성 중</span>
            {/*
              점 색: bg-muted(#EDF4FA) 위 bg-muted-foreground(#445A75) = 6.38:1 (비텍스트 3:1 충족).
              이전 bg-muted 는 배경과 동일해 1:1 — 빈 말풍선으로 보였다.
            */}
            <div className="flex gap-1" aria-hidden="true">
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
