// API 클라이언트
//
// 경로 정책(next.config.js와 한 쌍):
//  - 기본값: API_BASE=''  → `/api/*`를 same-origin으로 호출하고 next.config.js의 rewrite가
//    백엔드(API_PROXY_TARGET, 기본 localhost:8000)로 프록시한다. 개발·단일 호스트 배포의 기본 경로.
//  - 오버라이드: NEXT_PUBLIC_API_URL을 설정하면 그 절대 URL을 prefix로 붙여 백엔드를 직접 호출한다.
//    프론트/백엔드를 다른 호스트로 분리 배포할 때 사용(이때 rewrite는 경유하지 않음).
const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

interface ApiError {
  success: false;
  error: string;
  detail?: string;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      success: false,
      error: `HTTP ${response.status}`,
      detail: response.statusText,
    }));
    throw new Error(error.error || error.detail || 'Unknown error');
  }
  return response.json();
}

export const apiClient = {
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return handleResponse<T>(response);
  },

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse<T>(response);
  },

  async delete<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return handleResponse<T>(response);
  },
};
