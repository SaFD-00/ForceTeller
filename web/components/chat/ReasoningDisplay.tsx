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
        <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br from-amber-500/30 to-orange-500/30">
          <Icon
            name="solar:brain-bold"
            size={20}
            className={cn('text-amber-400', !isComplete && 'animate-pulse')}
          />
        </div>

        {/* Reasoning Content */}
        <div className="flex-1 p-4 rounded-2xl rounded-tl-md bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/20">
          {/* Header */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-medium text-amber-400/80">
              AI 사고 과정
            </span>
            {!isComplete && (
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="flex items-center gap-1"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animation-delay-200" />
                <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animation-delay-400" />
              </motion.div>
            )}
            {isComplete && (
              <Icon
                name="solar:check-circle-bold"
                size={14}
                className="text-amber-400/60"
              />
            )}
          </div>

          {/* Reasoning Text */}
          <div className="text-sm text-gray-600 leading-relaxed italic">
            {reasoning}
            {!isComplete && (
              <motion.span
                animate={{ opacity: [1, 0] }}
                transition={{ duration: 0.8, repeat: Infinity }}
                className="inline-block ml-0.5 text-amber-400"
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
