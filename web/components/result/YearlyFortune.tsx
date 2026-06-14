'use client';

import { motion } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import { ELEMENT_COLORS } from '@/lib/constants/elements';
import type { Element, SewunItem } from '@/types/saju';

interface YearlyFortuneProps {
  sewun: SewunItem[];
}

// 천간 인덱스 → 오행
const STEM_ELEMENTS: Element[] = ['목', '목', '화', '화', '토', '토', '금', '금', '수', '수'];

export function YearlyFortune({ sewun }: YearlyFortuneProps) {
  if (!sewun || sewun.length === 0) return null;

  const currentYear = new Date().getFullYear();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.45 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:calendar-bold" size={24} className="text-primary" />
        <h2 className="text-xl font-bold text-foreground">세운 (연도별 운세)</h2>
      </div>

      <GlassCard className="p-4 md:p-6">
        <p className="text-sm text-muted-foreground mb-4">
          올해부터 향후 {sewun.length}년간의 연운 흐름입니다. 그 해의 간지가 일간과 맺는 십성으로 운의 성격을 읽습니다.
        </p>
        <div className="flex gap-3 overflow-x-auto pb-2">
          {sewun.map((item) => {
            const element = STEM_ELEMENTS[item.stem_index] ?? '토';
            const color = ELEMENT_COLORS[element];
            const isCurrent = item.year === currentYear;

            return (
              <div
                key={item.year}
                className={`flex-shrink-0 w-28 p-3 rounded-xl border text-center transition-all ${
                  isCurrent
                    ? 'border-primary bg-primary/5 shadow-card'
                    : 'border-border bg-muted'
                }`}
              >
                <div className="flex items-center justify-center gap-1 mb-2">
                  <span className="text-sm font-semibold text-foreground">{item.year}</span>
                  {isCurrent && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-primary/20 text-primary">
                      올해
                    </span>
                  )}
                </div>
                <div
                  className={`mx-auto mb-2 w-12 h-12 rounded-lg flex items-center justify-center ${color.bg} ${color.border} border`}
                >
                  <span className={`text-lg font-bold ${color.text}`}>{item.ganji_korean}</span>
                </div>
                <p className="text-xs font-medium text-foreground">{item.ten_god}</p>
                <p className="text-[11px] text-muted-foreground">{item.twelve_phase}</p>
              </div>
            );
          })}
        </div>
      </GlassCard>
    </motion.div>
  );
}

export default YearlyFortune;
