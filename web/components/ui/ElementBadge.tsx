'use client';

import { cn } from '@/lib/utils';
import { ELEMENT_COLORS } from '@/lib/constants/elements';
import type { Element } from '@/types/saju';

interface ElementBadgeProps {
  element: Element | string;
  size?: 'sm' | 'md' | 'lg';
  showName?: boolean;
  className?: string;
}

// 영어 -> 한글 변환
const elementToKorean: Record<string, Element> = {
  wood: '목',
  fire: '화',
  earth: '토',
  metal: '금',
  water: '수',
  목: '목',
  화: '화',
  토: '토',
  금: '금',
  수: '수',
};

const elementChars: Record<Element, string> = {
  목: '木',
  화: '火',
  토: '土',
  금: '金',
  수: '水',
};

// 기본 색상 (fallback)
const defaultColors = {
  bg: 'bg-gray-500/20',
  text: 'text-gray-400',
  border: 'border-gray-500/50',
};

export function ElementBadge({
  element,
  size = 'md',
  showName = true,
  className,
}: ElementBadgeProps) {
  // 영어/한글 모두 한글로 변환
  const koreanElement = elementToKorean[element] || (element as Element);
  const colors = ELEMENT_COLORS[koreanElement] || defaultColors;

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center justify-center rounded-full border font-medium',
        colors.bg,
        colors.text,
        colors.border,
        sizes[size],
        className
      )}
    >
      {elementChars[koreanElement] || '?'}
      {showName && <span className="ml-1">{koreanElement}</span>}
    </span>
  );
}
