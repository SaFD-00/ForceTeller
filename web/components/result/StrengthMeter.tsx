'use client';

import { motion } from 'framer-motion';
import { GlassCard, Icon } from '@/components/ui';
import type { StrengthDisplay } from '@/types/saju';

interface StrengthMeterProps {
  analysis: StrengthDisplay;
}

export function StrengthMeter({ analysis }: StrengthMeterProps) {
  // Score from 0-100, where 50 is balanced, <50 is weak, >50 is strong
  const score = analysis.score;
  const isStrong = analysis.is_strong;

  // Calculate position on the meter (0-100%)
  const meterPosition = Math.min(Math.max(score, 0), 100);

  return (
    <section className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold text-white mb-6 text-center"
      >
        신강/신약 분석
      </motion.h2>

      <GlassCard className="p-8">
        <div className="max-w-xl mx-auto">
          {/* Result Label */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center mb-8"
          >
            <div
              className={`inline-flex items-center gap-3 px-6 py-3 rounded-full ${
                isStrong
                  ? 'bg-blue-500/20 border border-blue-500/30'
                  : 'bg-orange-500/20 border border-orange-500/30'
              }`}
            >
              <Icon
                name={isStrong ? 'solar:shield-bold' : 'solar:leaf-bold'}
                size={24}
                className={isStrong ? 'text-blue-400' : 'text-orange-400'}
              />
              <span className={`text-xl font-bold ${isStrong ? 'text-blue-400' : 'text-orange-400'}`}>
                {isStrong ? '신강 (身强)' : '신약 (身弱)'}
              </span>
            </div>
          </motion.div>

          {/* Meter */}
          <div className="relative mb-8">
            {/* Background bar */}
            <div className="h-4 bg-gradient-to-r from-orange-500/30 via-white/10 to-blue-500/30 rounded-full overflow-hidden">
              {/* Indicator */}
              <motion.div
                initial={{ left: '50%' }}
                animate={{ left: `${meterPosition}%` }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2"
              >
                <div className="w-6 h-6 bg-white rounded-full shadow-lg shadow-white/30 flex items-center justify-center">
                  <div className="w-3 h-3 bg-primary rounded-full" />
                </div>
              </motion.div>
            </div>

            {/* Labels */}
            <div className="flex justify-between mt-2">
              <span className="text-sm text-orange-400">신약</span>
              <span className="text-sm text-white/50">균형</span>
              <span className="text-sm text-blue-400">신강</span>
            </div>
          </div>

          {/* Details */}
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 rounded-xl bg-white/5">
              <div className="text-white/50 text-sm mb-1">일간 강도</div>
              <div className="text-2xl font-bold text-white">{score}%</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-white/5">
              <div className="text-white/50 text-sm mb-1">유형</div>
              <div className="text-2xl font-bold text-white">
                {analysis.type || (isStrong ? '강' : '약')}
              </div>
            </div>
          </div>

          {/* Description */}
          {analysis.description && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="text-center text-white/60 mt-6 leading-relaxed"
            >
              {analysis.description}
            </motion.p>
          )}
        </div>
      </GlassCard>
    </section>
  );
}
