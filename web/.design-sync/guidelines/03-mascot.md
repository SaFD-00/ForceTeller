---
title: 마스코트 "별이" 사용 규칙
category: Guidelines
---

# 마스코트 — 별·달 점성술사 "별이"

ForceTeller의 브랜드 캐릭터. 둥근 **달 얼굴 + 고깔모자 + 별**로 구성된 듀오링고식 마스코트로,
간단한 SVG 블록으로 조립돼 있어 어디서나 가볍게 재사용한다. 운세 안내자 역할 — 친근하되 신비롭게.

컴포넌트: `Mascot`(그리고 말풍선 헬퍼 `MascotBubble`) — `components/ui/Mascot.tsx`.

## Props
- `mood`: `idle` | `happy` | `thinking` | `talking` | `curious` | `sleeping` (표정)
- `size`: `xs`(28) | `sm`(38) | `md`(52) | `lg`(76) | `xl`(120)  — px
- `floating`: 살랑 떠다니는 모션(선택). design-sync 정적 캡처에선 `skipAnimations` 로 정지 렌더.
- `className`, `title`(접근성 라벨)

## 표정별 용도
| mood | 쓰는 곳 |
|---|---|
| `talking` | 채팅 어시스턴트 아바타(`MessageBubble`), 스트리밍 응답 |
| `happy` | 히어로 일러스트, 채팅 빈상태 인사 |
| `thinking` | 로딩(`LoadingOverlay`), 답변 생성 대기 |
| `curious` | 설명봇(`GlossaryTooltip`/`GlossaryModal`) 헤더 |
| `idle` | 사이드바 로고, 일반 브랜딩 |
| `sleeping` | 비활성/세션 종료 등(드묾) |

## 색
딥네이비 윤곽 `#1c202b`, 고깔모자 비비드 퍼플 `#7107e7`, 별 옐로우 `#ffd23f`, 달 얼굴 흰색.
색은 컴포넌트에 hex로 박혀 앱과 design-sync 헤드리스 렌더에서 동일하게 보인다(토큰 변수 의존 X).

## Do / Don't
- **Do** 아바타·빈상태·로딩·설명·로고 등 "안내자"가 필요한 곳에 쓴다.
- **Do** 크기는 맥락에 맞게(아바타 `sm`, 히어로/로딩 `xl`, 툴팁 `xs`).
- **Don't** 한 화면에 과하게 반복하지 않는다(주의 분산).
- **Don't** SVG 내부 색/비율을 임의 변형하지 않는다 — variant(mood/size)로만 제어.
- **Don't** 데이터 시각화(오행 차트 등)에 장식으로 끼워넣지 않는다.
