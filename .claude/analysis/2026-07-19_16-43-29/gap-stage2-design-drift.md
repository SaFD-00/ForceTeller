# Stage: design-drift — 디자인 시스템의 드리프트 내성

## Question
디자인 시스템이 구조적으로 드리프트에 견디는가? 다음에 조용히 깨질 지점은 어디인가?

## Evidence

| Source | Why it matters | Check |
|--------|----------------|-------|
| `web/tailwind.config.ts` (107줄) | 미러 #1, 선언된 토큰 SSOT | 전문 |
| `web/.ds-css/tailwind.ds.config.cjs` (86줄) | 미러 #2, design-sync 프리뷰 컴파일 | 전문 |
| `web/.design-sync/ds-tokens/tokens.css` (69줄) | 미러 #3, 디자인 에이전트용 CSS 변수 | 전문 |
| `web/app/globals.css` (175줄) | 손그림 radius·`.block-card`·`font-display` 가드의 실제 위치 | 전문 |
| `web/.eslintrc.json` (3줄) | 기계적 강제의 유일한 후보 | `{"extends":["next/core-web-vitals"]}` |
| `web/lib/utils.ts` | `cn = twMerge(clsx(...))` — `rounded-*` 오버라이드 가능성 | 6줄 |

## Findings

| Finding | Verdict | Evidence | Scope |
|---------|---------|----------|-------|
| **규칙 위반 4종 스윕이 전부 0건.** primary 텍스트/링/보더 0, 손그림 카드+`rounded-*` 0, `font-display`+bold 0, 원색 텍스트 노드 0. 규율이 실제로 지켜지고 있다 | `confirmed` | 4개 grep 전수 | cross-file |
| **그러나 기계적으로 강제되는 규칙은 2개뿐이다.** `globals.css:21-23`의 `font-display{font-weight:400 !important}`와 `tailwind.config.ts:103`의 `boxShadowColor:false`. 나머지(primary 채움 전용, ink 규칙, `rounded-*` 금지, 3중 미러 일치)는 **전부 산문에만 존재**한다. ESLint는 stock `next/core-web-vitals`이고 Tailwind plugin 0개, 토큰 테스트 0개 | `confirmed` | `.eslintrc.json:2`; `tailwind.config.ts:104`; `tailwind.ds.config.cjs:85`; 테스트 grep 결과 도메인 데이터만 | architectural |
| **실패 모드가 이미 한 번 발생했다: `animation-delay-200`/`400`이 어디에도 정의되지 않은 채 출하 중이다.** lint·tsc·build·CI를 전부 통과했다. "생각 중" 점 3개가 엇갈리지 않고 동시에 뛴다. 같은 파일의 `MessageList.tsx:112-114`는 인라인 `style`로 올바르게 구현했다 | `confirmed` | `ReasoningDisplay.tsx:51-52`; `globals.css` 전문에 해당 규칙 없음 | single-case |
| **미러 #3(`tokens.css`)에 11개 키가 누락됐다.** `success/warning/danger/info.foreground` 4개, `borderRadius` 6단계 전체, `borderWidth.3`. 존재하는 값은 전부 일치한다 | `confirmed` | `tailwind.config.ts:42-45,70-83` ↔ `tokens.css:9-69` | cross-file |
| **미러 #3은 앱에 소비자가 없어 드리프트해도 시각적 증상이 없다.** 오직 디자인 에이전트만 오도한다. 과거 `#ca8a04`/`#71717a` 드리프트가 살아남은 경로가 정확히 이것이다 | `confirmed` | `tokens.css:4-6`(자체 선언); `NOTES.md:73-75` | architectural |
| **미러 #1 ↔ #2는 일치한다.** 차이는 전부 의도적이고 주석돼 있다(폰트 리터럴, content 글롭, safelist) | `confirmed` | `tailwind.config.ts:14-94` ↔ `tailwind.ds.config.cjs:32-79`; 근거 주석 `:56` | cross-file |
| **자동 동기화 장치가 없다.** `package.json:5-11`에 sync/compile 스크립트 없음, `compile.mjs`는 수동, CI는 디자인 자산을 건드리지 않는다. `NOTES.md`가 스스로 "수동 동기화"·"Re-sync 위험 ①"로 기록 | `confirmed` | `package.json:5-11`, `ci.yml:43-74`, `NOTES.md:26-29,87` | architectural |
| **`cn()` + `.block-card`는 열린 드리프트 벡터다.** `twMerge`는 `.glass-card`가 `border-radius`를 설정한다는 걸 모른다. `<GlassCard className="rounded-xl">`을 쓰면 유틸리티가 뒤에 붙고, 유틸리티는 `@layer components`를 이긴다 — 손그림 윤곽이 **에러도 lint도 테스트도 없이** 죽는다. 현재 0건이지만 첫 발생을 막는 것이 없다 | `confirmed` | `lib/utils.ts:5`; `GlassCard.tsx:15-19` | architectural |
| **7곳이 카드 레시피를 손으로 재구현하고 있다** — `rounded-xl`/`lg` + `border-[1.5px] border-border` + `shadow-card`. 시각적으로는 손그림 윤곽 없는 Doodle 카드이고 `.block-card`를 우회하므로 향후 `.block-card` 변경에 보이지 않는다. 규칙 (b) 스윕은 클래스명이 없어 계속 "0건"을 반환한다 | `confirmed` | `BirthInfoForm.tsx:224`, `ReasoningDisplay.tsx:38`, `ElementDistribution.tsx:166`, `GlossaryTooltip.tsx:151`, `LoadingOverlay.tsx:27`, `YearlyFortune.tsx:45`, `result/page.tsx:499` | architectural |
| **손그림 radius 리터럴이 4곳에 중복**돼 있고 `tokens.css:63`에 미소비 사본이 1개 더 있다. `globals.css`는 `--ft-radius-doodle`을 참조하지 않는다. 한 곳만 어긋나면 보이지 않는다 | `confirmed` | `globals.css:53,65,81,91`; `tokens.css:63` | architectural |
| **죽은 토큰 다수.** `borderWidth['1.5']`는 사용 0인데 `border-[1.5px]`가 **50곳/26파일**에서 쓰인다. 그 외 `shadow-soft`·`shadow-block`·`shadow-block-lg`·`border-3`·`rounded-3xl`·`bg-card`·`text-info-ink`·`*-accent-foreground` 전부 소비 0 | `confirmed` | `tailwind.config.ts:36-39,78,81-82,90-93`; grep 50/26 | cross-file |
| **`TEN_GOD_COLORS` 10 hex는 토큰 표현이 전혀 없다.** `ElementDistribution.tsx:51-57`의 모듈 로컬 const라 디자인 에이전트가 볼 수도 재사용할 수도 없다 | `confirmed` | `ElementDistribution.tsx:51-57,321,370` | single-case |
| **오행 hex는 전 계층 일치.** `elements.ts` ↔ 두 Tailwind config ↔ `tokens.css` — 과거 드리프트는 복구됨 | `confirmed` | `elements.ts:8,14,20,26,32` ↔ `tailwind.config.ts:49-53` ↔ `tokens.css:35-39` | cross-file |
| **content 글롭 부류의 버그가 현재는 없으나 구조적으로 무방비다.** `stores/`·`types/`가 세 config의 글롭 밖에 있다(현재 클래스 문자열 0건). 미래에 그곳에 클래스 맵을 두면 과거 `lib/` 누락이 조용히 재발한다 | `confirmed` | `tailwind.config.ts:7-11`; `stores/`·`types/` grep 0건 | architectural |
| **`ds-compiled.css`는 gitignore된 수동 재생성 산출물**로 design-sync 전용이며 Next 빌드와 무관하다 | `confirmed` | `.gitignore:35`; `compile.mjs:17-27`; `NOTES.md:20-22` | architectural |

