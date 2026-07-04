'use client';

import { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import { BRANCHES } from '@/lib/ganji';
import type { Element, CurrentFortune, CurrentFortuneEntry, FortuneRanges } from '@/types/saju';

interface FortuneCycleItem {
  age?: number;
  year?: number;
  month?: number;
  day?: number;
  ten_god: string;
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
  branch_ten_god?: string;
  twelve_phase?: string;
  is_current?: boolean;
  comment?: string;
}

interface FortuneCycleSliderProps {
  title: string;
  subtitle?: string;
  items: FortuneCycleItem[]; // 대운 (백엔드 fortune_cycles 유래)
  startAge?: number;
  direction?: '순행' | '역행';
  showAge?: boolean;
  // 연/월/일운 — 백엔드 단일 진실 공급원. 없으면(구 localStorage) 해당 섹션 숨김
  fortuneRanges?: FortuneRanges;
  currentFortune?: CurrentFortune;
}

// 십성별 운세 코멘트 (세부 십성 10개)
const TEN_GOD_COMMENTS: Record<string, string> = {
  '비견': '독립심과 추진력이 강해지는 시기입니다. 동료와 협력하세요.',
  '겁재': '경쟁과 도전의 시기입니다. 승부사 기질을 발휘하세요.',
  '식신': '안정적인 생활력이 좋아집니다. 꾸준함이 복을 부릅니다.',
  '상관': '창의력과 표현력이 빛나는 시기입니다. 재능을 펼치세요.',
  '편재': '새로운 재물 기회가 찾아옵니다. 투자와 사업에 유리합니다.',
  '정재': '성실한 노력이 결실을 맺습니다. 저축과 안정에 집중하세요.',
  '편관': '책임과 압박이 따르지만 성장의 기회입니다.',
  '정관': '사회적 인정과 승진의 기회가 있습니다. 명예를 얻습니다.',
  '편인': '직관력과 응용력이 좋아집니다. 전문성을 키우세요.',
  '정인': '학습과 귀인의 도움이 있습니다. 배움에 집중하세요.',
};

// 12운성별 운세 코멘트 (전통적 의미 기반)
const PHASE_COMMENTS: Record<string, string> = {
  '태': '새로운 계획이 잉태되는 시기입니다. 구상과 준비에 집중하세요.',
  '양': '내면의 힘을 기르며 도약을 준비하는 시기입니다.',
  '장생': '새로운 시작과 희망이 가득한 시기입니다. 호기심을 따라가세요.',
  '목욕': '변화와 성장통을 겪는 시기입니다. 자기 정체성을 다듬어가세요.',
  '관대': '당당하게 도전하고 경쟁할 수 있는 시기입니다.',
  '건록': '노력의 결실을 맺고 자립하는 시기입니다.',
  '제왕': '에너지가 절정에 달하는 시기입니다. 리더십을 발휘하세요.',
  '쇠': '원숙한 지혜로 한 발 물러서서 관망하는 시기입니다.',
  '병': '마음을 정돈하고 심신의 안정을 취하는 시기입니다.',
  '사': '욕심을 내려놓고 마음을 비우는 시기입니다.',
  '묘': '실속을 챙기며 내실을 다지는 시기입니다.',
  '절': '끝이 곧 새로운 시작입니다. 전환점을 맞이하세요.',
};

// 운세 코멘트 생성 (12운성 우선) — 표시 텍스트 조회일 뿐 계산이 아니다
function generateFortuneComment(tenGod: string, twelvePhase: string): string {
  const phaseComment = PHASE_COMMENTS[twelvePhase] || '';
  const tenGodComment = TEN_GOD_COMMENTS[tenGod] || '';
  return phaseComment || tenGodComment || '';
}

// 백엔드 운세 Entry → 슬라이더 표시 아이템으로 변환 (간지·십성 계산 없음)
function entryToItem(entry: CurrentFortuneEntry, isCurrent: boolean): FortuneCycleItem {
  // 지지 오행은 인덱스 → 정적 속성 조회 (계산 아님)
  const branchElement = BRANCHES[entry.branch_index]?.element ?? entry.element;

  // date "YYYY-MM-DD" 라벨에서 월/일 파생
  let month = entry.calendar_month;
  let day: number | undefined;
  let year = entry.year;
  if (entry.date) {
    const [y, m, d] = entry.date.split('-').map(Number);
    year = year ?? y;
    month = month ?? m;
    day = d;
  }

  return {
    year,
    month,
    day,
    ten_god: entry.ten_god || '-',
    heavenly_stem: {
      korean: entry.stem,
      hanja: entry.stem_hanja,
      element: entry.element,
    },
    earthly_branch: {
      korean: entry.branch,
      hanja: entry.branch_hanja,
      element: branchElement,
    },
    branch_ten_god: entry.branch_ten_god || '-',
    twelve_phase: entry.twelve_phase || '-',
    is_current: isCurrent,
    comment: generateFortuneComment(entry.ten_god, entry.twelve_phase),
  };
}

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

// 개별 섹션 컴포넌트
interface FortuneSectionProps {
  title: string;
  subtitle?: string;
  items: FortuneCycleItem[];
  showAge?: boolean;
  showYear?: boolean;
  showMonth?: boolean;
  showDay?: boolean;
  onTitleClick?: () => void;
  comment?: string;
}

function FortuneSection({
  title,
  subtitle,
  items,
  showAge,
  showYear,
  showMonth,
  showDay,
  onTitleClick,
  comment,
}: FortuneSectionProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollLeft = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: -200, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: 200, behavior: 'smooth' });
    }
  };

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <button
          onClick={onTitleClick}
          className="text-lg font-bold text-foreground underline decoration-white/30 hover:decoration-primary transition-colors"
        >
          {title}
        </button>
        {subtitle && <span className="text-muted-foreground text-sm">{subtitle}</span>}
      </div>

      {comment && (
        <p className="text-muted-foreground text-sm mb-3 bg-muted rounded-lg px-3 py-2">
          💫 {comment}
        </p>
      )}

      <GlassCard className="p-3 md:p-4">
        <div className="relative">
          <button
            onClick={scrollLeft}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-primary/80 hover:bg-primary p-1.5 rounded-full text-primary-foreground transition-colors hidden md:block"
          >
            <Icon name="solar:alt-arrow-left-bold" size={16} />
          </button>

          <button
            onClick={scrollRight}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-primary/80 hover:bg-primary p-1.5 rounded-full text-primary-foreground transition-colors hidden md:block"
          >
            <Icon name="solar:alt-arrow-right-bold" size={16} />
          </button>

          <div
            ref={scrollRef}
            className="flex gap-2 overflow-x-auto scrollbar-hide pb-2 pt-1 px-0 md:px-6"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {items.map((item, index) => (
              <div
                key={index}
                className={`flex-shrink-0 w-16 text-center ${
                  item.is_current ? 'ring-2 ring-primary rounded-lg' : ''
                }`}
              >
                {/* 나이/연도/월/일 */}
                <div className="text-foreground font-bold text-sm mb-0.5">
                  {showAge && item.age !== undefined && item.age}
                  {showYear && item.year !== undefined && item.year}
                  {showMonth && item.month !== undefined && `${item.month}월`}
                  {showDay && item.day !== undefined && `${item.month}/${item.day}`}
                </div>

                {/* 천간 십성 */}
                <div className="text-muted-foreground text-xs mb-0.5">
                  {item.ten_god}
                </div>

                {/* 천간 */}
                <div
                  className={`${ELEMENT_BG[item.heavenly_stem.element]} rounded-md p-1.5 mb-0.5`}
                >
                  <span className="text-base font-bold text-foreground">
                    {item.heavenly_stem.korean}
                  </span>
                  <span className="text-xs text-muted-foreground ml-0.5">
                    {item.heavenly_stem.hanja}
                  </span>
                </div>

                {/* 지지 */}
                <div
                  className={`${ELEMENT_BG_LIGHT[item.earthly_branch.element]} rounded-md p-1.5`}
                >
                  <span className="text-base font-bold text-foreground">
                    {item.earthly_branch.korean}
                  </span>
                  <span className="text-xs text-muted-foreground ml-0.5">
                    {item.earthly_branch.hanja}
                  </span>
                </div>

                {/* 지지 십성 */}
                {item.branch_ten_god && item.branch_ten_god !== '-' && (
                  <div className="text-muted-foreground text-xs mt-0.5">
                    {item.branch_ten_god}
                  </div>
                )}

                {/* 12운성 */}
                {item.twelve_phase && item.twelve_phase !== '-' && (
                  <div className="text-muted-foreground text-xs">
                    {item.twelve_phase}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </GlassCard>
    </div>
  );
}

export function FortuneCycleSlider({
  title,
  items,
  startAge,
  direction,
  fortuneRanges,
  currentFortune,
}: FortuneCycleSliderProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // 현재 판정·라벨은 모두 백엔드 current_fortune에서 파생 (프론트에서 new Date() 재계산 없음)
  const currentYear = currentFortune?.yearly.year;
  const currentCalendarMonth = currentFortune?.daily.date
    ? Number(currentFortune.daily.date.slice(5, 7))
    : undefined;

  // 연운 (현재±5년): year 정확일치로 현재 판정
  const yearlyFortunes = (fortuneRanges?.yearly ?? []).map((entry) =>
    entryToItem(entry, currentYear !== undefined && entry.year === currentYear)
  );

  // 월운 (12개월): calendar_month(달력월) 일치로 현재 판정 — 항상 정확히 1개
  const monthlyFortunes = (fortuneRanges?.monthly ?? []).map((entry) =>
    entryToItem(
      entry,
      currentCalendarMonth !== undefined && entry.calendar_month === currentCalendarMonth
    )
  );

  // 일운 (현재±7일): date 정확일치로 현재 판정
  const dailyFortunes = (fortuneRanges?.daily ?? []).map((entry) =>
    entryToItem(entry, entry.date === currentFortune?.daily.date)
  );

  const hasRanges =
    yearlyFortunes.length > 0 || monthlyFortunes.length > 0 || dailyFortunes.length > 0;

  const handleTitleClick = (term: string) => {
    const entry = getGlossaryEntry(term);
    if (entry) {
      setSelectedEntry(entry);
      setIsModalOpen(true);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEntry(null);
  };

  // 현재 운세 코멘트 가져오기
  const currentYearFortune = yearlyFortunes.find((f) => f.is_current);
  const currentMonthFortune = monthlyFortunes.find((f) => f.is_current);
  const currentDailyFortune = dailyFortunes.find((f) => f.is_current);
  const currentDaewun = items.find((f) => f.is_current);
  const daewunComment = currentDaewun
    ? generateFortuneComment(currentDaewun.ten_god, currentDaewun.twelve_phase ?? '')
    : undefined;

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mb-8"
      >
        <div className="flex items-center gap-2 mb-4">
          <Icon name="solar:calendar-bold" size={24} className="text-primary" />
          <h2 className="text-xl font-bold text-foreground">운세 흐름</h2>
        </div>

        {/* 대운 섹션 */}
        <FortuneSection
          title={`${title}${startAge !== undefined ? `: ${startAge}` : ''}${direction ? ` (${direction})` : ''}`}
          items={items}
          showAge
          onTitleClick={() => handleTitleClick('대운')}
          comment={daewunComment}
        />

        {hasRanges ? (
          <>
            {/* 연운 섹션 */}
            {yearlyFortunes.length > 0 && (
              <FortuneSection
                title="연운"
                subtitle={currentYear !== undefined ? `${currentYear}년 기준` : undefined}
                items={yearlyFortunes}
                showYear
                onTitleClick={() => handleTitleClick('연운')}
                comment={currentYearFortune?.comment}
              />
            )}

            {/* 월운 섹션 */}
            {monthlyFortunes.length > 0 && (
              <FortuneSection
                title="월운"
                subtitle={currentYear !== undefined ? `${currentYear}년` : undefined}
                items={monthlyFortunes}
                showMonth
                onTitleClick={() => handleTitleClick('월운')}
                comment={currentMonthFortune?.comment}
              />
            )}

            {/* 일운 섹션 */}
            {dailyFortunes.length > 0 && (
              <FortuneSection
                title="일운"
                subtitle={currentCalendarMonth !== undefined ? `${currentCalendarMonth}월` : undefined}
                items={dailyFortunes}
                showDay
                onTitleClick={() => handleTitleClick('일운')}
                comment={currentDailyFortune?.comment}
              />
            )}
          </>
        ) : (
          <p className="text-muted-foreground text-sm bg-muted rounded-lg px-3 py-2">
            연·월·일운 정보는 사주를 다시 분석하면 표시됩니다.
          </p>
        )}
      </motion.div>

      <GlossaryModal
        entry={selectedEntry}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </>
  );
}

export default FortuneCycleSlider;
