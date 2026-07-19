'use client';

import { MotionConfig } from 'framer-motion';

/**
 * 앱 전역 모션 정책.
 * reducedMotion="user"는 OS의 "동작 줄이기" 설정을 존중해 transform/layout 애니메이션을
 * 자동으로 비활성화한다 (opacity는 유지). 개별 컴포넌트가 useReducedMotion()으로
 * 추가 분기할 수 있다.
 */
export function MotionProvider({ children }: { children: React.ReactNode }) {
  return <MotionConfig reducedMotion="user">{children}</MotionConfig>;
}

export default MotionProvider;
