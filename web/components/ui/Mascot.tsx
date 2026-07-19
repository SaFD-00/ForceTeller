'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

/**
 * Mascot — ForceTeller 브랜드 캐릭터 "별·달 점성술사" (별이).
 *
 * 간단한 div/SVG 블록으로 조립한 듀오링고식 마스코트. 둥근 달 얼굴 + 고깔모자 + 별로 구성되며
 * 표정(mood)·크기(size) variant 를 가진다. 채팅봇 아바타·설명봇·빈상태·로딩·로고 등 곳곳에 재사용.
 *
 * 색은 디자인 토큰(잉크 네이비 #263D5B 윤곽, 스카이 크레용 #49B6E5 모자, 별 옐로우 #ffd23f)을
 * hex 로 직접 넣어 앱과 design-sync 헤드리스 렌더에서 동일하게 보이게 한다.
 * path·표정·아이덴티티(달 얼굴 + 고깔모자 + 별)는 불변이고 팔레트만 Doodle 로 정합시킨다.
 */

export type MascotMood =
  | 'idle'
  | 'happy'
  | 'thinking'
  | 'talking'
  | 'curious'
  | 'sleeping';

export type MascotSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

interface MascotProps {
  mood?: MascotMood;
  size?: MascotSize;
  /** 살랑 떠다니는 모션 (design-sync 정적 캡처에서는 skipAnimations 로 정지) */
  floating?: boolean;
  className?: string;
  title?: string;
}

const SIZE_PX: Record<MascotSize, number> = {
  xs: 28,
  sm: 38,
  md: 52,
  lg: 76,
  xl: 120,
};

const INK = '#263D5B';      // 잉크 네이비 윤곽 (= border 토큰)
const SKY = '#49B6E5';      // 스카이 크레용 모자 (= primary 토큰, 채움 전용)
const SKY_DK = '#2E8CB5';   // 모자 챙·생각점 — SKY 파생 다크 (백색 대비 3.5:1, non-text AA)
const STAR = '#ffd23f';
const MOON = '#ffffff';
const CHEEK = '#f4a8e8'; // 옅은 핑크 볼

function Eyes({ mood }: { mood: MascotMood }) {
  const lx = 25;
  const rx = 39;
  switch (mood) {
    case 'happy':
      return (
        <g stroke={INK} strokeWidth={2.4} strokeLinecap="round" fill="none">
          <path d={`M${lx - 3},39 Q${lx},35 ${lx + 3},39`} />
          <path d={`M${rx - 3},39 Q${rx},35 ${rx + 3},39`} />
        </g>
      );
    case 'sleeping':
      return (
        <g stroke={INK} strokeWidth={2.4} strokeLinecap="round" fill="none">
          <path d={`M${lx - 3},38 Q${lx},41 ${lx + 3},38`} />
          <path d={`M${rx - 3},38 Q${rx},41 ${rx + 3},38`} />
        </g>
      );
    case 'curious':
      return (
        <g fill={INK}>
          <circle cx={lx} cy={38} r={3.6} />
          <circle cx={rx} cy={38} r={3.6} />
          <circle cx={lx + 1.2} cy={36.8} r={1.1} fill={MOON} />
          <circle cx={rx + 1.2} cy={36.8} r={1.1} fill={MOON} />
        </g>
      );
    case 'thinking':
      // 위를 올려다보는 눈 (동공 위쪽)
      return (
        <g fill={INK}>
          <circle cx={lx} cy={37} r={2.8} />
          <circle cx={rx} cy={37} r={2.8} />
          <circle cx={lx + 0.8} cy={35.8} r={0.9} fill={MOON} />
          <circle cx={rx + 0.8} cy={35.8} r={0.9} fill={MOON} />
        </g>
      );
    default: // idle, talking
      return (
        <g fill={INK}>
          <circle cx={lx} cy={38} r={2.9} />
          <circle cx={rx} cy={38} r={2.9} />
          <circle cx={lx + 1} cy={37} r={1} fill={MOON} />
          <circle cx={rx + 1} cy={37} r={1} fill={MOON} />
        </g>
      );
  }
}

