---
title: ForceTeller — 브랜드 & 레이아웃 가이드
category: Guidelines
---

# ForceTeller 브랜드 & 레이아웃 가이드

ForceTeller는 사주명리(만세력) 기반 AI 운세 분석 웹앱이다. 디자인은 **Doodle 손그림 톤**을
기준으로 한다 — 손으로 그린 듯한 불규칙한 선 + 종이 질감 + 부드러운 그림자.
사주라는 낯설고 무거운 주제의 **진입 장벽을 낮추는 친근함**이 목표이며, 동시에 분석 도구다운
**정확함**을 잃지 않도록 데이터·차트 영역은 정렬과 여백을 엄격히 지킨다.

## 톤 & 보이스
- **자신감 있고 명료하게.** 라벨은 직설적으로, 군더더기 없이. 게임처럼 또렷하되 가볍지 않게.
- 운세/점술이지만 데이터·시각화 중심의 **분석 도구**로 보이게 한다.
- 한자(五行·十神 등) 도메인 용어는 한글 병기. 예: `목(木)`, `정관(正官)`.
- 결과는 단정적 예언이 아니라 해석으로 제시 — `Disclaimer` 컴포넌트를 결과 화면 하단에 둔다.
- 브랜드 마스코트 **별이**(별·달 점성술사)가 안내자 역할: 채팅·설명·로딩에서 친근하게 거든다(→ `03-mascot.md`).

## 색 사용 (Doodle 팔레트)
- 앱 배경 `bg-background`(#FFFFFF 종이), 카드/표면 `bg-surface`(#FFFFFF) + `shadow-card`(소프트 페이퍼 그림자).
- 잉크(제목·본문)는 `text-foreground`(#111827, 17.74:1). 스케치 잉크(테두리·강조)는 `border-border`/`text-accent`(#263D5B, 11.05:1). 보조 텍스트 `text-muted-foreground`(#445A75, 7.08:1).
- **⚠ primary는 채움 전용이다.** `bg-primary`(#49B6E5 스카이 크레용)는 흰 배경 대비 **2.31:1**로 WCAG AA 텍스트(4.5:1)·non-text(3:1) 기준을 **둘 다 미달한다**. 따라서:
  - 텍스트·아이콘 강조·포커스 링·선택 테두리 → 반드시 `accent`(#263D5B)를 쓴다. `text-primary`/`ring-primary`/`border-primary`를 쓰지 마라.
  - primary 채움 위 텍스트 → `text-primary-foreground`(#111827, 7.69:1). `text-white`(2.31:1)를 쓰지 마라.
- 상태색: `success`(#16a34a) · `warning`(#d97706) · `danger`(#dc2626).
- 오행 색(목/화/토/금/수)은 **도메인 데이터 인코딩 전용** — 일반 UI 강조에 쓰지 말 것(자세히는 `02-oheng-color-system.md`). 디자인 테마가 바뀌어도 이 색은 고정이다.

## 손그림 스타일 규칙
- **형태**: 카드·버튼은 다중값 border-radius(`255px 15px 225px 15px / 15px 225px 15px 255px`)로 손으로 그린 윤곽을 만든다. `.glass-card`·`.btn-block`에 내장돼 있다.
  - **⚠ 컴포넌트에 `rounded-*` 유틸리티를 얹으면 이 형태가 무효화된다** — Tailwind 유틸리티가 `@layer components`를 이긴다. 손그림 윤곽을 원하면 `rounded-*`를 붙이지 마라.
- **그림자**: 소프트 페이퍼 그림자 — `shadow-card`(0 2px 6px), `shadow-card-hover`(0 4px 12px), `shadow-soft`(0 1px 4px). 전부 `rgba(38,61,91,*)` 잉크 계열. 하드 오프셋 솔리드 그림자는 쓰지 않는다.
- **테두리**: 카드·입력·버튼·뱃지는 `border-[1.5px] border-border`(스케치 잉크). divider도 동일 색.
- **인터랙션**: hover 시 미세하게 기울며 커짐(`scale(1.02) rotate(-0.6deg)`), 클릭 시 눌림(`.block-press` → `scale(0.97) rotate(0.5deg)`). focus는 `focus-visible:ring-2 ring-accent` 로 항상 가시.
- 공용 헬퍼: `.glass-card`(손그림 카드), `.card-elevated`, `.glass-button`, `.btn-block`(버튼 베이스), `.block-press`(눌림), `.sketch-underline`(물결 밑줄 — h1·h2 시그니처).

## 레이아웃
- 앱 셸: 좌측 `Sidebar`(데스크톱 고정, `lg:pl-16`, 로고는 마스코트) + 우측 본문. 모바일은 사이드바 collapse.
- 입력 흐름: `HeroSection`(마스코트 + 워드마크) → `BirthInfoForm`(생년월일·시·성별) → 결과.
- 결과 화면은 **카드 그리드**. 표·차트·리스트형(예: `PillarTable`, `FiveElementsChart`, `TenGodsDistribution`)은 폭이 넓으니 1열(풀폭) 카드로 배치한다.
- 카드는 `GlassCard`(=`.glass-card`)를 기본 컨테이너로 사용.

## 타이포
- 본문/한글: **Pretendard**(`font-sans`). 번들에 woff2 포함 → 디자인에서도 Pretendard 로 렌더.
  긴 사주 해석 텍스트의 가독성을 위해 본문은 손글씨로 바꾸지 않는다 — Doodle 스펙(body=Delius Swash Caps)에서 **의도적으로 일탈**한 지점이며 근거는 루트 `DESIGN.md`에 기록돼 있다.
- 디스플레이(`font-display`): 라틴은 **Delius Swash Caps**(예: `FORCETELLER`), 한글은 **Gaegu**(손글씨). 폰트 체인이 자동으로 갈라진다 — Delius에는 한글 글리프가 없어 Gaegu로 폴백된다.
  - 짧은 강조(로고·제목·큰 숫자)에만 쓴다. **본문·장문에는 쓰지 마라.**
  - 두 서체 모두 단일 웨이트(400)라 `font-bold`를 겹치면 브라우저 합성 볼드가 한글 속공간을 메워 뭉갠다. `globals.css`의 `.font-display { font-weight: 400 !important }` 가드가 이를 막고 있으니 제거하지 마라.
- 점수·간지(한자)·숫자·날짜: **JetBrains Mono**(`font-mono`). 데이터의 또렷함을 강조.
- 한글 본문 헤딩은 Pretendard `font-bold`, 장문은 `leading-relaxed`.

## 컴포넌트 선택 빠른 가이드
- 액션 버튼 → `Button`, 입력 → `Input`, 컨테이너 → `GlassCard`.
- 마스코트 → `Mascot`/`MascotBubble`, 용어 설명 → `GlossaryTooltip`/`GlossaryModal`(설명봇 별이 동반), 아이콘 → `Icon`(Iconify Solar 세트).
- 로딩 → `LoadingOverlay`(별이 등장). 채팅형 해석 → `chat/` 그룹(`ChatContainer`, `MessageBubble` 등).
