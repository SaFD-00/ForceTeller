'use client';

import { motion } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';

export interface LifeStage {
  age: number;
  ganji: string;
  tenGodGroup: string;
  isCurrent: boolean;
}

interface LifetimeReportProps {
  stages: LifeStage[];
  overallSummary?: string;
}

// 십성 그룹별 인생 시기 테마
const STAGE_THEME: Record<string, { theme: string; icon: string }> = {
  비겁: { theme: '자립과 주체성이 강조되는 시기로, 경쟁 속에서 자기 색을 세웁니다.', icon: 'solar:users-group-rounded-bold' },
  식상: { theme: '표현·재능·활동이 활발해지는 시기로, 새로운 시도가 빛을 봅니다.', icon: 'solar:lightbulb-bolt-bold' },
  재성: { theme: '재물과 현실적 성취, 결실을 거두는 시기입니다.', icon: 'solar:wallet-money-bold' },
  관성: { theme: '책임·명예·사회적 지위가 부각되는 시기입니다.', icon: 'solar:crown-bold' },
  인성: { theme: '학습과 내실, 주변의 도움을 받는 안정의 시기입니다.', icon: 'solar:book-bookmark-bold' },
};

export function LifetimeReport({ stages, overallSummary }: LifetimeReportProps) {
  if (!stages || stages.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.55 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:map-arrow-square-bold" size={24} className="text-primary" />
        <h2 className="text-xl font-bold text-foreground">평생운 흐름 (10년 대운)</h2>
      </div>

      <GlassCard className="p-4 md:p-6">
        {overallSummary && (
          <p className="text-sm text-foreground bg-muted rounded-lg p-3 mb-4 border-[1.5px] border-border">{overallSummary}</p>
        )}

        <div className="relative pl-6">
          {/* 세로 타임라인 선 */}
          <div className="absolute left-2 top-1 bottom-1 w-px bg-border" />

          <div className="space-y-4">
            {stages.map((stage, idx) => {
              const meta = STAGE_THEME[stage.tenGodGroup] ?? {
                theme: '운의 흐름이 전환되는 시기입니다.',
                icon: 'solar:star-bold',
              };
              return (
                <div key={idx} className="relative">
                  {/* 타임라인 점 */}
                  <div
                    className={`absolute -left-[18px] top-1 w-3 h-3 rounded-full border-2 ${
                      stage.isCurrent
                        ? 'bg-primary border-primary'
                        : 'bg-background border-border'
                    }`}
                  />
                  <div
                    className={`rounded-xl p-3 border-[1.5px] border-border ${
                      stage.isCurrent ? 'bg-primary/5' : 'bg-muted/40'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <Icon name={meta.icon} size={16} className="text-primary" />
                      <span className="text-sm font-mono font-semibold text-foreground">
                        {stage.age}~{stage.age + 9}세
                      </span>
                      <span className="text-xs px-1.5 py-0.5 rounded-lg bg-muted text-muted-foreground">
                        {stage.ganji} · {stage.tenGodGroup}
                      </span>
                      {stage.isCurrent && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-lg bg-primary/20 text-primary">
                          현재
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">{meta.theme}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </GlassCard>
    </motion.div>
  );
}

export default LifetimeReport;
