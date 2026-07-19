# ForceTeller Web

사주명리학 기반 AI 운세 분석 웹 애플리케이션

## 기술 스택

- **프레임워크**: Next.js 14 (App Router)
- **스타일링**: Tailwind CSS v3 (Doodle 손그림 톤 — 불규칙 스케치 테두리 + 소프트 페이퍼 그림자)
- **타이포**: Pretendard(본문) + Delius Swash Caps(라틴 디스플레이) + Gaegu(한글 디스플레이) + JetBrains Mono(숫자·간지)
- **마스코트**: "별이" — 별·달 점성술사 (간단한 SVG로 조립, 채팅·설명·로딩·로고에 재사용)
- **상태관리**: Zustand
- **차트**: Recharts
- **아이콘**: Iconify (Solar 아이콘셋)
- **애니메이션**: Framer Motion
- **마크다운**: react-markdown + remark-gfm

## 주요 기능

### 1. 히어로 섹션
- Doodle 손그림 디자인 — 종이 흰 배경 + 스카이 크레용 포인트 + 마스코트 "별이" + Delius Swash Caps 워드마크
- Framer Motion 진입 애니메이션
- 생년월일, 출생시간(시간 모름 옵션), 출생도시(자동완성), 성별, 달력유형(양력/음력/윤달) 입력

### 2. 기능 그리드
- 9가지 분석 기능 소개 (3x3 그리드)
  - 사주계산, 성격분석, 직업운
  - 연애운, 건강운, 대운분석
  - 신살, 오행분포, AI대화

### 3. 결과 페이지
- **사주팔자 (四柱八字)**: 년·월·일·시주 천간·지지 테이블 (`PillarTable`)
- **간지 상호작용·신살**: 합·충·형·파·해·공망(空亡) 관계 탭 (`InteractionsTabs`)과 신살(神殺) 상세 해설 (`ShenshaDetailCard`)
- **오행 분석**: 오행 분포와 오각형 차트, 일간 강도 분포 시각화 (`ElementDistribution`·`PentagonChart`·`StrengthDistributionChart`)
- **운세 점수·용신·개운법**: 운세 유형별 점수 대시보드 (`FortuneScoreDashboard`), 용신(用神) 안내 (`YongshinCard`), 개운법 가이드 (`LuckyGuideCard`)
- **5학파 비교**: 학파별 해석 비교와 일치도 (`SchoolComparison`)
- **대운·세운·평생운**: 대운/현재 운세 슬라이더 (`FortuneCycleSlider`), 세운(歲運, `YearlyFortune`), 평생운 내러티브 (`LifetimeReport`). 현재 연/월/일운은 백엔드 단일 진실 공급원(절기 기반)이 계산한 값을 그대로 렌더한다.
- **면책 고지**: 참고용 안내 (`Disclaimer`)

### 4. AI 채팅
- 8가지 전문 에이전트 선택
  - 종합상담, 성격분석, 직업/재물
  - 인연/궁합, 건강, 운세
  - 용신분석, 유파비교
- Multi-turn 대화 지원 (SSE 스트리밍)
- 사주 컨텍스트 기반 맞춤 상담
- 답변 생성 중에는 사용자가 채팅 하단(답변 생성 영역)에 있을 때만 자동 스크롤 — 다른 영역을 보고 있으면 화면이 끌려 내려가지 않음

## 프로젝트 구조

```
web/
├── app/
│   ├── layout.tsx          # 루트 레이아웃 (사이드바 + 폰트)
│   ├── page.tsx            # 홈페이지
│   ├── globals.css         # 글로벌 스타일
│   ├── icon.svg            # 파비콘 (App Router 규약)
│   ├── result/page.tsx     # 결과 페이지
│   └── chat/page.tsx       # 채팅 페이지
├── components/
│   ├── hero/               # 히어로 섹션
│   ├── features/           # 기능 그리드
│   ├── result/             # 결과 시각화
│   ├── chat/               # 채팅 인터페이스
│   ├── layout/             # 사이드바 등 레이아웃
│   └── ui/                 # 공통 UI 컴포넌트
├── data/                   # 정적 데이터 (사주 용어 사전 등)
├── lib/
│   ├── api/                # API 클라이언트 (client/manseol/chat)
│   ├── constants/          # 상수 정의 (오행·기능 목록)
│   ├── ganji.ts            # 간지 표시 사전 (천간·지지·십성 그룹)
│   ├── transforms.ts       # 백엔드 응답 → 표시용 변환
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

### 4. 검증
```bash
npm run lint      # ESLint (next/core-web-vitals)
npx tsc --noEmit  # 타입 체크
npm test          # vitest (lib 순수 함수 단위 테스트)
```

접근성(a11y) 회귀는 위 자동 테스트로 잡히지 않는다 — **프로덕션 빌드**(`npm run build && npm run start`)를 띄운
상태에서 Playwright로 실측 검증한다. 결과 화면에 mock API 응답을 주입해 렌더한 뒤, DOM 상태(`inert`, `aria-*`,
`role`)와 `getComputedStyle`(포커스 링 등)로 판정한다. 검증 하네스 자체는 셀프테스트를 갖춘다 — 고의로 계약을
깨는 변이(예: inert 미해제)를 주입해 FAIL이 실제로 뜨는지 먼저 확인한 뒤에만 정상 시나리오의 PASS를 신뢰한다.

#### a11y 하네스 실행

```bash
npx playwright install chromium   # 최초 1회 (브라우저 다운로드)

