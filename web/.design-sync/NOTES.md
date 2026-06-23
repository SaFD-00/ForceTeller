# ForceTeller web design-sync — repo notes

ForceTeller `web/` 는 DS 패키지가 아니라 **Next.js 14 앱**이다. design-sync는 앱 컴포넌트를
synth-entry로 번들하는 비표준 경로로 동작한다. 아래는 그 경로에서 배운 gotcha.
(레퍼런스: 동일 패턴의 PaperLight `.design-sync` — Next.js 앱 → synth-entry.)

## 빌드 메커니즘 (재현 필수)
- **shape=package, synth-entry 모드**: dist가 없으므로 컨버터가 `components/` 에서 entry를 합성한다.
  `--entry ./dist/index.js` 는 **일부러 존재하지 않는 경로**를 준다 — `PKG_DIR` 을 `web/`(package.json
  보유)로 잡으면서 동시에 synth-entry를 트리거하기 위함. 빌드 로그의 `[NO_DIST]` 2줄은 정상(에러 아님).
- `--node-modules ./node_modules` (monorepo 아님, react 18 여기 있음). `tsconfig: tsconfig.json` 으로
  esbuild가 `@/*` alias(`@/* → ./*`)를 해석한다.
- 첫 빌드 카운트: **42 components** (배럴(`*/index.ts`) 미export 내부 부품 AnalysisButtons /
  ReasoningDisplay / MarkdownRenderer 도 content scan에 포함됨). DS 품질상 제외하려면
  `cfg.componentSrcMap` 에 `{"AnalysisButtons": null, ...}`.

## CSS — Tailwind v3 정적 컴파일 (PaperLight v4와 다름)
- PaperLight는 v4(`@tailwindcss/postcss` + `@theme inline` + `@source`)였지만 ForceTeller는 **v3.4**.
- `.ds-css/compile.mjs` 가 `tailwindcss`(postcss 플러그인, **`@tailwindcss/postcss` 아님**) +
  `tailwind.ds.config.cjs`(content 스캔)로 `app/globals.css` 를 직접 `ds-compiled.css`(~52KB)로 컴파일.
  `cfg.cssEntry = .ds-css/ds-compiled.css`. (입력으로 별도 input.css 미러를 두지 않고 globals.css를
  직접 읽어 드리프트를 제거했다.)
