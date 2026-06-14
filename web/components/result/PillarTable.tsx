'use client';

import { motion } from 'framer-motion';
import { GlassCard, ElementBadge } from '@/components/ui';
import type { Element } from '@/types/saju';

// 오행별 배경색
const ELEMENT_BG_COLORS: Record<Element, string> = {
  '목': 'bg-element-wood/20',
  '화': 'bg-element-fire/20',
  '토': 'bg-element-earth/20',
  '금': 'bg-element-metal/20',
  '수': 'bg-element-water/20',
};

const ELEMENT_TEXT_COLORS: Record<Element, string> = {
  '목': 'text-element-wood',
  '화': 'text-element-fire',
  '토': 'text-element-earth',
  '금': 'text-element-metal',
  '수': 'text-element-water',
};

// 영어/한글 오행을 한글로 변환
const ELEMENT_KOREAN: Record<string, string> = {
  'wood': '목', 'fire': '화', 'earth': '토', 'metal': '금', 'water': '수',
  '목': '목', '화': '화', '토': '토', '금': '금', '수': '수',
};

// 오행 한자 매핑
const ELEMENT_HANJA: Record<string, string> = {
  'wood': '木', 'fire': '火', 'earth': '土', 'metal': '金', 'water': '水',
  '목': '木', '화': '火', '토': '土', '금': '金', '수': '水',
};

interface PillarInfo {
  heavenly_stem: {
    hanja: string;
    korean: string;
    element: Element;
    polarity: '양' | '음';
  };
  earthly_branch: {
    hanja: string;
    korean: string;
    element: Element;
    polarity: '양' | '음';
  };
  ten_god?: string | null;
  branch_ten_god?: string | null;
  hidden_stems?: string;
  twelve_phase?: string;
  twelve_shensha?: string;
}

interface PillarTableProps {
  pillars: {
    year: PillarInfo;
    month: PillarInfo;
    day: PillarInfo;
    hour: PillarInfo;
  };
  showHiddenStems?: boolean;
  showTwelvePhase?: boolean;
  showTwelveShensha?: boolean;
}

export function PillarTable({
  pillars,
  showHiddenStems = true,
  showTwelvePhase = true,
  showTwelveShensha = true,
}: PillarTableProps) {
  const columns = [
    { key: 'hour', label: '생시' },
    { key: 'day', label: '생일' },
    { key: 'month', label: '생월' },
    { key: 'year', label: '생년' },
  ];

  const getPillar = (key: string) => pillars[key as keyof typeof pillars];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-8"
    >
      <GlassCard className="p-4 md:p-6 overflow-x-auto">
        <table className="w-full min-w-[400px]">
          <thead>
            <tr>
              <th className="text-left text-muted-foreground text-sm py-2 px-2 w-16"></th>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="text-center text-gray-600 text-sm font-medium py-2 px-2 border-b border-border"
                >
                  <span className="underline decoration-white/30">{col.label}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* 천간 십성 행 */}
            <tr>
              <td className="text-muted-foreground text-xs py-2 px-2">십성</td>
              {columns.map((col) => {
                const pillar = getPillar(col.key);
                return (
                  <td key={col.key} className="text-center py-2 px-2">
                    <span className="text-sm text-foreground">
                      {pillar.ten_god || '-'}
                    </span>
                  </td>
                );
              })}
            </tr>

            {/* 천간 행 */}
            <tr>
              <td className="text-muted-foreground text-xs py-2 px-2">천간</td>
              {columns.map((col) => {
                const pillar = getPillar(col.key);
                const stem = pillar.heavenly_stem;
                const polarity = stem.polarity === '양' ? '+' : '-';
                const elementKorean = ELEMENT_KOREAN[stem.element] || stem.element;
                const elementHanja = ELEMENT_HANJA[stem.element] || '';
                return (
                  <td key={col.key} className="text-center py-2 px-2">
                    <div
                      className={`inline-flex flex-col items-center justify-center w-14 h-14 rounded-lg ${ELEMENT_BG_COLORS[elementKorean as Element]}`}
                    >
                      <span className={`text-xl font-bold ${ELEMENT_TEXT_COLORS[elementKorean as Element]}`}>
                        {stem.korean}
                        <span className="text-xs ml-0.5">{stem.hanja}</span>
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {polarity}{elementKorean} ({elementHanja})
                      </span>
                    </div>
                  </td>
                );
              })}
            </tr>

            {/* 지지 행 */}
            <tr>
              <td className="text-muted-foreground text-xs py-2 px-2">지지</td>
              {columns.map((col) => {
                const pillar = getPillar(col.key);
                const branch = pillar.earthly_branch;
                const polarity = branch.polarity === '양' ? '+' : '-';
                const elementKorean = ELEMENT_KOREAN[branch.element] || branch.element;
                const elementHanja = ELEMENT_HANJA[branch.element] || '';
                return (
                  <td key={col.key} className="text-center py-2 px-2">
                    <div
                      className={`inline-flex flex-col items-center justify-center w-14 h-14 rounded-lg ${ELEMENT_BG_COLORS[elementKorean as Element]}`}
                    >
                      <span className={`text-xl font-bold ${ELEMENT_TEXT_COLORS[elementKorean as Element]}`}>
                        {branch.korean}
                        <span className="text-xs ml-0.5">{branch.hanja}</span>
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {polarity}{elementKorean} ({elementHanja})
                      </span>
                    </div>
                  </td>
                );
              })}
            </tr>

            {/* 지지 십성 행 */}
            <tr>
              <td className="text-muted-foreground text-xs py-2 px-2">십성</td>
              {columns.map((col) => {
                const pillar = getPillar(col.key);
                return (
                  <td key={col.key} className="text-center py-2 px-2">
                    <span className="text-sm text-foreground">
                      {pillar.branch_ten_god || '-'}
                    </span>
                  </td>
                );
              })}
            </tr>

            {/* 지장간 행 */}
            {showHiddenStems && (
              <tr>
                <td className="text-muted-foreground text-xs py-2 px-2">지장간</td>
                {columns.map((col) => {
                  const pillar = getPillar(col.key);
                  return (
                    <td key={col.key} className="text-center py-2 px-2">
                      <span className="text-xs text-muted-foreground">
                        {pillar.hidden_stems || '-'}
                      </span>
                    </td>
                  );
                })}
              </tr>
            )}

            {/* 12운성 행 */}
            {showTwelvePhase && (
              <tr>
                <td className="text-muted-foreground text-xs py-2 px-2">12운성</td>
                {columns.map((col) => {
                  const pillar = getPillar(col.key);
                  return (
                    <td key={col.key} className="text-center py-2 px-2">
                      <span className="text-xs text-gray-600">
                        {pillar.twelve_phase || '-'}
                      </span>
                    </td>
                  );
                })}
              </tr>
            )}

            {/* 12신살 행 */}
            {showTwelveShensha && (
              <tr>
                <td className="text-muted-foreground text-xs py-2 px-2">12신살</td>
                {columns.map((col) => {
                  const pillar = getPillar(col.key);
                  return (
                    <td key={col.key} className="text-center py-2 px-2">
                      <span className="text-xs text-muted-foreground">
                        {pillar.twelve_shensha || '-'}
                      </span>
                    </td>
                  );
                })}
              </tr>
            )}
          </tbody>
        </table>
      </GlassCard>
    </motion.div>
  );
}

export default PillarTable;
