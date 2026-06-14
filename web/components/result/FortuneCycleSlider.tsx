'use client';

import { useRef, useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import type { Element } from '@/types/saju';

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
  items: FortuneCycleItem[];
  startAge?: number;
  direction?: '순행' | '역행';
  showAge?: boolean;
  showYear?: boolean;
  showMonth?: boolean;
  birthYear?: number;
  dayMasterElement?: Element;
  dayStemIndex?: number;
}

// 천간 데이터
const STEMS = [
  { korean: '갑', hanja: '甲', element: '목' as Element },
  { korean: '을', hanja: '乙', element: '목' as Element },
  { korean: '병', hanja: '丙', element: '화' as Element },
  { korean: '정', hanja: '丁', element: '화' as Element },
  { korean: '무', hanja: '戊', element: '토' as Element },
  { korean: '기', hanja: '己', element: '토' as Element },
  { korean: '경', hanja: '庚', element: '금' as Element },
  { korean: '신', hanja: '辛', element: '금' as Element },
  { korean: '임', hanja: '壬', element: '수' as Element },
  { korean: '계', hanja: '癸', element: '수' as Element },
];

// 지지 데이터
const BRANCHES = [
  { korean: '자', hanja: '子', element: '수' as Element },
  { korean: '축', hanja: '丑', element: '토' as Element },
  { korean: '인', hanja: '寅', element: '목' as Element },
  { korean: '묘', hanja: '卯', element: '목' as Element },
  { korean: '진', hanja: '辰', element: '토' as Element },
  { korean: '사', hanja: '巳', element: '화' as Element },
  { korean: '오', hanja: '午', element: '화' as Element },
  { korean: '미', hanja: '未', element: '토' as Element },
  { korean: '신', hanja: '申', element: '금' as Element },
  { korean: '유', hanja: '酉', element: '금' as Element },
  { korean: '술', hanja: '戌', element: '토' as Element },
  { korean: '해', hanja: '亥', element: '수' as Element },
];

// 월로부터 간지 계산 (년간 기준)
function getMonthGanji(year: number, month: number) {
  const yearStemIndex = (year - 4) % 10;
  const monthStemBase = (yearStemIndex % 5) * 2;
  const monthStemIndex = (monthStemBase + month - 1) % 10;
  const monthBranchIndex = (month + 1) % 12;

  return {
    stem: STEMS[monthStemIndex],
    branch: BRANCHES[monthBranchIndex],
    stemIndex: monthStemIndex,
    branchIndex: monthBranchIndex,
  };
}

// 일주 간지 계산 (날짜 기준)
function getDayGanji(date: Date) {
  const baseDate = new Date(1900, 0, 31);
  const diffTime = date.getTime() - baseDate.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  const stemIndex = ((diffDays % 10) + 10) % 10;
  const branchIndex = ((diffDays % 12) + 12) % 12;

  return {
    stem: STEMS[stemIndex],
    branch: BRANCHES[branchIndex],
    stemIndex,
    branchIndex,
  };
}

// 지지의 본기 천간 인덱스 (지장간 본기)
const BRANCH_MAIN_STEM: Record<number, number> = {
  0: 9,   // 자(子) → 계(癸)
  1: 5,   // 축(丑) → 기(己)
  2: 0,   // 인(寅) → 갑(甲)
  3: 1,   // 묘(卯) → 을(乙)
  4: 4,   // 진(辰) → 무(戊)
  5: 2,   // 사(巳) → 병(丙)
  6: 3,   // 오(午) → 정(丁)
  7: 5,   // 미(未) → 기(己)
  8: 6,   // 신(申) → 경(庚)
  9: 7,   // 유(酉) → 신(辛)
  10: 4,  // 술(戌) → 무(戊)
  11: 8,  // 해(亥) → 임(壬)
};

