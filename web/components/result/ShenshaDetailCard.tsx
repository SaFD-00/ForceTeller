'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Icon, GlassCard, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import type { Element } from '@/types/saju';

interface ShenshaItem {
  name: string;
  hanja?: string;
  type: '길신' | '흉신' | '중성';
  position: string;
  description: string;
}

interface PillarInfo {
  heavenly_stem: {
    hanja: string;
    korean: string;
    element: Element;
  };
  earthly_branch: {
    hanja: string;
    korean: string;
    element: Element;
  };
  ten_god?: string | null;
  branch_ten_god?: string | null;
}

interface ShenshaDetailCardProps {
  shensha: ShenshaItem[];
  pillars?: {
    year: PillarInfo;
    month: PillarInfo;
    day: PillarInfo;
    hour: PillarInfo;
  };
}

// 신살 타입별 색상 (길/흉/중성 = 시맨틱 상태 토큰과 정렬)
const typeColors = {
  '길신': {
    bg: 'bg-success/20',
    text: 'text-success',
    border: 'border-success/30',
    icon: 'solar:star-bold',
  },
  '흉신': {
    bg: 'bg-danger/20',
    text: 'text-danger',
    border: 'border-danger/30',
    icon: 'solar:danger-triangle-bold',
  },
  '중성': {
    bg: 'bg-warning/20',
    text: 'text-warning',
    border: 'border-warning/30',
    icon: 'solar:star-shine-bold',
  },
};

// 오행별 배경색 (element-* 토큰과 정렬)
const ELEMENT_BG: Record<Element, string> = {
  '목': 'bg-element-wood/80',
  '화': 'bg-element-fire/80',
  '토': 'bg-element-earth/80',
  '금': 'bg-element-metal/80',
  '수': 'bg-element-water/80',
};

const ELEMENT_BG_LIGHT: Record<Element, string> = {
  '목': 'bg-element-wood/20',
  '화': 'bg-element-fire/20',
  '토': 'bg-element-earth/20',
  '금': 'bg-element-metal/20',
  '수': 'bg-element-water/20',
};

// 위치 한글 표시
const positionNames: Record<string, string> = {
  year: '년주',
  month: '월주',
  day: '일주',
  hour: '시주',
};

