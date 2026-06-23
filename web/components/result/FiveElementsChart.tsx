'use client';

import { motion } from 'framer-motion';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
} from 'recharts';
import { GlassCard } from '@/components/ui';
import type { FiveElementsDisplay, Element } from '@/types/saju';

interface FiveElementsChartProps {
  analysis: FiveElementsDisplay;
}

const ELEMENT_COLORS: Record<Element, string> = {
  '목': '#22c55e',
  '화': '#ef4444',
  '토': '#eab308',
  '금': '#a1a1aa',
  '수': '#3b82f6',
};

const ELEMENT_LABELS: Record<Element, { hanja: string; korean: string }> = {
  '목': { hanja: '木', korean: '목' },
  '화': { hanja: '火', korean: '화' },
  '토': { hanja: '土', korean: '토' },
  '금': { hanja: '金', korean: '금' },
  '수': { hanja: '水', korean: '수' },
};

export function FiveElementsChart({ analysis }: FiveElementsChartProps) {
  const elements: Element[] = ['목', '화', '토', '금', '수'];

  const radarData = elements.map((element) => ({
    element: ELEMENT_LABELS[element].hanja,
    value: analysis.distribution[element] || 0,
    fullMark: 8,
  }));

  const barData = elements.map((element) => ({
    name: ELEMENT_LABELS[element].hanja,
    korean: ELEMENT_LABELS[element].korean,
    value: analysis.distribution[element] || 0,
    color: ELEMENT_COLORS[element],
  }));

  return (
    <section className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold text-foreground mb-6 text-center"
      >
        오행 분석 (五行)
      </motion.h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <GlassCard className="p-6">
            <h3 className="text-lg font-medium text-foreground mb-4 text-center">
              오행 균형도
            </h3>
            <ResponsiveContainer width="100%" height={280}>
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="rgba(28,32,43,0.15)" />
                <PolarAngleAxis
                  dataKey="element"
                  tick={{ fill: 'rgba(28,32,43,0.8)', fontSize: 14 }}
                />
                <PolarRadiusAxis
                  angle={90}
                  domain={[0, 8]}
                  tick={{ fill: 'rgba(84,96,138,0.7)', fontSize: 10 }}
                />
                <Radar
                  name="오행"
                  dataKey="value"
                  stroke="#7107e7"
                  fill="#7107e7"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </GlassCard>
        </motion.div>

        {/* Bar Chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <GlassCard className="p-6">
            <h3 className="text-lg font-medium text-foreground mb-4 text-center">
              오행 분포
            </h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={barData} layout="vertical">
                <XAxis type="number" domain={[0, 8]} tick={{ fill: 'rgba(84,96,138,0.7)' }} />
                <YAxis
                  type="category"
                  dataKey="name"
                  tick={{ fill: 'rgba(28,32,43,0.8)', fontSize: 16 }}
                  width={40}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </GlassCard>
        </motion.div>
      </div>

      {/* Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mt-6"
      >
        <GlassCard className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <span className="text-muted-foreground text-sm">주요 오행</span>
              <div className="text-xl font-bold font-mono text-primary mt-1">
                {analysis.dominant ? ELEMENT_LABELS[analysis.dominant].hanja : '-'}
              </div>
            </div>
            <div>
              <span className="text-muted-foreground text-sm">부족 오행</span>
              <div className="text-xl font-bold font-mono text-danger mt-1">
                {analysis.lacking ? ELEMENT_LABELS[analysis.lacking].hanja : '-'}
              </div>
            </div>
            <div>
              <span className="text-muted-foreground text-sm">용신</span>
              <div className="text-xl font-bold font-mono text-success mt-1">
                {analysis.yongshin ? ELEMENT_LABELS[analysis.yongshin].hanja : '-'}
              </div>
            </div>
            <div>
              <span className="text-muted-foreground text-sm">기신</span>
              <div className="text-xl font-bold font-mono text-warning mt-1">
                {analysis.gishin ? ELEMENT_LABELS[analysis.gishin].hanja : '-'}
              </div>
            </div>
          </div>
        </GlassCard>
      </motion.div>
    </section>
  );
}
