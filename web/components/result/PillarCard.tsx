'use client';

import { motion } from 'framer-motion';
import { GlassCard, ElementBadge } from '@/components/ui';
import type { PillarDisplay, Element } from '@/types/saju';
import { cn } from '@/lib/utils';

interface PillarCardProps {
  pillar: PillarDisplay;
  label: string;
  index: number;
}

const ELEMENT_COLORS: Record<Element, string> = {
  '목': 'text-element-wood',
  '화': 'text-element-fire',
  '토': 'text-element-earth',
  '금': 'text-element-metal',
  '수': 'text-element-water',
};

export function PillarCard({ pillar, label, index }: PillarCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <GlassCard className="p-4 text-center">
        {/* Label */}
        <div className="text-sm text-muted-foreground mb-3">{label}</div>

        {/* Heavenly Stem (천간) */}
        <div className="mb-4">
          <div
            className={cn(
              'text-4xl font-bold mb-1',
              ELEMENT_COLORS[pillar.heavenly_stem.element]
            )}
          >
            {pillar.heavenly_stem.hanja}
          </div>
          <div className="text-sm text-gray-600">
            {pillar.heavenly_stem.korean}
          </div>
          <ElementBadge
            element={pillar.heavenly_stem.element}
            size="sm"
            className="mt-2"
          />
        </div>

        {/* Divider */}
        <div className="w-full h-px bg-muted my-3" />

        {/* Earthly Branch (지지) */}
        <div className="mb-4">
          <div
            className={cn(
              'text-4xl font-bold mb-1',
              ELEMENT_COLORS[pillar.earthly_branch.element]
            )}
          >
            {pillar.earthly_branch.hanja}
          </div>
          <div className="text-sm text-gray-600">
            {pillar.earthly_branch.korean}
          </div>
          <ElementBadge
            element={pillar.earthly_branch.element}
            size="sm"
            className="mt-2"
          />
        </div>

        {/* Ten God (십성) - if present */}
        {pillar.ten_god && (
          <div className="mt-3 pt-3 border-t border-border">
            <span className="text-xs text-muted-foreground">십성</span>
            <div className="text-sm font-medium text-primary mt-1">
              {pillar.ten_god}
            </div>
          </div>
        )}
      </GlassCard>
    </motion.div>
  );
}
