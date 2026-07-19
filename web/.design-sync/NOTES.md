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
- **디스플레이/모노 폰트 추가 vendor**: `DeliusSwashCaps-Regular.woff2`(font-display),
  `JetBrainsMono-Regular.woff2`/`JetBrainsMono-Bold.woff2`(font-mono) 를 같은 `fonts/` 에 두고 동일
  `pretendard.css` 에 `@font-face`(라틴 전용 서브셋, Google Fonts) 선언 → extraFonts 가 셋 다 복사한다.
  family 이름 `Delius Swash Caps` / `JetBrains Mono` 가 tailwind font-display/font-mono 스택과 매칭.
  (Doodle 리디자인 전에는 `Bangers-Regular.woff2` 였다 — 파일 삭제 + @font-face 교체 완료.)
- **한글 디스플레이(Gaegu)는 vendor 하지 않는다**: 앱은 `<head>` 의 Google Fonts `<link>` 로 Gaegu 를
  로드하지만, 한글 웹폰트는 css2 가 ~100개 유니코드 서브셋 woff2 로 쪼개 배포해 단일 파일 vendor 가
  불가능하다. 기존 "한글은 Pretendard 만" 패턴을 그대로 유지 — design-sync 프리뷰의 한글은 Pretendard 로
  렌더되고 이는 `[FONT_MISSING]` 이 아니라 의도된 폴백이다.

## 토큰 (tokens/) — ds-tokens 로컬 패키지 via 심링크
- copyTokens는 **node_modules 패키지 기반**이라 로컬 파일 직접 지정이 안 된다(`tokensGlob=app/globals.css`만으론
  tokens/가 비었던 원인). 해결: `.design-sync/ds-tokens/{package.json,tokens.css}` 를 만들고
  `ln -sfn ../.design-sync/ds-tokens node_modules/ds-tokens` 심링크(esbuild 심링크와 동일 패턴 — **clone마다
  재생성**, gitignore). `cfg.tokensPkg="ds-tokens"` + `cfg.tokensGlob="*.css"`.
- `tokens.css` 는 `tailwind.config.ts` 의 팔레트를 `--ft-color-*`/`--ft-shadow-*`/`--ft-font-*` CSS 변수로 노출
  (컴포넌트는 미사용, 디자인 에이전트용 토큰 레퍼런스). **tailwind.config.ts 값 변경 시 tokens.css도 동기화**.
- **2026 Doodle 팔레트**(tetris-refined 대체): background/surface `#ffffff`(종이), foreground `#111827`,
  border/accent `#263d5b`(스케치 잉크), primary `#49b6e5`(스카이 크레용), muted `#edf4fa`/`#445a75`.
  그림자는 소프트 블러(card `0 2px 6px rgba(38,61,91,.12)`, card-hover `0 4px 12px …/.18`,
  soft/block-sm `0 1px 4px …/.10`) — **이름은 tetris 별칭을 보존**해 소비처 24파일이 무수정 전파된다.
- ⚠ **primary 대비 함정**: `#49b6e5` 는 백색 대비 **2.31:1** 로 AA 텍스트(4.5)·non-text(3) 모두 탈락.
  규칙은 "**채움·장식 = primary / 텍스트·아이콘강조·포커스링·선택보더 = accent(#263d5b, 11.0:1)**"이며
  `--ft-color-primary-foreground` 가 white 가 아닌 `#111827` 인 이유도 이것이다(DESIGN.md 앱 토큰 매핑).
- **드리프트 정정(2026 Doodle)**: tokens.css 의 element-earth `#ca8a04`→`#d97706`,
  element-metal `#71717a`→`#64748b` 로 수정 — SSOT 는 `lib/constants/elements.ts` ELEMENT_COLORS.hex 이고
  tailwind.config.ts 는 처음부터 올바른 값이었다(tokens.css 만 어긋나 있었음).

## 가이드라인 (guidelines/)
- `.design-sync/guidelines/*.md`(01 브랜드·레이아웃, 02 오행 색, **03 마스코트 "별이"**) + `cfg.guidelinesGlob`.
  빌드가 guidelines/로 복사하고 `index.md` 자동 생성. PKG_DIR(=web) 상대경로라
  `guidelines/.design-sync/guidelines/<name>.md` 로 중첩 배치되지만 index 링크는 resolve됨(정상).

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
  (참고: `.glass-card`/`.glass-button`/`.gradient-text`/`.btn-block`/`.block-press` 는 컴포넌트가 실제 사용하지만,
  안전하게 `.card-elevated`·`.element-*`·`.btn-block`·`.block-press` 를 safelist 에 보존했다.)
  Doodle 신규 유틸 `.sketch-underline`(손그림 물결 밑줄)도 아직 컴포넌트 미사용이라 safelist 에 추가했다.
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
  {"cardMode":"column"}` 적용(Mascot 추가 포함 17개: Mascot, MessageBubble, AgentSelector, SuggestedQuestions,
  ElementDistribution, FiveElementsChart, FortuneCycleTimeline, FortuneScoreDashboard, FourPillarsDisplay,
  InteractionsTabs, LuckyGuideCard, PentagonChart, SchoolComparison, ShenshaDetailCard, StrengthMeter,
  TenGodsDistribution, YongshinCard). column은 wide로 re-flag 불가하니 재검증 불필요.
- recharts(FiveElementsChart·PentagonChart 일부)는 프리뷰 wrapper를 고정폭/높이로 감싸야 0-height 방지.

## 검증 결과 (2026 tetris 리디자인, 로컬, 업로드 전)
- `package-build`: components **44**(기존 42 + Mascot/MascotBubble), fonts **4 @font-face**(Pretendard +
  Bangers + JetBrains Mono 400/700), guidelines **3**(01·02·03-mascot), tokens 1, previews 19 user-owned.
- `package-validate`: **44/44 previews render cleanly** (12 floor + 나머지 authored/props-renderable),
  `[FONT_MISSING]` **0건**(폰트 vendor 후 해소). contact-sheet 3장 + 컴포넌트별 스크린샷으로 시각 검증 —
  마스코트(6 mood×5 size)·채팅 블록 버블·히어로(Bangers 워드마크)·결과 표(오행 색 보존) 모두 good.
- 토큰 3중 동기화(tailwind.config.ts ↔ tailwind.ds.config.cjs ↔ ds-tokens/tokens.css) 일치 확인,
  앱 `npm run build` 7/7 페이지 + `tsc --noEmit` 통과.
- **claude.ai 업로드는 미수행** — DesignSync(create_project/finalize_plan/write_files) 호출 안 함.
  업로드는 사용자 명시 승인 후 별도 단계(SKILL §5, pinned projectId f17c4807 → atomic 경로).
