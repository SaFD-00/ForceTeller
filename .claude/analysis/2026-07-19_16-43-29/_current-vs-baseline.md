# Results — 정본 수치 SSoT

이 파일의 수치는 전부 원천에서 재계산했다. 다른 문서는 여기를 인용한다.

## 검증 인프라

| 항목 | 값 | SSoT |
|------|-----|------|
| CI 존재 | **있음** (`push:main` + `pull_request:main`) | `.github/workflows/ci.yml:3-7` |
| CI 프론트 게이트 | lint · `tsc --noEmit` · `npm test` · `next build` — 4개 전부 블로킹 | `ci.yml:63,66,69,72` |
| CI 백엔드 게이트 | pytest · ruff check · ruff format — 블로킹. mypy는 `continue-on-error` | `ci.yml:29,33,36,41` |
| CI에 **없는** 것 | `node .ds-css/compile.mjs`, a11y 실측, coverage 측정 | `ci.yml` 전문 |
| pre-commit hook | **없음** (`.husky/`·`.pre-commit-config.yaml` 부재) | glob 결과 없음 |
| 집계 게이트 스크립트 | **없음** — 5개 명령을 따로 쳐야 함 | `web/package.json:5-11` |

## 테스트 실태

| 항목 | 값 | SSoT |
|------|-----|------|
| 프론트 테스트 파일 | 2개 (`lib/transforms.test.ts`, `lib/ganji.test.ts`) | glob |
| 프론트 테스트 케이스 | 21 `it` 블록 | `npm test` 출력 |
| 프론트 테스트 성격 | **순수 데이터만** — 렌더 0, 이벤트 0, 훅 0 | 두 파일 전문 |
| vitest environment | `node` — DOM 테스트 불가 | `web/vitest.config.ts:17` |
| vitest include | `lib/**/*.test.ts` — `.tsx`는 수집 자체가 안 됨 | `web/vitest.config.ts:16` |
| 컴포넌트 테스트 도구 | **없음** (`@testing-library/*`·`jsdom`·`happy-dom` 미설치) | `web/package.json:25-36` |
| playwright | **의존성 아님** (next의 optional peer일 뿐, `node_modules/@playwright/` 부재) | `web/package-lock.json:6303-6316` |
| 백엔드 테스트 함수 | 202개 / 20개 파일 | `grep "^\s*(async )?def test_" tests/` |
| jsx-a11y 규칙 | 6개, 전부 `warn` — `--max-warnings=0` 없어 블로킹 안 함 | `eslint-config-next/index.js:67-78`, `web/package.json:9` |

## 접근성 도달 범위

| 라우트 | 브라우저 실측 | 비고 |
|--------|--------------|------|
| `/result` (데스크톱 1280×1000) | **실측 완료** — 19종 단언 PASS | 지난 4라운드 |
| `/result` (모바일 <1024px) | **미실측** | 모바일 채팅 오버레이가 마운트된 적 없음 (`result/page.tsx:509`) |
| `/` (홈) | 미실측 | 코드 읽기만 |
| `/chat` | 미실측 | populated 상태를 아무도 렌더한 적 없음 |

| 항목 | 값 | SSoT |
|------|-----|------|
| 라우트 수 | 3개 (`/`, `/chat`, `/result`) | `web/app/**/*.tsx` |
| a11y 이니셔티브 적용 컴포넌트 | 전부 `components/result/*` 하위 | `useFocusTrap` 소비자 1곳(`GlossaryModal.tsx:79`) |
| `aria-live`/`role="status"`/`sr-only` | **0건** (repo 전체) | grep |
| `prefers-reduced-motion` | **0건** | grep (`globals.css` 포함) |
| `text-*-400` / `*-500` 텍스트 잔존 | **0건** | grep — ink 마이그레이션 완료 |
| 오버레이(`fixed inset-0`) | 3개 — 계약 준수는 1개 | `GlossaryModal`(준수) / `LoadingOverlay`(미준수) / 모바일 채팅(미준수) |

## 디자인 시스템 정합

| 항목 | 값 | SSoT |
|------|-----|------|
| 토큰 미러 #1 ↔ #2 | **일치** (의도된 차이만: 폰트 리터럴, content 글롭, safelist) | `tailwind.config.ts` ↔ `tailwind.ds.config.cjs` |
| 토큰 미러 #1 ↔ #3 | **11개 키 누락** — `*.foreground` 4개, `borderRadius` 6단계, `borderWidth.3` | `tokens.css` |
| 자동 동기화 장치 | **없음** — 수동 | `package.json:5-11`, `ci.yml` |
| 규칙 위반 잔존 (4종 스윕) | **전부 0건** | primary 텍스트 0 / `rounded-*`+카드 0 / `font-display`+bold 0 / 원색 텍스트 0 |
| 기계적으로 강제되는 규칙 | **2개뿐** — `font-display` weight 핀(`globals.css:21-23`), `boxShadowColor:false`(`tailwind.config.ts:103`) | — |
| 나머지 규칙의 강제 수단 | **산문뿐** — ESLint는 stock `next/core-web-vitals`, Tailwind plugin 0, 토큰 테스트 0 | `.eslintrc.json:2` |
| 죽은 유틸리티 (실제 출하 중) | `animation-delay-200`/`400` — 어디에도 정의 없음 | `ReasoningDisplay.tsx:51-52` |
| 손그림 radius 리터럴 중복 | 4곳 + 미소비 사본 1곳 | `globals.css:53,65,81,91`, `tokens.css:63` |

## 문서 드리프트

| 항목 | 값 | SSoT |
|------|-----|------|
| 낡은 오행 hex를 담은 문서 | 2개 — 토 `#ca8a04`(실제 `#D97706`), 금 `#71717a`(실제 `#64748B`) | `conventions.md:46-47`, `guidelines/02:18-19,33` |
| ink 규칙 언급 (guidelines/02) | **0건** — 대신 `text-element-fire`·`border-element-*/30` 권장 | `grep -c "ink"` |
| 존재하지 않는 컴포넌트를 나열한 문서 | 4개 문서 × 6종 컴포넌트 | `conventions.md:56-59`, `guidelines/01:40`, `guidelines/02:29`, `NOTES.md:111-113` |
| 고아 프리뷰 파일 | 5개 (사라진 export를 import) | `web/.design-sync/previews/` |
| API 엔드포인트 드리프트 | **0건** — 12개 전부 일치 | `README.md:339-392` ↔ `api/routes/*.py` |
| 실행 명령 드리프트 | **0건** | `README.md` ↔ `package.json`·`pyproject.toml` |