export function ShenshaDetailCard({ shensha, pillars }: ShenshaDetailCardProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [viewMode, setViewMode] = useState<'type' | 'pillar'>('pillar');

  // 타입별로 그룹화
  const grouped = {
    길신: shensha.filter(s => s.type === '길신'),
    중성: shensha.filter(s => s.type === '중성'),
    흉신: shensha.filter(s => s.type === '흉신'),
  };

  // 위치별로 그룹화
  const byPosition = {
    hour: shensha.filter(s => s.position === 'hour'),
    day: shensha.filter(s => s.position === 'day'),
    month: shensha.filter(s => s.position === 'month'),
    year: shensha.filter(s => s.position === 'year'),
  };

  const handleShenshaClick = (shenshaName: string) => {
    // 신살 이름에서 한자 부분 제거 (예: "장성살 (將星殺)" -> "장성살")
    const koreanName = shenshaName.replace(/\s*\([^)]*\)\s*$/, '').trim();

    // 다양한 형태로 검색
    const searchTerms = [
      koreanName,
      koreanName + '살',
      koreanName.replace('살', ''),
    ];

    for (const term of searchTerms) {
      const entry = getGlossaryEntry(term);
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

  if (shensha.length === 0) {
    return null;
  }

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mb-8"
      >
        <div className="flex items-center gap-2 mb-4">
          <Icon name="solar:stars-bold" size={24} className="text-primary" />
          <button
            onClick={() => {
              const entry = getGlossaryEntry('신살');
              if (entry) {
                setSelectedEntry(entry);
                setIsModalOpen(true);
              }
            }}
            className="text-xl font-bold text-foreground underline decoration-border/30 hover:decoration-primary transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
          >
            신살(神煞)
          </button>
          <span className="text-sm text-muted-foreground">
            총 {shensha.length}개
          </span>
        </div>

        {/* 뷰 모드 토글 */}
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setViewMode('pillar')}
            className={`btn-block block-press px-4 py-2 rounded-lg border-[1.5px] border-border text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
              viewMode === 'pillar'
                ? 'bg-primary text-white'
                : 'bg-muted text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            주별 보기
          </button>
          <button
            onClick={() => setViewMode('type')}
            className={`btn-block block-press px-4 py-2 rounded-lg border-[1.5px] border-border text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
              viewMode === 'type'
                ? 'bg-primary text-white'
                : 'bg-muted text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            유형별 보기
          </button>
        </div>

        {viewMode === 'pillar' && pillars ? (
          /* 주별 신살 테이블 */
          <GlassCard className="p-4 md:p-6 overflow-x-auto">
            <div className="min-w-[320px]">
              {/* 테이블 헤더 */}
              <div className="grid grid-cols-4 gap-2 mb-2">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => (
                  <div key={pos} className="text-center">
                    <span className="text-sm text-muted-foreground">
                      {pos === 'hour' ? '생시' : pos === 'day' ? '생일' : pos === 'month' ? '생월' : '생년'}
                    </span>
                  </div>
                ))}
              </div>

              {/* 천간 행 */}
              <div className="grid grid-cols-4 gap-2 mb-1">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => {
                  const pillar = pillars[pos];
                  return (
                    <div
                      key={`stem-${pos}`}
                      className={`${ELEMENT_BG[pillar.heavenly_stem.element]} rounded-lg p-2 text-center`}
                    >
                      <span className="text-lg font-bold text-foreground">
                        {pillar.heavenly_stem.korean}
                      </span>
                      <span className="text-xs text-muted-foreground ml-0.5">
                        {pillar.heavenly_stem.hanja}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* 천간 십성 행 */}
              <div className="grid grid-cols-4 gap-2 mb-2">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => {
                  const pillar = pillars[pos];
                  return (
                    <div key={`stem-tg-${pos}`} className="text-center">
                      <span className="text-xs text-muted-foreground">{pillar.ten_god || '-'}</span>
                    </div>
                  );
                })}
              </div>

              {/* 지지 행 */}
              <div className="grid grid-cols-4 gap-2 mb-1">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => {
                  const pillar = pillars[pos];
                  return (
                    <div
                      key={`branch-${pos}`}
                      className={`${ELEMENT_BG_LIGHT[pillar.earthly_branch.element]} rounded-lg p-2 text-center`}
                    >
                      <span className="text-lg font-bold text-foreground">
                        {pillar.earthly_branch.korean}
                      </span>
                      <span className="text-xs text-muted-foreground ml-0.5">
                        {pillar.earthly_branch.hanja}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* 지지 십성 행 */}
              <div className="grid grid-cols-4 gap-2 mb-4">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => {
                  const pillar = pillars[pos];
                  return (
                    <div key={`branch-tg-${pos}`} className="text-center">
                      <span className="text-xs text-muted-foreground">{pillar.branch_ten_god || '-'}</span>
                    </div>
                  );
                })}
              </div>

              {/* 구분선 */}
              <div className="border-t-[1.5px] border-border my-4" />

              {/* 신살 섹션 헤더 */}
              <div className="text-sm text-muted-foreground mb-3">신살</div>

              {/* 신살 목록 (주별) */}
              <div className="grid grid-cols-4 gap-2">
                {(['hour', 'day', 'month', 'year'] as const).map((pos) => {
                  const positionShensha = byPosition[pos];
                  return (
                    <div key={`shensha-${pos}`} className="space-y-1">
                      {positionShensha.length === 0 ? (
                        <span className="text-xs text-muted-foreground">-</span>
                      ) : (
                        positionShensha.map((item, idx) => {
                          const colors = typeColors[item.type];
                          return (
                            <button
                              key={`${item.name}-${idx}`}
                              onClick={() => handleShenshaClick(item.name)}
                              className={`btn-block block-press w-full text-left px-2 py-1 rounded-lg border-[1.5px] border-border text-xs ${colors.bg} ${colors.text} hover:brightness-110 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary`}
                            >
                              {item.name}
                            </button>
                          );
                        })
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </GlassCard>
        ) : (
          /* 유형별 보기 (기존) */
          <GlassCard className="p-4 md:p-6">
            {/* 카테고리별 섹션 */}
            {(['길신', '중성', '흉신'] as const).map(type => {
              const items = grouped[type];
              if (items.length === 0) return null;

              const colors = typeColors[type];

              return (
                <div key={type} className="mb-6 last:mb-0">
                  {/* 섹션 헤더 */}
                  <div className="flex items-center gap-2 mb-3">
                    <Icon name={colors.icon} size={18} className={colors.text} />
                    <span className={`font-medium ${colors.text}`}>{type}</span>
                    <span className="text-xs text-muted-foreground">({items.length})</span>
                  </div>

                  {/* 신살 목록 */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {items.map((item, idx) => (
                      <motion.button
                        key={`${item.name}-${item.position}-${idx}`}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => handleShenshaClick(item.name)}
                        className={`btn-block block-press p-4 rounded-xl ${colors.bg} border-[1.5px] border-border
                          text-left shadow-block-sm transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <span className="text-lg font-bold text-foreground">
                              {item.name}
                            </span>
                            {item.hanja && (
                              <span className="ml-2 text-sm text-muted-foreground">
                                {item.hanja}
                              </span>
                            )}
                          </div>
                          <span className={`text-xs px-2 py-1 rounded-lg ${colors.bg} ${colors.text}`}>
                            {positionNames[item.position] || item.position}
                          </span>
                        </div>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {item.description}
                        </p>
                        <div className="mt-2 text-xs text-primary flex items-center gap-1">
                          <span>자세히 보기</span>
                          <Icon name="solar:arrow-right-linear" size={12} />
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>
              );
            })}
          </GlassCard>
        )}
      </motion.div>

      {/* 상세 정보 모달 */}
      <GlossaryModal
        entry={selectedEntry}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </>
  );
}

export default ShenshaDetailCard;
