'use client';

import { motion } from 'framer-motion';
import { GlassCard, Icon } from '@/components/ui';
import { ELEMENT_COLORS } from '@/lib/constants/elements';
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

// 생(生)/극(剋) 관계선 색상 (AA 대비 통과 · 흰 배경 기준)
const SHENG_COLOR = '#2563EB';
const KE_COLOR = '#DC2626';

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
        <Icon name="solar:chart-bold" size={24} className="text-accent" />
        <h2 className="font-display text-xl text-foreground">나의 오행: {dayStemKorean ? DAY_MASTER_DISPLAY[dayStemKorean] || dayMaster : dayMaster}</h2>
      </div>

      <GlassCard className="p-4 md:p-6">
        {/* 범례 */}
        <div className="flex items-center gap-6 mb-4 text-sm">
          <div className="flex items-center gap-2">
            <svg width="28" height="10" viewBox="0 0 28 10" aria-hidden="true">
              <defs>
                <marker id="legend-arrow-sheng" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                  <path d="M0,0 L6,3 L0,6 Z" fill={SHENG_COLOR} />
                </marker>
              </defs>
              <line
                x1="1"
                y1="5"
                x2="20"
                y2="5"
                stroke={SHENG_COLOR}
                strokeWidth="1.5"
                markerEnd="url(#legend-arrow-sheng)"
              />
            </svg>
            <span className="text-muted-foreground">생(生)</span>
          </div>
          <div className="flex items-center gap-2">
            <svg width="28" height="10" viewBox="0 0 28 10" aria-hidden="true">
              <defs>
                <marker id="legend-arrow-ke" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                  <path d="M0,0 L6,3 L0,6 Z" fill={KE_COLOR} />
                </marker>
              </defs>
              <line
                x1="1"
                y1="5"
                x2="20"
                y2="5"
                stroke={KE_COLOR}
                strokeWidth="1.5"
                strokeDasharray="5 4"
                markerEnd="url(#legend-arrow-ke)"
              />
            </svg>
            <span className="text-muted-foreground">극(剋)</span>
          </div>
        </div>

        <div className="flex justify-center">
          <svg viewBox="0 0 300 300" className="w-full max-w-[300px] h-auto">
            <defs>
              <marker id="arrowhead-sheng" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill={SHENG_COLOR} />
              </marker>
              <marker id="arrowhead-ke" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                <path d="M0,0 L6,3 L0,6 Z" fill={KE_COLOR} />
              </marker>
            </defs>

            {/* 생(生) 화살표 - 실선 외곽 */}
            {orderedElements.map((element, i) => {
              const from = getVertexPosition(i, centerX, centerY, outerRadius - 30);
              const to = getVertexPosition((i + 1) % 5, centerX, centerY, outerRadius - 30);
              const midX = (from.x + to.x) / 2;
              const midY = (from.y + to.y) / 2;
              // 외곽으로 휘어지게
              const curveX = midX + (midX - centerX) * 0.3;
              const curveY = midY + (midY - centerY) * 0.3;

              return (
                <path
                  key={`sheng-${i}`}
                  d={`M ${from.x} ${from.y} Q ${curveX} ${curveY} ${to.x} ${to.y}`}
                  fill="none"
                  stroke={SHENG_COLOR}
                  strokeWidth="1.5"
                  markerEnd="url(#arrowhead-sheng)"
                />
              );
            })}

            {/* 극(剋) 화살표 - 파선 내부 별 */}
            {orderedElements.map((element, i) => {
              const from = getVertexPosition(i, centerX, centerY, innerRadius + 20);
              const to = getVertexPosition((i + 2) % 5, centerX, centerY, innerRadius + 20);

              return (
                <line
                  key={`ke-${i}`}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke={KE_COLOR}
                  strokeWidth="1.5"
                  strokeDasharray="5 4"
                  markerEnd="url(#arrowhead-ke)"
                />
              );
            })}

            {/* 오행 노드들 */}
            {orderedElements.map((element, i) => {
              const pos = getVertexPosition(i, centerX, centerY, outerRadius);
              const percentage = total > 0 ? Math.round((distribution[element] / total) * 100) : 0;
              const tenGod = tenGodMapping?.[element] || TEN_GOD_GROUPS[element];
              const elementHex = ELEMENT_COLORS[element].hex;
              const isMyElement = element === dayMaster;

              return (
                <g key={element}>
                  {/* 원 배경 */}
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={35}
                    className={isMyElement ? 'stroke-accent stroke-2' : 'stroke-border/30 stroke-1'}
                    style={{ fill: `${elementHex}33` }}
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
                    className="text-sm font-bold font-mono fill-foreground"
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
