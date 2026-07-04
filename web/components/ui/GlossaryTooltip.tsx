'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mascot } from './Mascot';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';

interface GlossaryTooltipProps {
  term: string;
  children: React.ReactNode;
  onDetailClick?: (entry: GlossaryEntry) => void;
}

export function GlossaryTooltip({ term, children, onDetailClick }: GlossaryTooltipProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [position, setPosition] = useState<'top' | 'bottom'>('top');
  const triggerRef = useRef<HTMLSpanElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const entry = getGlossaryEntry(term);

  useEffect(() => {
    if (isOpen && triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      const spaceAbove = rect.top;
      const spaceBelow = window.innerHeight - rect.bottom;

      // 위에 공간이 부족하면 아래에 표시
      setPosition(spaceAbove < 150 ? 'bottom' : 'top');
    }
  }, [isOpen]);

  const handleMouseEnter = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      setIsOpen(true);
    }, 300); // 300ms 지연
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      setIsOpen(false);
    }, 200);
  };

  const handleTooltipMouseEnter = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  };

  const handleTooltipMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsOpen(false);
  };

  const handleClick = () => {
    if (entry && onDetailClick) {
      onDetailClick(entry);
    }
  };

  if (!entry) {
    return <>{children}</>;
  }

  return (
    <span className="relative inline-block">
      <span
        ref={triggerRef}
        className="cursor-help border-b border-dotted border-muted-foreground hover:border-primary transition-colors"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      >
        {children}
      </span>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            ref={tooltipRef}
            initial={{ opacity: 0, y: position === 'top' ? 10 : -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: position === 'top' ? 10 : -10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className={`absolute z-50 w-64 p-3 rounded-lg bg-surface border-[1.5px] border-border shadow-card-hover ${
              position === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'
            } left-1/2 -translate-x-1/2`}
            onMouseEnter={handleTooltipMouseEnter}
            onMouseLeave={handleTooltipMouseLeave}
          >
            {/* 화살표 */}
            <div
              className={`absolute left-1/2 -translate-x-1/2 w-2 h-2 bg-surface border-border rotate-45 ${
                position === 'top'
                  ? 'bottom-0 translate-y-1/2 border-r-[1.5px] border-b-[1.5px]'
                  : 'top-0 -translate-y-1/2 border-l-[1.5px] border-t-[1.5px]'
              }`}
            />

            {/* 헤더 — 설명봇 별이 */}
            <div className="flex items-center gap-2 mb-2">
              <Mascot mood="curious" size="xs" className="flex-shrink-0" />
              <span className="text-primary font-bold">{entry.term}</span>
              <span className="text-muted-foreground text-sm font-mono">{entry.hanja}</span>
            </div>

            {/* 한자 풀이 */}
            <p className="text-xs text-muted-foreground mb-2">{entry.hanjaBreakdown}</p>

            {/* 짧은 설명 */}
            <p className="text-sm text-foreground">{entry.shortDesc}</p>

            {/* 더 보기 버튼 */}
            {onDetailClick && (
              <button
                onClick={handleClick}
                className="mt-2 text-xs text-primary hover:text-primary/80 transition-colors"
              >
                자세히 보기 →
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </span>
  );
}

export default GlossaryTooltip;
