'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import type { FortuneScores } from '@/types/saju';

interface FortuneScoreDashboardProps {
  scores: FortuneScores;
}

const FORTUNE_META: Record<string, { label: string; icon: string }> = {
  general: { label: '종합운', icon: 'solar:star-bold' },
  career: { label: '직업운', icon: 'solar:case-round-bold' },
  wealth: { label: '재물운', icon: 'solar:wallet-money-bold' },
  health: { label: '건강운', icon: 'solar:heart-pulse-bold' },
  love: { label: '애정운', icon: 'solar:hearts-bold' },
};

const ORDER = ['general', 'career', 'wealth', 'health', 'love'];

function scoreColor(score: number): string {
  if (score >= 70) return 'bg-success';
  if (score >= 50) return 'bg-primary';
  if (score >= 35) return 'bg-warning';
  return 'bg-danger';
}

export function FortuneScoreDashboard({ scores }: FortuneScoreDashboardProps) {
  const keys = ORDER.filter((k) => scores[k]);
  const [openKey, setOpenKey] = useState<string | null>(keys[0] ?? null);

  if (keys.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:chart-2-bold" size={24} className="text-accent" />
        <h2 className="font-display text-xl text-foreground">운세 점수</h2>
      </div>

      <GlassCard className="p-4 md:p-6 space-y-3">
        {keys.map((key) => {
          const item = scores[key];
          const meta = FORTUNE_META[key] ?? { label: key, icon: 'solar:star-bold' };
          const isOpen = openKey === key;

          return (
            <div key={key} className="rounded-lg border-[1.5px] border-border overflow-hidden shadow-block-sm">
              <button
                onClick={() => setOpenKey(isOpen ? null : key)}
                className="w-full p-3 flex items-center gap-3 hover:bg-muted/50 transition-colors text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              >
                <Icon name={meta.icon} size={20} className="text-accent flex-shrink-0" />
                <span className="text-sm font-medium text-foreground w-16 flex-shrink-0">
                  {meta.label}
                </span>
                <div className="flex-1 h-2 rounded-full bg-muted border-[1.5px] border-border overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.score}%` }}
                    transition={{ duration: 0.6 }}
                    className={`h-full rounded-full ${scoreColor(item.score)}`}
                  />
                </div>
                <span className="text-sm font-mono font-bold text-foreground w-10 text-right flex-shrink-0">
                  {item.score}
                </span>
                <Icon
                  name={isOpen ? 'solar:alt-arrow-up-linear' : 'solar:alt-arrow-down-linear'}
                  size={16}
                  className="text-muted-foreground flex-shrink-0"
                />
              </button>

              <AnimatePresence>
                {isOpen && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="px-3 pb-3 space-y-2">
                      <p className="text-sm text-muted-foreground leading-relaxed">{item.summary}</p>
                      {item.advice && item.advice.length > 0 && (
                        <ul className="space-y-1">
                          {item.advice.map((a, i) => (
                            <li key={i} className="text-sm text-foreground pl-5 relative">
                              <span className="absolute left-0 text-accent">·</span>
                              {a}
                            </li>
                          ))}
                        </ul>
                      )}
                      {(item.lucky_colors?.length > 0 || item.lucky_directions?.length > 0) && (
                        <div className="flex flex-wrap gap-2 pt-1 text-xs text-muted-foreground">
                          {item.lucky_colors?.length > 0 && (
                            <span>행운색: {item.lucky_colors.join(', ')}</span>
                          )}
                          {item.lucky_directions?.length > 0 && (
                            <span>· 방위: {item.lucky_directions.join(', ')}</span>
                          )}
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </GlassCard>
    </motion.div>
  );
}

export default FortuneScoreDashboard;
