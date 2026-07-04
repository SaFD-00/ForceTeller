import type { Config } from 'tailwindcss';

// ForceTeller 디자인 토큰 — tetris-refined 블록 톤(고대비 비비드 컬러 블록 + 하드 오프셋 그림자).
// ⚠ 이 theme.extend 가 바뀌면 .ds-css/tailwind.ds.config.cjs 와 .design-sync/ds-tokens/tokens.css 도 동기화할 것.
const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // tetris-refined 팔레트 (쿨블루 surface + 비비드 퍼플 포인트 + 딥네이비 잉크).
        // 렌더되는 컴포넌트 다수가 원격 리스타일 기준으로 작성되어 hue 배정은 원격을 따른다:
        // primary=비비드 퍼플, accent=네이비블루, border/foreground=딥네이비 잉크.
        // info 토큰과 element.* 는 우리 도메인 소스(lib/constants/elements.ts ELEMENT_COLORS)를 보존한다.
        background: '#DFE7FF',   // 앱 배경 (쿨 블루 surface)
        foreground: '#1C202B',   // 잉크 — 제목·본문·테두리 (딥 네이비)
        surface: '#FFFFFF',      // 카드/패널 표면
        border: '#1C202B',       // 블록 테두리 (딥 네이비, 1.5px)
        primary: {
          DEFAULT: '#7107E7',    // 비비드 퍼플 (브랜드 강조)
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#1C398E',    // 네이비블루 (보조 강조·링크·차트 보조)
          foreground: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#EEF2FF',    // 옅은 쿨 블루 표면
          foreground: '#54608A', // 보조 텍스트 (네이비-그레이)
        },
        card: {
          DEFAULT: '#FFFFFF',
          foreground: '#1C202B',
        },
        // 시맨틱 상태 토큰
        success: { DEFAULT: '#16A34A', foreground: '#FFFFFF' },
        warning: { DEFAULT: '#D97706', foreground: '#FFFFFF' },
        danger: { DEFAULT: '#DC2626', foreground: '#FFFFFF' },
        info: { DEFAULT: '#2563EB', foreground: '#FFFFFF' },
        // 오행 색 — lib/constants/elements.ts ELEMENT_COLORS.hex 단일 소스와 일치
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
        // 모노: JetBrains Mono (간지 한자·수치, next/font)
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
      borderWidth: {
        '1.5': '1.5px',
        '3': '3px',
      },
      boxShadow: {
        // 네오브루탈리즘 하드 오프셋 솔리드 그림자 (딥 네이비 블록).
        // card/card-hover/soft: 원격 오프셋 값(기존 소비처 자동 승계). block/block-sm: 우리 별칭.
        card: '3px 3px 0 0 #1C202B',
        'card-hover': '5px 5px 0 0 #1C202B',
        soft: '2px 2px 0 0 #1C202B',
        block: '4px 4px 0 0 #1C202B',
        'block-sm': '2px 2px 0 0 #1C202B',
        'block-lg': '6px 6px 0 0 #1C202B',
      },
    },
  },
  plugins: [],
};

export default config;
