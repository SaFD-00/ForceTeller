'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';

interface StrengthDistributionChartProps {
  name: string;
  score: number; // 0-100 신강/신약 점수
  strengthType: string; // 극약, 태약, 신약, 중화신약, 중화신강, 신강, 태강, 극왕
  percentile?: number; // 해당 유형의 비율 (예: 10.50%)
  deukryeong?: boolean; // 득령
  deukji?: boolean; // 득지
  deuksi?: boolean; // 득시
  deukse?: boolean; // 득세
}

// 신강/신약 레벨 정의
const STRENGTH_LEVELS = [
  { label: '극약', min: 0, max: 12.5 },
  { label: '태약', min: 12.5, max: 25 },
  { label: '신약', min: 25, max: 37.5 },
  { label: '중화신약', min: 37.5, max: 50 },
  { label: '중화신강', min: 50, max: 62.5 },
  { label: '신강', min: 62.5, max: 75 },
  { label: '태강', min: 75, max: 87.5 },
  { label: '극왕', min: 87.5, max: 100 },
];

// 분포 곡선 데이터 (정규분포 형태)
const generateCurvePoints = () => {
  const points = [];
  const width = 300;
  const height = 100;

  for (let i = 0; i <= 100; i += 2) {
    // 정규분포 형태 - 중앙이 높고 양 끝이 낮음
    const x = (i / 100) * width;
    const normalY = Math.exp(-Math.pow((i - 50) / 20, 2) / 2);
    const y = height - normalY * height * 0.9;
    points.push(`${x},${y}`);
  }

  return points.join(' ');
};

export function StrengthDistributionChart({
  name,
  score,
  strengthType,
  percentile,
  deukryeong,
  deukji,
  deuksi,
  deukse,
}: StrengthDistributionChartProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const curvePoints = generateCurvePoints();
  const markerX = (score / 100) * 300;

  // 점수에 따라 y 좌표 계산
  const normalY = Math.exp(-Math.pow((score - 50) / 20, 2) / 2);
  const markerY = 100 - normalY * 100 * 0.9;

  const handleTitleClick = () => {
    const entry = getGlossaryEntry('신강신약');
    if (entry) {
      setSelectedEntry(entry);
      setIsModalOpen(true);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEntry(null);
  };

  return (
    <>
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:chart-2-bold" size={24} className="text-primary" />
        <button
          onClick={handleTitleClick}
          className="text-xl font-bold text-foreground underline decoration-white/30 hover:decoration-primary transition-colors"
        >
          신강/신약지수
        </button>
      </div>

      <GlassCard className="p-4 md:p-6">
        {/* 설명 텍스트 */}
        <p className="text-foreground mb-2">
          {name}님은 <strong className="text-primary">{strengthType}</strong>한 사주입니다.
        </p>
        {percentile && (
          <p className="text-muted-foreground text-sm mb-4">
            {percentile}%의 사람이 여기에 해당합니다.
          </p>
        )}

        {/* 득령/득지/득시/득세 표시 */}
        {(deukryeong !== undefined || deukji !== undefined || deuksi !== undefined || deukse !== undefined) && (
          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-muted-foreground">득령</span>
              {deukryeong ? (
                <Icon name="solar:check-circle-bold" size={18} className="text-cyan-400" />
              ) : (
                <Icon name="solar:close-circle-bold" size={18} className="text-red-400" />
              )}
            </div>
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-muted-foreground">득지</span>
              {deukji ? (
                <Icon name="solar:check-circle-bold" size={18} className="text-cyan-400" />
              ) : (
                <Icon name="solar:close-circle-bold" size={18} className="text-red-400" />
              )}
            </div>
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-muted-foreground">득시</span>
              {deuksi ? (
                <Icon name="solar:check-circle-bold" size={18} className="text-cyan-400" />
              ) : (
                <Icon name="solar:close-circle-bold" size={18} className="text-red-400" />
              )}
            </div>
            <div className="flex items-center gap-1.5">
              <span className="text-sm text-muted-foreground">득세</span>
              {deukse ? (
                <Icon name="solar:check-circle-bold" size={18} className="text-cyan-400" />
              ) : (
                <Icon name="solar:close-circle-bold" size={18} className="text-red-400" />
              )}
            </div>
          </div>
        )}

        {/* 분포 곡선 차트 */}
        <div className="relative">
          <svg viewBox="0 0 300 130" className="w-full h-auto">
            {/* 배경 그리드 */}
            {STRENGTH_LEVELS.map((level, i) => (
              <rect
                key={level.label}
                x={(level.min / 100) * 300}
                y={0}
                width={(300 / 8)}
                height={100}
                fill={i % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.04)'}
              />
            ))}

            {/* 분포 곡선 */}
            <polyline
              points={curvePoints}
              fill="none"
              stroke="rgba(255,255,255,0.5)"
              strokeWidth="2"
            />

            {/* 곡선 아래 영역 채우기 */}
            <polygon
              points={`0,100 ${curvePoints} 300,100`}
              fill="url(#curveGradient)"
              opacity="0.3"
            />

            {/* 그라데이션 정의 */}
            <defs>
              <linearGradient id="curveGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="white" stopOpacity="0.2" />
                <stop offset="100%" stopColor="white" stopOpacity="0" />
              </linearGradient>
            </defs>

            {/* 현재 위치 마커 */}
            <circle
              cx={markerX}
              cy={markerY}
              r={6}
              fill="#0a0a0a"
              stroke="white"
              strokeWidth="2"
            />
            <text
              x={markerX}
              y={markerY + 20}
              textAnchor="middle"
              fill="white"
              fontSize="10"
            >
              나
            </text>

            {/* X축 레이블 */}
            {STRENGTH_LEVELS.map((level) => (
              <text
                key={level.label}
                x={(level.min / 100) * 300 + (300 / 16)}
                y={115}
                textAnchor="middle"
                fill="rgba(255,255,255,0.5)"
                fontSize="7"
              >
                {level.label}
              </text>
            ))}
          </svg>
        </div>

        {/* Y축 레이블 */}
        <div className="flex justify-between text-xs text-gray-400 mt-2 px-2">
          <span>0%</span>
          <span>25</span>
          <span></span>
          <span></span>
          <span></span>
        </div>
      </GlassCard>
    </motion.div>

    <GlossaryModal
      entry={selectedEntry}
      isOpen={isModalOpen}
      onClose={handleCloseModal}
    />
    </>
  );
}

export default StrengthDistributionChart;
