'use client';

import { useEffect, useId, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from './Icon';
import { useFocusTrap } from '@/lib/hooks/useFocusTrap';
import type { GlossaryEntry } from '@/data/saju-glossary';

interface GlossaryModalProps {
  entry: GlossaryEntry | null;
  isOpen: boolean;
  onClose: () => void;
}

// 카테고리별 색상
// 다색 카테고리 코딩 유지 + 라이트 tint 위 4.5:1 대비 확보를 위해 천간/12운성/합충은 -800로,
// 지지/신살은 -700로 이미 통과라 유지. (십성=퍼플 계열은 리터럴 대신 accent 토큰 사용)
const categoryColors: Record<GlossaryEntry['category'], string> = {
  '천간': 'bg-green-500/20 text-green-800',
  '지지': 'bg-blue-500/20 text-blue-700',
  '십성': 'bg-accent/15 text-accent',
  '12운성': 'bg-yellow-500/20 text-yellow-800',
  '신살': 'bg-red-500/20 text-red-700',
  '합충': 'bg-orange-500/20 text-orange-800',
  '용어': 'bg-muted text-muted-foreground',
};

export function GlossaryModal({ entry, isOpen, onClose }: GlossaryModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const titleId = useId();

  // 호출부 5곳이 전부 "isOpen=false + entry=null"을 한 번에 세팅한다.
  // 마지막 entry를 캐시해 두지 않으면 닫는 순간 본문이 사라져(early return) exit 애니메이션이
  // 통째로 스킵된다. 렌더 기준은 isOpen, 존재 기준은 캐시된 shown으로 분리한다.
  const lastEntryRef = useRef(entry);
  if (entry) lastEntryRef.current = entry;
  const shown = entry ?? lastEntryRef.current;

  const active = isOpen && !!shown;

  // 포탈 컨테이너. body 직계에 붙여야 "배경 = body의 나머지 직계 자식"이라는
  // 단순한 규칙으로 inert를 걸 수 있다(레이아웃 래퍼 + BottomNav).
  const [portalContainer, setPortalContainer] = useState<HTMLDivElement | null>(null);
  useEffect(() => {
    const el = document.createElement('div');
    el.setAttribute('data-glossary-portal', '');
    document.body.appendChild(el);
    setPortalContainer(el);
    return () => {
      el.remove();
    };
  }, []);

  // ⚠ 이 effect는 반드시 아래 useFocusTrap 호출보다 "앞에" 선언돼 있어야 한다.
  // React는 한 컴포넌트의 cleanup을 effect 선언 순서대로 실행한다. inert 해제가
  // useFocusTrap의 포커스 복원보다 먼저 돌아야 복원 대상(모달을 연 헤딩 버튼)이
  // 그 시점에 focusable하다. 순서가 뒤집히면 아직 inert인 서브트리 안의 요소에
  // focus()를 거는 셈이라 no-op이 되고 포커스가 body로 낙하한다.
  useEffect(() => {
    if (!active || !portalContainer) return;
    // 이미 inert를 갖고 있던 요소를 구분해 두었다가 cleanup에서 원래 상태로 되돌린다.
    // (일괄 removeAttribute는 남의 inert를 지운다)
    const previousInert = new Map<Element, string | null>();
    Array.from(document.body.children).forEach((child) => {
      if (child === portalContainer) return;
      previousInert.set(child, child.getAttribute('inert'));
      child.setAttribute('inert', '');
    });
    return () => {
      previousInert.forEach((prev, child) => {
        if (prev === null) child.removeAttribute('inert');
        else child.setAttribute('inert', prev);
      });
    };
  }, [active, portalContainer]);

  // 포커스 트랩 + 복귀 (early return 위에서 호출 — rules of hooks)
  useFocusTrap(dialogRef, active);

  // ESC 키로 닫기 + 배경 스크롤 잠금
  useEffect(() => {
    if (!active) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);

    // 인라인 overflow의 원래 값을 저장했다가 그대로 되돌린다.
    // 'unset'으로 리셋하면 모달이 열리기 전에 누군가 걸어 둔 값을 조용히 지운다.
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = previousOverflow;
    };
  }, [active, onClose]);

  // shown이 없으면 그릴 내용 자체가 없다. isOpen=false는 여기서 걸러내지 않는다 —
  // AnimatePresence가 계속 마운트돼 있어야 exit가 재생된다.
  if (!shown || !portalContainer) return null;

  return createPortal(
    <AnimatePresence>
      {active && (
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
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            tabIndex={-1}
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
                <span id={titleId} className="text-2xl font-bold text-foreground">{shown.term}</span>
                <span className="text-lg text-muted-foreground">{shown.hanja}</span>
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
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${categoryColors[shown.category]}`}>
                  {shown.category}
                </span>
              </div>

              {/* 한자 풀이 */}
              <div className="mb-4 p-3 bg-muted rounded-lg">
                <p className="text-xs text-muted-foreground mb-1">한자 풀이</p>
                <p className="text-sm text-foreground">{shown.hanjaBreakdown}</p>
              </div>

              {/* 짧은 설명 */}
              <div className="mb-4">
                <p className="text-xs text-muted-foreground mb-1">간단 설명</p>
                <p className="text-base text-accent font-medium">{shown.shortDesc}</p>
              </div>

              {/* 상세 설명 */}
              <div className="mb-4">
                <p className="text-xs text-muted-foreground mb-2">상세 설명</p>
                <p className="text-sm text-foreground leading-relaxed">{shown.longDesc}</p>
              </div>
            </div>

            {/* 푸터 */}
            <div className="px-5 py-4 border-t border-border">
              <button
                onClick={onClose}
                className="w-full py-3 bg-primary hover:bg-primary/90 text-primary-foreground font-medium rounded-lg transition-colors"
              >
                닫기
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>,
    portalContainer
  );
}

export default GlossaryModal;
