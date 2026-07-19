# Solutions — 우선순위 fix / 후속 작업

**이 문서는 제안이다. 현재 상태가 아니다.** 현재 상태는 `_current-vs-baseline.md`에 있다.

우선순위 기준: **사용자에게 지금 해를 끼치는 것 > 회귀를 자동 재유입시키는 것 > 다음에 조용히 깨질 것 > 정리**

---

## S-1 — design-sync 문서가 접근성 회귀를 재유입시킨다 `[stage:docs-drift]` — P1

`web/.design-sync/guidelines/02-oheng-color-system.md`가 `text-element-fire`·`border-element-fire/30`·"테두리 50%"를 권장하고 ink 언급이 **0건**이다. 오행 토·금 hex도 낡았다(`#ca8a04`/`#71717a`). 이 문서의 독자는 **사람이 아니라 디자인 에이전트**다.

**왜 P1인가**: 방금 4라운드에 걸쳐 고친 접근성 회귀를 다음 디자인 작업이 자동으로 되돌린다. 다른 어떤 항목보다 파급이 빠르다. 그리고 `NOTES.md:73-75`가 같은 드리프트를 이미 인지하고 `tokens.css`만 고쳤다는 사실이 이것이 **반복되는 실패 모드**임을 보여준다.

- `guidelines/02` 전면 개정: ink 토큰(`text-element-*-ink`), `border-border` 규칙, "테두리 50%"·`border-element-*/30` 삭제, "primary 바이올렛"→"스카이"
- `conventions.md:46-47`, `guidelines/02:18-19,33`의 토·금 hex 정정
- `README.md:493`·`conventions.md:50`의 "하드 오프셋"→"소프트"

**Honest ceiling**: 문서를 고쳐도 **강제 장치는 여전히 없다**. 다음 드리프트를 막으려면 S-4의 토큰 패리티 테스트가 필요하다. 이 항목은 지금 있는 지뢰를 제거할 뿐 재발을 막지 못한다.

---

## S-2 — 채팅 표면의 사용자 직격 결함 `[stage:a11y-reach]` — P1

3개 라우트 중 2개에 렌더되는 채팅 서브트리가 이니셔티브를 하나도 받지 못했다.

| 결함 | 위치 | 사용자 영향 |
|------|------|------------|
| 로딩 점이 `bg-muted` on `bg-muted` (1:1) | `MessageList.tsx:110-114` | **스트림 대기 중 빈 말풍선만 보인다** — 앱이 멈춘 것처럼 보임 |
| `aria-live` 0건 | repo 전역 | 스트리밍 답변·reasoning·에러가 스크린리더에 **전혀** 전달 안 됨 |
| textarea에 접근 가능한 이름 없음 | `ChatInput.tsx:50-59` | 같은 저장소 `Input.tsx:19-25`는 제대로 하고 있어 패턴이 갈림 |
| 추천 질문 버튼 포커스 표시 없음 | `MessageBubble.tsx:87-95` | 형제 `SuggestedQuestions.tsx:41`에는 있음 |

**왜 P1인가**: 로딩 점은 시각 사용자 전원에게 지금 영향을 준다. `aria-live` 부재는 제품의 핵심 인터랙션을 스크린리더 사용자에게 통째로 차단한다.

**Honest ceiling**: 이 수정들은 코드 읽기에 근거한다 — `/chat`의 populated 상태를 아무도 렌더한 적이 없다. **고치기 전에 먼저 렌더해서 확인해야 한다.** 특히 `aria-live` 배치는 스트리밍 중 과도한 낭독(매 토큰마다 재낭독)을 피하는 설계가 필요해 `polite` + 적절한 원자성 선택이 실측을 요구한다.

---

## S-3 — 계약을 안 따르는 오버레이 2개 `[stage:a11y-reach]` — P2

`GlossaryModal`에 확립한 계약(portal+inert+트랩+Escape)을 나머지 두 오버레이가 따르지 않는다.

- `LoadingOverlay.tsx:25` (홈) — `fixed inset-0`만 있고 role·aria·portal·트랩 전부 없음. 뒤 폼이 Tab으로 도달 가능
- `result/page.tsx:509-540` (모바일 채팅) — 동일. **"검증된 페이지"에 있으면서 `isMobile` 게이트라 데스크톱 실측을 빠져나갔다**

`useFocusTrap`이 이미 있으므로 재사용이 가능하다. `LoadingOverlay`는 `role="status"`+`aria-live="polite"`도 필요하다(로딩 알림).

**Honest ceiling**: `LoadingOverlay`는 사용자 조작이 불가능한 대기 화면이라 포커스 트랩의 가치가 모달보다 낮다 — `inert`+`role="status"`만으로 충분할 수 있다. 모바일 오버레이는 실제 모달이라 전체 계약이 필요하다. **둘을 같은 강도로 다루지 말 것.**

---

## S-4 — 디자인 규칙의 기계적 강제 `[stage:design-drift]` — P2

현재 기계적으로 강제되는 규칙은 **2개뿐**이다(`font-display` weight 핀, `boxShadowColor:false`). primary 채움 전용·ink·`rounded-*` 금지·3중 미러 일치는 전부 산문이다.

이 실패 모드는 **이미 발생했다**: `animation-delay-200`/`400`이 정의되지 않은 채 lint·tsc·build·CI를 전부 통과해 출하 중이다(`ReasoningDisplay.tsx:51-52`).

레버리지 순:

