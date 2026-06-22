// design-sync 번들 전역 셋업 — cfg.extraEntries 로 번들 entry에 합류한다.
// 컴포넌트 다수가 framer-motion `motion.*` 에 initial={{opacity:0}} 마운트 페이드인을
// 쓴다. 정적 캡처(headless 스크린샷)는 애니메이션 시작 순간을 찍어 카드가 투명/빈
// 박스로 나온다(실제 claude.ai/design 실시간 렌더는 정상이지만 캡처·grade가 왜곡됨).
// MotionGlobalConfig.skipAnimations 로 애니메이션을 건너뛰고 최종 상태로 렌더한다 —
// 디자인 시스템 미리보기는 정적 최종 상태가 오히려 적합하다.
import { MotionGlobalConfig } from 'framer-motion';

MotionGlobalConfig.skipAnimations = true;

export const __dsPreviewSetup = true;
