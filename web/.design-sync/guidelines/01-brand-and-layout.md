---
title: ForceTeller — 브랜드 & 레이아웃 가이드
category: Guidelines
---

# ForceTeller 브랜드 & 레이아웃 가이드

ForceTeller는 사주명리(만세력) 기반 AI 운세 분석 웹앱이다. 디자인은 **tetris-refined 블록 톤**을
기준으로 한다 — 고대비 비비드 컬러 블록 + 하드 오프셋(솔리드) 그림자 + 컴팩트한 게임감.
단, 운세/분석 도구다운 **신뢰감**을 위해 모서리는 살짝 둥글리고(8~12px) 테두리는 1.5px로 절제한다.

## 톤 & 보이스
- **자신감 있고 명료하게.** 라벨은 직설적으로, 군더더기 없이. 게임처럼 또렷하되 가볍지 않게.
- 운세/점술이지만 데이터·시각화 중심의 **분석 도구**로 보이게 한다.
- 한자(五行·十神 등) 도메인 용어는 한글 병기. 예: `목(木)`, `정관(正官)`.
- 결과는 단정적 예언이 아니라 해석으로 제시 — `Disclaimer` 컴포넌트를 결과 화면 하단에 둔다.
- 브랜드 마스코트 **별이**(별·달 점성술사)가 안내자 역할: 채팅·설명·로딩에서 친근하게 거든다(→ `03-mascot.md`).

## 색 사용 (tetris-refined 팔레트)
- 앱 배경 `bg-background`(#dfe7ff 쿨블루), 카드/표면 `bg-surface`(#ffffff) + `shadow-card`(하드 오프셋).
- 잉크(제목·본문·테두리)는 딥네이비 `text-foreground`/`border-border`(#1c202b). 보조 텍스트 `text-muted-foreground`(#54608a).
- 액션·브랜드 강조는 **비비드 퍼플** `bg-primary`/`text-primary`(#7107e7) 하나로 통일. 보조 강조·링크·차트 보조는 `accent`(#1c398e 네이비블루).
- 상태색: `success`(#16a34a) · `warning`(#d97706) · `danger`(#dc2626).
- 오행 색(목/화/토/금/수)은 **도메인 데이터 인코딩 전용** — 일반 UI 강조에 쓰지 말 것(자세히는 `02-oheng-color-system.md`).

## 블록 스타일 규칙
- **그림자**: 카드·버튼·패널은 하드 오프셋 솔리드 그림자 — `shadow-card`(3px 3px 0), `shadow-card-hover`(5px 5px 0), `shadow-block-sm`(2px 2px 0). 블러 그림자는 쓰지 않는다.
- **테두리**: 카드·입력·버튼·뱃지는 `border-[1.5px] border-border`(딥네이비). divider도 동일 색.
- **라운드**: 카드 `rounded-xl`, 칩/뱃지 `rounded-lg`, 진짜 원형(점·일부 아바타)만 `rounded-full`.
- **인터랙션**: hover 시 살짝 들림(`hover:-translate-x-px hover:-translate-y-px hover:shadow-card-hover`), 클릭 시 눌림(`.block-press` → active에서 그림자 쪽으로 밀려들어감). focus는 `focus-visible:ring-2 ring-primary` 로 항상 가시.
- 공용 헬퍼: `.glass-card`(블록 카드), `.card-elevated`, `.glass-button`, `.btn-block`(버튼 베이스), `.block-press`(눌림), `.gradient-text`(퍼플→네이비).

## 레이아웃
- 앱 셸: 좌측 `Sidebar`(데스크톱 고정, `lg:pl-16`, 로고는 마스코트) + 우측 본문. 모바일은 사이드바 collapse.
- 입력 흐름: `HeroSection`(마스코트 + 워드마크) → `BirthInfoForm`(생년월일·시·성별) → 결과.
- 결과 화면은 **카드 그리드**. 표·차트·리스트형(예: `PillarTable`, `FiveElementsChart`, `TenGodsDistribution`)은 폭이 넓으니 1열(풀폭) 카드로 배치한다.
- 카드는 `GlassCard`(=`.glass-card`)를 기본 컨테이너로 사용.

## 타이포
- 본문/한글: **Pretendard**(`font-sans`). 번들에 woff2 포함 → 디자인에서도 Pretendard 로 렌더.
- 라틴 워드마크/대형 헤딩: **Bangers**(`font-display`). 예: `FORCETELLER`. (라틴 전용 — 한글엔 쓰지 말 것)
- 점수·간지(한자)·숫자·날짜: **JetBrains Mono**(`font-mono`). 데이터의 또렷함을 강조.
- 한글 헤딩은 Pretendard `font-bold`, 장문은 `leading-relaxed`.

## 컴포넌트 선택 빠른 가이드
- 액션 버튼 → `Button`, 입력 → `Input`, 컨테이너 → `GlassCard`.
- 마스코트 → `Mascot`/`MascotBubble`, 용어 설명 → `GlossaryTooltip`/`GlossaryModal`(설명봇 별이 동반), 아이콘 → `Icon`(Iconify Solar 세트).
- 로딩 → `LoadingOverlay`(별이 등장). 채팅형 해석 → `chat/` 그룹(`ChatContainer`, `MessageBubble` 등).
