'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '@/components/ui';
import { cn } from '@/lib/utils';

interface ReasoningDisplayProps {
  reasoning: string;
  isComplete: boolean;
  className?: string;
}

export function ReasoningDisplay({
  reasoning,
  isComplete,
  className,
}: ReasoningDisplayProps) {
  if (!reasoning) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10, height: 0 }}
        animate={{ opacity: 1, y: 0, height: 'auto' }}
        exit={{ opacity: 0, y: -10, height: 0 }}
        className={cn('flex gap-3', className)}
      >
        {/* Avatar */}
        <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-surface border-[1.5px] border-border shadow-block-sm">
          <Icon
            name="solar:brain-bold"
            size={20}
            className={cn('text-warning', !isComplete && 'animate-pulse')}
          />
        </div>

        {/* Reasoning Content */}
        <div className="flex-1 p-4 rounded-xl bg-surface border-[1.5px] border-border shadow-card">
          {/* Header */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-medium text-warning">
              AI 사고 과정
            </span>
            {!isComplete && (
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="flex items-center gap-1"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-warning" />
                <div className="w-1.5 h-1.5 rounded-full bg-warning animation-delay-200" />
                <div className="w-1.5 h-1.5 rounded-full bg-warning animation-delay-400" />
              </motion.div>
            )}
            {isComplete && (
              <Icon
                name="solar:check-circle-bold"
                size={14}
                className="text-warning"
              />
            )}
          </div>

          {/* Reasoning Text */}
          <div className="text-sm text-muted-foreground leading-relaxed italic">
            {reasoning}
            {!isComplete && (
              <motion.span
                animate={{ opacity: [1, 0] }}
                transition={{ duration: 0.8, repeat: Infinity }}
                className="inline-block ml-0.5 text-warning"
              >
                ▌
              </motion.span>
            )}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
