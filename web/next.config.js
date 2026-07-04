/** @type {import('next').NextConfig} */

// API 경로 정책:
//  - 기본은 same-origin `/api/*` → 아래 rewrite로 백엔드에 프록시(개발/단일 호스트 배포).
//  - rewrite 대상은 `API_PROXY_TARGET`(빌드타임 env, 기본 http://localhost:8000)로 오버라이드.
//  - 프론트/백엔드를 다른 호스트로 분리 배포하면 `NEXT_PUBLIC_API_URL`(런타임 노출)을 설정해
//    lib/api/client.ts가 절대 URL로 직접 호출하도록 전환한다(그 경우 이 rewrite는 미사용).
const API_PROXY_TARGET = process.env.API_PROXY_TARGET || 'http://localhost:8000';

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${API_PROXY_TARGET}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
