---
title: 오행(五行) 색 시스템 사용 규칙
category: Guidelines
---

# 오행(五行) 색 시스템

ForceTeller의 핵심 도메인 시각 언어. 오행 색은 **데이터 인코딩 전용**이다 — 어떤 요소가 어떤
오행(목·화·토·금·수)에 속하는지를 색으로 나타낸다. 일반 UI 강조(버튼·링크 등)에는 쓰지 말 것
(그건 `primary` 바이올렛의 몫).

## 팔레트

| 오행 | 한자 | hex | 유틸리티 | 토큰 |
|---|---|---|---|---|
| 목 | 木 | `#16a34a` | `text-element-wood` / `bg-element-wood` / `.element-wood` | `--ft-color-element-wood` |
| 화 | 火 | `#dc2626` | `text-element-fire` / `bg-element-fire` / `.element-fire` | `--ft-color-element-fire` |
| 토 | 土 | `#ca8a04` | `text-element-earth` / `bg-element-earth` / `.element-earth` | `--ft-color-element-earth` |
| 금 | 金 | `#71717a` | `text-element-metal` / `bg-element-metal` / `.element-metal` | `--ft-color-element-metal` |
| 수 | 水 | `#2563eb` | `text-element-water` / `bg-element-water` / `.element-water` | `--ft-color-element-water` |

## 사용법
- **단일 오행 뱃지/라벨**: `.element-wood` 등 시맨틱 단축 클래스를 쓴다(배경 10% + 텍스트 + 테두리 30%가
  한 번에 적용됨). 예: `<span class="element-water px-2 py-0.5 rounded">수(水)</span>`. 전용 컴포넌트는
  `ElementBadge`.
- **세분 제어**가 필요하면 유틸리티를 조합: `text-element-fire`, `bg-element-fire/10`,
  `border-element-fire/30`.
- **차트/분포**(`FiveElementsChart`, `ElementDistribution`, `PentagonChart`)는 위 5색을 계열로 매핑.
  같은 화면에서 오행→색 매핑은 항상 동일하게 유지(일관성).

## 접근성
- 금(金) `#71717a` 은 회색 계열이라 흰 배경에서 대비가 낮다 — 작은 텍스트엔 `bg-element-metal/10`
  배경 + 진한 텍스트 조합으로 가독성을 확보한다.
- 색만으로 오행을 구분하지 말고 항상 라벨(한자/한글)을 동반한다(색각 이상 대응).
