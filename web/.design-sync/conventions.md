# ForceTeller — building with this design system

ForceTeller는 사주명리(만세력) 기반 AI 운세 분석 웹앱이다. 여기 컴포넌트는 앱 `web/components/` 의
**실제 shipped 컴포넌트**(Next.js 14 + Tailwind CSS v3)다 — 재구현이 아니라 실제 export를 렌더한다.

## 스타일링 — Tailwind v3 유틸리티 + 오행 토큰
디자인 토큰은 `tailwind.config.ts` 의 `theme.extend` 에 hex로 정의된다(CSS 변수 아님). 새 마크업을
작성할 때는 **컴포넌트가 이미 쓰는 유틸리티 클래스**를 재사용하거나 인라인 스타일을 써라(임의 Tailwind
클래스는 정적 컴파일된 ds-compiled.css에 없을 수 있다).

팔레트(라이트 미니멀 — FigureLabs 스타일, 흰 배경 + 바이올렛 포인트):

| 역할 | 값 | 유틸리티 |
|---|---|---|
| 앱 배경 | `#f7f8fa` | `bg-background` |
| 본문 텍스트 | `#111827` | `text-foreground` |
| 카드/표면 | `#ffffff` | `bg-surface` |
| 테두리 | `#e5e7eb` | `border-border` |
| 주요(바이올렛) | `#7c3aed` | `bg-primary` / `text-primary` |
| 보조 텍스트 | `#6b7280` | `text-muted-foreground` |
| 그림자 | — | `shadow-card` / `shadow-card-hover` / `shadow-soft` |

**오행(五行) 색 시스템** — 도메인 핵심:

| 오행 | 한자 | hex | 유틸리티 |
|---|---|---|---|
| 목(木) | 木 | `#16a34a` | `text-element-wood` / `bg-element-wood` / `.element-wood` |
| 화(火) | 火 | `#dc2626` | `text-element-fire` / `.element-fire` |
| 토(土) | 土 | `#ca8a04` | `text-element-earth` / `.element-earth` |
| 금(金) | 金 | `#71717a` | `text-element-metal` / `.element-metal` |
| 수(水) | 水 | `#2563eb` | `text-element-water` / `.element-water` |

공용 클래스: `.glass-card`(라이트 카드 — 흰 표면+옅은 테두리+shadow-card, 구 glassmorphism 별칭이지만
실제는 라이트), `.card-elevated`, `.glass-button`, `.gradient-text`(바이올렛 그라데이션 텍스트). 폰트는
Pretendard(한글).

## 컴포넌트 구성
- `ui/`: Button, Input, GlassCard, Icon(Iconify Solar), ElementBadge, Disclaimer, GlossaryTooltip/Modal, LoadingOverlay.
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
