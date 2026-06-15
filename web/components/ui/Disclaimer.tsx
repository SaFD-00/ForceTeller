'use client';

import { Icon } from './Icon';
import { cn } from '@/lib/utils';

interface DisclaimerProps {
  className?: string;
}

/**
 * 면책 고지 — 운세 해석은 참고용 엔터테인먼트이며 전문 상담을 대체하지 않음을 알린다.
 * 결과 페이지·채팅 하단에 상시 노출.
 */
export function Disclaimer({ className }: DisclaimerProps) {
  return (
    <div
      className={cn(
        'flex items-start gap-2 rounded-lg border border-border bg-muted/50 px-3 py-2 text-xs text-muted-foreground',
        className
      )}
    >
      <Icon name="solar:info-circle-linear" size={14} className="mt-0.5 flex-shrink-0" />
      <p className="leading-relaxed">
        본 해석은 사주명리학에 기반한 <strong>참고용 정보</strong>이며 재미를 위한 콘텐츠입니다.
        의료·법률·재정 등 중요한 결정은 반드시 해당 분야 전문가와 상담하세요. 운명은 정해져 있지 않으며,
        선택과 노력에 따라 달라질 수 있습니다.
      </p>
    </div>
  );
}

export default Disclaimer;
