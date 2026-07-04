'use client';

import { motion } from 'framer-motion';
import { Icon, Mascot } from '@/components/ui';
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
      {isUser ? (
        <div className="w-10 h-10 rounded-lg border-[1.5px] border-border bg-primary/15 flex items-center justify-center flex-shrink-0">
          <Icon name="solar:user-bold" size={20} className="text-primary" />
        </div>
      ) : (
        <div className="w-10 h-10 flex items-center justify-center flex-shrink-0">
          <Mascot mood="talking" size="sm" />
        </div>
      )}

      {/* Message */}
      <div
        className={cn(
          'max-w-[75%] p-4 rounded-xl border-[1.5px] border-border shadow-block-sm',
          isUser
            ? 'bg-primary/15 rounded-tr-sm'
            : 'bg-surface rounded-tl-sm'
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
              <span className="text-xs px-1.5 py-0.5 rounded-md border-[1.5px] border-border bg-primary/10 text-foreground">
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
          <p className="text-xs text-muted-foreground mt-2 font-mono">
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
                         border-[1.5px] border-border rounded-lg text-foreground
                         shadow-block-sm transition-all hover:-translate-x-px hover:-translate-y-px"
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
