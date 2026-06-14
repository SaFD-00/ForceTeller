'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useSajuStore } from '@/stores/sajuStore';
import { Button, Icon, GlassCard } from '@/components/ui';
import {
  PillarTable,
  InteractionsTabs,
  ShenshaDetailCard,
  ElementDistribution,
  PentagonChart,
  YongshinCard,
  StrengthDistributionChart,
  FortuneCycleSlider,
  YearlyFortune,
  LuckyGuideCard,
} from '@/components/result';
import { ChatContainer } from '@/components/chat';
import type { Element, HiddenStemDisplay, ShenshaDisplay } from '@/types/saju';

// 지장간 배열을 문자열로 변환
function formatHiddenStems(hiddenStems?: HiddenStemDisplay[]): string {
  if (!hiddenStems || hiddenStems.length === 0) return '-';
  return hiddenStems.map((hs) => hs.korean).join(' ');
}

// 해당 위치의 신살을 찾아 반환 (첫 번째 것만)
function getShensha(shensha: ShenshaDisplay[] | undefined, position: string): string {
  if (!shensha) return '-';
  const found = shensha.filter((s) => s.position === position || s.position === `${position}주`);
  if (found.length === 0) return '-';
  return found[0]?.name || '-';
}

// 지장간의 본기로부터 십성 반환
function getBranchTenGod(hiddenStems?: HiddenStemDisplay[]): string {
  if (!hiddenStems || hiddenStems.length === 0) return '-';
  // 마지막 항목이 본기
  const mainQi = hiddenStems[hiddenStems.length - 1];
  return mainQi.ten_god || '-';
}

// 십성 계산 함수 (대운용)
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

// 천간 한글명 → 인덱스 매핑 (12운성 계산용)
const STEM_INDEX_MAP: Record<string, number> = {
  '갑': 0, '을': 1, '병': 2, '정': 3, '무': 4,
  '기': 5, '경': 6, '신': 7, '임': 8, '계': 9,
};

// 지지 한글명 → 인덱스 매핑
const BRANCH_INDEX_MAP: Record<string, number> = {
  '자': 0, '축': 1, '인': 2, '묘': 3, '진': 4, '사': 5,
  '오': 6, '미': 7, '신': 8, '유': 9, '술': 10, '해': 11,
};

// 지지의 본기 천간 인덱스 (지장간 본기)
const BRANCH_MAIN_STEM: Record<number, number> = {
  0: 9, 1: 5, 2: 0, 3: 1, 4: 4, 5: 2,
  6: 3, 7: 5, 8: 6, 9: 7, 10: 4, 11: 8,
};

// 천간 데이터 (오행 정보 포함)
const STEMS: Array<{ korean: string; element: Element }> = [
  { korean: '갑', element: '목' },
  { korean: '을', element: '목' },
  { korean: '병', element: '화' },
  { korean: '정', element: '화' },
  { korean: '무', element: '토' },
  { korean: '기', element: '토' },
  { korean: '경', element: '금' },
  { korean: '신', element: '금' },
  { korean: '임', element: '수' },
  { korean: '계', element: '수' },
];

// 12운성 순서
const TWELVE_PHASES = ['장생', '목욕', '관대', '건록', '제왕', '쇠', '병', '사', '묘', '절', '태', '양'];

// 천간별 장생 위치 (지지 인덱스)
const CHANGSHENG_POSITIONS: Record<number, number> = {
  0: 11, 1: 6, 2: 2, 3: 9, 4: 2, 5: 9, 6: 5, 7: 0, 8: 8, 9: 3,
};

function getDayStemIndex(koreanStem: string): number | undefined {
  return STEM_INDEX_MAP[koreanStem];
}

