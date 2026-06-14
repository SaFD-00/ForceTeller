'use client';

import { motion } from 'framer-motion';
import { BirthInfoForm } from './BirthInfoForm';
import { Icon } from '@/components/ui';

export function HeroSection() {
  return (
    <section className="hero-gradient relative flex flex-col items-center px-4 pt-24 pb-16">
      <motion.div
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-10"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary mb-6">
          <Icon name="solar:magic-stick-3-bold" size={15} />
          <span className="text-xs font-medium">AI 기반 사주명리 분석</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground mb-3">
          사주, <span className="gradient-text">손쉽게 풀이.</span>
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