// 지지 십성 계산 (본기 기준)
function calculateBranchTenGod(dayMasterElement: Element, branchIndex: number): string {
  const mainStemIndex = BRANCH_MAIN_STEM[branchIndex];
  const mainStemElement = STEMS[mainStemIndex].element;
  return calculateTenGod(dayMasterElement, mainStemElement);
}

// 12운성 순서
const TWELVE_PHASES = ['장생', '목욕', '관대', '건록', '제왕', '쇠', '병', '사', '묘', '절', '태', '양'];

// 천간별 장생 위치 (지지 인덱스)
const CHANGSHENG_POSITIONS: Record<number, number> = {
  0: 11, // 갑 → 해
  1: 6,  // 을 → 오
  2: 2,  // 병 → 인
  3: 9,  // 정 → 유
  4: 2,  // 무 → 인
  5: 9,  // 기 → 유
  6: 5,  // 경 → 사
  7: 0,  // 신 → 자
  8: 8,  // 임 → 신
  9: 3,  // 계 → 묘
};

// 12운성 계산
function calculateTwelvePhase(dayStemIndex: number, branchIndex: number): string {
  const isYang = dayStemIndex % 2 === 0;
  const changshengBranch = CHANGSHENG_POSITIONS[dayStemIndex];

  const distance = isYang
    ? (branchIndex - changshengBranch + 12) % 12
    : (changshengBranch - branchIndex + 12) % 12;

  return TWELVE_PHASES[distance];
}

// 십성별 운세 코멘트 (10개 세분화)
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

// 운세 코멘트 생성 (12운성 우선)
function generateFortuneComment(tenGod: string, twelvePhase: string): string {
  const phaseComment = PHASE_COMMENTS[twelvePhase] || '';
  const tenGodComment = TEN_GOD_COMMENTS[tenGod] || '';

  // 12운성 코멘트 우선 표시
  return phaseComment || tenGodComment || '';
}

// 오행별 배경색
const ELEMENT_BG: Record<Element, string> = {
  '목': 'bg-green-600/80',
  '화': 'bg-red-500/80',
  '토': 'bg-yellow-600/80',
  '금': 'bg-gray-400/80',
  '수': 'bg-blue-500/80',
};

const ELEMENT_BG_LIGHT: Record<Element, string> = {
  '목': 'bg-green-200/60',
  '화': 'bg-red-200/60',
  '토': 'bg-yellow-200/60',
  '금': 'bg-gray-200/60',
  '수': 'bg-blue-200/60',
};

// 오행 상생상극 관계
const GENERATING: Record<Element, Element> = { '목': '화', '화': '토', '토': '금', '금': '수', '수': '목' };
const CONTROLLING: Record<Element, Element> = { '목': '토', '토': '수', '수': '화', '화': '금', '금': '목' };

// 십성 계산 함수 (개별 십성 반환, 음양 구분)
function calculateTenGodDetailed(
  dayMasterElement: Element,
  dayStemIndex: number,
  targetStemIndex: number
): string {
  const targetElement = STEMS[targetStemIndex].element;
  const isSamePolarity = (dayStemIndex % 2) === (targetStemIndex % 2);

  if (dayMasterElement === targetElement) {
    return isSamePolarity ? '비견' : '겁재';
  } else if (GENERATING[dayMasterElement] === targetElement) {
    return isSamePolarity ? '식신' : '상관';
  } else if (CONTROLLING[dayMasterElement] === targetElement) {
    return isSamePolarity ? '편재' : '정재';
  } else if (CONTROLLING[targetElement] === dayMasterElement) {
    return isSamePolarity ? '편관' : '정관';
  } else {
    return isSamePolarity ? '편인' : '정인';
  }
}

