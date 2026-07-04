// 간지(干支) 표시 전용 사전 — 단일 진실 공급원
//
// 간지·십성·12운성의 "계산"은 전적으로 백엔드(manseol) 소관이다. 이 파일에는
// 인덱스 → 한글/한자/오행 같은 정적 표시 속성 조회 사전만 둔다.
// 절기를 무시한 근사로 간지를 재유도하던 프론트 계산 코드를 대체한다.

import type { Element } from '@/types/saju';

// 천간(天干) — 인덱스 0~9
export const STEMS: Array<{ korean: string; hanja: string; element: Element }> = [
  { korean: '갑', hanja: '甲', element: '목' },
  { korean: '을', hanja: '乙', element: '목' },
  { korean: '병', hanja: '丙', element: '화' },
  { korean: '정', hanja: '丁', element: '화' },
  { korean: '무', hanja: '戊', element: '토' },
  { korean: '기', hanja: '己', element: '토' },
  { korean: '경', hanja: '庚', element: '금' },
  { korean: '신', hanja: '辛', element: '금' },
  { korean: '임', hanja: '壬', element: '수' },
  { korean: '계', hanja: '癸', element: '수' },
];

// 지지(地支) — 인덱스 0~11
export const BRANCHES: Array<{ korean: string; hanja: string; element: Element }> = [
  { korean: '자', hanja: '子', element: '수' },
  { korean: '축', hanja: '丑', element: '토' },
  { korean: '인', hanja: '寅', element: '목' },
  { korean: '묘', hanja: '卯', element: '목' },
  { korean: '진', hanja: '辰', element: '토' },
  { korean: '사', hanja: '巳', element: '화' },
  { korean: '오', hanja: '午', element: '화' },
  { korean: '미', hanja: '未', element: '토' },
  { korean: '신', hanja: '申', element: '금' },
  { korean: '유', hanja: '酉', element: '금' },
  { korean: '술', hanja: '戌', element: '토' },
  { korean: '해', hanja: '亥', element: '수' },
];

// 십성 세부명 → 그룹명 매핑
// 백엔드 ten_god은 세부명(비견/겁재…)을 내려주므로, 그룹명(비겁/식상…)이
// 필요한 표시(평생운 테마 등)에서 이 사전으로 축약한다.
export const TEN_GOD_GROUP: Record<string, string> = {
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
