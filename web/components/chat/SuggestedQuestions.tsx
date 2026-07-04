'use client';

import { motion } from 'framer-motion';
import { Icon } from '@iconify/react';

interface SuggestedQuestionsProps {
  questions: string[];
  onQuestionClick: (question: string) => void;
  disabled?: boolean;
}

export function SuggestedQuestions({
  questions,
  onQuestionClick,
  disabled = false,
}: SuggestedQuestionsProps) {
  // 질문이 없으면 표시하지 않음
  if (!questions || questions.length === 0) {
    return null;
  }

  // 최대 3개까지만 표시
  const displayQuestions = questions.slice(0, 3);

  return (
    <div className="px-4 py-2 border-t border-border">
      <div className="text-xs text-muted-foreground mb-2 flex items-center gap-1">
        <Icon icon="mdi:lightbulb-outline" className="w-3.5 h-3.5" />
        이어서 질문해보세요
      </div>
      <div className="flex flex-wrap gap-2">
        {displayQuestions.map((question, index) => (
          <motion.button
            key={index}
            whileHover={{ scale: disabled ? 1 : 1.02 }}
            whileTap={{ scale: disabled ? 1 : 0.98 }}
            onClick={() => !disabled && onQuestionClick(question)}
            disabled={disabled}
            className={`
              inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full
              text-sm transition-all duration-200 text-left
              ${disabled
                ? 'bg-muted text-muted-foreground cursor-not-allowed'
                : 'bg-muted text-muted-foreground hover:bg-accent/20 hover:text-foreground cursor-pointer'
              }
            `}
          >
            <Icon icon="mdi:chat-question-outline" className="w-4 h-4 flex-shrink-0" />
            <span className="line-clamp-1">{question}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
