---
title: 오행(五行) 색 시스템 사용 규칙
category: Guidelines
---

# 오행(五行) 색 시스템

ForceTeller의 핵심 도메인 시각 언어. 오행 색은 **데이터 인코딩 전용**이다 — 어떤 요소가 어떤
오행(목·화·토·금·수)에 속하는지를 색으로 나타낸다. 일반 UI 강조(버튼·링크 등)에는 쓰지 말 것.
UI 강조는 채움 전용 `primary`(`bg-primary`)나 텍스트·포커스링용 `accent`(`text-accent`/
`ring-accent`)의 몫이다 — 자세히는 `01-brand-and-layout.md`.

## 팔레트

각 오행은 **DEFAULT**(600급 원색, non-text 전용)와 **ink**(텍스트 전용 파생) 두 톤을 가진다.
DEFAULT는 채움·보더·차트·아이콘에, ink는 텍스트에 쓴다 — 원색을 텍스트에 직접 쓰면 흰/옅은
배경에서 대비가 부족하다.

| 오행 | 한자 | hex (DEFAULT) | ink (텍스트 전용) | 유틸리티 | 토큰 |
|---|---|---|---|---|---|
| 목 | 木 | `#16a34a` | `#166534` | `text-element-wood-ink` / `bg-element-wood` / `.element-wood` | `--ft-color-element-wood` |
| 화 | 火 | `#dc2626` | `#991b1b` | `text-element-fire-ink` / `bg-element-fire` / `.element-fire` | `--ft-color-element-fire` |
| 토 | 土 | `#d97706` | `#92400e` | `text-element-earth-ink` / `bg-element-earth` / `.element-earth` | `--ft-color-element-earth` |
| 금 | 金 | `#64748b` | `#475569` | `text-element-metal-ink` / `bg-element-metal` / `.element-metal` | `--ft-color-element-metal` |
| 수 | 水 | `#2563eb` | `#1e40af` | `text-element-water-ink` / `bg-element-water` / `.element-water` | `--ft-color-element-water` |

DEFAULT hex는 도메인 SSOT(`web/lib/constants/elements.ts` `ELEMENT_COLORS.hex`)와 항상 일치해야
한다. 목(木)=`success`, 토(土)=`warning`, 화(火)=`danger`와 hue가 같아 상태색과도 정합된다.

## 사용법
- **단일 오행 뱃지/라벨**: `.element-wood` 등 시맨틱 단축 클래스를 쓴다. 실제 구현(`globals.css`
  `@layer components`)은 `bg-element-wood/15 text-element-wood-ink border-border`다 — 배경 15%
  틴트 + **ink 텍스트** + **잉크(스케치 네이비) 테두리**가 한 번에 적용된다(오행 원색 테두리가
  아니다). 블록 톤이므로 `rounded-lg`(원형 pill 대신)에 `border-[1.5px]`로 감싼다.
  예: `<span class="element-water px-2 py-0.5 rounded-lg border-[1.5px]">수(水)</span>`. 전용 컴포넌트는
  `ElementBadge`.
- **세분 제어**가 필요하면 유틸리티를 조합: 배경 틴트는 `bg-element-fire/10`~`/20`, 텍스트는 항상
  `text-element-fire-ink`. **테두리는 항상 `border-border`를 쓴다** — 오행 원색에 반투명도만 준
  테두리(예: 화 계열 옅은 테두리)는 non-text 대비 기준 3:1에 못 미쳐 금지다.
- **차트/분포**(`PentagonChart`, `ElementDistribution`)는 위 5색을 계열로 매핑. 같은 화면에서
  오행→색 매핑은 항상 동일하게 유지(일관성).

## 접근성
- **텍스트에는 DEFAULT(600급) 원색을 직접 쓰지 않는다** — 항상 `*-ink` 파생(`text-element-*-ink`)을
  쓴다. 특히 금(金) `#64748b`는 슬레이트 계열이라 흰 배경 대비가 낮으므로 텍스트는 반드시
  `text-element-metal-ink`(`#475569`)를 쓴다.
- 색만으로 오행을 구분하지 말고 항상 라벨(한자/한글)을 동반한다(색각 이상 대응).
