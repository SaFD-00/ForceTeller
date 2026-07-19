'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { useSajuStore } from '@/stores/sajuStore';
import { Button, Icon, GlassCard, Disclaimer } from '@/components/ui';
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
  SchoolComparison,
  FortuneScoreDashboard,
  LifetimeReport,
} from '@/components/result';
import { ChatContainer } from '@/components/chat';
import { TEN_GOD_GROUP } from '@/lib/ganji';
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

export default function ResultPage() {
  const router = useRouter();
  const { result, error, isLoading, hasHydrated, clearResult } = useSajuStore();
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

  // 저장된 결과 복원 전에는 판단을 보류한다 (자동 리다이렉트 없음 — 사용자가 직접 선택한다).
  if (!hasHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Icon
          name="solar:refresh-bold"
          size={32}
          className="text-muted-foreground animate-spin"
          aria-label="불러오는 중"
        />
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Icon
            name="solar:refresh-bold"
            size={48}
            className="text-accent animate-spin mx-auto mb-4"
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
            className="text-danger mx-auto mb-4"
          />
          <h2 className="text-xl font-bold text-foreground mb-2">오류가 발생했습니다</h2>
          <p className="text-muted-foreground mb-6">{error}</p>
          <Button onClick={() => router.push('/')}>
            <Icon name="solar:home-2-linear" size={20} className="mr-2" />
            홈으로 돌아가기
          </Button>
        </GlassCard>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <GlassCard className="max-w-md p-8 text-center">
          <Icon
            name="solar:chart-2-bold"
            size={48}
            className="text-muted-foreground mx-auto mb-4"
          />
          <h2 className="text-xl font-bold text-foreground mb-2">
            사주 분석 결과가 없습니다
          </h2>
          <p className="text-muted-foreground mb-6">
            생년월일시를 입력하면 사주 분석 결과를 확인할 수 있습니다.
          </p>
          <Link href="/">
            <Button>
              <Icon name="solar:home-2-linear" size={20} className="mr-2" />
              홈으로 가기
            </Button>
          </Link>
        </GlassCard>
      </div>
    );
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

  // Transform fortune cycles for slider (십성·12운성은 백엔드 값을 그대로 사용)
  const fortuneItems = result.fortune_cycles?.map((cycle) => ({
    age: cycle.start_age,
    ten_god: cycle.ten_god ?? '-',
    heavenly_stem: cycle.heavenly_stem,
    earthly_branch: cycle.earthly_branch,
    branch_ten_god: cycle.branch_ten_god || '-',
    twelve_phase: cycle.twelve_phase ?? '-',
    is_current: currentAge >= cycle.start_age && currentAge < (cycle.start_age + 10),
  })) || [];

  // Strength info
  const strengthScore = result.strength?.score || 50;
  const isStrong = result.strength?.is_strong ?? true;
  const strengthType = result.strength?.type || (isStrong ? '신강' : '신약');

  // 평생운 리포트용 대운 단계 (fortuneItems 재사용)
  // 백엔드 ten_god은 세부명(비견…)이므로 그룹명(비겁…)으로 축약해 테마에 매핑
  const lifeStages = fortuneItems.map((item) => ({
    age: item.age,
    ganji: `${item.heavenly_stem.korean}${item.earthly_branch.korean}`,
    tenGodGroup: TEN_GOD_GROUP[item.ten_god] ?? item.ten_god,
    isCurrent: item.is_current,
  }));

  return (
    <main className="min-h-screen bg-background">
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
                <p className="text-lg md:text-xl text-accent font-medium mb-2">
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
                <p className="text-muted-foreground text-xs md:text-sm">
                  지역시: 양 {result.adjusted_time.true_solar_time.split(' ')[0]} {result.adjusted_time.true_solar_time.split(' ')[1]?.slice(0, 5)}
                  {' '}(보정: 지역 {result.adjusted_time.longitude_correction_minutes > 0 ? '+' : ''}{Math.round(result.adjusted_time.longitude_correction_minutes)}분)
                </p>
              )}
            </motion.div>

            {/* 운세 유형별 점수 — 요약을 먼저 보여주고 근거(원국)로 내려간다 */}
            {result.fortune_scores && (
              <FortuneScoreDashboard scores={result.fortune_scores} />
            )}

            {/* 사주 테이블 (Posteller 스타일) */}
            <PillarTable pillars={pillarTableData} />

            {/* 천간 지지 작용 */}
            <InteractionsTabs interactions={result.interactions ?? {}} />

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

            {/* 신강/신약 지수 */}
            <StrengthDistributionChart
              name={result.birth_info.name}
              score={strengthScore}
              strengthType={strengthType}
              percentile={10.5}
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

            {/* 5학파 비교 해석 */}
            {result.school_comparison && (
              <SchoolComparison comparison={result.school_comparison} />
            )}

            {/* 대운 슬라이더 */}
            {fortuneItems.length > 0 && (
              <FortuneCycleSlider
                title="대운수"
                subtitle="좌우로 슬라이드 해보세요."
                items={fortuneItems}
                startAge={fortuneItems[0]?.age}
                fortuneRanges={result.fortune_ranges}
                currentFortune={result.current_fortune}
                showAge
              />
            )}

            {/* 세운 (연도별 운세) */}
            {result.sewun && result.sewun.length > 0 && (
              <YearlyFortune sewun={result.sewun} />
            )}

            {/* 평생운 흐름 (10년 대운 내러티브) */}
            {lifeStages.length > 0 && (
              <LifetimeReport
                stages={lifeStages}
                overallSummary={result.fortune_scores?.general?.summary}
              />
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
                <Icon name="solar:chat-round-dots-linear" size={20} className="mr-2" />
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
                <Icon name="solar:refresh-linear" size={20} className="mr-2" />
                다시 분석하기
              </Button>
            </motion.div>

            {/* 면책 고지 */}
            <Disclaimer className="mt-8" />
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
                  <Icon name="solar:chat-round-dots-bold" size={24} className="text-accent" />
                  AI 상담
                </h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsChatOpen(false)}
                  className="text-muted-foreground hover:text-foreground"
                  aria-label="AI 상담 닫기"
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
              className="bg-primary hover:bg-primary/90 text-primary-foreground p-4 rounded-l-xl border-[1.5px] border-border shadow-card-hover flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
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
              <div className="flex items-center justify-between p-4 border-b-[1.5px] border-border">
                <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
                  <Icon name="solar:chat-round-dots-bold" size={24} className="text-accent" />
                  AI 상담
                </h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsChatOpen(false)}
                  className="text-muted-foreground hover:text-foreground"
                  aria-label="AI 상담 닫기"
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
