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
        className="text-2xl font-bold text-foreground mb-6 text-center"
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
              className={`inline-flex items-center gap-3 px-6 py-3 rounded-lg border-[1.5px] border-border shadow-block-sm ${
                isStrong
                  ? 'bg-accent/10'
                  : 'bg-warning/10'
              }`}
            >
              <Icon
                name={isStrong ? 'solar:shield-bold' : 'solar:leaf-bold'}
                size={24}
                className={isStrong ? 'text-accent' : 'text-warning'}
              />
              <span className={`text-xl font-bold ${isStrong ? 'text-accent' : 'text-warning'}`}>
                {isStrong ? '신강 (身强)' : '신약 (身弱)'}
              </span>
            </div>
          </motion.div>

          {/* Meter */}
          <div className="relative mb-8">
            {/* Background bar */}
            <div className="h-4 bg-gradient-to-r from-warning/30 via-muted to-accent/30 rounded-full overflow-hidden border-[1.5px] border-border">
              {/* Indicator */}
              <motion.div
                initial={{ left: '50%' }}
                animate={{ left: `${meterPosition}%` }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2"
              >
                <div className="w-6 h-6 bg-surface rounded-full border-[1.5px] border-border shadow-block-sm flex items-center justify-center">
                  <div className="w-3 h-3 bg-primary rounded-full" />
                </div>
              </motion.div>
            </div>

            {/* Labels */}
            <div className="flex justify-between mt-2">
              <span className="text-sm text-warning">신약</span>
              <span className="text-sm text-muted-foreground">균형</span>
              <span className="text-sm text-accent">신강</span>
            </div>
          </div>

          {/* Details */}
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 rounded-xl border-[1.5px] border-border bg-muted shadow-block-sm">
              <div className="text-muted-foreground text-sm mb-1">일간 강도</div>
              <div className="text-2xl font-bold font-mono text-foreground">{score}%</div>
            </div>
            <div className="text-center p-4 rounded-xl border-[1.5px] border-border bg-muted shadow-block-sm">
              <div className="text-muted-foreground text-sm mb-1">유형</div>
              <div className="text-2xl font-bold text-foreground">
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
              className="text-center text-muted-foreground mt-6 leading-relaxed"
            >
              {analysis.description}
            </motion.p>
          )}
        </div>
      </GlassCard>
    </section>
  );
}
