import { describe, it, expect } from 'vitest';
import { STEMS, BRANCHES, TEN_GOD_GROUP } from './ganji';
import type { Element } from '@/types/saju';

const ELEMENTS: Element[] = ['목', '화', '토', '금', '수'];

describe('STEMS (천간)', () => {
  it('정확히 10개다', () => {
    expect(STEMS).toHaveLength(10);
  });

  it('모든 항목이 한글·한자·유효 오행을 갖는다', () => {
    for (const s of STEMS) {
      expect(s.korean).toMatch(/^[가-힣]$/); // 한글 1자
      expect(s.hanja).toMatch(/^[一-鿿]$/); // 한자 1자
      expect(ELEMENTS).toContain(s.element);
    }
  });

  it('한글·한자가 서로 중복되지 않는다', () => {
    expect(new Set(STEMS.map((s) => s.korean)).size).toBe(10);
    expect(new Set(STEMS.map((s) => s.hanja)).size).toBe(10);
  });

  it('앵커 값이 표준 간지표와 일치한다', () => {
    expect(STEMS[0]).toEqual({ korean: '갑', hanja: '甲', element: '목' });
    expect(STEMS[9]).toEqual({ korean: '계', hanja: '癸', element: '수' });
  });

  it('오행 분포가 천간 규칙(각 오행 2개)을 따른다', () => {
    const counts = STEMS.reduce<Record<string, number>>((acc, s) => {
      acc[s.element] = (acc[s.element] || 0) + 1;
      return acc;
    }, {});
    expect(counts).toEqual({ 목: 2, 화: 2, 토: 2, 금: 2, 수: 2 });
  });
});

describe('BRANCHES (지지)', () => {
  it('정확히 12개다', () => {
    expect(BRANCHES).toHaveLength(12);
  });

  it('모든 항목이 한글·한자·유효 오행을 갖는다', () => {
    for (const b of BRANCHES) {
      expect(b.korean).toMatch(/^[가-힣]$/);
      expect(b.hanja).toMatch(/^[一-鿿]$/);
      expect(ELEMENTS).toContain(b.element);
    }
  });

  it('한글·한자가 서로 중복되지 않는다', () => {
    expect(new Set(BRANCHES.map((b) => b.korean)).size).toBe(12);
    expect(new Set(BRANCHES.map((b) => b.hanja)).size).toBe(12);
  });

  it('앵커 값이 표준 간지표와 일치한다', () => {
    expect(BRANCHES[0]).toEqual({ korean: '자', hanja: '子', element: '수' });
    expect(BRANCHES[11]).toEqual({ korean: '해', hanja: '亥', element: '수' });
  });
});

describe('TEN_GOD_GROUP (십성 세부명 → 그룹)', () => {
  const EXPECTED: Record<string, string> = {
    비견: '비겁',
    겁재: '비겁',
    식신: '식상',
    상관: '식상',
    편재: '재성',
    정재: '재성',
    편관: '관성',
    정관: '관성',
    편인: '인성',
    정인: '인성',
  };

  it('세부명 10개를 전수 매핑한다', () => {
    expect(Object.keys(TEN_GOD_GROUP)).toHaveLength(10);
    expect(TEN_GOD_GROUP).toEqual(EXPECTED);
  });

  it('그룹은 정확히 5개이며 각 그룹에 2개씩 속한다', () => {
    const groups = Object.values(TEN_GOD_GROUP);
    const uniq = Array.from(new Set(groups));
    expect(uniq.slice().sort()).toEqual(['관성', '비겁', '식상', '인성', '재성']);
    for (const g of uniq) {
      expect(groups.filter((x) => x === g)).toHaveLength(2);
    }
  });
});