- 디자인 토큰은 CSS 변수가 아니라 **tailwind.config 의 hex 리터럴**(element.wood=#16a34a 등). 그래서
  v4식 `@theme inline` 미러가 불필요 — `tailwind.ds.config.cjs` 의 theme.extend 를 보존하면 모든 커스텀
  유틸(`.element-*`, `.glass-card`, `gradient-text`, `shadow-card`)이 컴파일된다.
- **Re-sync 위험 ①**: `tailwind.config.ts` 의 theme.extend 가 바뀌면 `tailwind.ds.config.cjs` 도
  수동 동기화해야 새 토큰/유틸이 ds-compiled.css에 포함된다.
- **Re-sync 위험 ②**: 컴포넌트 클래스가 바뀌면 `cd web && node .ds-css/compile.mjs` 를 먼저 재실행
  (ds-compiled.css 는 gitignore).

## bundle.mjs override (process shim + next/navigation stub — 둘 다 우리 코드서 트리거)
- 앱 코드(`lib/api/client.ts`, `lib/api/chat.ts` 의 `process.env.NEXT_PUBLIC_API_URL`)와 번들된
  remark/vfile 폴리필이 bare `process` 를 참조 → `ReferenceError: process is not defined` 방지 배너.
- `Sidebar`(usePathname), `BirthInfoForm`(useRouter)이 `next/navigation` 호출 → Next 앱 밖(=모든
  design·프리뷰)에서 "invariant expected app router to be mounted" throw → no-op stub.
- 포크가 bare `esbuild` import → `ln -sfn ../.ds-sync/node_modules .design-sync/node_modules` 심링크
  필요(clone마다 재생성, gitignore). `cfg.libOverrides["bundle.mjs"]` 에 선언됨.

## 폰트 (Pretendard vendor — 2026-06-23부터 ship)
- 앱(`app/layout.tsx`)은 Pretendard를 jsDelivr CDN `<link>` 로 로드(next/font 아님)하지만, claude.ai/design
  렌더엔 그 link가 없어 시스템 폴백 → `[FONT_MISSING]` 경고가 났었다.
- 해결: `orioncactus/pretendard@v1.3.9` variable woff2(2.0MB)를 `.design-sync/fonts/PretendardVariable.woff2`
  로 vendor 하고 `.design-sync/fonts/pretendard.css` 에 `@font-face{font-family:'Pretendard'; …
  src:url('./PretendardVariable.woff2') format('woff2-variations')}` 선언. `cfg.extraFonts` 로 연결 →
  빌드가 woff2를 `fonts/` 로 복사하고 `fonts/fonts.css` 생성, styles.css 클로저에 @import. 이제 디자인이
  Pretendard로 렌더되고 `[FONT_MISSING]` 사라짐.
- ⚠ family 이름은 번들 CSS의 font-sans 스택이 가리키는 **`Pretendard`**(앱 css의 `Pretendard Variable` 아님)
  여야 매칭된다. woff2는 레포에 커밋(extraFonts 소스).

## 토큰 (tokens/) — ds-tokens 로컬 패키지 via 심링크
- copyTokens는 **node_modules 패키지 기반**이라 로컬 파일 직접 지정이 안 된다(`tokensGlob=app/globals.css`만으론
  tokens/가 비었던 원인). 해결: `.design-sync/ds-tokens/{package.json,tokens.css}` 를 만들고
  `ln -sfn ../.design-sync/ds-tokens node_modules/ds-tokens` 심링크(esbuild 심링크와 동일 패턴 — **clone마다
  재생성**, gitignore). `cfg.tokensPkg="ds-tokens"` + `cfg.tokensGlob="*.css"`.
- `tokens.css` 는 `tailwind.config.ts` 의 팔레트를 `--ft-color-*` CSS 변수로 노출(컴포넌트는 미사용, 디자인
  에이전트용 토큰 레퍼런스). **tailwind.config.ts 값 변경 시 tokens.css도 동기화**.

## 가이드라인 (guidelines/)
- `.design-sync/guidelines/*.md`(브랜드·레이아웃, 오행 색 규칙) + `cfg.guidelinesGlob`. 빌드가 guidelines/로
  복사하고 `index.md` 자동 생성. PKG_DIR(=web) 상대경로라 `guidelines/.design-sync/guidelines/<name>.md` 로
  중첩 배치되지만 index 링크는 resolve됨(정상).

## 아이콘
- `@iconify/react` 가 런타임 API로 아이콘을 페치(오프라인 아이콘셋 미설치). headless 캡처에서 아이콘이
  빈 박스로 보일 수 있음 — 실패 아님(benign).

## Re-sync risks (다음 sync가 주의할 것)
- tailwind.ds.config.cjs ↔ tailwind.config.ts 수동 동기화(위 ①).
- **CSS safelist (Re-sync 위험 ③)**: globals.css `@layer components` 의 시맨틱 헬퍼
  `.element-{wood,fire,earth,metal,water}` / `.card-elevated` 는 컴포넌트가 직접 안 써서
  Tailwind purge 로 ds-compiled.css 에서 빠진다. conventions.md 가 디자인 에이전트에 안내하는
  클래스라 `tailwind.ds.config.cjs` 의 `safelist` 로 보존했다. globals.css 에 새 @layer 헬퍼를
  추가하고 컴포넌트가 안 쓰면 동일하게 safelist 에 넣어야 배포 CSS(ds-compiled.css)에 포함된다.
  (참고: `.glass-card`/`.glass-button`/`.gradient-text` 는 컴포넌트가 실제 사용 → safelist 불필요.)
- claude.ai 업로드: **2026-06-23 첫 업로드 완료** — `cfg.projectId = f17c4807-52e8-496c-bf0f-1b58844eea77`
  ("ForceTeller Design System"). 다음 sync 는 pinned → atomic 경로(SKILL §1).
- store-coupled 프리뷰(ChatContainer 등)의 seed 값은 `stores/sajuStore.ts`(SajuResultDisplay/ChatMessage)
  인터페이스에 묶임 — store 형태가 바뀌면 프리뷰 seed도 갱신.

## framer-motion 정적 캡처 (필수 gotcha)
- 다수 컴포넌트가 `motion.*` 에 `initial={{opacity:0}}` 마운트 페이드인을 쓴다. 정적 헤드리스 캡처는
  애니메이션 시작 순간을 찍어 카드가 **투명/빈 박스**로 나온다(처음 PillarTable·MessageBubble이 빈
  박스였던 원인). 해결: `.design-sync/ds-preview-setup.ts` 가 `MotionGlobalConfig.skipAnimations = true`
  를 설정하고 `cfg.extraEntries` 로 번들 entry에 합류 → 번들 내 framer-motion 인스턴스에 적용되어 모든
  motion이 최종 상태로 즉시 렌더. **이 셋업이 없으면 motion 쓰는 모든 카드가 투명**해진다.

## GRID_OVERFLOW (wide 컴포넌트 cardMode)
- result/chat 의 표·차트·리스트형 컴포넌트는 그리드 셀보다 넓어 `[GRID_OVERFLOW]` → `cfg.overrides.<Name>:
  {"cardMode":"column"}` 16개 적용(MessageBubble, AgentSelector, SuggestedQuestions, ElementDistribution,
  FiveElementsChart, FortuneCycleTimeline, FortuneScoreDashboard, FourPillarsDisplay, InteractionsTabs,
  LuckyGuideCard, PentagonChart, SchoolComparison, ShenshaDetailCard, StrengthMeter, TenGodsDistribution,
  YongshinCard). column은 wide로 re-flag 불가하니 재검증 불필요.
- recharts(FiveElementsChart·PentagonChart 일부)는 프리뷰 wrapper를 고정폭/높이로 감싸야 0-height 방지.

## 이번 sync 검증 결과 (로컬, 업로드 전)
- `package-validate` 42/42 previews render cleanly, 경고는 `[FONT_MISSING] Pretendard`(benign — CDN/시스템
  폴백) 1건뿐. **authored 18 / floor 12 / props-renderable 12** (총 42). authored 18종은 contact-sheet로
  시각 확인 결과 스타일·완결성 good(솔로 3종은 `.cache/review/*.grade.json` 에 good 기록, 나머지 15종은
  render check + contact sheet 시각 검증).
- 로컬 산출물: `ds-bundle/.review.html` (헤드리스라 serve 생략 — 사람이 열어볼 진입점).
- **claude.ai 업로드는 미수행** — DesignSync(create_project/finalize_plan/write_files) 호출 안 함, projectId
  미기록. 업로드는 사용자 명시 승인 후 별도 단계(SKILL §5).