1. **토큰 패리티 vitest** — 세 config의 키 집합·값 동등성 단언. 현재 누락된 11개 키와 과거 오행 드리프트를 전부 잡았을 것이고, 기존 `npm test` CI 스텝에 **신규 인프라 없이** 들어간다
2. `eslint-plugin-tailwindcss`의 `no-custom-classname` — `animation-delay-*`를 잡는다
3. grep 기반 CI 가드 2줄 — `(text|ring|border)-primary(?!-foreground)`, 손그림 카드+`rounded-*` 동시 출현

**Honest ceiling**: 토큰 패리티 테스트는 **값 일치만** 검증한다. "primary를 텍스트에 쓰지 마라" 같은 의미론적 규칙은 여전히 grep 수준이고, 합성 알파 대비는 어떤 정적 검사로도 못 잡는다 — 그건 S-5의 브라우저 하네스 영역이다.

---

## S-5 — a11y 하네스를 저장소에 편입 `[stage:test-gate]` — P2

CI는 존재하고 프론트 4게이트를 전부 돌린다. 그런데 **판별력을 가졌던 것은 CI에 없다** — `GlossaryModal`을 되돌리면 P1 4건, 툴팁 리스너를 빼면 P2 2건이 FAIL했는데 tsc·lint·test·build 중 무엇도 그 revert를 잡지 못한다.

필요한 결정(전부 미해결):

- `@playwright/test`를 실제 devDependency로 → `npm ci`에 브라우저 다운로드 추가
- fixture 위치 — `web/e2e/fixtures/saju-result.json`을 **백엔드 골든(`test_manseol_regression.py:19-27`)과 같은 입력**에서 파생시켜 두 골든이 갈라지지 않게
- CI 브라우저 — 세션은 `channel:'chrome'`을 썼으나 `ubuntu-latest`에 없다 → 번들 chromium
- 런타임 — 하네스가 `build && start`를 요구하므로 `ci.yml:72` 빌드 재사용 여부
- flake 정책 — 초기엔 mypy처럼 `continue-on-error` 스테이징
- **`A11Y_SELFTEST=1` 변이 모드를 CI 스텝으로 보존** — 하네스가 공허하게 통과하지 않음을 증명하는 유일한 장치

**Honest ceiling**: 비용이 실질적이다(브라우저 다운로드, 두 번째 프로덕션 빌드, flake 리스크). 더 싼 부분 승리가 있다 — `jsdom`+`@testing-library/react`를 넣으면 `useFocusTrap`의 Tab 순환 계약이 브라우저 없이 CI에서 단위 테스트된다. **대비와 `inert` 레이아웃은 못 잡으므로 하네스를 대체하지 않고 보완한다.**

---

## S-6 — 문서의 구조 드리프트 정리 `[stage:docs-drift]` — P3

- 존재하지 않는 컴포넌트 6종을 4개 문서가 나열(`conventions.md:56-59` 등). **`types/saju.ts`의 동명 타입은 보존할 것** — `TenGodsDistribution`은 타입으로는 실재한다
- 고아 프리뷰 5개가 사라진 export를 import(`previews/`) — 이건 문서가 아니라 코드 이슈
- BottomNav·MotionProvider·`lib/hooks/`가 구조 문서에 전무
- `guidelines/01:38`의 "사이드바 collapse" → 실제는 숨김+BottomNav 대체

**Honest ceiling**: 고아 프리뷰가 design-sync 빌드를 실제로 깨뜨리는지는 빌드를 돌려야 확정된다. import 대상 부재만 확정이다.

---

## S-7 — reduced-motion 커버리지 `[stage:a11y-reach]` — P3

`MotionProvider`의 `reducedMotion="user"`는 framer-motion만 덮고 Tailwind `animate-spin`/`bounce`/`pulse` 7곳을 못 덮는다. `globals.css`에 `@media (prefers-reduced-motion)` 블록이 없다.

**Honest ceiling**: 무한 opacity 펄스는 0.8~2.4s 주기로 3Hz 발작 임계 한참 아래다 — **WCAG 2.3.1 실패가 아니라 편의성 문제**다. P1으로 취급하면 실제 위험을 과장하는 것이다.

---

## S-8 — 게이트 재현성 `[stage:test-gate]` — P3

- 집계 스크립트 없음 — 5개 명령을 따로 쳐야 하고 CI 정의와 로컬 정의가 드리프트할 수 있다. `"gate": "..."` 하나를 만들고 CI가 그걸 호출하게 하면 원천 차단
- `node .ds-css/compile.mjs`가 npm script·CI 어디에도 없다 — 산문에만 존재
- `next lint`에 `--max-warnings=0`이 없어 jsx-a11y 6개 규칙이 경고만 내고 통과할 가능성 (**확인 필요**)
- pre-commit hook 전무

---

## 다음 실험 제안 (현재 결과 아님)

1. `/chat` populated 상태를 프로덕션 빌드로 렌더해 S-2 결함 4건을 실측 — 고치기 전 필수
2. `/result`를 <1024px로 열어 모바일 오버레이 실측 (S-3)
3. `Icon` 렌더 DOM 확인으로 Iconify `aria-hidden` 기본 동작 확정 — 어느 쪽이든 결함이지만 **어느 쪽인지 모르면 고칠 방향이 정해지지 않는다**
4. 키보드만으로 도시 자동완성 Tab 이동 — 200ms `onBlur` 트랩이 실제로 포커스를 `<body>`로 떨어뜨리는지
5. OS 동작 줄이기 켜고 framer는 멈추고 CSS는 도는 분기 확인 (S-7)
