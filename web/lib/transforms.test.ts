import { describe, it, expect } from 'vitest';
import { transformSajuResult } from './transforms';
import type {
  SajuResult,
  PillarData,
  CurrentFortuneEntry,
} from '@/types/saju';

// 백엔드 응답(SajuResult) 형태의 fixture. 전체 타입을 명시해 orphan 타입 제거 이후에도
// 계약이 어긋나면 tsc가 잡도록 한다. transformFortuneCycle은 module-private이므로
// public API인 transformSajuResult(...).fortune_cycles 경유로 index→표시 조회를 검증한다.

function makeStem(index: number, korean: string, chinese: string) {
  return { index, korean, chinese, element: '목' as const, polarity: '양' as const };
}

function makeBranch(index: number, korean: string, chinese: string) {
  return {
    index,
    korean,
    chinese,
    element: '목' as const,
    polarity: '양' as const,
    animal: '호랑이',
    hidden_stems: [
      { stem_index: 0, korean: '갑', chinese: '甲', element: '목' as const, type: '정기', ratio: 1 },
    ],
  };
}

function makePillar(): PillarData {
  return {
    stem: makeStem(0, '갑', '甲'),
    branch: makeBranch(2, '인', '寅'),
    ganji_korean: '갑인',
    ganji_chinese: '甲寅',
    ten_god: '비견',
    twelve_phase: '건록',
  };
}

function makeEntry(over: Partial<CurrentFortuneEntry> = {}): CurrentFortuneEntry {
  return {
    stem: '병',
    branch: '오',
    stem_hanja: '丙',
    branch_hanja: '午',
    stem_index: 2,
    branch_index: 6,
    element: '화',
    ganji_korean: '병오',
    ganji_chinese: '丙午',
    ten_god: '식신',
    branch_ten_god: '상관',
    twelve_phase: '제왕',
    ...over,
  };
}

function baseResult(): SajuResult {
  return {
    meta: { version: '1.0', generated_at: '2026-01-01T00:00:00Z', engine: 'manseol' },
    input: {
      name: '홍길동',
      birth_date: '1990-05-15',
      birth_time: '10:30',
      calendar: 'solar',
      city: 'Seoul',
      gender: 'male',
      jajasi: false,
    },
    adjusted_time: null,
    pillars: {
      year: makePillar(),
      month: makePillar(),
      day: makePillar(),
      hour: makePillar(),
    },
    analysis: {
      day_master: {
        element: '목',
        polarity: '양',
        korean: '갑',
        chinese: '甲',
        metaphor: '큰 나무',
        characteristics: ['강직함'],
      },
      five_elements: {
        wood: 3,
        fire: 1,
        earth: 2,
        metal: 1,
        water: 1,
        dominant: ['목'],
        lacking: ['금'],
        distribution: { 목: 3, 화: 1, 토: 2, 금: 1, 수: 1 },
      },
      ten_gods_dist: {
        비견: 1,
        겁재: 0,
        식신: 2,
        상관: 0,
        편재: 1,
        정재: 0,
        편관: 0,
        정관: 5,
        편인: 0,
        정인: 1,
      },
      strength: {
        level: '신강',
        score: 72,
        supporting_count: 4,
        weakening_count: 2,
        analysis: '일간이 강하다',
      },
      useful_god: {
        type: '억부',
        primary: '금',
        secondary: '수',
        avoid: '목',
        reasoning: '신강하므로 억제',
      },
      shensha: [
        { name: '천을귀인', type: '길신', position: '일지', description: '귀인의 도움' },
      ],
    },
    fortune_cycles: {
      start_age: 3,
      direction: '순행',
      current_cycle_index: 0,
      cycles: [
        {
          start_age: 3,
          end_age: 12,
          stem_index: 0, // 갑/甲/목
          branch_index: 2, // 인/寅/목
          ganji_korean: '갑인',
          ganji_chinese: '甲寅',
          ten_god: '비견',
          branch_ten_god: '편재',
          twelve_phase: '건록',
        },
      ],
    },
    current_fortune: {
      reference_datetime: '2026-07-05T00:00:00Z',
      yearly: makeEntry({ year: 2026 }),
      monthly: makeEntry({ year: 2026, month: 6 }),
      daily: makeEntry({ date: '2026-07-05' }),
    },
    fortune_ranges: {
      yearly: [makeEntry({ year: 2025 }), makeEntry({ year: 2026 })],
      monthly: [makeEntry({ month: 6, calendar_month: 7 })],
      daily: [makeEntry({ date: '2026-07-05' })],
    },
  };
}

