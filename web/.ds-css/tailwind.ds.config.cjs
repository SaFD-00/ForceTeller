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
  // globals.css 의 @layer components 시맨틱 헬퍼(.element-*, .card-elevated, .block-press,
  // .btn-block)는 컴포넌트가 직접 안 쓸 수 있어 purge 된다. conventions.md 가 디자인 에이전트에
  // 안내하는 클래스이므로 safelist 로 보존해 ds-compiled.css(=배포 CSS)에 포함시킨다(NOTES.md 참조).
  safelist: [
    'element-wood',
    'element-fire',
    'element-earth',
    'element-metal',
    'element-water',
    'card-elevated',
    'btn-block',
    'block-press',
  ],
  theme: {
    extend: {
      colors: {
        background: '#dfe7ff',
        foreground: '#1c202b',
        surface: '#ffffff',
        border: '#1c202b',
        primary: { DEFAULT: '#7107e7', foreground: '#ffffff' },
        accent: { DEFAULT: '#1c398e', foreground: '#ffffff' },
        muted: { DEFAULT: '#eef1ff', foreground: '#54608a' },
        card: { DEFAULT: '#ffffff', foreground: '#1c202b' },
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
