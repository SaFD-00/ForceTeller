'use client';

import { motion } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import { cn } from '@/lib/utils';
import type { AgentType } from '@/types/saju';

interface AgentSelectorProps {
  selected: AgentType;
  onSelect: (agent: AgentType) => void;
}

const AGENTS: { type: AgentType; name: string; icon: string; description: string }[] = [
  {
    type: 'general',
    name: '종합 상담',
    icon: 'solar:magic-stick-3-linear',
    description: '전반적인 사주 분석',
  },
  {
    type: 'personality',
    name: '성격 분석',
    icon: 'solar:user-heart-linear',
    description: '성격과 기질 해석',
  },
  {
    type: 'career',
    name: '직업/재물',
    icon: 'solar:wallet-money-linear',
    description: '진로 및 재물운',
  },
  {
    type: 'relationship',
    name: '인연/궁합',
    icon: 'solar:hearts-linear',
    description: '인간관계와 궁합',
  },
  {
    type: 'health',
    name: '건강',
    icon: 'solar:health-linear',
    description: '체질과 건강 조언',
  },
  {
    type: 'fortune',
    name: '운세',
    icon: 'solar:stars-linear',
    description: '시기별 운세 흐름',
  },
  {
    type: 'yongsin',
    name: '용신 분석',
    icon: 'solar:atom-linear',
    description: '용신과 기신 해석',
  },
  {
    type: 'school_compare',
    name: '유파 비교',
    icon: 'solar:notebook-bookmark-linear',
    description: '5대 유파별 해석',
  },
];

export function AgentSelector({ selected, onSelect }: AgentSelectorProps) {
  return (
    <div className="p-3 border-b-[1.5px] border-border">
      <h3 className="text-xs font-medium text-muted-foreground mb-2">상담 분야 선택</h3>
      <div className="flex flex-wrap gap-1.5">
        {AGENTS.map((agent) => {
          const isSelected = selected === agent.type;
          return (
            <motion.button
              key={agent.type}
              type="button"
              aria-pressed={isSelected}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onSelect(agent.type)}
              className={cn(
                'focus-ring min-h-11 px-4 rounded-lg border-[1.5px] border-border transition-all flex items-center gap-1.5 block-press',
                isSelected
                  ? 'bg-primary/15 text-accent border-border shadow-block-sm'
                  : 'bg-surface hover:bg-muted'
              )}
            >
              <Icon
                name={isSelected ? 'solar:check-circle-linear' : agent.icon}
                size={16}
                className={cn(isSelected ? 'text-accent' : 'text-muted-foreground')}
              />
              <span
                className={cn(
                  'text-xs text-foreground',
                  isSelected ? 'font-semibold' : 'font-medium'
                )}
              >
                {agent.name}
              </span>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
