'use client';

import { useState } from 'react';
import { Icon } from '@iconify/react';
import type { AnalysisType, YongSinMethodType, SchoolCodeType } from '@/types/saju';

interface AnalysisButtonsProps {
  onAnalysisClick: (
    type: AnalysisType,
    options?: { yongsinMethod?: YongSinMethodType; schools?: SchoolCodeType[] }
  ) => void;
  disabled?: boolean;
}

// 운세 분석 버튼 설정
const FORTUNE_BUTTONS = [
  { type: 'fortune_general' as const, label: '종합운', icon: 'mdi:star' },
  { type: 'fortune_career' as const, label: '직업운', icon: 'mdi:briefcase' },
  { type: 'fortune_wealth' as const, label: '재물운', icon: 'mdi:cash' },
  { type: 'fortune_health' as const, label: '건강운', icon: 'mdi:heart-pulse' },
  { type: 'fortune_love' as const, label: '애정운', icon: 'mdi:heart' },
];

// 용신 방법론 버튼 설정
const YONGSIN_METHODS = [
  { code: 'strength' as const, label: '강약', icon: 'mdi:scale-balance', description: '일간 강약 기준' },
  { code: 'seasonal' as const, label: '조후', icon: 'mdi:thermometer', description: '계절 기준' },
  { code: 'mediation' as const, label: '통관', icon: 'mdi:link-variant', description: '오행 충돌 중재' },
  { code: 'disease' as const, label: '병약', icon: 'mdi:pill', description: '병 치료 관점' },
];

export function AnalysisButtons({ onAnalysisClick, disabled = false }: AnalysisButtonsProps) {
  const [showYongsinMethods, setShowYongsinMethods] = useState(false);

  const handleFortuneClick = (type: AnalysisType) => {
    if (disabled) return;
    onAnalysisClick(type);
  };

  const handleYongsinMethodClick = (method: YongSinMethodType) => {
    if (disabled) return;
    onAnalysisClick('yongsin_method', { yongsinMethod: method });
    setShowYongsinMethods(false);
  };

  const handleSchoolCompareClick = () => {
    if (disabled) return;
    onAnalysisClick('school_compare');
  };

  const toggleYongsinMethods = () => {
    if (disabled) return;
    setShowYongsinMethods(!showYongsinMethods);
  };

  return (
    <div className="px-4 py-2 border-t-[1.5px] border-border">
      {/* 용신 방법론 선택 패널 (확장시 표시) */}
      {showYongsinMethods && (
        <div className="mb-2 p-2 rounded-xl bg-surface border-[1.5px] border-border shadow-card">
          <div className="text-xs text-muted-foreground mb-2">용신 분석 방법론 선택</div>
          <div className="grid grid-cols-4 gap-2">
            {YONGSIN_METHODS.map(({ code, label, icon, description }) => (
              <button
                key={code}
                onClick={() => handleYongsinMethodClick(code)}
                disabled={disabled}
                className={`
                  flex flex-col items-center gap-1 p-2 rounded-lg border-[1.5px] border-border
                  text-xs transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
                  ${disabled
                    ? 'bg-muted text-muted-foreground cursor-not-allowed'
                    : 'bg-surface text-foreground hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover block-press'
                  }
                `}
                title={description}
              >
                <Icon icon={icon} className="w-4 h-4" />
                <span>{label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 메인 버튼 그리드 */}
      <div className="flex flex-wrap gap-2">
        {/* 운세 분석 버튼들 */}
        {FORTUNE_BUTTONS.map(({ type, label, icon }) => (
          <button
            key={type}
            onClick={() => handleFortuneClick(type)}
            disabled={disabled}
            className={`
              inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border-[1.5px] border-border
              text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
              ${disabled
                ? 'bg-muted text-muted-foreground cursor-not-allowed'
                : 'bg-surface text-foreground hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover block-press'
              }
            `}
          >
            <Icon icon={icon} className="w-4 h-4" />
            {label}
          </button>
        ))}

        {/* 구분선 */}
        <div className="w-px h-6 bg-border self-center mx-1" />

        {/* 용신 분석 버튼 (드롭다운 토글) */}
        <div className="relative">
          <button
            onClick={toggleYongsinMethods}
            disabled={disabled}
            className={`
              inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border-[1.5px] border-border
              text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
              ${showYongsinMethods
                ? 'bg-primary/15 text-primary shadow-block-sm'
                : disabled
                  ? 'bg-muted text-muted-foreground cursor-not-allowed'
                  : 'bg-surface text-foreground hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover block-press'
              }
            `}
          >
            <Icon icon="mdi:sparkles" className="w-4 h-4" />
            용신분석
            <Icon
              icon={showYongsinMethods ? 'mdi:chevron-up' : 'mdi:chevron-down'}
              className="w-3 h-3"
            />
          </button>
        </div>

        {/* 유파 비교 버튼 */}
        <button
          onClick={handleSchoolCompareClick}
          disabled={disabled}
          className={`
            inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border-[1.5px] border-border
            text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
            ${disabled
              ? 'bg-muted text-muted-foreground cursor-not-allowed'
              : 'bg-surface text-foreground hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover block-press'
            }
          `}
        >
          <Icon icon="mdi:book-open-variant" className="w-4 h-4" />
          유파비교
        </button>
      </div>

      {/* 안내 텍스트 */}
      <div className="mt-2 text-xs text-muted-foreground text-center">
        버튼을 클릭하여 원하는 분석을 시작하세요
      </div>
    </div>
  );
}
