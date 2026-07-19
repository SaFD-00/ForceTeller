// 만세력 API 함수

import { apiClient } from './client';
import { transformSajuResult } from '@/lib/transforms';
import type { ManseolRequest, ManseolResponse, SajuResultDisplay } from '@/types/saju';

export async function calculateManseol(data: ManseolRequest): Promise<SajuResultDisplay> {
  const response = await apiClient.post<ManseolResponse>('/api/manseol', data);

  if (!response.success || !response.data) {
    throw new Error(response.error || '사주 계산에 실패했습니다');
  }

  return transformSajuResult(response.data);
}

export interface City {
  name: string;           // 영어 이름 (API 전송용)
  name_ko?: string;       // 한글 이름 (표시용)
  country: string;        // 영어 국가명
  country_ko?: string;    // 한글 국가명
  latitude?: number;
  longitude?: number;
}

interface CitiesResponse {
  success: boolean;
  cities: City[];
  total: number;
}

// 도시 검색 결과. isFallback=true면 백엔드 조회 실패로 하드코딩 목록을 대신 쓴 것 —
// 호출부(입력 폼)가 이를 알고 사용자에게 안내할 수 있도록 조용히 삼키지 않고 표면화한다.
export interface CitySearchResult {
  cities: City[];
  isFallback: boolean;
}

// 백엔드 부재 시 사용하는 최소 도시 목록.
// 한글명은 표시용, 영어명은 API 전송용이다 (렌더부는 name_ko를 우선 사용).
const FALLBACK_CITIES: City[] = [
  { name: 'Seoul', name_ko: '서울', country: 'South Korea', country_ko: '대한민국', latitude: 37.5665, longitude: 126.978 },
  { name: 'Busan', name_ko: '부산', country: 'South Korea', country_ko: '대한민국', latitude: 35.1796, longitude: 129.0756 },
  { name: 'Tokyo', name_ko: '도쿄', country: 'Japan', country_ko: '일본', latitude: 35.6762, longitude: 139.6503 },
  { name: 'New York City', name_ko: '뉴욕', country: 'United States', country_ko: '미국', latitude: 40.7128, longitude: -74.006 },
  { name: 'London', name_ko: '런던', country: 'United Kingdom', country_ko: '영국', latitude: 51.5074, longitude: -0.1278 },
  { name: 'Paris', name_ko: '파리', country: 'France', country_ko: '프랑스', latitude: 48.8566, longitude: 2.3522 },
  { name: 'Beijing', name_ko: '베이징', country: 'China', country_ko: '중국', latitude: 39.9042, longitude: 116.4074 },
  { name: 'Sydney', name_ko: '시드니', country: 'Australia', country_ko: '호주', latitude: -33.8688, longitude: 151.2093 },
  { name: 'Singapore', name_ko: '싱가포르', country: 'Singapore', country_ko: '싱가포르', latitude: 1.3521, longitude: 103.8198 },
  { name: 'Hong Kong', name_ko: '홍콩', country: 'Hong Kong', country_ko: '홍콩', latitude: 22.3193, longitude: 114.1694 },
];

export async function searchCities(query: string, limit: number = 20): Promise<CitySearchResult> {
  try {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    params.set('limit', limit.toString());

    const response = await apiClient.get<CitiesResponse>(
      `/api/manseol/cities?${params.toString()}`
    );

    if (response.success && response.cities) {
      return { cities: response.cities, isFallback: false };
    }
    return { cities: [], isFallback: false };
  } catch {
    // 백엔드가 없을 경우 기본 도시 목록으로 폴백하되, isFallback로 호출부에 알린다.
    if (!query) return { cities: FALLBACK_CITIES, isFallback: true };

    const queryLower = query.toLowerCase();
    // 목록이 한글로 표시되므로 한글 질의("서울")도 매칭해야 한다.
    const filtered = FALLBACK_CITIES.filter(
      (city) =>
        city.name.toLowerCase().includes(queryLower) ||
        city.country.toLowerCase().includes(queryLower) ||
        city.name_ko?.includes(query) ||
        city.country_ko?.includes(query)
    );
    return { cities: filtered, isFallback: true };
  }
}
