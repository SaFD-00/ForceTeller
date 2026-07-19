'use client';

import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Mascot } from './Mascot';
import { useOverlayPortal } from '@/lib/hooks/useOverlayPortal';

interface LoadingOverlayProps {
  isVisible: boolean;
  message?: string;
  subMessage?: string;
}

export function LoadingOverlay({
  isVisible,
  message = '사주를 분석하고 있습니다',
  subMessage = '잠시만 기다려주세요...',
}: LoadingOverlayProps) {
  // 오버레이 접근성 계약의 "축소판". 뒤 폼이 Tab으로 도달 가능한 채 남지 않도록
  // portal + inert 로 배경을 봉쇄하되, 포커스 트랩과 Escape는 의도적으로 제외한다:
  // - 트랩 없음: 이 오버레이 안에는 focusable 요소가 하나도 없다. 트랩을 걸면 포커스가
  //   갇힌 채 어디로도 못 간다. 배경이 inert라 어차피 포커스가 새어 나가지도 않는다.
  // - Escape 없음: 분석 요청에는 취소 경로가 없다(스토어에 abort/cancel 액션이 없어
  //   응답이 오면 isLoading이 내려간다). 닫히지 않는 키를 광고하지 않는다.
  // 알림은 role="status" + aria-live="polite" 로 — 대기 상태를 끼어들지 않고 전달한다.
  const portalContainer = useOverlayPortal('data-loading-portal', isVisible);

  if (!portalContainer) return null;

  return createPortal(
    <AnimatePresence>
      {isVisible && (
        <motion.div
          role="status"
          aria-live="polite"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm"
        >
          <div className="text-center rounded-xl border-[1.5px] border-border bg-surface shadow-card-hover px-10 py-8">
            {/* 별이가 사주를 들여다보는 중 */}
            <Mascot mood="thinking" size="xl" floating className="mx-auto mb-6" />

            {/* Text */}
            <motion.h2
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-2xl font-bold text-foreground mb-2"
            >
              {message}
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-muted-foreground"
            >
              {subMessage}
            </motion.p>

            {/* Animated dots */}
            <div className="flex justify-center gap-2 mt-6">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  animate={{
                    y: [0, -8, 0],
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: 0.8,
                    repeat: Infinity,
                    delay: i * 0.15,
                  }}
                  className="w-2 h-2 rounded-full bg-primary"
                />
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>,
    portalContainer
  );
}
