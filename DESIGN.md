---
name: Doodle
colors:
  primary: "#49B6E5"
  secondary: "#263D5B"
  success: "#16A34A"
  warning: "#D97706"
  danger: "#DC2626"
  surface: "#FFFFFF"
  text: "#111827"
  neutral: "#FFFFFF"
typography:
  h1:
    fontFamily: "Delius Swash Caps"
    fontSize: 2.5rem
  body-md:
    fontFamily: "Delius Swash Caps"
    fontSize: 1rem
  label-caps:
    fontFamily: "JetBrains Mono"
    fontSize: 0.875rem
  sourceScale: "14/16/18/24/32/40"
  weights: "100, 200, 300, 400, 500, 600, 700, 800, 900"
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 4px
  md: 8px
  sourceScale: "4/8/12/16/24/32"
---

## Overview

Hand-drawn, sketch-like style with doodles, handwritten fonts, and imperfect lines for a playful, informal feel.

## Style Foundations

- **Visual style:** playful
- **Typography scale:** 14/16/18/24/32/40
- **Typography fonts:** primary=Delius Swash Caps, display=Delius Swash Caps, mono=JetBrains Mono
- **Typography weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- **Color palette:** primary, secondary, neutral, success, warning, danger
- **Spacing scale:** 4/8/12/16/24/32

## Colors

