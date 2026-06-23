---
title: ForceTeller — 브랜드 & 레이아웃 가이드
category: Guidelines
---

# ForceTeller 브랜드 & 레이아웃 가이드

ForceTeller는 사주명리(만세력) 기반 AI 운세 분석 웹앱이다. 디자인은 **라이트 미니멀**
톤(흰 배경 + 바이올렛 포인트, FigureLabs 스타일)을 기준으로 한다.

## 톤 & 보이스
- **신뢰감 있되 가볍지 않게.** 운세/점술이지만 데이터·시각화 중심의 분석 도구로 보이게 한다.
- 한자(五行·十神 등) 도메인 용어는 한글 병기. 예: `목(木)`, `정관(正官)`.
- 결과는 단정적 예언이 아니라 해석으로 제시 — `Disclaimer` 컴포넌트를 결과 화면 하단에 둔다.

## 색 사용
- 기본 배경은 `bg-background`(#f7f8fa), 카드/표면은 `bg-surface`(#ffffff) + `shadow-card`.
- 액션·강조는 `bg-primary`/`text-primary`(바이올렛 #7c3aed) 하나로 통일. 보조 강조만 `accent`.
- 오행 색(목/화/토/금/수)은 **도메인 데이터 인코딩 전용** — 일반 UI 강조에 쓰지 말 것
  (자세한 규칙은 `02-oheng-color-system.md`).
- 본문 `text-foreground`(#111827), 보조 텍스트 `text-muted-foreground`(#6b7280).

## 레이아웃
- 앱 셸: 좌측 `Sidebar`(데스크톱 고정, `lg:pl-16`) + 우측 본문. 모바일은 사이드바 collapse.
- 입력 흐름: `HeroSection` → `BirthInfoForm`(생년월일·시·성별) → 결과.
- 결과 화면은 **카드 그리드**로 구성. 표·차트·리스트형(예: `PillarTable`, `FiveElementsChart`,
  `TenGodsDistribution`)은 폭이 넓으니 1열(풀폭) 카드로 배치한다.
- 카드는 `GlassCard`(=`.glass-card`: 흰 표면 + 옅은 테두리 + `shadow-card`)를 기본 컨테이너로 사용.

## 타이포
- 폰트는 **Pretendard**(`font-sans`). 번들에 woff2 가 포함되어 디자인에서도 Pretendard 로 렌더된다.
- 숫자·점수 강조는 굵게(`font-bold`/`font-semibold`) + 큰 사이즈. 한글 장문은 `leading-relaxed`.

## 컴포넌트 선택 빠른 가이드
- 액션 버튼 → `Button`, 입력 → `Input`, 컨테이너 → `GlassCard`.
- 용어 설명 → `GlossaryTooltip`/`GlossaryModal`, 아이콘 → `Icon`(Iconify Solar 세트).
- 로딩 → `LoadingOverlay`. 채팅형 해석 → `chat/` 그룹(`ChatContainer`, `MessageBubble` 등).
