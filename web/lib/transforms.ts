import type {
  SajuResult,
  SajuResultDisplay,
  FourPillarsDisplay,
  PillarDisplay,
  FiveElementsDisplay,
  TenGodsDisplay,
  StrengthDisplay,
  FortuneCycleDisplay,
  Element,
  PillarData,
  FortuneCycle,
  HiddenStemDisplay,
  ShenshaDisplay,
} from '@/types/saju';

/**
 * 백엔드 Pillar 데이터를 프론트엔드 Display 타입으로 변환
 */
function transformPillar(pillar: PillarData | null): PillarDisplay {
  if (!pillar) {
    return {
      heavenly_stem: { hanja: '-', korean: '-', element: '토' as Element },
      earthly_branch: { hanja: '-', korean: '-', element: '토' as Element },
      ten_god: null,
      twelve_phase: null,
    };
  }

  // 지장간 변환
  const hiddenStems: HiddenStemDisplay[] = pillar.branch.hidden_stems?.map((hs) => ({
    korean: hs.korean,
    chinese: hs.chinese,
    element: hs.element,
    type: hs.type,
    ratio: hs.ratio,
    ten_god: (hs as { ten_god?: string }).ten_god,
  })) || [];

  return {
    heavenly_stem: {
      hanja: pillar.stem.chinese,
      korean: pillar.stem.korean,
      element: pillar.stem.element,
    },
    earthly_branch: {
      hanja: pillar.branch.chinese,
      korean: pillar.branch.korean,
      element: pillar.branch.element,
      hidden_stems: hiddenStems,
    },
    ten_god: pillar.ten_god,
    twelve_phase: pillar.twelve_phase,
  };
}

/**
 * 대운 데이터를 프론트엔드 Display 타입으로 변환
 */
function transformFortuneCycle(cycle: FortuneCycle): FortuneCycleDisplay {
  // 천간/지지 인덱스로부터 한글/한자 매핑
  const stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'];
  const stemsHanja = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  const branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'];
  const branchesHanja = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

  const stemElements: Element[] = ['목', '목', '화', '화', '토', '토', '금', '금', '수', '수'];
  const branchElements: Element[] = ['수', '토', '목', '목', '토', '화', '화', '토', '금', '금', '토', '수'];

  return {
    start_age: cycle.start_age,
    heavenly_stem: {
      hanja: stemsHanja[cycle.stem_index] || cycle.ganji_chinese[0],
      korean: stems[cycle.stem_index] || cycle.ganji_korean[0],
      element: stemElements[cycle.stem_index] || '토',
    },
    earthly_branch: {
      hanja: branchesHanja[cycle.branch_index] || cycle.ganji_chinese[1],
      korean: branches[cycle.branch_index] || cycle.ganji_korean[1],
      element: branchElements[cycle.branch_index] || '토',
    },
  };
}

/**
 * 백엔드 SajuResult를 프론트엔드 SajuResultDisplay로 변환
 */
export function transformSajuResult(result: SajuResult): SajuResultDisplay {
  const {
    input,
    pillars,
    analysis,
    fortune_cycles,
    adjusted_time,
    interactions,
    sewun,
    yongsin_comparison,
    yongsin_recommendations,
  } = result;

  // Four Pillars 변환
  const fourPillars: FourPillarsDisplay = {
    year: transformPillar(pillars.year),
    month: transformPillar(pillars.month),
    day: transformPillar(pillars.day),
    hour: transformPillar(pillars.hour),
  };

  // Five Elements 변환
  const fiveElements: FiveElementsDisplay = {
    distribution: {
      '목': analysis.five_elements.wood,
      '화': analysis.five_elements.fire,
      '토': analysis.five_elements.earth,
      '금': analysis.five_elements.metal,
      '수': analysis.five_elements.water,
    },
    dominant: (analysis.five_elements.dominant[0] as Element) || null,
    lacking: (analysis.five_elements.lacking[0] as Element) || null,
    yongshin: analysis.useful_god?.primary || null,
    gishin: analysis.useful_god?.avoid || null,
  };

  // Ten Gods 변환
  const tenGods: TenGodsDisplay = {
    counts: {
      '비견': analysis.ten_gods_dist.비견,
      '겁재': analysis.ten_gods_dist.겁재,
      '식신': analysis.ten_gods_dist.식신,
      '상관': analysis.ten_gods_dist.상관,
      '편재': analysis.ten_gods_dist.편재,
      '정재': analysis.ten_gods_dist.정재,
      '편관': analysis.ten_gods_dist.편관,
      '정관': analysis.ten_gods_dist.정관,
      '편인': analysis.ten_gods_dist.편인,
      '정인': analysis.ten_gods_dist.정인,
    },
    primary: Object.entries(analysis.ten_gods_dist).reduce(
      (max, [god, count]) =>
        count > (analysis.ten_gods_dist[max as keyof typeof analysis.ten_gods_dist] || 0)
          ? god
          : max,
      '비견'
    ),
  };

  // Strength 변환
  const strength: StrengthDisplay = {
    score: analysis.strength.score,
    is_strong: analysis.strength.level === '신강',
    type: analysis.strength.level,
    description: analysis.strength.analysis,
  };

  // Fortune Cycles 변환
  const fortuneCycles = fortune_cycles?.cycles.map(transformFortuneCycle) || [];

  // Shensha 변환
  const shensha: ShenshaDisplay[] = analysis.shensha?.map((s) => ({
    name: s.name,
    type: s.type as '길신' | '흉신' | '중성',
    position: s.position,
    description: s.description,
  })) || [];

  return {
    birth_info: {
      name: input.name,
      birth_date: input.birth_date,
      birth_time: input.birth_time || undefined,
      city: input.city,
      gender: input.gender,
      // 음력 정보
      lunar_year: input.lunar_year,
      lunar_month: input.lunar_month,
      lunar_day: input.lunar_day,
      is_leap_month: input.is_leap_month,
      // 일주 정보
      day_ganji_korean: input.day_ganji_korean,
      day_ganji_chinese: input.day_ganji_chinese,
      day_metaphor: input.day_metaphor,
      day_animal: input.day_animal,
    },
    four_pillars: fourPillars,
    five_elements: fiveElements,
    ten_gods: tenGods,
    strength: strength,
    fortune_cycles: fortuneCycles,
    shensha: shensha,
    adjusted_time: adjusted_time,
    interactions: interactions,
    sewun: sewun,
    yongsin_comparison: yongsin_comparison,
    yongsin_recommendations: yongsin_recommendations,
  };
}