npm run build
PORT=3456 npm run start &         # 하네스는 3456 포트의 프로덕션 서버를 기대한다

npm run e2e                       # 4종 전부 — 전부 VERDICT: PASS 여야 한다
npm run e2e:selftest              # 변이 주입 — 하네스가 결함을 잡으면 성공(종료코드 0)
```

`e2e:selftest`는 `A11Y_SELFTEST=1`로 알려진 결함 4종을 DOM에 심고, 하네스가 이를 잡아 실패(exit 1)하는지
확인한다. npm script가 종료코드를 반전하므로 **`npm run e2e:selftest`가 성공해야 정상**이다. 이 스텝이 실패하면
하네스가 아무것도 판별하지 못하고 공허하게 통과하고 있다는 뜻이다.

| 스크립트 | 대상 | 검사 |
|---|---|---|
| `e2e/a11y-result.mjs` | `/result` | 렌더 가드, 전역 대비 스윕, 도넛 갭/대비, 오각형 화살표·범례, aria-label ↔ fixture 대조, 용어 모달(포커스 트랩·`inert`·`overflow` 복원·exit 애니메이션), 툴팁 Escape 해제, 십성 범례 |
| `e2e/a11y-chat.mjs` | `/chat` | 로딩 점 대비, `aria-live`, textarea 접근 가능한 이름 |
| `e2e/a11y-mobile-chat.mjs` | `/result` 390×844 | 모바일 채팅 오버레이 M0~M11 (포탈·ARIA·`inert`·트랩·Escape·포커스 복귀) |
| `e2e/a11y-loading.mjs` | `/` | LoadingOverlay L0~L10 (포탈·`role=status`·`inert`·배경 Tab 차단·복원) |

- 브라우저 채널: 로컬은 시스템 Chrome, CI는 번들 chromium을 쓴다. `PW_CHANNEL=`(빈 값)으로 실행하면
  로컬에서도 CI와 동일한 번들 chromium 조건을 재현할 수 있다.
- 다른 포트로 띄웠다면 `E2E_BASE_URL=http://localhost:PORT`로 넘긴다.
- 백엔드는 필요 없다. mock은 `e2e/fixtures/mock-saju.json`을 localStorage(`saju-storage`)에 주입하고,
  도시 검색은 프론트의 오프라인 폴백 목록으로 동작한다.
- CI에서는 아직 **비차단**(`continue-on-error`)으로 스테이징 중이다 — `.github/workflows/ci.yml` 참조.

> ⚠️ `e2e/fixtures/mock-saju.json`은 백엔드 골든(`tests/unit/manseol/test_manseol_regression.py`)과
> **다른 입력**에서 파생됐다(mock은 1990-03-15, 백엔드 골든은 1990-05-15 → 사주팔자 자체가 다르다).
> 이 mock은 프론트 렌더 계약 검증용 고정 입력일 뿐 만세력 계산의 정답이 아니다. 둘을 같은 것으로 읽지 마라.

## API 연동 · 경로 정책

웹이 사용하는 백엔드 엔드포인트 (전체 API는 루트 README 참조):
- `POST /api/manseol` - 사주 계산
- `GET /api/manseol/cities` - 도시 검색(자동완성)
- `POST /api/chat/stream` - AI 대화 (SSE 스트리밍)

경로 정책은 `next.config.js`와 `lib/api/client.ts`가 한 쌍으로 관리한다:

- **기본(개발·단일 호스트 배포)**: 프론트는 same-origin `/api/*`로 호출하고,
  `next.config.js`의 rewrite가 이를 백엔드로 프록시한다. rewrite 대상은
  환경변수 `API_PROXY_TARGET`(기본 `http://localhost:8000`)로 오버라이드한다.
