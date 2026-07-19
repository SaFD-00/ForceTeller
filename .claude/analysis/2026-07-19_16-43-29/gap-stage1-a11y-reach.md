# Stage: a11y-reach — 접근성 이니셔티브의 실제 도달 범위

## Question
4라운드에 걸친 접근성 작업이 실제로 어디까지 닿았고, 어디가 검증되지 않은 채 남았는가?

## Evidence

| Source | Why it matters | Check |
|--------|----------------|-------|
| `web/app/**/*.tsx` | 라우트가 3개뿐 — 미검증 표면이 열거 가능한 크기 | glob |
| `useFocusTrap` 소비자 추적 | 이니셔티브가 닿은 범위의 실측 | `GlossaryModal.tsx:79` 단 1곳 |
| `GlossaryModal` importer 5곳 | 전부 `components/result/` | grep |
| repo 전역 `aria-live\|role="status"\|sr-only` | 라이브 리전 존재 여부 | **0건** |
| repo 전역 `prefers-reduced-motion` | CSS 애니메이션의 모션 설정 존중 여부 | **0건** |
| `MessageList.tsx:110-114` | 로딩 점 색상 | 컨테이너·점 모두 `bg-muted` |
| `Icon.tsx:6-21` | props 계약 | rest spread 없음 |

## Findings

| Finding | Verdict | Evidence | Scope |
|---------|---------|----------|-------|
| **이니셔티브 전체가 `/result` 하위 컴포넌트에만 착지했다.** `useFocusTrap`·`GlossaryModal`·`GlossaryTooltip`·`PentagonChart`·도넛 범례 모두 `components/result/*`가 유일한 소비자다. 채팅 서브트리는 3개 라우트 중 2개에 렌더되는데 아무것도 받지 못했다 | `confirmed` | `useFocusTrap` 소비자 = `GlossaryModal.tsx:79`; `GlossaryModal` importer 5곳 전부 `components/result/` | architectural |
| **채팅 로딩 점이 완전히 보이지 않는다.** 컨테이너(`:110`)가 `bg-muted`, 점 3개(`:112-114`)도 `bg-muted`(`#EDF4FA`) — 대비 1:1. 스트림 시작 전 대기 동안 사용자는 빈 말풍선만 본다 | `confirmed` | `MessageList.tsx:110-114`; `tailwind.config.ts:33` | cross-page |
| **`aria-live`가 repo 전체에 0건 — 스트리밍 AI 답변이 스크린리더에 전혀 전달되지 않는다.** 제품의 핵심 인터랙션(토큰 단위 응답)이 무음이고, `reasoning`도, `ChatContainer.tsx:158-163`이 밀어넣는 에러 메시지도 마찬가지다 | `confirmed` | grep 0건; `MessageList.tsx:59-119`; `ChatContainer.tsx:158` | cross-page |
| **`Icon`이 `aria-label`을 조용히 버린다.** `IconProps`에 rest spread가 없어 호출자가 넘긴 `aria-label`이 DOM에 도달하지 못한다. TypeScript는 하이픈 JSX 속성의 초과 프로퍼티 검사를 건너뛰므로 컴파일 에러도 없다. 두 하이드레이션 스피너가 이름 없이 렌더된다 | `confirmed` | `Icon.tsx:6-21`; 유실 지점 `chat/page.tsx:21`, `result/page.tsx:78` | architectural |
| **오버레이가 3개인데 계약을 따르는 건 1개다.** `LoadingOverlay`(홈, `:25`)는 portal·inert·트랩·Escape·`role="status"` 전부 없어 뒤의 폼이 Tab으로 도달 가능하다. `/result`의 모바일 채팅 오버레이(`:509`)도 동일 | `confirmed` | `LoadingOverlay.tsx:25`; `result/page.tsx:509-540` | architectural |
| **모바일 오버레이는 "검증된 페이지"에 있으면서 검증을 빠져나갔다.** `isMobile` 게이트라 데스크톱 1280×1000 실측에서 마운트된 적이 없다 | `confirmed` | `result/page.tsx:54-68,509` | single-case |
| **`MotionProvider`는 framer-motion만 덮는다.** `reducedMotion="user"`는 Tailwind `animate-spin`/`bounce`/`pulse`에 영향을 줄 수 없고 `globals.css`에 `@media (prefers-reduced-motion)` 블록이 없다. 우회 지점 7곳 | `confirmed` | `MotionProvider.tsx:12`; `BirthInfoForm.tsx:227,315`, `Button.tsx:39`, `MessageList.tsx:112-114`, `ReasoningDisplay.tsx:33`, `chat/page.tsx:20`, `result/page.tsx:77,91` | architectural |
| **채팅 textarea에 접근 가능한 이름이 없다.** placeholder만 있고 label·`aria-label` 없음. 같은 저장소의 `Input.tsx:19-25`는 `htmlFor`/`id`를 제대로 연결하고 있어 패턴이 갈린다 | `confirmed` | `ChatInput.tsx:50-59` vs `Input.tsx:19-25` | cross-page |
| **도시 자동완성이 콤보박스가 아니고 키보드에 적대적이다.** `role="combobox"/"listbox"/"option"` 없음, `aria-expanded` 없음, 화살표 내비 없음. 더 나쁜 것은 `onBlur`가 200ms 타이머로 드롭다운을 닫아, 입력에서 옵션으로 Tab하면 이동 도중 옵션이 언마운트되고 포커스가 `<body>`로 떨어진다. 이것이 앱의 **유일한 데이터 입력 경로**다 | `confirmed` (거동은 타이밍 의존이라 실측 필요) | `BirthInfoForm.tsx:201-255`, 특히 `:217-220,237-246` | single-case (고트래픽) |
| **말풍선 안 추천 질문 버튼에 포커스 표시가 없다.** 형제 구현 `SuggestedQuestions.tsx:41`에는 있어 두 경로가 갈린다 | `confirmed` | `MessageBubble.tsx:87-95` vs `SuggestedQuestions.tsx:41` | cross-page |
| **skip link 없음.** 모든 라우트가 사이드바/내비 랜드마크로 시작한다 | `confirmed` | `sr-only` 0건; `layout.tsx:60-69` | architectural |
| 무한 opacity 펄스가 `reducedMotion="user"`를 살아남는다(framer는 transform만 끈다). 0.8~2.4s 주기라 3Hz 발작 임계 아래 — WCAG 2.3.1 실패가 아니라 편의성 문제 | `plausible` | `Mascot.tsx:190`, `MessageList.tsx:93-95`, `ReasoningDisplay.tsx:46-47,68-70` | cross-page |
| `role="button"` 오용·키보드 없는 `onClick`·`<img>` alt 누락은 **없다**. `GlossaryTooltip.tsx:128-137`은 `role`+`tabIndex`+`onKeyDown`을 올바로 짝지었다 | `confirmed` | grep 5줄 전수 확인 | architectural |

