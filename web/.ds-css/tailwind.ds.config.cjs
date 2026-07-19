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
    // Doodle 시그니처 손그림 밑줄 — 아직 컴포넌트 미사용(적용은 후속 단위)이라 purge 대상.
    'sketch-underline',
  ],
  theme: {
    extend: {
      // Doodle 팔레트 미러 (../tailwind.config.ts 와 값 동일).
      colors: {
        background: '#FFFFFF',
        foreground: '#111827',
        surface: '#FFFFFF',
        border: '#263D5B',
        // primary(#49B6E5)는 백색 대비 2.31:1 — 채움·장식 전용, foreground 는 잉크.
        primary: { DEFAULT: '#49B6E5', foreground: '#111827' },
        accent: { DEFAULT: '#263D5B', foreground: '#FFFFFF' },
        muted: { DEFAULT: '#EDF4FA', foreground: '#445A75' },
        card: { DEFAULT: '#FFFFFF', foreground: '#111827' },
        success: { DEFAULT: '#16A34A', foreground: '#FFFFFF' },
        warning: { DEFAULT: '#D97706', foreground: '#FFFFFF' },
        danger: { DEFAULT: '#DC2626', foreground: '#FFFFFF' },
        info: { DEFAULT: '#2563EB', foreground: '#FFFFFF' },
        element: {
          wood: '#16A34A',
          fire: '#DC2626',
          earth: '#D97706',
          metal: '#64748B',
          water: '#2563EB',
        },
      },
      fontFamily: {
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        // 프리뷰에는 next/font 변수(--font-display-latin)가 없으므로 family 이름을 직접 쓴다.
        display: ['"Delius Swash Caps"', 'Gaegu', 'Pretendard', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
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
        card: '0 2px 6px rgba(38,61,91,0.12)',
        'card-hover': '0 4px 12px rgba(38,61,91,0.18)',
        soft: '0 1px 4px rgba(38,61,91,0.10)',
        block: '0 2px 6px rgba(38,61,91,0.12)',
        'block-sm': '0 1px 4px rgba(38,61,91,0.10)',
        'block-lg': '0 4px 12px rgba(38,61,91,0.18)',
      },
    },
  },
  // ../tailwind.config.ts 와 동일 — `card` 가 colors/boxShadow 양쪽에 있어 생기는 `.shadow-card`
  // 이름 충돌로 그림자가 흰색이 되는 것을 막는다(사전 존재 버그, 상세는 본 config 주석 참조).
  corePlugins: { boxShadowColor: false },
  plugins: [],
};