- **분리 배포(프론트/백엔드가 다른 호스트)**: `NEXT_PUBLIC_API_URL`을 설정하면
  `client.ts`가 그 절대 URL을 prefix로 붙여 백엔드를 직접 호출한다(이 경우 rewrite 미경유).

## 환경 변수

`.env.local` 예시:
```env
# 분리 배포 시에만 필요 — 백엔드 절대 URL을 직접 호출
NEXT_PUBLIC_API_URL=https://api.example.com

# (선택) rewrite 프록시 대상 오버라이드. 기본 http://localhost:8000
# API_PROXY_TARGET=http://backend:8000
```

## 디자인 시스템 (Doodle 손그림)

[typeui.sh `doodle` 디자인 스킬](https://www.typeui.sh/design-skills/doodle) 기반 — 손으로 그린 듯한 불규칙한 선 + 종이 질감 + 부드러운 그림자. 사주라는 무거운 주제의 진입 장벽을 낮추는 친근한 톤이 목표다.

| 역할 | 토큰 | hex | 흰 배경 대비 |
|---|---|---|---|
| 앱 배경(종이) | `bg-background` | `#FFFFFF` | — |
| 잉크(제목·본문·테두리) | `text-foreground` | `#111827` | 17.74:1 |
| 스케치 잉크(테두리·강조) | `border-border`/`text-accent` | `#263D5B` | 11.05:1 |
| 카드/표면 | `bg-surface` | `#FFFFFF` | — |
| 브랜드 채움(스카이 크레용) | `bg-primary` | `#49B6E5` | 2.31:1 ⚠ |
| 보조 텍스트 | `text-muted-foreground` | `#445A75` | 7.08:1 |
| 상태(성공/경고/위험) | `success`/`warning`/`danger` | `#16a34a`·`#d97706`·`#dc2626` | — |

> ⚠ **대비 규칙 (필수)**: `primary`(#49B6E5)는 흰 배경 대비 2.31:1로 WCAG AA 텍스트(4.5:1)·non-text(3:1) 기준을 **둘 다 미달한다**. 따라서 **채움·장식에만** 쓰고, 텍스트·아이콘 강조·포커스 링·선택 테두리는 반드시 `accent`(#263D5B)를 쓴다. primary 채움 위 텍스트는 `text-primary-foreground`(#111827, 7.69:1) — `text-white`(2.31:1)를 쓰지 말 것.

- **그림자(페이퍼)**: `shadow-card`(0 2px 6px) · `shadow-card-hover`(0 4px 12px) · `shadow-soft`(0 1px 4px). 전부 `rgba(38,61,91,*)` 잉크 계열.
- **형태**: 카드·버튼은 다중값 border-radius(`255px 15px 225px 15px / 15px 225px 15px 255px`)로 손그림 윤곽을 만든다. **컴포넌트에 `rounded-*` 유틸리티를 얹으면 이 형태가 무효화**되므로 주의.
- **공용 헬퍼**: `.glass-card`(손그림 카드) · `.btn-block`(버튼 베이스) · `.block-press`(눌림) · `.sketch-underline`(물결 밑줄).
- **폰트**: `font-sans`(Pretendard, 본문) · `font-display`(Delius Swash Caps 라틴 → Gaegu 한글) · `font-mono`(JetBrains Mono, 숫자·간지). 본문은 긴 사주 해석의 가독성을 위해 Pretendard를 유지한다(Doodle 스펙에서 의도적으로 일탈 — 근거는 [DESIGN.md](../DESIGN.md)).
- **마스코트 "별이"**: `Mascot`/`MascotBubble` — mood(idle/happy/thinking/talking/curious/sleeping)·size(xs~xl) variant.

## 오행 색상 시스템

디자인 토큰은 `tailwind.config.ts` 의 `theme.extend.colors.element` 에 정의되며, 유틸리티(`text-element-*`, `bg-element-*`, `.element-*`)로 사용합니다.

| 오행 | 한자 | 색상 |
|------|------|------|
| 목(木) | 木 | `#16A34A` (Green) |
| 화(火) | 火 | `#DC2626` (Red) |
| 토(土) | 土 | `#D97706` (Amber) |
| 금(金) | 金 | `#64748B` (Slate) |
| 수(水) | 水 | `#2563EB` (Blue) |

> `tailwind.config.ts` 의 `element.*` 토큰과 차트(`lib/constants/elements.ts` 의 `ELEMENT_COLORS.hex`)는 동일한 hex 단일 소스를 사용합니다.

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

Apache License 2.0 — 루트 [LICENSE](../LICENSE) 참조.