## Risks / Ambiguities

- **`/chat`의 populated 상태를 아무도 렌더한 적이 없다.** 위 채팅 관련 findings 전부가 코드 읽기 기반이다. 세 분기(`!hasHydrated`, `!result`, populated) 중 결함이 사는 곳은 populated인데 그게 미검증이다.
- **`@iconify/react`의 기본 `aria-hidden` 동작 미확인.** 기본으로 붙인다면 스피너는 완전 은닉(더 나쁨), 안 붙인다면 앱 전역 장식 아이콘이 전부 이름 없는 그래픽으로 읽힌다. 어느 쪽이든 결함이나 어느 쪽인지 미정.
- **합성 알파 대비를 계산하지 않았다.** `bg-muted` on `bg-muted`만 색 동일성으로 확정했다.
- `components/result/*` 13개를 전문 읽지 않았다 — 검증된 표면이라 import만 추적했다.

## Next Local Checks

1. `/chat`을 mock `result` + 정지된 스트림으로 렌더 → 로딩 말풍선이 실제로 비어 보이는지 확인.
2. `/result`를 <1024px 뷰포트로 열고 모바일 채팅 오버레이에서 Tab → 뒤 콘텐츠로 포커스가 새는지, Escape가 무반응인지 확인.
3. 홈에서 폼 제출 후 `LoadingOverlay` 중 Tab → 뒤 폼이 도달 가능한지 확인.
4. OS "동작 줄이기" 켜고 `/`·`/chat` 로드 → Mascot은 멈추고 `animate-spin`은 계속 도는 분기가 `MotionProvider` 공백의 구체적 증거.
5. 키보드만으로 도시 입력에 "서" 입력 후 Tab → 옵션에 안착하는지 `<body>`로 떨어지는지.
6. `Icon` 렌더 DOM 확인으로 Iconify `aria-hidden` 질문 해소.