function Mouth({ mood }: { mood: MascotMood }) {
  switch (mood) {
    case 'happy':
      return <path d="M26,46 Q32,53 38,46" stroke={INK} strokeWidth={2.4} strokeLinecap="round" fill="none" />;
    case 'talking':
      return <ellipse cx={32} cy={48} rx={3.2} ry={2.6} fill={INK} />;
    case 'curious':
      return <circle cx={32} cy={48} r={2.2} fill={INK} />;
    case 'thinking':
      return <path d="M29,48 H35" stroke={INK} strokeWidth={2.2} strokeLinecap="round" />;
    case 'sleeping':
      return <path d="M30,48 Q32,50 34,48" stroke={INK} strokeWidth={2} strokeLinecap="round" fill="none" />;
    default: // idle
      return <path d="M28,47 Q32,50.5 36,47" stroke={INK} strokeWidth={2.2} strokeLinecap="round" fill="none" />;
  }
}

export function Mascot({
  mood = 'idle',
  size = 'md',
  floating = false,
  className,
  title = 'ForceTeller 마스코트 별이',
}: MascotProps) {
  const px = SIZE_PX[size];

  const svg = (
    <svg
      viewBox="0 0 64 64"
      width={px}
      height={px}
      role="img"
      aria-label={title}
      className={cn('inline-block select-none', !floating && className)}
    >
      {/* 모자 끝 별 */}
      <path
        d="M32 1.5l1.6 3.9 4.2.3-3.2 2.7 1 4.1-3.6-2.2-3.6 2.2 1-4.1-3.2-2.7 4.2-.3z"
        fill={STAR}
        stroke={INK}
        strokeWidth={1.4}
        strokeLinejoin="round"
      />
      {/* 고깔모자 */}
      <path
        d="M32 12 L19 30 Q32 25 45 30 Z"
        fill={SKY}
        stroke={INK}
        strokeWidth={2.4}
        strokeLinejoin="round"
      />
      {/* 모자 위 작은 별 장식 */}
      <circle cx={29} cy={24} r={1.1} fill={STAR} />
      <circle cx={35} cy={21} r={0.9} fill={STAR} />
      {/* 모자 챙 */}
      <path
        d="M16 30 Q32 24 48 30 Q32 37 16 30 Z"
        fill={SKY_DK}
        stroke={INK}
        strokeWidth={2.2}
        strokeLinejoin="round"
      />
      {/* 달 얼굴 */}
      <circle cx={32} cy={42} r={17} fill={MOON} stroke={INK} strokeWidth={2.4} />
      {/* 볼 */}
      <circle cx={22} cy={45} r={2.6} fill={CHEEK} opacity={0.75} />
      <circle cx={42} cy={45} r={2.6} fill={CHEEK} opacity={0.75} />
      <Eyes mood={mood} />
      <Mouth mood={mood} />
      {/* thinking: 생각 점들 / sleeping: Z */}
      {mood === 'thinking' && (
        <g fill={SKY_DK}>
          <circle cx={50} cy={30} r={1.6} />
          <circle cx={54} cy={26} r={2.1} />
          <circle cx={59} cy={21} r={2.7} />
        </g>
      )}
      {mood === 'sleeping' && (
        <text x={48} y={28} fontFamily="'JetBrains Mono', monospace" fontSize={9} fontWeight={700} fill={SKY_DK}>
          z
        </text>
      )}
    </svg>
  );

  if (floating) {
    return (
      <motion.div
        className={cn('inline-block', className)}
        animate={{ y: [0, -4, 0] }}
        transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}
      >
        {svg}
      </motion.div>
    );
  }

  return svg;
}

interface MascotBubbleProps {
  children: React.ReactNode;
  mood?: MascotMood;
  size?: MascotSize;
  className?: string;
}

/** 마스코트 + 말풍선 — 설명봇/빈상태에 재사용하는 소형 헬퍼. */
export function MascotBubble({ children, mood = 'talking', size = 'sm', className }: MascotBubbleProps) {
  return (
    <div className={cn('flex items-start gap-2.5', className)}>
      <Mascot mood={mood} size={size} className="flex-shrink-0" />
      <div className="relative rounded-xl border-[1.5px] border-border bg-surface px-3 py-2 text-sm text-foreground shadow-block-sm">
        {children}
      </div>
    </div>
  );
}
