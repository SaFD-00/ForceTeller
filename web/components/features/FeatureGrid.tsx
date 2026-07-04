'use client';

import { motion } from 'framer-motion';
import { FeatureCard } from './FeatureCard';
import { FEATURES } from '@/lib/constants/features';

export function FeatureGrid() {
  return (
    <section className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="font-display text-3xl md:text-4xl text-foreground mb-4">
            다양한 분석 기능
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            정확한 만세력 계산을 기반으로 다양한 관점에서
            당신의 사주를 분석해드립니다
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature, index) => (
            <FeatureCard
              key={feature.title}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