// 십성 계산 함수 (그룹명 반환, 하위호환)
function calculateTenGod(dayMasterElement: Element, stemElement: Element): string {
  const relations: Record<Element, Record<Element, string>> = {
    '목': { '목': '비겁', '화': '식상', '토': '재성', '금': '관성', '수': '인성' },
    '화': { '목': '인성', '화': '비겁', '토': '식상', '금': '재성', '수': '관성' },
    '토': { '목': '관성', '화': '인성', '토': '비겁', '금': '식상', '수': '재성' },
    '금': { '목': '재성', '화': '관성', '토': '인성', '금': '비겁', '수': '식상' },
    '수': { '목': '식상', '화': '재성', '토': '관성', '금': '인성', '수': '비겁' },
  };
  return relations[dayMasterElement]?.[stemElement] || '-';
}

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
        <p className="text-gray-600 text-sm mb-3 bg-muted rounded-lg px-3 py-2">
          💫 {comment}
        </p>
      )}

      <GlassCard className="p-3 md:p-4">
        <div className="relative">
          <button
            onClick={scrollLeft}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 p-1.5 rounded-full text-gray-600 hover:text-foreground transition-colors hidden md:block"
          >
            <Icon name="solar:alt-arrow-left-bold" size={16} />
          </button>

          <button
            onClick={scrollRight}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 p-1.5 rounded-full text-gray-600 hover:text-foreground transition-colors hidden md:block"
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
                  <span className="text-xs text-gray-600 ml-0.5">
                    {item.heavenly_stem.hanja}
                  </span>
                </div>

                {/* 지지 */}
                <div
                  className={`${ELEMENT_BG_LIGHT[item.earthly_branch.element]} rounded-md p-1.5`}
                >
                  <span className="text-base font-bold text-gray-800">
                    {item.earthly_branch.korean}
                  </span>
                  <span className="text-xs text-gray-600 ml-0.5">
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
                  <div className="text-gray-400 text-xs">
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
  dayMasterElement,
  dayStemIndex,
}: FortuneCycleSliderProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const currentYear = new Date().getFullYear();
  const currentMonth = new Date().getMonth() + 1;

  // 연운 데이터 생성 (±5년)
  const yearlyFortunes = useMemo(() => {
    const fortunes: FortuneCycleItem[] = [];
    for (let year = currentYear - 5; year <= currentYear + 5; year++) {
      const stemIndex = (year - 4) % 10;
      const branchIndex = (year - 4) % 12;
      const stem = STEMS[stemIndex >= 0 ? stemIndex : stemIndex + 10];
      const branch = BRANCHES[branchIndex >= 0 ? branchIndex : branchIndex + 12];
      const actualBranchIndex = branchIndex >= 0 ? branchIndex : branchIndex + 12;

      const actualStemIndex = stemIndex >= 0 ? stemIndex : stemIndex + 10;
      const tenGod = (dayMasterElement && dayStemIndex !== undefined)
        ? calculateTenGodDetailed(dayMasterElement, dayStemIndex, actualStemIndex)
        : '-';
      const branchTenGod = dayMasterElement ? calculateBranchTenGod(dayMasterElement, actualBranchIndex) : '-';
      const twelvePhase = dayStemIndex !== undefined ? calculateTwelvePhase(dayStemIndex, actualBranchIndex) : '-';

      fortunes.push({
        year,
        ten_god: tenGod,
        branch_ten_god: branchTenGod,
        twelve_phase: twelvePhase,
        heavenly_stem: {
          korean: stem.korean,
          hanja: stem.hanja,
          element: stem.element,
        },
        earthly_branch: {
          korean: branch.korean,
          hanja: branch.hanja,
          element: branch.element,
        },
        is_current: year === currentYear,
        comment: generateFortuneComment(tenGod, twelvePhase),
      });
    }
    return fortunes;
  }, [currentYear, dayMasterElement, dayStemIndex]);

  // 월운 데이터 생성 (12개월)
  const monthlyFortunes = useMemo(() => {
    const fortunes: FortuneCycleItem[] = [];
    for (let month = 1; month <= 12; month++) {
      const { stem, branch, stemIndex, branchIndex } = getMonthGanji(currentYear, month);

      const tenGod = (dayMasterElement && dayStemIndex !== undefined)
        ? calculateTenGodDetailed(dayMasterElement, dayStemIndex, stemIndex)
        : '-';
      const branchTenGod = dayMasterElement ? calculateBranchTenGod(dayMasterElement, branchIndex) : '-';
      const twelvePhase = dayStemIndex !== undefined ? calculateTwelvePhase(dayStemIndex, branchIndex) : '-';

      fortunes.push({
        month,
        year: currentYear,
        ten_god: tenGod,
        branch_ten_god: branchTenGod,
        twelve_phase: twelvePhase,
        heavenly_stem: {
          korean: stem.korean,
          hanja: stem.hanja,
          element: stem.element,
        },
        earthly_branch: {
          korean: branch.korean,
          hanja: branch.hanja,
          element: branch.element,
        },
        is_current: month === currentMonth,
        comment: generateFortuneComment(tenGod, twelvePhase),
      });
    }
    return fortunes;
  }, [currentYear, currentMonth, dayMasterElement, dayStemIndex]);

  // 일운 데이터 생성 (오늘 기준 ±7일)
  const dailyFortunes = useMemo(() => {
    const fortunes: FortuneCycleItem[] = [];
    const today = new Date();

    for (let i = -7; i <= 7; i++) {
      const targetDate = new Date(today);
      targetDate.setDate(today.getDate() + i);

      const { stem, branch, stemIndex, branchIndex } = getDayGanji(targetDate);

      const tenGod = (dayMasterElement && dayStemIndex !== undefined)
        ? calculateTenGodDetailed(dayMasterElement, dayStemIndex, stemIndex)
        : '-';
      const branchTenGod = dayMasterElement ? calculateBranchTenGod(dayMasterElement, branchIndex) : '-';
      const twelvePhase = dayStemIndex !== undefined ? calculateTwelvePhase(dayStemIndex, branchIndex) : '-';

      fortunes.push({
        day: targetDate.getDate(),
        month: targetDate.getMonth() + 1,
        year: targetDate.getFullYear(),
        ten_god: tenGod,
        branch_ten_god: branchTenGod,
        twelve_phase: twelvePhase,
        heavenly_stem: {
          korean: stem.korean,
          hanja: stem.hanja,
          element: stem.element,
        },
        earthly_branch: {
          korean: branch.korean,
          hanja: branch.hanja,
          element: branch.element,
        },
        is_current: i === 0,
        comment: generateFortuneComment(tenGod, twelvePhase),
      });
    }
    return fortunes;
  }, [dayMasterElement, dayStemIndex]);

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
  const currentYearFortune = yearlyFortunes.find(f => f.is_current);
  const currentMonthFortune = monthlyFortunes.find(f => f.is_current);
  const currentDailyFortune = dailyFortunes.find(f => f.is_current);
  const currentDaewun = items.find(f => f.is_current);

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
          comment={currentDaewun?.comment}
        />

        {/* 연운 섹션 */}
        <FortuneSection
          title="연운"
          subtitle={`${currentYear}년 기준`}
          items={yearlyFortunes}
          showYear
          onTitleClick={() => handleTitleClick('연운')}
          comment={currentYearFortune?.comment}
        />

        {/* 월운 섹션 */}
        <FortuneSection
          title="월운"
          subtitle={`${currentYear}년`}
          items={monthlyFortunes}
          showMonth
          onTitleClick={() => handleTitleClick('월운')}
          comment={currentMonthFortune?.comment}
        />

        {/* 일운 섹션 */}
        <FortuneSection
          title="일운"
          subtitle={`${currentMonth}월`}
          items={dailyFortunes}
          showDay
          onTitleClick={() => handleTitleClick('일운')}
          comment={currentDailyFortune?.comment}
        />
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
