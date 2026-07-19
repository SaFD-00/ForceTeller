import type { Config } from 'tailwindcss';

// ForceTeller 디자인 토큰 — Doodle 톤(손그림 종이 위 스케치 잉크 + 소프트 섀도).
// SSOT: 레포 루트 DESIGN.md(typeui.sh Doodle) + 그 "앱 토큰 매핑" 섹션의 파생 규칙.
// ⚠ 이 theme.extend 가 바뀌면 .ds-css/tailwind.ds.config.cjs 와 .design-sync/ds-tokens/tokens.css 도 동기화할 것.
const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        // Doodle 팔레트 (백색 종이 + 스케치 잉크 네이비 + 스카이블루 크레용 포인트).
        // ⚠ 대비 제약: primary #49B6E5 는 흰 배경 대비 2.31:1 로 AA 텍스트(4.5)·non-text(3) 모두 탈락.
        //   → 규칙: "채움·장식 = primary / 텍스트·아이콘강조·포커스링·선택보더 = accent(#263D5B, 11.0:1)".
        //   자세한 근거는 DESIGN.md "앱 토큰 매핑" 참조.
        // info 토큰과 element.* 는 우리 도메인 소스(lib/constants/elements.ts ELEMENT_COLORS)를 보존한다.
        background: '#FFFFFF',   // 앱 배경 (스케치북 종이)
        foreground: '#111827',   // 잉크 — 제목·본문 (Doodle text)
        surface: '#FFFFFF',      // 카드/패널 표면
        border: '#263D5B',       // 스케치 선 (Doodle secondary, 백색 대비 11.0:1)
        primary: {
          DEFAULT: '#49B6E5',    // 스카이블루 크레용 (채움·장식 전용)
          foreground: '#111827', // ⚠ white 금지 — #49B6E5 위 white 는 2.3:1
        },
        accent: {
          DEFAULT: '#263D5B',    // 잉크 네이비 (텍스트 강조·링크·포커스 링)
          foreground: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#EDF4FA',    // 옅은 스카이 워시 표면
          foreground: '#445A75', // 보조 텍스트 (백색 대비 7.1:1)
        },
        card: {
          DEFAULT: '#FFFFFF',
          foreground: '#111827',
        },
        // 시맨틱 상태 토큰
        // ink = 텍스트 전용 파생(같은 계열 800급, 전 배경 조합 4.5:1 실측) — DEFAULT hex(도메인 SSOT)는 불변
        success: { DEFAULT: '#16A34A', foreground: '#FFFFFF', ink: '#166534' },
        warning: { DEFAULT: '#D97706', foreground: '#FFFFFF', ink: '#92400E' },
        danger: { DEFAULT: '#DC2626', foreground: '#FFFFFF', ink: '#991B1B' },
        info: { DEFAULT: '#2563EB', foreground: '#FFFFFF', ink: '#1E40AF' },
        // 오행 색 — lib/constants/elements.ts ELEMENT_COLORS.hex 단일 소스와 일치.
        // Doodle 스펙의 success/warning/danger 와 hex 가 그대로 일치해 리디자인에도 불변.
        element: {
          wood:  { DEFAULT: '#16A34A', ink: '#166534' },
          fire:  { DEFAULT: '#DC2626', ink: '#991B1B' },
          earth: { DEFAULT: '#D97706', ink: '#92400E' },
          metal: { DEFAULT: '#64748B', ink: '#475569' },
          water: { DEFAULT: '#2563EB', ink: '#1E40AF' },
        },
      },
      fontFamily: {
        // 본문: Pretendard 유지 (Delius Swash Caps는 한글 글리프가 없어 본문 적용 불가 —
        // DESIGN.md "앱 토큰 매핑"에 문서화된 의도적 일탈)
        // 디스플레이: Delius Swash Caps(라틴/숫자, next/font) → Gaegu(한글, <link>) → Pretendard 폴백 체인
        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        display: [
          'var(--font-display-latin)',
          'Gaegu',
          'Pretendard',
          'sans-serif',
        ],
        // 모노: JetBrains Mono (간지 한자·수치, next/font)
        mono: ['var(--font-mono)', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
        // Doodle rounded 토큰 sm=4px / md=8px 기준 (rounded-full은 유지).
        // 카드/버튼의 손그림 불규칙 radius 는 globals.css 의 .block-card/.btn-block 이 담당.
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
        // Doodle 소프트 섀도 — 종이 위에 살짝 뜬 스케치(잉크 #263D5B 저알파 블러).
        // 이름은 tetris 시절 별칭을 그대로 보존한다: 24개 소비 파일이 shadow-card 등을
        // 직접 쓰므로 값만 교체하면 무수정 전파된다. block=card, block-sm=soft, block-lg=card-hover.
        card: '0 2px 6px rgba(38,61,91,0.12)',
        'card-hover': '0 4px 12px rgba(38,61,91,0.18)',
        soft: '0 1px 4px rgba(38,61,91,0.10)',
        block: '0 2px 6px rgba(38,61,91,0.12)',
        'block-sm': '0 1px 4px rgba(38,61,91,0.10)',
        'block-lg': '0 4px 12px rgba(38,61,91,0.18)',
      },
    },
  },
  // ⚠ boxShadowColor 비활성화 — 이름 충돌 해소(사전 존재 버그).
  // `card` 가 theme.colors 와 theme.boxShadow 양쪽에 있어 Tailwind 가 `.shadow-card` 를 두 번 생성한다:
  // ① boxShadow 유틸(정상) ② boxShadowColor 유틸 `--tw-shadow-color:#FFFFFF; --tw-shadow:var(--tw-shadow-colored)`.
  // ②가 뒤에 와서 이겨 그림자가 항상 흰색(=흰 배경에서 비가시)이 된다. tetris 팔레트에서도 동일했다.
  // 코드베이스는 shadow-card 를 오직 박스섀도 토큰으로만 쓰고 shadow-<color> 용법은 0건이므로
  // boxShadowColor 를 끄는 것이 토큰 이름·값을 건드리지 않는 최소 수정이다.
  corePlugins: { boxShadowColor: false },
  plugins: [],
};

export default config;
