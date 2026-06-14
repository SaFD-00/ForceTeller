// 분석 API
import { apiClient } from './client';
import type {
  AnalysisRequest,
  AnalysisResponse,
  AnalysisTypesResponse,
  AnalysisType,
  YongSinMethodType,
  SchoolCodeType,
} from '@/types/saju';

/**
 * 분석 유형 목록 가져오기
 */
export async function getAnalysisTypes(): Promise<AnalysisTypesResponse> {
  return apiClient.get<AnalysisTypesResponse>('/api/analysis/types');
}

/**
 * 분석 요청
 */
export async function requestAnalysis(
  request: AnalysisRequest
): Promise<AnalysisResponse> {
  return apiClient.post<AnalysisResponse>('/api/analysis', request);
}

/**
 * 운세 분석 요청 (편의 함수)
 */
export async function analyzeFortuneType(
  sessionId: string,
  fortuneType: 'general' | 'career' | 'wealth' | 'health' | 'love'
): Promise<AnalysisResponse> {
  const analysisType = `fortune_${fortuneType}` as AnalysisType;
  return requestAnalysis({
    session_id: sessionId,
    analysis_type: analysisType,
  });
}

/**
 * 용신 분석 요청 (자동)
 */
export async function analyzeYongsinAuto(
  sessionId: string
): Promise<AnalysisResponse> {
  return requestAnalysis({
    session_id: sessionId,
    analysis_type: 'yongsin',
  });
}

/**
 * 용신 분석 요청 (특정 방법론)
 */
export async function analyzeYongsinMethod(
  sessionId: string,
  method: YongSinMethodType
): Promise<AnalysisResponse> {
  return requestAnalysis({
    session_id: sessionId,
    analysis_type: 'yongsin_method',
    yongsin_method: method,
  });
}

/**
 * 유파 비교 분석 요청
 */
export async function analyzeSchoolComparison(
  sessionId: string,
  schools?: SchoolCodeType[]
): Promise<AnalysisResponse> {
  return requestAnalysis({
    session_id: sessionId,
    analysis_type: 'school_compare',
    schools,
  });
}

// 분석 유형 정보 (클라이언트 사이드 캐시용)
export const FORTUNE_TYPES = [
  { code: 'fortune_general', name: '종합운', icon: 'Star' },
  { code: 'fortune_career', name: '직업운', icon: 'Briefcase' },
  { code: 'fortune_wealth', name: '재물운', icon: 'DollarSign' },
  { code: 'fortune_health', name: '건강운', icon: 'Heart' },
  { code: 'fortune_love', name: '애정운', icon: 'Heart' },
] as const;

export const YONGSIN_METHODS = [
  { code: 'strength', name: '강약', description: '일간의 강약을 기준으로 분석' },
  { code: 'seasonal', name: '조후', description: '계절(월령)을 기준으로 분석' },
  { code: 'mediation', name: '통관', description: '오행 충돌을 중재하는 분석' },
  { code: 'disease', name: '병약', description: '사주의 병(病)을 치료하는 분석' },
] as const;

export const SCHOOL_CODES = [
  { code: 'ziping', name: '자평명리', description: '일간 중심의 강약 분석과 격국론' },
  { code: 'dts', name: '적천수', description: '오행의 생극제화와 통변성정' },
  { code: 'qtbj', name: '궁통보감', description: '월령과 조후 중심 해석' },
  { code: 'modern', name: '현대명리', description: '심리학적 관점과 실용적 조언' },
  { code: 'shensha', name: '신살중심', description: '신살로 길흉 판단' },
] as const;
