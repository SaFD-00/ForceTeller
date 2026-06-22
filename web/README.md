# ForceTeller Web

사주명리학 기반 AI 운세 분석 웹 애플리케이션

## 기술 스택

- **프레임워크**: Next.js 14 (App Router)
- **스타일링**: Tailwind CSS v3 (라이트 미니멀 — FigureLabs 스타일)
- **상태관리**: Zustand
- **데이터 페칭**: React Query
- **차트**: Recharts
- **아이콘**: Iconify (Solar 아이콘셋)
- **애니메이션**: Framer Motion

## 주요 기능

### 1. 히어로 섹션
- 라이트 미니멀(FigureLabs 스타일) 디자인 — 흰 배경 + 바이올렛 포인트
- 생년월일, 출생시간(시간 모름 옵션), 출생도시(자동완성), 성별, 달력유형(양력/음력/윤달) 입력

### 2. 기능 그리드
- 9가지 분석 기능 소개 (3x3 그리드)
  - 사주계산, 성격분석, 직업운
  - 연애운, 건강운, 대운분석
  - 신살, 오행분포, AI대화

### 3. 결과 페이지
- **사주팔자 (四柱八字)**: 년주, 월주, 일주, 시주 시각화
- **오행 분석**: 레이더 차트 + 막대 차트
- **십성 분포**: 10가지 십성의 분포 시각화
- **신강/신약 분석**: 일간 강도 게이지
- **대운 타임라인**: 10년 주기 운세 흐름

### 4. AI 채팅
- 8가지 전문 에이전트 선택 (종합/성격/직업·재물/인연·궁합/건강/운세/용신/학파비교)
- Multi-turn 대화 지원
- 사주 컨텍스트 기반 맞춤 상담
- 답변 생성 중에는 사용자가 채팅 하단(답변 생성 영역)에 있을 때만 자동 스크롤 — 다른 영역을 보고 있으면 화면이 끌려 내려가지 않음

## 프로젝트 구조

```
web/
├── app/
│   ├── layout.tsx          # 루트 레이아웃
│   ├── page.tsx            # 홈페이지
│   ├── providers.tsx       # 전역 Provider
│   ├── globals.css         # 글로벌 스타일
│   ├── icon.svg            # 파비콘 (App Router 규약)
│   ├── result/page.tsx     # 결과 페이지
│   └── chat/page.tsx       # 채팅 페이지
├── components/
│   ├── hero/               # 히어로 섹션
│   ├── features/           # 기능 그리드
│   ├── result/             # 결과 시각화
│   ├── chat/               # 채팅 인터페이스
│   └── ui/                 # 공통 UI 컴포넌트
├── hooks/                  # 커스텀 훅
├── lib/
│   ├── api/                # API 클라이언트
│   ├── constants/          # 상수 정의
│   ├── transforms.ts       # 데이터 변환
│   └── utils.ts            # 유틸리티
├── stores/                 # Zustand 스토어
├── types/                  # TypeScript 타입
├── .design-sync/           # claude.ai/design 동기화 인프라 (아래 참고)
└── .ds-css/                # design-sync용 Tailwind v3 정적 CSS 컴파일
```

## 시작하기

### 1. 의존성 설치
```bash
cd web
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```

### 3. 빌드
```bash
npm run build
npm run start
```

## 환경 변수

`.env.local` 파일 생성:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 오행 색상 시스템

디자인 토큰은 `tailwind.config.ts` 의 `theme.extend.colors.element` 에 정의되며, 유틸리티(`text-element-*`, `bg-element-*`, `.element-*`)로 사용합니다.

| 오행 | 한자 | 색상(유틸리티) |
|------|------|------|
| 목(木) | 木 | `#16a34a` (Green) |
| 화(火) | 火 | `#dc2626` (Red) |
| 토(土) | 土 | `#ca8a04` (Yellow) |
| 금(金) | 金 | `#71717a` (Gray) |
| 수(水) | 水 | `#2563eb` (Blue) |

> 차트(`lib/constants/elements.ts` 의 `ELEMENT_COLORS.hex`)는 시각 대비를 위해 약간 밝은 변형(목 `#22c55e`, 화 `#ef4444`, 토 `#eab308`, 금 `#a1a1aa`, 수 `#3b82f6`)을 사용합니다.

## API 연동

백엔드 API 엔드포인트:
- `POST /api/manseol` - 사주 계산
- `GET /api/manseol/cities` - 도시 검색
- `POST /api/chat` - AI 대화

개발 시 `next.config.js` 의 rewrite가 `/api/*` 를 백엔드(`http://localhost:8000`)로 프록시합니다.

## 디자인 시스템 동기화 (design-sync)

`web/.design-sync/` 는 컴포넌트 라이브러리를 외부 서비스 **claude.ai/design** 디자인시스템과 동기화하는 인프라입니다(Next.js 앱을 synth-entry로 번들). 재현 gotcha는 `.design-sync/NOTES.md` 참고.

```bash
node .ds-css/compile.mjs          # Tailwind v3 정적 CSS 컴파일 → .ds-css/ds-compiled.css
node .ds-sync/package-build.mjs --config .design-sync/config.json \
  --node-modules ./node_modules --entry ./dist/index.js --out ./ds-bundle
node .ds-sync/package-validate.mjs ./ds-bundle   # 헤드리스 렌더 체크 → ds-bundle/.review.html
```

- 프리뷰: `.design-sync/previews/<Name>.tsx` (직접 author, 커밋 대상). 빌드 산출물(`.ds-sync/`, `ds-bundle/`, `ds-compiled.css`)은 gitignore.
- claude.ai 업로드(publish)는 별도 승인 단계입니다.

## 라이선스

MIT License
