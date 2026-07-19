'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import { ELEMENT_COLORS } from '@/lib/constants/elements';
import type { Element } from '@/types/saju';

interface ElementDistributionProps {
  distribution: Record<Element, number>;
  tenGods: Record<string, number>;
  dominant: Element | null;
}

// 오행별 정보 (색상은 element-* 토큰 = 시맨틱 팔레트와 정렬)
const ELEMENT_INFO: Record<Element, { hanja: string; color: string; bg: string }> = {
  '목': { hanja: '木', color: 'bg-element-wood', bg: 'bg-element-wood/20' },
  '화': { hanja: '火', color: 'bg-element-fire', bg: 'bg-element-fire/20' },
  '토': { hanja: '土', color: 'bg-element-earth', bg: 'bg-element-earth/20' },
  '금': { hanja: '金', color: 'bg-element-metal', bg: 'bg-element-metal/20' },
  '수': { hanja: '水', color: 'bg-element-water', bg: 'bg-element-water/20' },
};

// 십성별 오행 매핑
const TEN_GOD_TO_ELEMENT: Record<string, Element> = {
  '비견': '금',
  '겁재': '금',
  '식신': '수',
  '상관': '수',
  '편재': '목',
  '정재': '목',
  '편관': '화',
  '정관': '화',
  '편인': '토',
  '정인': '토',
};

// 십성 그룹 (음양 쌍)
const TEN_GOD_PAIRS = [
  { yin: '정재', yang: '편재', hanja: { yin: '正財', yang: '偏財' } },
  { yin: '정관', yang: '편관', hanja: { yin: '正官', yang: '偏官' } },
  { yin: '정인', yang: '편인', hanja: { yin: '正印', yang: '偏印' } },
  { yin: '겁재', yang: '비견', hanja: { yin: '劫財', yang: '比肩' } },
  { yin: '상관', yang: '식신', hanja: { yin: '傷官', yang: '食神' } },
];

// 십성 순서 및 색상 (도넛·범례 공유)
const TEN_GOD_ORDER = ['비견', '겁재', '식신', '상관', '편재', '정재', '편관', '정관', '편인', '정인'];
// 무채 slate 램프 — 쌍=밴드·양간=밝음, 백색 대비 바닥 3.47:1, muted 위 3.13:1
const TEN_GOD_COLORS: Record<string, string> = {
  '비견': '#748BAF', '겁재': '#637DA6',   // 비겁 밴드(최명) 3.47 / 4.19:1
  '식신': '#43587B', '상관': '#3A4D6C',   // 식상 밴드(중)   7.19 / 8.54:1
  '편재': '#1E293B', '정재': '#131A25',   // 재   밴드(최암) 14.63 / 17.47:1
  '편관': '#57709A', '정관': '#4D648B',   // 관   밴드(명중) 5.01 / 5.98:1
  '편인': '#31425C', '정인': '#28364C',   // 인   밴드(암중) 10.17 / 12.19:1
};

