// 사주 관련 타입 정의

export type CalendarType = 'solar' | 'lunar' | 'leap_lunar';
export type Gender = 'male' | 'female';
export type Element = '목' | '화' | '토' | '금' | '수';
export type Polarity = '양' | '음';

export interface StemData {
  index: number;
  korean: string;
  chinese: string;
  element: Element;
  polarity: Polarity;
}

export interface BranchData {
  index: number;
  korean: string;
  chinese: string;
  element: Element;
  polarity: Polarity;
  animal: string;
  hidden_stems: Array<{
    stem_index: number;
    korean: string;
    chinese: string;
    element: Element;
    type: string;
    ratio: number;
  }>;
}

export interface PillarData {
  stem: StemData;
  branch: BranchData;
  ganji_korean: string;
  ganji_chinese: string;
  ten_god: string | null;
  twelve_phase: string | null;
}

export interface FourPillars {
  year: PillarData;
  month: PillarData;
  day: PillarData;
  hour: PillarData | null;
}

export interface TimeCorrection {
  original_time: string;
  true_solar_time: string;
  longitude_correction_minutes: number;
  eot_correction_minutes: number;
  dst_correction_minutes: number;
  total_correction_minutes: number;
  standard_meridian: number;
  birth_longitude: number;
}

export interface DayMasterAnalysis {
  element: Element;
  polarity: Polarity;
  korean: string;
  chinese: string;
  metaphor: string;
  characteristics: string[];
}

export interface FiveElementsAnalysis {
  wood: number;
  fire: number;
  earth: number;
  metal: number;
  water: number;
  dominant: string[];
  lacking: string[];
  distribution: Record<string, number>;
}

export interface TenGodsDistribution {
  비견: number;
  겁재: number;
  식신: number;
  상관: number;
  편재: number;
  정재: number;
  편관: number;
  정관: number;
  편인: number;
  정인: number;
}

export interface StrengthAnalysis {
  level: '신강' | '신약' | '중화';
  score: number;
  supporting_count: number;
  weakening_count: number;
  analysis: string;
}

export interface UsefulGodAnalysis {
  type: string;
  primary: Element;
  secondary: Element | null;
  avoid: Element | null;
  reasoning: string;
}

export interface ShenshaData {
  name: string;
  type: '길신' | '흉신' | '중성';
  position: string;
  description: string;
}

export interface FortuneCycle {
  start_age: number;
  end_age: number;
  stem_index: number;
  branch_index: number;
  ganji_korean: string;
  ganji_chinese: string;
  ten_god?: string;
  branch_ten_god?: string;
  twelve_phase?: string;
}

// 현재 운세(연/월/일운) 및 슬라이더 범위 — 백엔드 단일 진실 공급원 계약
// Entry 공통 필드 + 종류별 라벨(year/month/calendar_month/date)
export interface CurrentFortuneEntry {
  stem: string;
  branch: string;
  stem_hanja: string;
  branch_hanja: string;
  stem_index: number;
  branch_index: number;
  element: Element;
  ganji_korean: string;
  ganji_chinese: string;
  ten_god: string;
  branch_ten_god: string;
  twelve_phase: string;
  // 라벨 (종류에 따라 일부만 존재)
  year?: number;
  month?: number; // 절기월
  calendar_month?: number; // 달력월 (fortune_ranges.monthly 전용)
  date?: string; // "YYYY-MM-DD"
}

export interface CurrentFortune {
  reference_datetime: string;
  yearly: CurrentFortuneEntry;
  monthly: CurrentFortuneEntry;
  daily: CurrentFortuneEntry;
}

export interface FortuneRanges {
  yearly: CurrentFortuneEntry[]; // 현재±5년 (11)
  monthly: CurrentFortuneEntry[]; // 해당 절기연 12개월 (12)
  daily: CurrentFortuneEntry[]; // 현재±7일 (15)
}

export interface FortuneCycleData {
  start_age: number;
  direction: '순행' | '역행';
  cycles: FortuneCycle[];
  current_cycle_index: number | null;
}

// 천간/지지 상호작용 (합·충·형·파·해·공망)
export interface InteractionItem {
  type: string;
  positions?: string[];
  stems?: number[];
  branches?: number[];
  result?: string;
  description: string;
  name?: string;
  position?: string;
  branch?: number;
}

