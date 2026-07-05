---
name: Tetris
colors:
  primary: "#1C202B"
  secondary: "#7107E7"
  success: "#16A34A"
  warning: "#D97706"
  danger: "#DC2626"
  surface: "#DFE7FF"
  text: "#1C398E"
  neutral: "#DFE7FF"
typography:
  h1:
    fontFamily: "Bangers"
    fontSize: 3rem
  body-md:
    fontFamily: "Bangers"
    fontSize: 1rem
  label-caps:
    fontFamily: "JetBrains Mono"
    fontSize: 0.75rem
  sourceScale: "desktop-first expressive scale"
  weights: "100, 200, 300, 400, 500, 600, 700, 800, 900"
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 4px
  md: 8px
  sourceScale: "compact density mode"
---

## 앱 토큰 매핑 주의

이 파일은 `npx typeui.sh pull tetris --format design` 원본 스펙 덤프다(위 frontmatter는 원본 그대로 보존). 앱(`web/tailwind.config.ts`)은 스펙 색을 **역할 재배치**해 사용하므로, 토큰 이름을 스펙과 1:1로 대응시키지 말 것:

- 스펙 `secondary`(#7107E7 비비드 퍼플) → 앱 `primary` (브랜드 강조)
- 스펙 `primary`(#1C202B 딥네이비) → 앱 `foreground`/`border` (잉크·테두리)
- 스펙 `text`(#1C398E 네이비블루) → 앱 `accent`
- 스펙 `surface`(#DFE7FF 쿨블루) → 앱 `background` (카드 surface는 `#FFFFFF`)

실제 적용 토큰 표는 `web/README.md`의 "디자인 시스템" 섹션 참조.

## Overview

Classic block-game inspired design with playful colors, bold display fonts, and compact, high-energy layouts.

## Style Foundations

- **Visual style:** high-contrast, playful, premium
- **Typography scale:** desktop-first expressive scale
- **Typography fonts:** primary=Bangers, display=Bangers, mono=JetBrains Mono
- **Typography weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- **Color palette:** primary, secondary, success, warning, danger, info
- **Spacing scale:** compact density mode

## Colors

- **Primary (#1C202B):** Token from style foundations.
- **Secondary (#7107E7):** Token from style foundations.
- **Success (#16A34A):** Token from style foundations.
- **Warning (#D97706):** Token from style foundations.
- **Danger (#DC2626):** Token from style foundations.
- **Surface (#DFE7FF):** Token from style foundations.
- **Text (#1C398E):** Token from style foundations.
- **Neutral (#DFE7FF):** Derived from the surface token for official format compatibility.