- **Primary (#49B6E5):** Token from style foundations.
- **Secondary (#263D5B):** Token from style foundations.
- **Success (#16A34A):** Token from style foundations.
- **Warning (#D97706):** Token from style foundations.
- **Danger (#DC2626):** Token from style foundations.
- **Surface (#FFFFFF):** Token from style foundations.
- **Text (#111827):** Token from style foundations.
- **Neutral (#FFFFFF):** Derived from the surface token for official format compatibility.

## 앱 토큰 매핑 (ForceTeller 적용 규칙)

> 위 front-matter 는 typeui.sh Doodle 원본(SSOT)이며 **raw pull 로 통째로 덮어써진다**.
> 이 섹션은 그 원본을 `web/tailwind.config.ts` 에 적용할 때의 파생 규칙이다 — pull 후 유실되면 복원할 것.

### 파생 토큰 유도

원본에 없는 앱 토큰은 아래 근거로 파생한다.

| 앱 토큰 | 값 | 유도 근거 |
| --- | --- | --- |
| `background` / `surface` / `card` | `#FFFFFF` | 원본 surface·neutral 이 모두 백색 — 스케치북 종이 |
| `foreground` / `card.foreground` | `#111827` | 원본 text |
| `border` | `#263D5B` | 원본 secondary. 손그림 선은 잉크색이어야 하고, 백색 대비 11.0:1 로 non-text AA(3:1) 충족 |
| `accent` | `#263D5B` / fg `#FFFFFF` | 원본 secondary. primary 가 대비 미달이라 **텍스트·링 역할을 accent 가 흡수** |
| `muted` | `#EDF4FA` | primary 를 백색에 얹은 저채도 워시(스카이 톤 유지) |
| `muted.foreground` | `#445A75` | border 를 밝기만 올린 값. 백색 대비 **7.1:1** 로 AA 본문(4.5:1) 여유 충족 |
| `info` | `#2563EB` | 원본에 없음 — 도메인 소스(오행 水)를 그대로 유지 |

`rounded` sm=4 / md=8, `spacing` 4/8/12/16/24/32 는 원본 그대로. 손그림 느낌의 불규칙 모서리는
radius 토큰이 아니라 `globals.css` 의 `.block-card` / `.btn-block` 이
`border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px` (순수 CSS hand-drawn 트릭)으로 낸다 —
**신규 런타임 의존성(rough.js 등)은 도입하지 않는다.**

### ⚠ primary 대비 제약 — "채움 = primary / 텍스트·링 = accent"

Doodle primary `#49B6E5` 는 흰 배경 대비 **2.31:1** 로 WCAG 2.2 AA 의 텍스트 기준(4.5:1)과
non-text/UI 기준(3:1) 을 **모두 탈락**한다. 앱은 `text-primary` / `ring-primary` / `border-primary` 를
27개 파일 78곳에서 쓰므로 그대로 두면 접근성이 광범위하게 깨진다. 따라서 다음을 규칙으로 고정한다.

- **채움·장식에만 primary**: `bg-primary`, 채워진 배지/칩, 차트 계열색, 일러스트 면적, 알파 워시.
- **텍스트·아이콘 강조·포커스 링·선택 보더는 accent(`#263D5B`, 11.0:1)**: `text-accent`, `ring-accent`,
  `border-accent`, `focus-visible:ring-accent`.
- `primary.foreground` 는 **`#111827`(잉크)이며 white 가 아니다** — `#49B6E5` 위 white 는 2.3:1 로 탈락하고,
  잉크는 4.5:1 이상을 확보한다. 이 값을 white 로 되돌리지 말 것.
- 접근성 기준선: **WCAG 2.2 AA, keyboard-first, 항상 보이는 focus state**(`.focus-ring` = accent 2px + offset).

### 원색 텍스트 금지 — ink 파생 토큰

오행·상태 원색(600급 hex)은 채움·보더·차트·아이콘 등 **non-text 전용**이다 — 텍스트는 항상
같은 계열의 `*-ink` 토큰(틴트·muted 포함 전 배경 조합 4.5:1 실측 보증)을 쓴다.
칩·배지 윤곽선은 잉크(`border-border`)이며 원색 `/50` 보더(1.75~2.29:1)는 금지.
ink 는 도메인 값이 아니라 표현 파생값이다 — 도메인 SSOT(`elements.ts` `ELEMENT_COLORS.hex`)는 불변.
(wood #166534 / fire #991B1B / earth #92400E / metal #475569 / water #1E40AF,
 success·warning·danger·info 는 동일 hue 미러.)

### 오행(五行) 색 보존

`element.{wood,fire,earth,metal,water}` 는 **리디자인 대상이 아니다.** 오행 색은 브랜드 장식이 아니라
사주 도메인의 의미 체계이며 SSOT 는 `web/lib/constants/elements.ts` 의 `ELEMENT_COLORS.hex` 다.
마침 Doodle 의 success/warning/danger 와 wood/fire/earth 의 hex 가 일치해 팔레트 충돌도 없다.
(wood `#16A34A` = success, fire `#DC2626` = danger, earth `#D97706` = warning, metal `#64748B`,
water `#2563EB` = info.) 토큰 미러가 어긋나면 항상 `elements.ts` 쪽으로 맞춘다.

### 십성(十星) 무채 램프

십성 도넛·범례는 오행과 별도로 무채(slate) 램프 10 hex 를 쓴다 — 오행처럼 도메인 색이 있는 게 아니라
"음양 쌍 = 명암 밴드" 규칙으로 유도한 값이다. SSOT 는 `web/components/result/ElementDistribution.tsx` 의
`TEN_GOD_COLORS`(코드가 원본, 여기는 설명):

```
비견 #748BAF · 겁재 #637DA6   (비겁 밴드, 최명)
식신 #43587B · 상관 #3A4D6C   (식상 밴드, 중)
편재 #1E293B · 정재 #131A25   (재성 밴드, 최암)
편관 #57709A · 정관 #4D648B   (관성 밴드, 명중)
편인 #31425C · 정인 #28364C   (인성 밴드, 암중)
```

배정 규칙: 쌍(자기 지지 십성 5쌍)마다 하나의 명암 밴드를 배정하고, 밴드 안에서 **양간이 밝은 쪽**을 쓴다.
백색 대비 최저 3.47:1(비견) ~ 최고 17.47:1(정재)으로 전 구간 non-text AA(3:1) 이상을 확보했고,
`element-metal #64748B`(오행 금)과 정확히 겹치던 구 값은 이번 램프에서 제거해 두 도넛의 색이 충돌하지 않는다.

### 폰트 체인 — 본문 Pretendard 유지는 문서화된 의도적 일탈

| 역할 | 스택 | 로드 |
| --- | --- | --- |
| `font-sans` (본문) | `Pretendard` → system | jsDelivr `<link>` |
| `font-display` (제목) | `var(--font-display-latin)`(Delius Swash Caps) → `Gaegu` → `Pretendard` | next/font + Google `<link>` |
| `font-mono` (간지·수치) | `JetBrains Mono` | next/font |

- **원본 body-md 는 Delius Swash Caps 지만 본문에 적용하지 않는다.** Delius 에는 한글 글리프가 없고,
  이 앱의 본문은 수백~수천 자의 사주 해석 텍스트다. 원본 스펙은 라틴 본문을 전제한 값이라 한글 앱에
  그대로 적용할 수 없다 — 가독성을 우선해 본문은 Pretendard 를 유지하는 **의도적 일탈**이다.
  손글씨 톤은 제목·워드마크·큰 숫자 등 `font-display` 짧은 요소가 담당한다.
- **한글 디스플레이로 Gaegu 를 선택한 이유**: 한글 손글씨 후보 3종 중 유일하게 다중 웨이트(300/400/700)를
  제공하고, 획이 가장 단정해 제목 크기에서 가독성이 가장 좋다. Delius 와 톤도 어긋나지 않는다.
- Gaegu 는 next/font/google 이 latin subset 만 노출해 번들할 수 없어 `<head>` 의 Google Fonts `<link>` 로
  로드한다(로드 실패 시 Pretendard 로 자연 폴백). 같은 이유로 `.design-sync/fonts/` 에도 vendor 하지 않는다.
- **weight 400 가드 유지**: Delius 는 단일 웨이트라 `font-bold` 를 겹치면 브라우저 합성 볼드가 밀도 높은
  한글 글리프의 속공간을 메워 뭉갠다. `globals.css` 의 `.font-display { font-weight: 400 !important }` 가드를
  제거하지 말 것.

### 토큰 4-소스 동기화

값을 바꾸면 네 곳을 함께 고친다: `web/tailwind.config.ts`(SSOT) ↔ `web/app/globals.css`(형태 계층) ↔
`web/.ds-css/tailwind.ds.config.cjs`(design-sync 컴파일) ↔ `web/.design-sync/ds-tokens/tokens.css`(토큰 레퍼런스).
동기화 규약과 gotcha 는 `web/.design-sync/NOTES.md`.