export interface InteractionsData {
  천간합?: InteractionItem[];
  천간충극?: InteractionItem[];
  지지육합?: InteractionItem[];
  지지삼합?: InteractionItem[];
  지지방합?: InteractionItem[];
  지지반합?: InteractionItem[];
  지지충?: InteractionItem[];
  지지형?: InteractionItem[];
  지지파?: InteractionItem[];
  지지해?: InteractionItem[];
  공망?: InteractionItem[];
}

// 세운(歲運) - 연도별 운세
export interface SewunItem {
  year: number;
  stem_index: number;
  branch_index: number;
  ganji_korean: string;
  ganji_chinese: string;
  ten_god: string;
  twelve_phase: string;
}

// 용신 개운법 (오행별 추천)
export interface YongsinElementGuide {
  element: string;
  colors: string[];
  directions: string[];
  main_careers: string[];
  recommended_activities: string[];
}

export interface YongsinRecommendations {
  summary: string;
  primary_element: YongsinElementGuide;
  lucky_items?: Record<string, unknown>;
  lifestyle_tips?: string[];
  cautions?: string[];
  seasonal_advice?: Record<string, string>;
  secondary_element?: YongsinElementGuide;
}

// 운세 유형별 점수
export interface FortuneScoreItem {
  score: number;
  summary: string;
  positive: string[];
  negative: string[];
  advice: string[];
  lucky_colors: string[];
  lucky_numbers: number[];
  lucky_directions: string[];
}

export type FortuneScores = Record<string, FortuneScoreItem>;

// 용신 4방법 비교 (강약/조후/통관/병약)
export interface YongsinComparison {
  results: Record<string, Record<string, unknown>>;
  applicabilities: Record<string, number>;
  recommendation: {
    method: string;
    algorithm_name: string;
    result: Record<string, unknown>;
  };
  algorithms?: unknown[];
}

export interface SajuAnalysis {
  day_master: DayMasterAnalysis;
  five_elements: FiveElementsAnalysis;
  ten_gods_dist: TenGodsDistribution;
  strength: StrengthAnalysis;
  useful_god: UsefulGodAnalysis;
  shensha: ShenshaData[];
}

export interface InputSummary {
  name: string;
  birth_date: string;
  birth_time: string | null;
  calendar: CalendarType;
  city: string;
  gender: Gender;
  jajasi: boolean;
  // 음력 정보
  lunar_year?: number;
  lunar_month?: number;
  lunar_day?: number;
  is_leap_month?: boolean;
  // 일주 정보
  day_ganji_korean?: string;
  day_ganji_chinese?: string;
  day_metaphor?: string;
  day_animal?: string;
}

export interface MetaInfo {
  version: string;
  generated_at: string;
  engine: string;
}

export interface SajuResult {
  meta: MetaInfo;
  input: InputSummary;
  adjusted_time: TimeCorrection | null;
  pillars: FourPillars;
  analysis: SajuAnalysis;
  fortune_cycles: FortuneCycleData | null;
  interactions?: InteractionsData;
  sewun?: SewunItem[];
  yongsin_comparison?: YongsinComparison;
  yongsin_recommendations?: YongsinRecommendations;
  school_comparison?: SchoolComparisonResult;
  fortune_scores?: FortuneScores;
  current_fortune?: CurrentFortune;
  fortune_ranges?: FortuneRanges;
}

// API 요청/응답 타입
export interface ManseolRequest {
  name: string;
  birth_date: string;
  birth_time?: string;
  calendar?: CalendarType;
  city?: string;
  gender: Gender;
  jajasi?: boolean;
  longitude?: number;
  apply_time_correction?: boolean;
}

export interface ManseolResponse {
  success: boolean;
  data: SajuResult;
  error?: string;
}

export interface ChatRequest {
  session_id?: string;
  saju_data?: SajuResult;
  message: string;
  interpretation_type?: 'full' | 'quick' | 'specific';
  focus?: string;
  llm_provider?: 'openai' | 'gemini';
}

export interface ChatResponse {
  success: boolean;
  session_id: string;
  message: string;
  suggested_questions?: string[];
  interpretations?: Record<string, unknown>;
  agents_used: string[];
  error?: string;
}

