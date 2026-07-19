'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import type { SchoolComparisonResult } from '@/types/saju';

interface SchoolComparisonProps {
  comparison: SchoolComparisonResult;
}

const CATEGORY_LABELS: Record<string, string> = {
  yongsin: '용신',
  health: '건강',
  wealth: '재물',
  career: '직업·사업',
  relationship: '인연',
  fame: '명예',
};

function confidenceLabel(c: number): { label: string; cls: string } {
  if (c >= 0.8) return { label: '일치도 높음', cls: 'bg-success/15 text-success-ink' };
  if (c >= 0.5) return { label: '일치도 보통', cls: 'bg-warning/15 text-warning-ink' };
  return { label: '해석 분분', cls: 'bg-danger/15 text-danger-ink' };
}

export function SchoolComparison({ comparison }: SchoolComparisonProps) {
  const { interpretations, consensus, recommendation, confidence } = comparison;
  const [activeSchool, setActiveSchool] = useState(interpretations[0]?.school || '');

  if (!interpretations || interpretations.length === 0) return null;

  const active = interpretations.find((i) => i.school === activeSchool) || interpretations[0];
  const badge = confidenceLabel(confidence ?? 0);

  const aspectRows: Array<[string, string]> = [
    ['용신', active.yong_sin],
    ['총평', active.overall],
    ['건강', active.health],
    ['재물', active.wealth],
    ['직업', active.career],
    ['인연', active.relationship],
    ['명예', active.fame],
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:scale-bold" size={24} className="text-accent" />
        <h2 className="font-display text-xl text-foreground">5학파 비교 해석</h2>
        {typeof confidence === 'number' && (
          <span className={`text-xs px-2 py-0.5 rounded-lg ${badge.cls}`}>{badge.label}</span>
        )}
      </div>

      <GlassCard className="p-4 md:p-6 space-y-5">
        {/* 종합 권장 */}
        {recommendation && (
          <p className="text-sm text-foreground bg-muted rounded-lg p-3 border-[1.5px] border-border">{recommendation}</p>
        )}

        {/* 학파 합의 */}
        {consensus && consensus.length > 0 && (
          <div>
            <p className="flex items-center gap-1 text-sm font-medium text-foreground mb-2">
              <Icon name="solar:check-read-bold" size={16} className="text-success" />
              학파 공통 견해
            </p>
            <ul className="space-y-2">
              {consensus.map((c, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className="px-1.5 py-0.5 rounded-lg bg-primary/10 text-accent text-xs flex-shrink-0">
                    {CATEGORY_LABELS[c.category] || c.category}
                  </span>
                  <span className="text-muted-foreground">
                    {c.agreement}
                    <span className="text-xs text-muted-foreground"> ({c.schools.length}개 학파 동의)</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 학파별 탭 */}
        <div>
          <div className="flex flex-wrap gap-2 mb-4 pb-3 border-b-[1.5px] border-border">
            {interpretations.map((interp) => {
              const isActive = activeSchool === interp.school;
              return (
                <button
                  key={interp.school}
                  onClick={() => setActiveSchool(interp.school)}
                  className={`px-3 py-1.5 rounded-lg border-[1.5px] border-border text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
                    isActive
                      ? 'bg-primary/15 text-accent'
                      : 'bg-muted text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {interp.school_name}
                </button>
              );
            })}
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={active.school}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-2"
            >
              {active.geok_guk && (
                <p className="text-sm">
                  <span className="text-muted-foreground">격국: </span>
                  <span className="text-foreground font-medium">{active.geok_guk}</span>
                </p>
              )}
              {aspectRows.map(([label, value]) =>
                value ? (
                  <div key={label} className="text-sm">
                    <span className="text-accent font-medium">{label}</span>
                    <span className="text-muted-foreground"> · {value}</span>
                  </div>
                ) : null
              )}
              {active.key_features && active.key_features.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {active.key_features.map((f, i) => (
                    <span
                      key={i}
                      className="text-xs px-2 py-0.5 rounded-lg bg-muted text-muted-foreground border-[1.5px] border-border"
                    >
                      {f}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </GlassCard>
    </motion.div>
  );
}

export default SchoolComparison;
