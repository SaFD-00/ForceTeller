import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Tetris 디자인 시스템 팔레트 (블록게임풍 · 쿨 블루 + 딥 네이비 + 비비드 퍼플)
        background: '#DFE7FF',   // 페이지 배경 (Tetris surface, 쿨 블루)
        foreground: '#1C398E',   // 본문 텍스트 (Tetris text)
        surface: '#FFFFFF',      // 카드/패널 표면 (배경 대비 유지)
        border: '#B9C6F2',       // 기본 테두리 (primary 계열 저채도)
        primary: {
          DEFAULT: '#1C202B',    // 딥 네이비 (주요 액션·헤딩 강조)
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#7107E7',    // 비비드 퍼플 (secondary)
          foreground: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#EEF2FF',    // 옅은 쿨 블루 표면
          foreground: '#4C63B0', // 보조 텍스트 (페이지 배경·카드·muted 모두 AA-normal 통과)
        },
        card: {
          DEFAULT: '#FFFFFF',
          foreground: '#1C398E',
        },
        // 시맨틱 상태 토큰
        success: { DEFAULT: '#16A34A', foreground: '#FFFFFF' },
        warning: { DEFAULT: '#D97706', foreground: '#FFFFFF' },
        danger: { DEFAULT: '#DC2626', foreground: '#FFFFFF' },
        info: { DEFAULT: '#2563EB', foreground: '#FFFFFF' },
        // 오행 색 — 시맨틱 토큰과 정렬 (도메인 시맨틱 보존)
        element: {
          wood: '#16A34A',   // = success
          fire: '#DC2626',   // = danger
          earth: '#D97706',  // = warning
          metal: '#64748B',  // slate (무채색 유지)
          water: '#2563EB',  // = info
        },
      },
      fontFamily: {
        // 본문: Pretendard 유지 (Bangers는 한글 글리프가 없어 본문 적용 불가)
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        // 디스플레이: Bangers(라틴/숫자, next/font) → Black Han Sans(한글, <link>) → Pretendard 폴백 체인
        display: [
          'var(--font-display-latin)',
          'Black Han Sans',
          'Pretendard',
          'sans-serif',
        ],
        // 모노: JetBrains Mono (간지 한자·수치)
        mono: ['var(--font-mono)', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
        // 블록 감성 — radius를 sm=4px / md=8px 중심으로 하향 (rounded-full은 유지)
        sm: '4px',
        md: '8px',
        lg: '8px',
        xl: '8px',
        '2xl': '8px',
        '3xl': '12px',
      },
      boxShadow: {
        // 네오브루탈리즘 하드 섀도 (딥 네이비 오프셋 블록)
        block: '4px 4px 0 0 #1C202B',
        'block-sm': '2px 2px 0 0 #1C202B',
        // 기존 소비처 호환 별칭 → 블록 섀도로 재정의
        card: '2px 2px 0 0 #1C202B',
        'card-hover': '4px 4px 0 0 #1C202B',
        soft: '2px 2px 0 0 #1C202B',
      },
    },
  },
  plugins: [],
};

export default config;
