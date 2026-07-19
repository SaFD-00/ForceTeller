# ForceTeller — building with this design system

ForceTeller는 사주명리(만세력) 기반 AI 운세 분석 웹앱이다. 여기 컴포넌트는 앱 `web/components/` 의
**실제 shipped 컴포넌트**(Next.js 14 + Tailwind CSS v3)다 — 재구현이 아니라 실제 export를 렌더한다.

## 스타일링 — Tailwind v3 유틸리티 + 오행 토큰 (Doodle 손그림 톤)
디자인 토큰은 `tailwind.config.ts` 의 `theme.extend` 에 hex로 정의된다(CSS 변수 아님). 새 마크업을
작성할 때는 **컴포넌트가 이미 쓰는 유틸리티 클래스**를 재사용하거나 인라인 스타일을 써라(임의 Tailwind
클래스는 정적 컴파일된 ds-compiled.css에 없을 수 있다).

팔레트(Doodle — 종이 흰 surface + 스카이 크레용 포인트 + 스케치 잉크, 소프트 페이퍼 그림자):

| 역할 | 값 | 유틸리티 | 흰 배경 대비 |
|---|---|---|---|
| 앱 배경(종이) | `#FFFFFF` | `bg-background` | — |
| 본문/잉크 | `#111827` | `text-foreground` | 17.74:1 |
| 스케치 잉크(테두리·강조) | `#263D5B` | `border-border` / `text-accent` / `bg-accent` | 11.05:1 |
| 카드/표면 | `#FFFFFF` | `bg-surface` | — |
| muted 면 | `#EDF4FA` | `bg-muted` | — |
| 주요 채움(스카이 크레용) | `#49B6E5` | `bg-primary` **만** | 2.31:1 ⚠ |
| 보조 텍스트 | `#445A75` | `text-muted-foreground` | 7.08:1 |
| 상태 | `#16a34a`·`#d97706`·`#dc2626` | `success` / `warning` / `danger` | — |
| 그림자(페이퍼) | 0 2px 6px · 0 4px 12px · 0 1px 4px | `shadow-card` / `shadow-card-hover` / `shadow-soft` | — |

> **⚠ 대비 규칙 (필수)**: `primary`(#49B6E5)는 2.31:1로 AA 텍스트(4.5:1)·non-text(3:1)를 **둘 다 미달한다**.
> `text-primary` / `ring-primary` / `border-primary` / `stroke-primary` 를 **쓰지 마라** — 전부 `accent`(#263D5B)를 쓴다.
> primary 채움 위 텍스트는 `text-primary-foreground`(#111827, 7.69:1)이며 `text-white`(2.31:1)를 쓰지 않는다.

**손그림 규칙**: 카드/입력/버튼/뱃지는 `border-[1.5px] border-border` + 소프트 페이퍼 그림자 + 다중값 border-radius
(`255px 15px 225px 15px / 15px 225px 15px 255px`, `.glass-card`·`.btn-block`에 내장).
**`rounded-*` 유틸리티를 얹으면 손그림 윤곽이 무효화**되니 붙이지 마라(Tailwind 유틸리티가 `@layer components`를 이긴다).
hover=미세하게 기울며 커짐(`scale(1.02) rotate(-0.6deg)`), 클릭=`.block-press`(`scale(0.97) rotate(0.5deg)`), focus=`focus-visible:ring-2 ring-accent`.

**타이포**: 한글/본문 Pretendard(`font-sans` — 긴 해석 가독성 위해 손글씨로 바꾸지 않는다),
디스플레이 `font-display`(라틴 Delius Swash Caps → 한글 Gaegu 자동 폴백, **짧은 강조 전용·`font-bold` 금지**),
점수·간지·숫자 JetBrains Mono(`font-mono`).

**마스코트**: 브랜드 캐릭터 `Mascot`("별이", 별·달 점성술사) — 채팅 아바타·로딩·설명봇·로고에 재사용(`MascotBubble` 말풍선 헬퍼). 상세 규칙 `guidelines/03-mascot.md`.

**오행(五行) 색 시스템** — 도메인 핵심:

| 오행 | 한자 | hex | 유틸리티 |
|---|---|---|---|
| 목(木) | 木 | `#16a34a` | `text-element-wood` / `bg-element-wood` / `.element-wood` |
| 화(火) | 火 | `#dc2626` | `text-element-fire` / `.element-fire` |
| 토(土) | 土 | `#ca8a04` | `text-element-earth` / `.element-earth` |
| 금(金) | 金 | `#71717a` | `text-element-metal` / `.element-metal` |
| 수(水) | 水 | `#2563eb` | `text-element-water` / `.element-water` |

공용 클래스: `.glass-card`(블록 카드 — 흰 표면+딥네이비 1.5px 테두리+하드 오프셋 shadow-card, 구
glassmorphism 별칭), `.card-elevated`, `.glass-button`, `.btn-block`(버튼 베이스), `.block-press`(눌림),
`.gradient-text`(퍼플→네이비 그라데이션 텍스트).

## 컴포넌트 구성
- `ui/`: Button, Input, GlassCard, Icon(Iconify Solar), ElementBadge, Disclaimer, GlossaryTooltip/Modal, LoadingOverlay, **Mascot/MascotBubble**("별이").
- `result/`: 사주 결과 시각화 — PillarTable(사주팔자 표), FourPillarsDisplay/PillarCard, FiveElementsChart(오행
  레이더), PentagonChart, TenGodsDistribution, ElementDistribution, StrengthMeter/StrengthDistributionChart(신강·신약),
  FortuneCycleTimeline/FortuneCycleSlider/YearlyFortune/LifetimeReport(대운·세운·평생운), YongshinCard/LuckyGuideCard(용신·개운),
  FortuneScoreDashboard, SchoolComparison(학파 비교), InteractionsTabs(합·충·형·파·해·공망), ShenshaDetailCard(신살).
- `chat/`: AI 상담 — ChatContainer, MessageList, MessageBubble, AgentSelector, ChatInput, SuggestedQuestions.
- `hero/`: HeroSection, BirthInfoForm(생년월일·시간·도시·성별·달력유형 입력). `features/`: FeatureGrid/FeatureCard.

## props 형태의 진실
result/chat 컴포넌트는 대부분 순수 props-driven이다. props 타입은 `web/types/saju.ts`
(SajuResultDisplay, FourPillars, FiveElementsAnalysis, TenGodsDistribution, StrengthAnalysis,
UsefulGodAnalysis, FortuneCycleData, ShenshaData 등). 프리뷰 mock은 realistic 한글 도메인 값으로:
천간 "갑/을/병/…/계", 지지 "자/축/…/해", 오행 "목/화/토/금/수", 십성 "비견/겁재/…/정인".
store 결합 컴포넌트(ChatContainer)는 `stores/sajuStore.ts`(`useSajuStore`/`useChatStore`)를
`cfg.extraEntries`로 공유해 `setState` seed 한다.
