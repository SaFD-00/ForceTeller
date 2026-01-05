import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0a',
        foreground: '#fafafa',
        primary: {
          DEFAULT: '#8b5cf6',
          foreground: '#fafafa',
        },
        accent: {
          DEFAULT: '#a855f7',
          foreground: '#fafafa',
        },
        muted: {
          DEFAULT: '#1a1a1a',
          foreground: '#a1a1aa',
        },
        card: {
          DEFAULT: 'rgba(255, 255, 255, 0.05)',
          foreground: '#fafafa',
        },
        element: {
          wood: '#22c55e',
          fire: '#ef4444',
          earth: '#eab308',
          metal: '#a1a1aa',
          water: '#3b82f6',
        },
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};

export default config;
