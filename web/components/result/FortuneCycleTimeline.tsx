'use client';

import { motion } from 'framer-motion';
import { GlassCard, ElementBadge, Icon } from '@/components/ui';
import type { FortuneCycleDisplay, Element } from '@/types/saju';
import { cn } from '@/lib/utils';

interface FortuneCycleTimelineProps {
  cycles: FortuneCycleDisplay[];
  currentAge?: number;
}

const ELEMENT_COLORS: Record<Element, string> = {
  '목': 'border-element-wood',
  '화': 'border-element-fire',
  '토': 'border-element-earth',
  '금': 'border-element-metal',
  '수': 'border-element-water',
};

export function FortuneCycleTimeline({ cycles, currentAge = 0 }: FortuneCycleTimelineProps) {
  const currentCycleIndex = cycles.findIndex(
    (cycle) => currentAge >= cycle.start_age && currentAge < cycle.start_age + 10
  );

  return (
    <section className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold text-white mb-6 text-center"
      >
        대운 흐름 (大運)
      </motion.h2>

      <GlassCard className="p-6 overflow-x-auto">
        <div className="flex gap-4 min-w-max pb-2">
          {cycles.map((cycle, index) => {
            const isCurrent = index === currentCycleIndex;
            const isPast = index < currentCycleIndex;

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="flex flex-col items-center"
              >
                {/* Age range */}
                <div className="text-xs text-white/50 mb-2">
                  {cycle.start_age} ~ {cycle.start_age + 9}세
                </div>

                {/* Pillar */}
                <div
                  className={cn(
                    'relative w-20 p-3 rounded-xl border-2 transition-all',
                    isCurrent
                      ? 'bg-primary/20 border-primary scale-110 shadow-lg shadow-primary/20'
                      : isPast
                      ? 'bg-white/5 border-white/10 opacity-60'
                      : 'bg-white/5 border-white/20'
                  )}
                >
                  {isCurrent && (
                    <div className="absolute -top-2 -right-2">
                      <Icon
                        name="solar:star-bold"
                        size={16}
                        className="text-primary"
                      />
                    </div>
                  )}

                  {/* Heavenly Stem */}
                  <div className="text-center mb-2">
                    <div className="text-xl font-bold text-white">
                      {cycle.heavenly_stem.hanja}
                    </div>
                    <div className="text-xs text-white/60">
                      {cycle.heavenly_stem.korean}
                    </div>
                  </div>

                  {/* Divider */}
                  <div className="w-full h-px bg-white/10 my-2" />

                  {/* Earthly Branch */}
                  <div className="text-center">
                    <div className="text-xl font-bold text-white">
                      {cycle.earthly_branch.hanja}
                    </div>
                    <div className="text-xs text-white/60">
                      {cycle.earthly_branch.korean}
                    </div>
                  </div>
                </div>

                {/* Element badge */}
                <div className="flex gap-1 mt-2">
                  <ElementBadge
                    element={cycle.heavenly_stem.element}
                    size="sm"
                    showName={false}
                  />
                  <ElementBadge
                    element={cycle.earthly_branch.element}
                    size="sm"
                    showName={false}
                  />
                </div>

                {/* Current indicator */}
                {isCurrent && (
                  <div className="mt-2 px-2 py-1 rounded-full bg-primary/20 text-primary text-xs">
                    현재
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </GlassCard>
    </section>
  );
}
