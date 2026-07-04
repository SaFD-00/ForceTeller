'use client';

import { motion } from 'framer-motion';
import { Icon } from '@/components/ui';
import { cn } from '@/lib/utils';
import { MarkdownRenderer } from './MarkdownRenderer';
import type { ChatMessage } from '@/types/saju';

interface MessageBubbleProps {
  message: ChatMessage;
  onSuggestedQuestionClick?: (question: string) => void;
}

function confidenceLabel(confidence: number): string {
  if (confidence >= 0.85) return '신뢰도 높음';
  if (confidence >= 0.7) return '신뢰도 보통';
  return '신뢰도 참고';
}

export function MessageBubble({ message, onSuggestedQuestionClick }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        'flex gap-3',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
          isUser
            ? 'bg-primary/20'
            : 'bg-gradient-to-br from-accent/25 to-info/25'
        )}
      >
        <Icon
          name={isUser ? 'solar:user-bold' : 'solar:magic-stick-3-bold'}
          size={20}
          className={isUser ? 'text-primary' : 'text-foreground'}
        />
      </div>

      {/* Message */}
      <div
        className={cn(
          'max-w-[75%] p-4 rounded-2xl',
          isUser
            ? 'bg-primary/20 border border-primary/30 rounded-tr-md'
            : 'bg-muted border border-border rounded-tl-md'
        )}
      >
        {/* 에이전트 출처·신뢰도 배지 (어시스턴트) */}
        {!isUser && message.agent_display_name && (
          <div className="flex items-center gap-1.5 mb-2 pb-2 border-b border-border">
            <Icon name="solar:verified-check-bold" size={14} className="text-primary" />
            <span className="text-xs font-medium text-primary">
              {message.agent_display_name} 에이전트
            </span>
            {typeof message.confidence === 'number' && (
              <span className="text-xs px-1.5 py-0.5 rounded-full bg-primary/10 text-muted-foreground">
                {confidenceLabel(message.confidence)}
              </span>
            )}
          </div>
        )}

        {isUser ? (
          <p className="text-foreground whitespace-pre-wrap leading-relaxed">
            {message.content}
          </p>
        ) : (
          <MarkdownRenderer content={message.content} />
        )}
        {message.timestamp && (
          <p className="text-xs text-muted-foreground mt-2">
            {new Date(message.timestamp).toLocaleTimeString('ko-KR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        )}

        {/* 추천 질문 버튼 */}
        {!isUser && message.suggested_questions && message.suggested_questions.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-border">
            {message.suggested_questions.map((question, idx) => (
              <button
                key={idx}
                onClick={() => onSuggestedQuestionClick?.(question)}
                className="px-3 py-1.5 text-sm bg-primary/10 hover:bg-primary/20
                         border border-primary/30 rounded-full text-foreground
                         transition-colors hover:text-foreground"
              >
                {question}
              </button>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
