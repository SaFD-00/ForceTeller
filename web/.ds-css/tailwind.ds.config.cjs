/** @type {import('tailwindcss').Config} */
// design-sync 프리뷰용 Tailwind v3 정적 컴파일 config.
// 기존 ../tailwind.config.ts 의 theme.extend(오행 색·primary·shadow 등)를 그대로
// 보존하되 content 를 components + design-sync previews 로 한정한다(cwd=web 기준).
// ⚠ Re-sync 위험: ../tailwind.config.ts 의 theme.extend 가 바뀌면 이 파일도 동기화해야
// 새 토큰/유틸이 ds-compiled.css 에 포함된다(NOTES.md 참조).
module.exports = {
  content: [
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './.design-sync/previews/**/*.{ts,tsx}',
  ],
  // globals.css 의 @layer components 시맨틱 헬퍼(.element-*, .card-elevated)는 컴포넌트가
  // 직접 쓰지 않아 purge 된다. conventions.md 가 디자인 에이전트에 안내하는 클래스이므로
  // safelist 로 보존해 ds-compiled.css(=배포 CSS)에 포함시킨다(NOTES.md 참조).
  safelist: [
    'element-wood',
    'element-fire',
    'element-earth',
    'element-metal',
    'element-water',
    'card-elevated',
  ],
  theme: {
    extend: {
      colors: {
        background: '#f7f8fa',
        foreground: '#111827',
        surface: '#ffffff',
        border: '#e5e7eb',
        primary: { DEFAULT: '#7c3aed', foreground: '#ffffff' },
        accent: { DEFAULT: '#8b5cf6', foreground: '#ffffff' },
        muted: { DEFAULT: '#f3f4f6', foreground: '#6b7280' },
        card: { DEFAULT: '#ffffff', foreground: '#111827' },
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
