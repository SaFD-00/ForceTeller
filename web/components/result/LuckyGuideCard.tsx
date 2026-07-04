'use client';

import { motion } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import { ELEMENT_COLORS } from '@/lib/constants/elements';
import type { Element, YongsinRecommendations, YongsinComparison } from '@/types/saju';

interface LuckyGuideCardProps {
  recommendations: YongsinRecommendations;
  comparison?: YongsinComparison;
}

function ChipRow({ label, items, icon }: { label: string; items?: string[]; icon: string }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="flex items-center gap-1 text-sm text-muted-foreground">
        <Icon name={icon} size={16} className="text-primary" />
        {label}
      </span>
      {items.map((item, i) => (
        <span
          key={i}
          className="px-2.5 py-1 text-sm rounded-full bg-primary/10 text-foreground border border-primary/20"
        >
          {item}
        </span>
      ))}
    </div>
  );
}

export function LuckyGuideCard({ recommendations, comparison }: LuckyGuideCardProps) {
  const primary = recommendations.primary_element;
  if (!primary) return null;

  const element = (primary.element as Element) ?? '토';
  const color = ELEMENT_COLORS[element] ?? ELEMENT_COLORS['토'];
  const methodName = comparison?.recommendation?.algorithm_name;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:magic-stick-3-bold" size={24} className="text-primary" />
        <h2 className="text-xl font-bold text-foreground">용신 개운법</h2>
        {methodName && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-muted text-muted-foreground border border-border">
            추천: {methodName}
          </span>
        )}
      </div>

      <GlassCard className="p-4 md:p-6 space-y-4">
        {/* 용신 오행 + 요약 */}
        <div className="flex items-center gap-3">
          <div
            className={`w-14 h-14 rounded-xl flex items-center justify-center ${color.bg} ${color.border} border`}
          >
            <span className={`text-2xl font-bold ${color.text}`}>{element}</span>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">나에게 이로운 기운</p>
            <p className="text-lg font-semibold text-foreground">{element} 기운 보강</p>
          </div>
        </div>

        {recommendations.summary && (
          <p className="text-sm text-foreground leading-relaxed bg-muted rounded-lg p-3">
            {recommendations.summary}
          </p>
        )}

        {/* 개운 요소 */}
        <div className="space-y-3">
          <ChipRow label="행운의 색" items={primary.colors} icon="solar:palette-bold" />
          <ChipRow label="길한 방위" items={primary.directions} icon="solar:compass-bold" />
          <ChipRow label="유리한 직업" items={primary.main_careers} icon="solar:case-round-bold" />
          <ChipRow label="추천 활동" items={primary.recommended_activities} icon="solar:running-bold" />
        </div>

        {/* 생활 팁 / 주의 */}
        {recommendations.lifestyle_tips && recommendations.lifestyle_tips.length > 0 && (
          <div>
            <p className="flex items-center gap-1 text-sm font-medium text-foreground mb-2">
              <Icon name="solar:check-circle-bold" size={16} className="text-success" />
              생활 속 개운법
            </p>
            <ul className="space-y-1">
              {recommendations.lifestyle_tips.map((tip, i) => (
                <li key={i} className="text-sm text-muted-foreground pl-5 relative">
                  <span className="absolute left-0 text-primary">•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </div>
        )}

        {recommendations.cautions && recommendations.cautions.length > 0 && (
          <div>
            <p className="flex items-center gap-1 text-sm font-medium text-foreground mb-2">
              <Icon name="solar:danger-triangle-bold" size={16} className="text-warning" />
              주의할 점
            </p>
            <ul className="space-y-1">
              {recommendations.cautions.map((c, i) => (
                <li key={i} className="text-sm text-muted-foreground pl-5 relative">
                  <span className="absolute left-0 text-warning">•</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>
        )}
      </GlassCard>
    </motion.div>
  );
}

export default LuckyGuideCard;