## Risks / Ambiguities

**시스템은 현재 깨끗하지만 구조적으로 무방비다.** 4종 스윕 0건은 실제 규율의 결과이지 방어의 결과가 아니다. "다음에 조용히 깨질" 순서:

1. `cn()` + `.block-card` — 첫 `rounded-*` 오버라이드가 손그림 윤곽을 무성으로 죽인다.
2. 손으로 재구현한 7곳 — 신규 기여자가 복사하면 경쟁 패턴이 번지고, 규칙 (b) 스윕은 계속 0건을 반환한다.
3. `tokens.css` 단방향 드리프트 — 소비자가 없어 증상이 없고, 이미 11개 키가 어긋나 있다.
4. `ds-compiled.css` 기본 stale — CI에도 npm script에도 없다.
5. `animation-delay-*` — 이 실패 모드가 이론이 아니라 이미 일어났다는 증거.

**미해결 질문**: 손으로 재구현한 7곳이 의도적인가(작은 표면에서 손그림 흔들림이 안 어울려서) 아니면 드리프트인가. `globals.css:44-45`는 `.block-card`가 표준임을 시사하나 예외를 명시한 문서가 없다 → `needs-user-input`.

## Next Local Checks

1. **토큰 패리티 vitest 추가** — `tailwind.config.ts`·`tokens.css`·`tailwind.ds.config.cjs`의 키 집합과 값 동등성을 단언. 11개 누락과 과거 오행 드리프트를 전부 잡았을 것이고, 기존 `npm test` CI 스텝에 신규 인프라 없이 들어간다. **가장 레버리지가 높다.**
2. `eslint-plugin-tailwindcss`의 `no-custom-classname` — `animation-delay-200`을 잡았을 것이다.
3. grep 기반 CI 가드 2줄: `(text|ring|border)-primary(?!-foreground)`와 손그림 카드+`rounded-*` 동시 출현.
4. 손으로 재구현한 7곳 결정 — `.block-card`로 전환하거나 `.block-card-sm` 변종을 문서화해 예외를 명명 가능하게.
5. `globals.css`의 radius 리터럴 4개를 `var(--ft-radius-doodle)`로 치환하고 변수를 `@layer base`로 이동 → `tokens.css:63`이 5번째 사본이 아니라 진짜 미러가 된다.
