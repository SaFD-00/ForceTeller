import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Light minimalist palette (FigureLabs-style)
        background: '#f7f8fa',   // 앱 배경 (아주 옅은 회색)
        foreground: '#111827',   // 본문 텍스트 (거의 검정)
        surface: '#ffffff',      // 카드/패널 표면
        border: '#e5e7eb',       // 기본 테두리
        primary: {
          DEFAULT: '#7c3aed',    // 바이올렛 (라이트 배경에 잘 맞음)
          foreground: '#ffffff',
        },
        accent: {
          DEFAULT: '#8b5cf6',
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#f3f4f6',    // 옅은 회색 표면
          foreground: '#6b7280', // 보조 텍스트
        },
        card: {
          DEFAULT: '#ffffff',
          foreground: '#111827',
        },
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
      },
      boxShadow: {
        card: '0 1px 3px rgba(17, 24, 39, 0.04), 0 1px 2px rgba(17, 24, 39, 0.06)',
        'card-hover': '0 4px 16px rgba(17, 24, 39, 0.08)',
        soft: '0 2px 8px rgba(17, 24, 39, 0.06)',
      },
    },
  },
  plugins: [],
};

export default config;