// 지지 십성 계산 (본기 기준)
function calculateBranchTenGod(dayMasterElement: Element, branchKorean: string): string {
  const branchIndex = BRANCH_INDEX_MAP[branchKorean];
  if (branchIndex === undefined) return '-';
  const mainStemIndex = BRANCH_MAIN_STEM[branchIndex];
  const mainStemElement = STEMS[mainStemIndex].element;
  return calculateTenGod(dayMasterElement, mainStemElement);
}

// 12운성 계산
function calculateTwelvePhase(dayStemIndex: number, branchKorean: string): string {
  const branchIndex = BRANCH_INDEX_MAP[branchKorean];
  if (branchIndex === undefined) return '-';

  const isYang = dayStemIndex % 2 === 0;
  const changshengBranch = CHANGSHENG_POSITIONS[dayStemIndex];
  const distance = isYang
    ? (branchIndex - changshengBranch + 12) % 12
    : (changshengBranch - branchIndex + 12) % 12;

  return TWELVE_PHASES[distance];
}

export default function ResultPage() {
  const router = useRouter();
  const { result, error, isLoading, clearResult } = useSajuStore();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(true);

  useEffect(() => {
    const checkDesktop = () => {
      const isDesktop = window.innerWidth >= 1024;
      setIsMobile(!isDesktop);
      if (isDesktop) {
        setIsChatOpen(true);
      }
    };

    checkDesktop();
    window.addEventListener('resize', checkDesktop);
    return () => window.removeEventListener('resize', checkDesktop);
  }, []);

  useEffect(() => {
    if (!result && !isLoading) {
      router.push('/');
    }
  }, [result, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Icon
            name="solar:refresh-bold"
            size={48}
            className="text-primary animate-spin mx-auto mb-4"
          />
          <p className="text-muted-foreground">사주를 분석하고 있습니다...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <GlassCard className="max-w-md p-8 text-center">
          <Icon
            name="solar:danger-triangle-bold"
            size={48}
            className="text-red-400 mx-auto mb-4"
          />
          <h2 className="text-xl font-bold text-foreground mb-2">오류가 발생했습니다</h2>
          <p className="text-muted-foreground mb-6">{error}</p>
          <Button onClick={() => router.push('/')}>
            <Icon name="solar:home-2-bold" size={20} className="mr-2" />
            홈으로 돌아가기
          </Button>
        </GlassCard>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  // Calculate current age
  const birthYear = new Date(result.birth_info.birth_date).getFullYear();
  const currentAge = new Date().getFullYear() - birthYear;

  // Transform data for PillarTable
  const pillarTableData = {
    year: {
      heavenly_stem: {
        hanja: result.four_pillars.year.heavenly_stem.hanja,
        korean: result.four_pillars.year.heavenly_stem.korean,
        element: result.four_pillars.year.heavenly_stem.element,
        polarity: '양' as const,
      },
      earthly_branch: {
        hanja: result.four_pillars.year.earthly_branch.hanja,
        korean: result.four_pillars.year.earthly_branch.korean,
        element: result.four_pillars.year.earthly_branch.element,
        polarity: '양' as const,
      },
      ten_god: result.four_pillars.year.ten_god,
      branch_ten_god: getBranchTenGod(result.four_pillars.year.earthly_branch.hidden_stems),
      hidden_stems: formatHiddenStems(result.four_pillars.year.earthly_branch.hidden_stems),
      twelve_phase: result.four_pillars.year.twelve_phase || '-',
      twelve_shensha: getShensha(result.shensha, 'year'),
    },
    month: {
      heavenly_stem: {
        hanja: result.four_pillars.month.heavenly_stem.hanja,
        korean: result.four_pillars.month.heavenly_stem.korean,
        element: result.four_pillars.month.heavenly_stem.element,
        polarity: '양' as const,
      },
      earthly_branch: {
        hanja: result.four_pillars.month.earthly_branch.hanja,
        korean: result.four_pillars.month.earthly_branch.korean,
        element: result.four_pillars.month.earthly_branch.element,
        polarity: '양' as const,
      },
      ten_god: result.four_pillars.month.ten_god,
      branch_ten_god: getBranchTenGod(result.four_pillars.month.earthly_branch.hidden_stems),
      hidden_stems: formatHiddenStems(result.four_pillars.month.earthly_branch.hidden_stems),
      twelve_phase: result.four_pillars.month.twelve_phase || '-',
      twelve_shensha: getShensha(result.shensha, 'month'),
    },
    day: {
      heavenly_stem: {
        hanja: result.four_pillars.day.heavenly_stem.hanja,
        korean: result.four_pillars.day.heavenly_stem.korean,
        element: result.four_pillars.day.heavenly_stem.element,
        polarity: '양' as const,
      },
      earthly_branch: {
        hanja: result.four_pillars.day.earthly_branch.hanja,
        korean: result.four_pillars.day.earthly_branch.korean,
        element: result.four_pillars.day.earthly_branch.element,
        polarity: '양' as const,
      },
      ten_god: '비견',
      branch_ten_god: getBranchTenGod(result.four_pillars.day.earthly_branch.hidden_stems),
      hidden_stems: formatHiddenStems(result.four_pillars.day.earthly_branch.hidden_stems),
      twelve_phase: result.four_pillars.day.twelve_phase || '-',
      twelve_shensha: getShensha(result.shensha, 'day'),
    },
    hour: {
      heavenly_stem: {
        hanja: result.four_pillars.hour.heavenly_stem.hanja,
        korean: result.four_pillars.hour.heavenly_stem.korean,
        element: result.four_pillars.hour.heavenly_stem.element,
        polarity: '양' as const,
      },
      earthly_branch: {
        hanja: result.four_pillars.hour.earthly_branch.hanja,
        korean: result.four_pillars.hour.earthly_branch.korean,
        element: result.four_pillars.hour.earthly_branch.element,
        polarity: '양' as const,
      },
      ten_god: result.four_pillars.hour.ten_god,
      branch_ten_god: getBranchTenGod(result.four_pillars.hour.earthly_branch.hidden_stems),
      hidden_stems: formatHiddenStems(result.four_pillars.hour.earthly_branch.hidden_stems),
      twelve_phase: result.four_pillars.hour.twelve_phase || '-',
      twelve_shensha: getShensha(result.shensha, 'hour'),
    },
  };

  // Transform distribution data
  const elementDistribution: Record<Element, number> = {
    '목': result.five_elements.distribution?.['목'] || 0,
    '화': result.five_elements.distribution?.['화'] || 0,
    '토': result.five_elements.distribution?.['토'] || 0,
    '금': result.five_elements.distribution?.['금'] || 0,
    '수': result.five_elements.distribution?.['수'] || 0,
  };

  const tenGodsDistribution = result.ten_gods?.counts || {};

  // Day master element
  const dayMaster = result.four_pillars.day.heavenly_stem.element;

  // Day stem index for 12운성 calculation
  const dayStemIndex = getDayStemIndex(result.four_pillars.day.heavenly_stem.korean);

  // Transform fortune cycles for slider
  const fortuneItems = result.fortune_cycles?.map((cycle) => ({
    age: cycle.start_age,
    ten_god: calculateTenGod(dayMaster, cycle.heavenly_stem.element),
    heavenly_stem: cycle.heavenly_stem,
    earthly_branch: cycle.earthly_branch,
    branch_ten_god: calculateBranchTenGod(dayMaster, cycle.earthly_branch.korean),
    twelve_phase: dayStemIndex !== undefined
      ? calculateTwelvePhase(dayStemIndex, cycle.earthly_branch.korean)
      : '-',
    is_current: currentAge >= cycle.start_age && currentAge < (cycle.start_age + 10),
  })) || [];

  // Strength info
  const strengthScore = result.strength?.score || 50;
  const isStrong = result.strength?.is_strong ?? true;
  const strengthType = result.strength?.type || (isStrong ? '신강' : '신약');

  return (
    <main className="min-h-screen bg-gradient-to-b from-white to-background">
      <div className="flex">
        {/* Left: Results Section */}
        <div
          className={`transition-all duration-300 ${
            isChatOpen ? 'w-full lg:w-3/4' : 'w-full'
          }`}
        >
          <div className="py-8 px-4 lg:py-12 lg:px-8 max-w-5xl mx-auto">
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center mb-8 lg:mb-12"
            >
              <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground mb-2">
                {result.birth_info.name}
              </h1>
              {/* 일주 정보 */}
              {result.birth_info.day_ganji_korean && (
                <p className="text-lg md:text-xl text-primary font-medium mb-2">
                  {result.birth_info.day_ganji_korean}
                  {result.birth_info.day_metaphor && ` (${result.birth_info.day_metaphor})`}
                </p>
              )}
              {/* 양력 */}
              <p className="text-muted-foreground text-sm md:text-base mb-1">
                양 {result.birth_info.birth_date}
                {result.birth_info.birth_time && ` ${result.birth_info.birth_time}`}
                {' '}{result.birth_info.city} {result.birth_info.gender === 'male' ? '남자' : '여자'}
              </p>
              {/* 음력 */}
              {result.birth_info.lunar_year && (
                <p className="text-muted-foreground text-sm md:text-base mb-1">
                  음{result.birth_info.is_leap_month ? '(윤달)' : '(평달)'}{' '}
                  {result.birth_info.lunar_year}/{String(result.birth_info.lunar_month).padStart(2, '0')}/{String(result.birth_info.lunar_day).padStart(2, '0')}
                  {result.birth_info.birth_time && ` ${result.birth_info.birth_time}`}
                </p>
              )}
              {/* 시간 보정 */}
              {result.adjusted_time && (
                <p className="text-gray-400 text-xs md:text-sm">
                  지역시: 양 {result.adjusted_time.true_solar_time.split(' ')[0]} {result.adjusted_time.true_solar_time.split(' ')[1]?.slice(0, 5)}
                  {' '}(보정: 지역 {result.adjusted_time.longitude_correction_minutes > 0 ? '+' : ''}{Math.round(result.adjusted_time.longitude_correction_minutes)}분)
                </p>
              )}
            </motion.div>

            {/* 사주 테이블 (Posteller 스타일) */}
            <PillarTable pillars={pillarTableData} />

            {/* 천간 지지 작용 */}
            <InteractionsTabs interactions={result.interactions ?? {}} />

            {/* 신살 카드 */}
            <ShenshaDetailCard
              shensha={result.shensha || []}
              pillars={{
                year: {
                  heavenly_stem: pillarTableData.year.heavenly_stem,
                  earthly_branch: pillarTableData.year.earthly_branch,
                  ten_god: pillarTableData.year.ten_god,
                  branch_ten_god: pillarTableData.year.branch_ten_god,
                },
                month: {
                  heavenly_stem: pillarTableData.month.heavenly_stem,
                  earthly_branch: pillarTableData.month.earthly_branch,
                  ten_god: pillarTableData.month.ten_god,
                  branch_ten_god: pillarTableData.month.branch_ten_god,
                },
                day: {
                  heavenly_stem: pillarTableData.day.heavenly_stem,
                  earthly_branch: pillarTableData.day.earthly_branch,
                  ten_god: pillarTableData.day.ten_god,
                  branch_ten_god: pillarTableData.day.branch_ten_god,
                },
                hour: {
                  heavenly_stem: pillarTableData.hour.heavenly_stem,
                  earthly_branch: pillarTableData.hour.earthly_branch,
                  ten_god: pillarTableData.hour.ten_god,
                  branch_ten_god: pillarTableData.hour.branch_ten_god,
                },
              }}
            />

            {/* 오행/십성 분포 */}
            <ElementDistribution
              distribution={elementDistribution}
              tenGods={tenGodsDistribution}
              dominant={result.five_elements.dominant}
            />

            {/* 오행 오각형 도표 */}
            <PentagonChart
              dayMaster={dayMaster}
              distribution={elementDistribution}
              dayStemKorean={result.four_pillars.day.heavenly_stem.korean}
            />

            {/* 용신 */}
            {result.five_elements.yongshin && (
              <YongshinCard
                type="억부용신"
                element={result.five_elements.yongshin}
              />
            )}

            {/* 용신 개운법 (색/방위/직업/생활) */}
            {result.yongsin_recommendations && (
              <LuckyGuideCard
                recommendations={result.yongsin_recommendations}
                comparison={result.yongsin_comparison}
              />
            )}

            {/* 신강/신약 지수 */}
            <StrengthDistributionChart
              name={result.birth_info.name}
              score={strengthScore}
              strengthType={strengthType}
              percentile={10.5}
            />

            {/* 대운 슬라이더 */}
            {fortuneItems.length > 0 && (
              <FortuneCycleSlider
                title="대운수"
                subtitle="좌우로 슬라이드 해보세요."
                items={fortuneItems}
                startAge={fortuneItems[0]?.age}
                dayMasterElement={dayMaster}
                dayStemIndex={dayStemIndex}
                showAge
              />
            )}

            {/* 세운 (연도별 운세) */}
            {result.sewun && result.sewun.length > 0 && (
              <YearlyFortune sewun={result.sewun} />
            )}

            {/* Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center mt-8 lg:mt-12"
            >
              <Button
                className="w-full sm:w-auto lg:hidden"
                onClick={() => setIsChatOpen(!isChatOpen)}
              >
                <Icon name="solar:chat-round-dots-bold" size={20} className="mr-2" />
                {isChatOpen ? 'AI 상담 닫기' : 'AI 상담 열기'}
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  clearResult();
                  router.push('/');
                }}
                className="w-full sm:w-auto"
              >
                <Icon name="solar:refresh-bold" size={20} className="mr-2" />
                다시 분석하기
              </Button>
            </motion.div>
          </div>
        </div>

        {/* Right: Chat Panel (Desktop) */}
        <div
          className={`hidden lg:block transition-all duration-300 ${
            isChatOpen ? 'w-1/4' : 'w-0'
          }`}
        >
          <div className="sticky top-0 h-screen p-4">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
                  <Icon name="solar:chat-round-dots-bold" size={24} className="text-primary" />
                  AI 상담
                </h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsChatOpen(false)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <Icon name="solar:close-circle-bold" size={20} />
                </Button>
              </div>
              <div className="flex-1 min-h-0">
                <ChatContainer />
              </div>
            </div>
          </div>
        </div>

        {/* Chat Toggle Button (Desktop - when closed) */}
        {!isChatOpen && (
          <div className="hidden lg:block fixed right-4 top-1/2 -translate-y-1/2 z-50">
            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsChatOpen(true)}
              className="bg-primary hover:bg-primary/90 text-white p-4 rounded-l-xl shadow-card-hover flex items-center gap-2"
            >
              <Icon name="solar:chat-round-dots-bold" size={24} />
              <span className="font-medium">AI 상담</span>
            </motion.button>
          </div>
        )}
      </div>

      {/* Mobile: Full-screen Chat Overlay */}
      <AnimatePresence>
        {isChatOpen && isMobile && (
          <motion.div
            initial={{ opacity: 0, y: '100%' }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed inset-0 z-50 bg-background"
          >
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between p-4 border-b border-border">
                <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
                  <Icon name="solar:chat-round-dots-bold" size={24} className="text-primary" />
                  AI 상담
                </h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsChatOpen(false)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <Icon name="solar:close-circle-bold" size={24} />
                </Button>
              </div>
              <div className="flex-1 min-h-0">
                <ChatContainer />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
