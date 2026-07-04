'use client';

import { motion } from 'framer-motion';
import { GlassCard, Icon } from '@/components/ui';
import type { Element } from '@/types/saju';

interface PentagonChartProps {
  dayMaster: Element;
  distribution: Record<Element, number>;
  tenGodMapping?: Record<Element, string>;
  dayStemKorean?: string; // 일간 천간 한글 (예: '경')
}

// 일간 천간 → 표시 매핑
const DAY_MASTER_DISPLAY: Record<string, string> = {
  '갑': '갑목(甲木)',
  '을': '을목(乙木)',
  '병': '병화(丙火)',
  '정': '정화(丁火)',
  '무': '무토(戊土)',
  '기': '기토(己土)',
  '경': '경금(庚金)',
  '신': '신금(辛金)',
  '임': '임수(壬水)',
  '계': '계수(癸水)',
};

// 오행 순서 (오각형 배치: 위쪽부터 시계방향)
const ELEMENTS_ORDER: Element[] = ['금', '수', '화', '목', '토'];

// 오행별 색상
const ELEMENT_COLORS: Record<Element, { bg: string; text: string; border: string }> = {
  '목': { bg: 'bg-green-500/20', text: 'text-green-400', border: 'border-green-500' },
  '화': { bg: 'bg-red-500/20', text: 'text-red-400', border: 'border-red-500' },
  '토': { bg: 'bg-yellow-500/20', text: 'text-yellow-400', border: 'border-yellow-500' },
  '금': { bg: 'bg-gray-300/20', text: 'text-gray-300', border: 'border-gray-300' },
  '수': { bg: 'bg-blue-500/20', text: 'text-blue-400', border: 'border-blue-500' },
};

// 십성 그룹 (오행 -> 십성)
const TEN_GOD_GROUPS: Record<Element, string> = {
  '금': '비겁',
  '수': '식상',
  '목': '재성',
  '화': '관성',
  '토': '인성',
};

// 오각형 꼭지점 좌표 계산 (SVG viewBox 기준)
const getVertexPosition = (index: number, centerX: number, centerY: number, radius: number) => {
  // 위쪽(12시 방향)부터 시작, 시계방향
  const angle = (index * 72 - 90) * (Math.PI / 180);
  return {
    x: centerX + radius * Math.cos(angle),
    y: centerY + radius * Math.sin(angle),
  };
};

