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
    icon: 'solar:magic-stick-3-bold',
    description: '전반적인 사주 분석',
  },
  {
    type: 'personality',
    name: '성격 분석',
    icon: 'solar:user-heart-bold',
    description: '성격과 기질 해석',
  },
  {
    type: 'career',
    name: '직업/재물',
    icon: 'solar:wallet-money-bold',
    description: '진로 및 재물운',
  },
  {
    type: 'relationship',
    name: '인연/궁합',
    icon: 'solar:hearts-bold',
    description: '인간관계와 궁합',
  },
  {
    type: 'health',
    name: '건강',
    icon: 'solar:health-bold',
    description: '체질과 건강 조언',
  },
  {
    type: 'fortune',
    name: '운세',
    icon: 'solar:stars-bold',
    description: '시기별 운세 흐름',
  },
  {
    type: 'yongsin',
    name: '용신 분석',
    icon: 'solar:atom-bold',
    description: '용신과 기신 해석',
  },
  {
    type: 'school_compare',
    name: '유파 비교',
    icon: 'solar:notebook-bookmark-bold',
    description: '5대 유파별 해석',
  },
];

export function AgentSelector({ selected, onSelect }: AgentSelectorProps) {
  return (
    <div className="p-3 border-b border-border">
      <h3 className="text-xs font-medium text-muted-foreground mb-2">상담 분야 선택</h3>
      <div className="flex flex-wrap gap-1.5">
        {AGENTS.map((agent) => (
          <motion.button
            key={agent.type}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(agent.type)}
            className={cn(
              'px-3 py-1.5 rounded-lg border transition-all flex items-center gap-1.5',
              selected === agent.type
                ? 'bg-primary/20 border-primary'
                : 'bg-muted border-border hover:bg-muted'
            )}
          >
            <Icon
              name={agent.icon}
              size={16}
              className={cn(
                selected === agent.type ? 'text-primary' : 'text-muted-foreground'
              )}
            />
            <span className="text-xs font-medium text-foreground">{agent.name}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
