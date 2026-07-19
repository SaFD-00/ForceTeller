'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  index: number;
}

export function FeatureCard({ icon, title, description, index }: FeatureCardProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    // 마운트 즉시 애니메이션한다. opacity는 건드리지 않는다 —
    // whileInView + opacity:0 조합은 스크롤 전/JS 미실행 시 카드를 완전히 감춘다.
    <motion.div
      initial={shouldReduceMotion ? false : { y: 20 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <GlassCard className="h-full p-6 hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover transition-all duration-300 group cursor-pointer">
        <div className="flex flex-col items-center text-center">
          <div className="w-14 h-14 rounded-xl border-[1.5px] border-border bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-primary/15 transition-all duration-300">
            <Icon name={icon} size={28} className="text-accent" />
          </div>

          <h3 className="text-lg font-semibold text-foreground mb-2">
            {title}
          </h3>

          <p className="text-sm text-muted-foreground leading-relaxed">
            {description}
          </p>
        </div>
      </GlassCard>
    </motion.div>
  );
}
