'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { BirthInfoForm } from './BirthInfoForm';
import { Icon, Mascot } from '@/components/ui';

export function HeroSection() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className="hero-gradient relative flex flex-col items-center px-4 pt-20 pb-16">
      {/* FeatureCard 와 동일 규약: y 만 애니메이트하고 opacity 는 건드리지 않는다 —
          initial opacity:0 은 JS 미실행 시 히어로 전체(마스코트·헤드라인·입력폼)를 완전히 감춘다. */}
      <motion.div
        initial={shouldReduceMotion ? false : { y: -12 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-10"
      >
        <Mascot mood="happy" size="xl" floating className="mx-auto mb-5" />

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border-[1.5px] border-border bg-primary/10 text-accent shadow-block-sm mb-5">
          <Icon name="solar:magic-stick-3-bold" size={15} />
          <span className="text-xs font-bold">AI 기반 사주명리 분석</span>
        </div>

        <p className="font-display text-2xl tracking-wide text-accent mb-1">FORCETELLER</p>
        {/* sketch-underline 은 배경 반복이라 블록 폭 전체로 늘어난다 → inline-block 으로 글자 폭에 맞춘다.
            강조구는 .gradient-text(from-primary #49B6E5, 2.31:1) 대신 text-accent(11.0:1)로 — 헤드라인은 텍스트이므로 AA 필수. */}
        <h1 className="inline-block sketch-underline text-4xl md:text-5xl font-bold tracking-tight text-foreground mb-3">
          사주, <span className="text-accent">손쉽게 풀이.</span>
        </h1>
        <p className="text-muted-foreground text-base md:text-lg max-w-xl mx-auto">
          생년월일시를 입력하면 진태양시 보정 만세력과 8개의 전문 AI 에이전트가
          당신의 사주팔자를 정밀하게 해석합니다.
        </p>
      </motion.div>

      <BirthInfoForm />
    </section>
  );
}
