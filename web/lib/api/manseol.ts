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
const FALLBACK_CITIES: City[] = [
  { name: 'Seoul', country: 'South Korea', latitude: 37.5665, longitude: 126.978 },
  { name: 'Busan', country: 'South Korea', latitude: 35.1796, longitude: 129.0756 },
  { name: 'Tokyo', country: 'Japan', latitude: 35.6762, longitude: 139.6503 },
  { name: 'New York City', country: 'United States', latitude: 40.7128, longitude: -74.006 },
  { name: 'London', country: 'United Kingdom', latitude: 51.5074, longitude: -0.1278 },
  { name: 'Paris', country: 'France', latitude: 48.8566, longitude: 2.3522 },
  { name: 'Beijing', country: 'China', latitude: 39.9042, longitude: 116.4074 },
  { name: 'Sydney', country: 'Australia', latitude: -33.8688, longitude: 151.2093 },
  { name: 'Singapore', country: 'Singapore', latitude: 1.3521, longitude: 103.8198 },
  { name: 'Hong Kong', country: 'Hong Kong', latitude: 22.3193, longitude: 114.1694 },
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
    const filtered = FALLBACK_CITIES.filter(
      (city) =>
        city.name.toLowerCase().includes(queryLower) ||
        city.country.toLowerCase().includes(queryLower)
    );
    return { cities: filtered, isFallback: true };
  }
}