// 채팅 관련 타입
export type AgentType = 'general' | 'personality' | 'career' | 'relationship' | 'health' | 'fortune' | 'yongsin' | 'school_compare';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  suggested_questions?: string[];
  // 응답을 담당한 에이전트 출처·신뢰도 (어시스턴트 메시지)
  agent?: string;
  agent_display_name?: string;
  confidence?: number;
  // 실패를 알리는 메시지 — 렌더 시 role="alert" 로 즉시 낭독된다
  isError?: boolean;
}

// 컴포넌트용 호환 타입 (백엔드 응답을 프론트엔드에서 사용하기 위한 변환 타입)
export interface HeavenlyStemDisplay {
  hanja: string;
  korean: string;
  element: Element;
  index?: number;
}

export interface HiddenStemDisplay {
  korean: string;
  chinese: string;
  element: string;
  type: string;
  ratio: number;
  ten_god?: string;
}

export interface EarthlyBranchDisplay {
  hanja: string;
  korean: string;
  element: Element;
  hidden_stems?: HiddenStemDisplay[];
}

export interface PillarDisplay {
  heavenly_stem: HeavenlyStemDisplay;
  earthly_branch: EarthlyBranchDisplay;
  ten_god?: string | null;
  twelve_phase?: string | null;
}

export interface FourPillarsDisplay {
  year: PillarDisplay;
  month: PillarDisplay;
  day: PillarDisplay;
  hour: PillarDisplay;
}

export interface FiveElementsDisplay {
  distribution: Record<Element, number>;
  dominant: Element | null;
  lacking: Element | null;
  yongshin: Element | null;
  gishin: Element | null;
}

export interface TenGodsDisplay {
  counts: Record<string, number>;
  primary: string | null;
}

export interface StrengthDisplay {
  score: number;
  is_strong: boolean;
  type?: string;
  description?: string;
}

export interface FortuneCycleDisplay {
  start_age: number;
  heavenly_stem: HeavenlyStemDisplay;
  earthly_branch: EarthlyBranchDisplay;
  ten_god?: string;
  branch_ten_god?: string;
  twelve_phase?: string;
}

export interface BirthInfo {
  name: string;
  birth_date: string;
  birth_time?: string;
  city: string;
  gender: Gender;
  // 음력 정보
  lunar_year?: number;
  lunar_month?: number;
  lunar_day?: number;
  is_leap_month?: boolean;
  // 일주 정보
  day_ganji_korean?: string;
  day_ganji_chinese?: string;
  day_metaphor?: string;
  day_animal?: string;
}

export interface ShenshaDisplay {
  name: string;
  type: '길신' | '흉신' | '중성';
  position: string;
  description: string;
}

// 프론트엔드에서 사용하는 통합 결과 타입
export interface SajuResultDisplay {
  birth_info: BirthInfo;
  four_pillars: FourPillarsDisplay;
  five_elements: FiveElementsDisplay;
  ten_gods: TenGodsDisplay;
  strength: StrengthDisplay;
  fortune_cycles?: FortuneCycleDisplay[];
  shensha?: ShenshaDisplay[];
  adjusted_time?: TimeCorrection | null;
  interactions?: InteractionsData;
  sewun?: SewunItem[];
  yongsin_comparison?: YongsinComparison;
  yongsin_recommendations?: YongsinRecommendations;
  school_comparison?: SchoolComparisonResult;
  fortune_scores?: FortuneScores;
  current_fortune?: CurrentFortune;
  fortune_ranges?: FortuneRanges;
}

// 유틸리티: 백엔드 응답을 프론트엔드 타입으로 변환하는 함수 타입
export type TransformSajuResult = (result: SajuResult) => SajuResultDisplay;

// ============== 유파 비교 타입 ==============
// (SajuResult.school_comparison / SajuResultDisplay.school_comparison에서 사용)

// 유파 해석 결과
export interface SchoolInterpretation {
  school: string;
  school_name: string;
  yong_sin: string;
  geok_guk?: string;
  overall: string;
  health: string;
  wealth: string;
  career: string;
  relationship: string;
  fame: string;
  confidence: number;
  key_features: string[];
}

// 유파 비교 결과
export interface SchoolComparisonResult {
  schools: string[];
  interpretations: SchoolInterpretation[];
  consensus: Array<{
    category: string;
    agreement: string;
    schools: string[];
  }>;
  differences: Array<{
    category: string;
    interpretations: Array<{
      school: string;
      school_name: string;
      interpretation: string;
    }>;
  }>;
  recommendation: string;
  confidence?: number;
}