describe('transformSajuResult - 사주팔자', () => {
  it('사주(pillars)의 ten_god/twelve_phase를 그대로 통과시킨다', () => {
    const out = transformSajuResult(baseResult());
    expect(out.four_pillars.year.ten_god).toBe('비견');
    expect(out.four_pillars.year.twelve_phase).toBe('건록');
  });

  it('지장간(hidden_stems)을 ten_god 포함해 변환한다', () => {
    const out = transformSajuResult(baseResult());
    const hidden = out.four_pillars.day.earthly_branch.hidden_stems;
    expect(hidden).toHaveLength(1);
    expect(hidden?.[0]).toMatchObject({ korean: '갑', chinese: '甲', element: '목', type: '정기' });
  });

  it('birth_info·오행분포·십성 primary·신강 여부를 매핑한다', () => {
    const out = transformSajuResult(baseResult());
    expect(out.birth_info.name).toBe('홍길동');
    expect(out.five_elements.distribution).toEqual({ 목: 3, 화: 1, 토: 2, 금: 1, 수: 1 });
    expect(out.five_elements.dominant).toBe('목');
    expect(out.five_elements.lacking).toBe('금');
    expect(out.five_elements.yongshin).toBe('금');
    expect(out.five_elements.gishin).toBe('목');
    expect(out.ten_gods.primary).toBe('정관'); // count 5로 최대
    expect(out.strength.is_strong).toBe(true);
  });
});

describe('transformSajuResult - 대운(fortune cycles)', () => {
  it('stem_index/branch_index를 ganji 사전으로 표시 변환한다', () => {
    const out = transformSajuResult(baseResult());
    const cycle = out.fortune_cycles?.[0];
    expect(cycle?.heavenly_stem).toMatchObject({ hanja: '甲', korean: '갑', element: '목' });
    expect(cycle?.earthly_branch).toMatchObject({ hanja: '寅', korean: '인', element: '목' });
  });

  it('ten_god/branch_ten_god/twelve_phase를 백엔드 값 그대로 통과시킨다', () => {
    const out = transformSajuResult(baseResult());
    const cycle = out.fortune_cycles?.[0];
    expect(cycle?.ten_god).toBe('비견');
    expect(cycle?.branch_ten_god).toBe('편재');
    expect(cycle?.twelve_phase).toBe('건록');
  });

  it('인덱스가 범위를 벗어나면 ganji 문자열로 폴백한다', () => {
    const data = baseResult();
    data.fortune_cycles!.cycles[0].stem_index = 99;
    data.fortune_cycles!.cycles[0].branch_index = 99;
    const out = transformSajuResult(data);
    const cycle = out.fortune_cycles?.[0];
    expect(cycle?.heavenly_stem.hanja).toBe('甲'); // ganji_chinese[0]
    expect(cycle?.earthly_branch.korean).toBe('인'); // ganji_korean[1]
  });
});

describe('transformSajuResult - current_fortune / fortune_ranges 통과', () => {
  it('current_fortune를 그대로 전달한다', () => {
    const data = baseResult();
    const out = transformSajuResult(data);
    expect(out.current_fortune).toEqual(data.current_fortune);
    expect(out.current_fortune?.yearly.ten_god).toBe('식신');
  });

  it('fortune_ranges를 그대로 전달한다', () => {
    const data = baseResult();
    const out = transformSajuResult(data);
    expect(out.fortune_ranges).toEqual(data.fortune_ranges);
    expect(out.fortune_ranges?.yearly).toHaveLength(2);
  });
});

describe('transformSajuResult - 구 데이터(필드 누락) 안전 동작', () => {
  it('fortune_cycles=null이면 빈 배열, current_fortune/fortune_ranges 없으면 undefined', () => {
    const data = baseResult();
    data.fortune_cycles = null;
    delete data.current_fortune;
    delete data.fortune_ranges;
    const out = transformSajuResult(data);
    expect(out.fortune_cycles).toEqual([]);
    expect(out.current_fortune).toBeUndefined();
    expect(out.fortune_ranges).toBeUndefined();
  });

  it('시주(hour pillar)가 null이면 placeholder로 안전 변환한다', () => {
    const data = baseResult();
    data.pillars.hour = null;
    const out = transformSajuResult(data);
    expect(out.four_pillars.hour.heavenly_stem.hanja).toBe('-');
    expect(out.four_pillars.hour.ten_god).toBeNull();
  });
});
