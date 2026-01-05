'use client';

import { motion } from 'framer-motion';
import { PillarCard } from './PillarCard';
import type { FourPillarsDisplay as FourPillarsType } from '@/types/saju';

interface FourPillarsDisplayProps {
  pillars: FourPillarsType;
}

export function FourPillarsDisplay({ pillars }: FourPillarsDisplayProps) {
  const pillarEntries = [
    { key: 'year', label: '년주 (年柱)', data: pillars.year },
    { key: 'month', label: '월주 (月柱)', data: pillars.month },
    { key: 'day', label: '일주 (日柱)', data: pillars.day },
    { key: 'hour', label: '시주 (時柱)', data: pillars.hour },
  ];

  return (
    <section className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold text-white mb-6 text-center"
      >
        사주팔자 (四柱八字)
      </motion.h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {pillarEntries.map((entry, index) => (
          <PillarCard
            key={entry.key}
            pillar={entry.data}
            label={entry.label}
            index={index}
          />
        ))}
      </div>
    </section>
  );
}
