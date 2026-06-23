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
        // tetris-refined 팔레트 (쿨블루 surface + 비비드 퍼플 포인트 + 딥네이비 잉크)
        background: '#dfe7ff',   // 앱 배경 (쿨블루 surface)
        foreground: '#1c202b',   // 잉크 — 제목·본문·테두리
        surface: '#ffffff',      // 카드/패널 표면
        border: '#1c202b',       // 블록 테두리 (딥네이비, 1.5px)
        primary: {
          DEFAULT: '#7107e7',    // 비비드 퍼플 (브랜드 강조)
          foreground: '#ffffff',
        },
        accent: {
          DEFAULT: '#1c398e',    // 네이비블루 (보조 강조·링크·차트 보조)
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#eef1ff',    // 옅은 블루 틴트 면
          foreground: '#54608a', // 보조 텍스트 (네이비-그레이)
        },
        card: {
          DEFAULT: '#ffffff',
          foreground: '#1c202b',
        },
        success: { DEFAULT: '#16a34a', foreground: '#ffffff' },
        warning: { DEFAULT: '#d97706', foreground: '#ffffff' },
        danger: { DEFAULT: '#dc2626', foreground: '#ffffff' },
        element: {
          wood: '#16a34a',
          fire: '#dc2626',
          earth: '#ca8a04',
          metal: '#71717a',
          water: '#2563eb',
        },
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        display: ['Bangers', 'Pretendard', 'cursive'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderWidth: {
        '1.5': '1.5px',
        '3': '3px',
      },
      boxShadow: {
        // 하드 오프셋 솔리드 그림자(블록감). 기존 card/card-hover/soft 이름 유지 → 사용처 자동 승계.
        card: '3px 3px 0 0 #1c202b',
        'card-hover': '5px 5px 0 0 #1c202b',
        soft: '2px 2px 0 0 #1c202b',
        block: '3px 3px 0 0 #1c202b',
        'block-sm': '2px 2px 0 0 #1c202b',
        'block-lg': '6px 6px 0 0 #1c202b',
      },
    },
  },
  plugins: [],
};

export default config;