export function PentagonChart({ dayMaster, distribution, tenGodMapping, dayStemKorean }: PentagonChartProps) {
  const centerX = 150;
  const centerY = 150;
  const outerRadius = 120;
  const innerRadius = 50;

  // dayMaster가 유효한지 확인
  const validDayMaster = ELEMENTS_ORDER.includes(dayMaster) ? dayMaster : '금';

  // 오행 배치 순서 (나의 오행 기준으로 재배치)
  const dayMasterIndex = ELEMENTS_ORDER.indexOf(validDayMaster);
  const orderedElements = ELEMENTS_ORDER.map((_, i) =>
    ELEMENTS_ORDER[(dayMasterIndex + i) % 5]
  );

  // 총합 계산
  const total = Object.values(distribution).reduce((sum, val) => sum + (val || 0), 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:chart-bold" size={24} className="text-primary" />
        <h2 className="text-xl font-bold text-foreground">나의 오행: {dayStemKorean ? DAY_MASTER_DISPLAY[dayStemKorean] || dayMaster : dayMaster}</h2>
      </div>

      <GlassCard className="p-4 md:p-6">
        {/* 범례 */}
        <div className="flex items-center gap-6 mb-4 text-sm">
          <div className="flex items-center gap-2">
            <span className="text-cyan-400">→</span>
            <span className="text-muted-foreground">생(生)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-red-400">→</span>
            <span className="text-muted-foreground">극(剋)</span>
          </div>
        </div>

        <div className="flex justify-center">
          <svg viewBox="0 0 300 300" className="w-full max-w-[300px] h-auto">
            {/* 생(生) 화살표 - 파란색 외곽 */}
            {orderedElements.map((element, i) => {
              const from = getVertexPosition(i, centerX, centerY, outerRadius - 30);
              const to = getVertexPosition((i + 1) % 5, centerX, centerY, outerRadius - 30);
              const midX = (from.x + to.x) / 2;
              const midY = (from.y + to.y) / 2;
              // 외곽으로 휘어지게
              const curveX = midX + (midX - centerX) * 0.3;
              const curveY = midY + (midY - centerY) * 0.3;

              return (
                <g key={`sheng-${i}`}>
                  <defs>
                    <marker
                      id={`arrowhead-blue-${i}`}
                      markerWidth="6"
                      markerHeight="6"
                      refX="5"
                      refY="3"
                      orient="auto"
                    >
                      <path d="M0,0 L6,3 L0,6 Z" fill="#22d3ee" />
                    </marker>
                  </defs>
                  <path
                    d={`M ${from.x} ${from.y} Q ${curveX} ${curveY} ${to.x} ${to.y}`}
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    markerEnd={`url(#arrowhead-blue-${i})`}
                    opacity="0.6"
                  />
                </g>
              );
            })}

            {/* 극(剋) 화살표 - 빨간색 내부 별 */}
            {orderedElements.map((element, i) => {
              const from = getVertexPosition(i, centerX, centerY, innerRadius + 20);
              const to = getVertexPosition((i + 2) % 5, centerX, centerY, innerRadius + 20);

              return (
                <g key={`ke-${i}`}>
                  <defs>
                    <marker
                      id={`arrowhead-red-${i}`}
                      markerWidth="6"
                      markerHeight="6"
                      refX="5"
                      refY="3"
                      orient="auto"
                    >
                      <path d="M0,0 L6,3 L0,6 Z" fill="#f87171" />
                    </marker>
                  </defs>
                  <line
                    x1={from.x}
                    y1={from.y}
                    x2={to.x}
                    y2={to.y}
                    stroke="#f87171"
                    strokeWidth="1.5"
                    markerEnd={`url(#arrowhead-red-${i})`}
                    opacity="0.6"
                  />
                </g>
              );
            })}

            {/* 오행 노드들 */}
            {orderedElements.map((element, i) => {
              const pos = getVertexPosition(i, centerX, centerY, outerRadius);
              const percentage = total > 0 ? Math.round((distribution[element] / total) * 100) : 0;
              const tenGod = tenGodMapping?.[element] || TEN_GOD_GROUPS[element];
              const colors = ELEMENT_COLORS[element];
              const isMyElement = element === dayMaster;

              return (
                <g key={element}>
                  {/* 원 배경 */}
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={35}
                    className={`${colors.bg} ${isMyElement ? 'stroke-primary stroke-2' : 'stroke-border/30 stroke-1'}`}
                    fill="currentColor"
                    style={{ fill: colors.bg.includes('green') ? 'rgba(34, 197, 94, 0.2)' :
                             colors.bg.includes('red') ? 'rgba(239, 68, 68, 0.2)' :
                             colors.bg.includes('yellow') ? 'rgba(234, 179, 8, 0.2)' :
                             colors.bg.includes('gray') ? 'rgba(209, 213, 219, 0.2)' :
                             'rgba(59, 130, 246, 0.2)' }}
                  />
                  {/* 오행 + 십성 */}
                  <text
                    x={pos.x}
                    y={pos.y - 8}
                    textAnchor="middle"
                    className={`text-xs fill-foreground/80`}
                  >
                    {element}({tenGod})
                  </text>
                  {/* 비율 */}
                  <text
                    x={pos.x}
                    y={pos.y + 10}
                    textAnchor="middle"
                    className={`text-sm font-bold font-mono ${colors.text}`}
                    style={{ fill: colors.text.includes('green') ? '#16A34A' :
                             colors.text.includes('red') ? '#DC2626' :
                             colors.text.includes('yellow') ? '#D97706' :
                             colors.text.includes('gray') ? '#64748B' :
                             '#2563EB' }}
                  >
                    {percentage}%
                  </text>
                </g>
              );
            })}
          </svg>
        </div>
      </GlassCard>
    </motion.div>
  );
}

export default PentagonChart;