export function ElementDistribution({ distribution, tenGods, dominant }: ElementDistributionProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const total = Object.values(distribution).reduce((sum, val) => sum + val, 0);
  const totalTenGods = Object.values(tenGods).reduce((sum, val) => sum + val, 0);

  // 오행 또는 십성 클릭 시 용어집 모달 열기
  const handleClick = (term: string) => {
    // 다양한 형태로 검색 (예: "목" -> "갑목" 또는 "목")
    const searchTerms = [term];

    // 오행인 경우 관련 천간 추가
    const elementToStem: Record<string, string[]> = {
      '목': ['갑목', '을목'],
      '화': ['병화', '정화'],
      '토': ['무토', '기토'],
      '금': ['경금', '신금'],
      '수': ['임수', '계수'],
    };

    if (elementToStem[term]) {
      searchTerms.push(...elementToStem[term]);
    }

    for (const searchTerm of searchTerms) {
      const entry = getGlossaryEntry(searchTerm);
      if (entry) {
        setSelectedEntry(entry);
        setIsModalOpen(true);
        return;
      }
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEntry(null);
  };

  // 오행 순서: 목, 화, 토, 금, 수
  const elementOrder: Element[] = ['목', '화', '토', '금', '수'];

  const getPercentage = (value: number, total: number) => {
    if (total === 0) return 0;
    return Math.round((value / total) * 1000) / 10;
  };

  const getStatus = (element: Element, percentage: number) => {
    if (percentage === 0) return { label: '부족', color: 'text-danger-ink' };
    if (percentage >= 30) return { label: '발달', color: 'text-success-ink' };
    return { label: '', color: '' };
  };

  // 도넛 aria-label (색-단독 인코딩 보완)
  const elementAriaLabel =
    '오행 분포: ' +
    elementOrder
      .map((element) => `${element} ${getPercentage(distribution[element] || 0, total)}%`)
      .join(', ');
  const tenGodAriaLabel =
    '십성 분포: ' +
    TEN_GOD_ORDER.filter((god) => getPercentage(tenGods[god] || 0, totalTenGods) > 0)
      .map((god) => `${god} ${getPercentage(tenGods[god] || 0, totalTenGods)}%`)
      .join(', ');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.25 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:pie-chart-2-bold" size={24} className="text-accent" />
        <button
          onClick={() => {
            const entry = getGlossaryEntry('오행분포');
            if (entry) {
              setSelectedEntry(entry);
              setIsModalOpen(true);
            }
          }}
          className="font-display text-xl text-foreground underline decoration-border/30 hover:decoration-accent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          오행 / 십성 분포
        </button>
      </div>

      <p className="text-muted-foreground text-sm mb-4">아래 박스를 터치해보세요.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 오행 분포 */}
        <div className="space-y-3">
          {elementOrder.map((element) => {
            const value = distribution[element] || 0;
            const percentage = getPercentage(value, total);
            const info = ELEMENT_INFO[element];
            const status = getStatus(element, percentage);

            return (
              <div key={element} className="flex items-stretch gap-3">
                {/* 오행 박스 */}
                <div
                  onClick={() => handleClick(element)}
                  className={`${info.bg} rounded-xl border-[1.5px] border-border shadow-block-sm p-3 min-w-[100px] flex flex-col justify-center cursor-pointer hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover transition-all`}
                >
                  <div className="text-foreground font-bold font-mono">
                    {element}{info.hanja}{' '}
                    {percentage > 0 ? `${percentage}%` : '-'}
                  </div>
                  {status.label && (
                    <span className={`text-xs ${status.color} mt-1`}>
                      {status.label}
                    </span>
                  )}
                </div>

                {/* 관련 십성 */}
                <GlassCard className="flex-1 p-3">
                  <div className="space-y-1">
                    {TEN_GOD_PAIRS
                      .filter((pair) => TEN_GOD_TO_ELEMENT[pair.yin] === element)
                      .map((pair) => {
                        const yinValue = tenGods[pair.yin] || 0;
                        const yangValue = tenGods[pair.yang] || 0;
                        const yinPct = getPercentage(yinValue, totalTenGods);
                        const yangPct = getPercentage(yangValue, totalTenGods);

                        return (
                          <div
                            key={pair.yin}
                            onClick={() => handleClick(pair.yin)}
                            className="flex justify-between text-sm cursor-pointer hover:bg-muted rounded-lg px-1 -mx-1 transition-colors"
                          >
                            <span className="text-muted-foreground">
                              {pair.yin}({pair.hanja.yin})
                            </span>
                            <span className="text-muted-foreground font-mono">
                              {yinPct > 0 ? `${yinPct}%` : '-'}
                            </span>
                          </div>
                        );
                      })}
                    {TEN_GOD_PAIRS
                      .filter((pair) => TEN_GOD_TO_ELEMENT[pair.yang] === element)
                      .map((pair) => {
                        const yangValue = tenGods[pair.yang] || 0;
                        const yangPct = getPercentage(yangValue, totalTenGods);

                        return (
                          <div
                            key={pair.yang}
                            onClick={() => handleClick(pair.yang)}
                            className="flex justify-between text-sm border-t-[1.5px] border-border pt-1 cursor-pointer hover:bg-muted rounded-lg px-1 -mx-1 transition-colors"
                          >
                            <span className="text-muted-foreground">
                              {pair.yang}({pair.hanja.yang})
                            </span>
                            <span className="text-muted-foreground font-mono">
                              {yangPct > 0 ? `${yangPct}%` : '-'}
                            </span>
                          </div>
                        );
                      })}
                  </div>
                </GlassCard>
              </div>
            );
          })}
        </div>

        {/* 도넛 차트 영역 - 오행/십성 2개 */}
        <div className="flex flex-col items-center justify-center gap-6">
          {/* 오행/십성 차트 나란히 */}
          <div className="flex gap-8 items-start">
            {/* 오행 도넛 */}
            <div className="flex flex-col items-center">
              <span className="text-sm text-muted-foreground mb-2">오행</span>
              <div className="relative w-32 h-32">
                <svg viewBox="0 0 100 100" className="w-full h-full" role="img" aria-label={elementAriaLabel}>
                  {(() => {
                    const radius = 40;
                    const circumference = 2 * Math.PI * radius;
                    let cumulativeOffset = 0;
                    const startOffset = circumference * 0.25;
                    const GAP = 2;
                    const segmentCount = elementOrder.filter(
                      (element) => getPercentage(distribution[element] || 0, total) > 0
                    ).length;

                    return elementOrder.map((element) => {
                      const percentage = getPercentage(distribution[element] || 0, total);
                      const segmentLength = (percentage / 100) * circumference;
                      const visible = segmentCount > 1 ? Math.max(segmentLength - GAP, 1) : segmentLength;
                      const dashArray = `${visible} ${circumference - visible}`;
                      const dashOffset = startOffset - cumulativeOffset;

                      cumulativeOffset += segmentLength;

                      if (percentage === 0) return null;

                      return (
                        <circle
                          key={element}
                          cx="50"
                          cy="50"
                          r={radius}
                          fill="none"
                          stroke={ELEMENT_COLORS[element].hex}
                          strokeWidth="12"
                          strokeDasharray={dashArray}
                          strokeDashoffset={dashOffset}
                          strokeLinecap="butt"
                        />
                      );
                    });
                  })()}
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xl font-bold text-foreground">{dominant || '-'}</span>
                </div>
              </div>
            </div>

            {/* 십성 도넛 */}
            <div className="flex flex-col items-center">
              <span className="text-sm text-muted-foreground mb-2">십성</span>
              <div className="relative w-32 h-32">
                <svg viewBox="0 0 100 100" className="w-full h-full" role="img" aria-label={tenGodAriaLabel}>
                  {(() => {
                    const radius = 40;
                    const circumference = 2 * Math.PI * radius;
                    let cumulativeOffset = 0;
                    const startOffset = circumference * 0.25;
                    const GAP = 2;

                    const segmentCount = TEN_GOD_ORDER.filter(
                      (god) => getPercentage(tenGods[god] || 0, totalTenGods) > 0
                    ).length;

                    return TEN_GOD_ORDER.map((god) => {
                      const value = tenGods[god] || 0;
                      const percentage = getPercentage(value, totalTenGods);
                      const segmentLength = (percentage / 100) * circumference;
                      const visible = segmentCount > 1 ? Math.max(segmentLength - GAP, 1) : segmentLength;
                      const dashArray = `${visible} ${circumference - visible}`;
                      const dashOffset = startOffset - cumulativeOffset;

                      cumulativeOffset += segmentLength;

                      if (percentage === 0) return null;

                      return (
                        <circle
                          key={god}
                          cx="50"
                          cy="50"
                          r={radius}
                          fill="none"
                          stroke={TEN_GOD_COLORS[god]}
                          strokeWidth="12"
                          strokeDasharray={dashArray}
                          strokeDashoffset={dashOffset}
                          strokeLinecap="butt"
                        />
                      );
                    });
                  })()}
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-lg font-bold text-foreground">
                    {(() => {
                      // 가장 많은 십성 찾기
                      const maxGod = Object.entries(tenGods).reduce(
                        (max, [god, count]) => (count > max.count ? { god, count } : max),
                        { god: '-', count: 0 }
                      );
                      return maxGod.god;
                    })()}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 범례 */}
          <div className="flex flex-wrap justify-center gap-2">
            {elementOrder.map((element) => {
              const percentage = getPercentage(distribution[element] || 0, total);
              return (
                <div key={element} className="flex items-center gap-1 text-xs">
                  <div className={`w-3 h-3 rounded-sm border-[1.5px] border-border ${ELEMENT_INFO[element].color}`} />
                  <span className="text-muted-foreground font-mono">
                    {element} {percentage}%
                  </span>
                </div>
              );
            })}
          </div>

          {/* 십성 범례 */}
          <div data-legend="ten-gods" className="flex flex-wrap justify-center gap-2">
            {TEN_GOD_ORDER.map((god) => {
              const percentage = getPercentage(tenGods[god] || 0, totalTenGods);
              return (
                <div key={god} className="flex items-center gap-1 text-xs">
                  <div
                    className="w-3 h-3 rounded-sm border-[1.5px] border-border"
                    style={{ backgroundColor: TEN_GOD_COLORS[god] }}
                  />
                  <span className="text-muted-foreground font-mono">
                    {god} {percentage}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* 상세 정보 모달 */}
      <GlossaryModal
        entry={selectedEntry}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </motion.div>
  );
}

export default ElementDistribution;
