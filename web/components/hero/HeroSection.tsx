'use client';

import { motion } from 'framer-motion';
import { UnicornBackground } from './UnicornBackground';
import { BirthInfoForm } from './BirthInfoForm';
import { Icon } from '@/components/ui';

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center py-20 px-4">
      <UnicornBackground />

      <div className="relative z-10 w-full max-w-lg">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-6">
            <Icon name="solar:magic-stick-3-bold" size={16} className="text-primary" />
            <span className="text-sm text-white/70">AI 기반 사주명리 분석</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            운명의 흐름을
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
              읽어드립니다
            </span>
          </h1>

          <p className="text-white/60 text-lg max-w-md mx-auto">
            정확한 만세력 계산과 AI 해석으로
            <br />
            당신의 사주팔자를 분석해드립니다
          </p>
        </motion.div>

        <BirthInfoForm />

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.6 }}
          className="mt-8 flex justify-center"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
            className="flex flex-col items-center gap-2 text-white/40"
          >
            <span className="text-xs">더 알아보기</span>
            <Icon name="solar:alt-arrow-down-linear" size={20} />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
