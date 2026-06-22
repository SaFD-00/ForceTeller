'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from './Icon';
import type { GlossaryEntry } from '@/data/saju-glossary';

interface GlossaryModalProps {
  entry: GlossaryEntry | null;
  isOpen: boolean;
  onClose: () => void;
}

// 카테고리별 색상
const categoryColors: Record<GlossaryEntry['category'], string> = {
  '천간': 'bg-green-500/20 text-green-400',
  '지지': 'bg-blue-500/20 text-blue-400',
  '십성': 'bg-purple-500/20 text-purple-400',
  '12운성': 'bg-yellow-500/20 text-yellow-400',
  '신살': 'bg-red-500/20 text-red-400',
  '합충': 'bg-orange-500/20 text-orange-400',
  '용어': 'bg-gray-500/20 text-gray-400',
};

export function GlossaryModal({ entry, isOpen, onClose }: GlossaryModalProps) {
  // ESC 키로 닫기
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!entry) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 배경 오버레이 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
          />

          {/* 모달 (데스크톱) / 바텀시트 (모바일) */}
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed z-50
              bottom-0 left-0 right-0 max-h-[80vh]
              md:bottom-auto md:left-1/2 md:top-1/2 md:-translate-x-1/2 md:-translate-y-1/2
              lg:left-[37.5%]
              md:max-w-md md:w-full md:max-h-[80vh]
              bg-background rounded-t-2xl md:rounded-2xl
              border border-border shadow-card
              overflow-hidden"
          >
            {/* 모바일 드래그 핸들 */}
            <div className="md:hidden flex justify-center py-2">
              <div className="w-10 h-1 bg-muted rounded-full" />
            </div>

            {/* 헤더 */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-border">
              <div className="flex items-center gap-3">
                <span className="text-2xl font-bold text-foreground">{entry.term}</span>
                <span className="text-lg text-muted-foreground">{entry.hanja}</span>
              </div>
              <button
                onClick={onClose}
                aria-label="닫기"
                className="p-2 rounded-full hover:bg-muted transition-colors"
              >
                <Icon name="solar:close-circle-bold" size={24} className="text-muted-foreground" />
              </button>
            </div>

            {/* 본문 */}
            <div className="px-5 py-4 overflow-y-auto max-h-[60vh]">
              {/* 카테고리 태그 */}
              <div className="mb-4">
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${categoryColors[entry.category]}`}>
                  {entry.category}
                </span>
              </div>

              {/* 한자 풀이 */}
              <div className="mb-4 p-3 bg-muted rounded-lg">
                <p className="text-xs text-muted-foreground mb-1">한자 풀이</p>
                <p className="text-sm text-foreground">{entry.hanjaBreakdown}</p>
              </div>

              {/* 짧은 설명 */}
              <div className="mb-4">
                <p className="text-xs text-muted-foreground mb-1">간단 설명</p>
                <p className="text-base text-primary font-medium">{entry.shortDesc}</p>
              </div>

              {/* 상세 설명 */}
              <div className="mb-4">
                <p className="text-xs text-muted-foreground mb-2">상세 설명</p>
                <p className="text-sm text-foreground leading-relaxed">{entry.longDesc}</p>
              </div>
            </div>

            {/* 푸터 */}
            <div className="px-5 py-4 border-t border-border">
              <button
                onClick={onClose}
                className="w-full py-3 bg-primary hover:bg-primary/90 text-white font-medium rounded-lg transition-colors"
              >
                닫기
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

export default GlossaryModal;
