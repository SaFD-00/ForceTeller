'use client';

import { motion } from 'framer-motion';
import { GlassCard } from '@/components/ui';
import type { TenGodsDisplay } from '@/types/saju';

interface TenGodsDistributionProps {
  distribution: TenGodsDisplay;
}

const TEN_GODS_INFO: Record<string, { description: string; category: string }> = {
  '비견': { description: '경쟁, 독립', category: 'self' },
  '겁재': { description: '의지, 도전', category: 'self' },
  '식신': { description: '표현, 창의', category: 'output' },
  '상관': { description: '재능, 반항', category: 'output' },
  '편재': { description: '재물, 투자', category: 'wealth' },
  '정재': { description: '안정, 저축', category: 'wealth' },
  '편관': { description: '권력, 변화', category: 'power' },
  '정관': { description: '명예, 직위', category: 'power' },
  '편인': { description: '학문, 창조', category: 'resource' },
  '정인': { description: '보호, 지혜', category: 'resource' },
};

const CATEGORY_COLORS: Record<string, string> = {
  self: 'from-blue-500/20 to-blue-600/20 border-blue-500/30',
  output: 'from-green-500/20 to-green-600/20 border-green-500/30',
  wealth: 'from-yellow-500/20 to-yellow-600/20 border-yellow-500/30',
  power: 'from-red-500/20 to-red-600/20 border-red-500/30',
  resource: 'from-purple-500/20 to-purple-600/20 border-purple-500/30',
};

export function TenGodsDistribution({ distribution }: TenGodsDistributionProps) {
  const maxCount = Math.max(...Object.values(distribution.counts), 1);

  return (
    <section className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold text-foreground mb-6 text-center"
      >
        십성 분포 (十星)
      </motion.h2>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {Object.entries(TEN_GODS_INFO).map(([god, info], index) => {
          const count = distribution.counts[god] || 0;
          const percentage = (count / maxCount) * 100;

          return (
            <motion.div
              key={god}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <GlassCard
                className={`p-4 bg-gradient-to-br ${CATEGORY_COLORS[info.category]}`}
              >
                <div className="text-center">
                  <div className="text-lg font-bold text-foreground mb-1">{god}</div>
                  <div className="text-xs text-muted-foreground mb-3">{info.description}</div>

                  {/* Count indicator */}
                  <div className="relative h-2 bg-muted rounded-full overflow-hidden mb-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${percentage}%` }}
                      transition={{ duration: 0.5, delay: 0.3 + index * 0.05 }}
                      className="absolute h-full bg-muted rounded-full"
                    />
                  </div>

                  <div className="text-2xl font-bold text-foreground">{count}</div>
                </div>
              </GlassCard>
            </motion.div>
          );
        })}
      </div>

      {/* Primary Ten God */}
      {distribution.primary && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-6"
        >
          <GlassCard className="p-6 text-center">
            <span className="text-muted-foreground text-sm">주 십성</span>
            <div className="text-2xl font-bold text-primary mt-2">
              {distribution.primary}
            </div>
            <p className="text-muted-foreground text-sm mt-2">
              {TEN_GODS_INFO[distribution.primary]?.description}
            </p>
          </GlassCard>
        </motion.div>
      )}
    </section>
  );
}
