# Stage: test-gate — 검증 체계의 지속가능성

## Question
회귀를 자동으로 잡을 수 있는가? 지금 통과하는 게이트가 다음 사람에게도 남는가?

## Evidence

| Source | Why it matters | Check |
|--------|----------------|-------|
| `.github/workflows/ci.yml:1-75` | 저장소의 유일한 CI. PR을 실제로 막는 것의 정의 | 전문 |
| `web/vitest.config.ts:14-18` | `environment`/`include`가 컴포넌트 테스트 가능 여부를 결정 | 전문 |
| `web/package.json:5-11,25-36` | scripts = 게이트 재현성, devDeps = 존재하는 테스트 도구 | 전문 |
| `web/package-lock.json:6303-6316` | playwright가 실제 의존성인지 유령 peer인지 | 해당 블록 |
| `web/node_modules/@playwright/**` | 설치 여부의 실측 | **파일 없음** |
| `tests/` 전역 `def test_` grep | 백엔드 테스트 함수 census | 202개 / 20파일 |
| `.husky/**`, `.pre-commit-config.yaml` | hook 레이어 | **없음** |

## Findings

| Finding | Verdict | Evidence | Scope |
|---------|---------|----------|-------|
| **CI가 존재하고 프론트 게이트가 완전히 배선돼 있다.** `push:main`·`pull_request:main`에서 lint(63)·`tsc --noEmit`(66)·`npm test`(69)·`build`(72)를 전부 블로킹 실행한다. **"CI가 없다"는 내 사전 전제는 틀렸다** | `contradicted` (전제가) | `ci.yml:3-7,43-74` | architectural |
| **그럼에도 판별력을 가졌던 것은 CI에 남지 않는다.** devlog는 `GlossaryModal`을 되돌리면 P1 4건, 툴팁 리스너를 빼면 P2 2건이 FAIL했다고 기록한다. **tsc·lint·npm test·build 중 어느 것도 두 revert를 잡지 못한다.** 하네스만이 "컴파일된다"와 "접근 가능하다"를 갈랐다 | `confirmed` | `ci.yml:63-72`; devlog `2026-07-19_16-41-23_a11y-overlay-contract.md` verification 절 | architectural |
| **a11y 하네스가 저장소에 존재하지 않는다.** repo 전역 `a11y\|axe` grep이 소스 주석·README·devlog만 반환한다. `a11y-verify.mjs` 없음, playwright config 없음, fixture 없음 | `confirmed` | grep 16파일 중 실행 가능 파일 0 | architectural |
| **playwright는 어디에도 의존성이 아니다.** lockfile의 `@playwright/test`는 `next`의 optional peerDependency이고 `web/node_modules/@playwright/`는 존재하지 않는다 | `confirmed` | `package-lock.json:6303-6316`; glob 결과 없음 | architectural |
| **vitest가 컴포넌트를 구조적으로 배제한다.** `include: ['lib/**/*.test.ts']` + `environment: 'node'` — `.tsx` 테스트는 수집조차 안 되고, `lib/` 아래 DOM 테스트도 document 부재로 실패한다. config 주석이 의도적이라고 명시 | `confirmed` | `vitest.config.ts:16-17` | architectural |
| **컴포넌트 테스트 도구가 미설치.** devDeps에 vitest만 — `@testing-library/*`·`jsdom`·`happy-dom` 없음(lockfile 히트는 vitest의 optional peer 선언) | `confirmed` | `package.json:25-36`; `package-lock.json:8753-8794` | architectural |
| **프론트 테스트는 순수 데이터만 덮는다.** 2파일 / 21 `it`. 렌더 0, 이벤트 0, 훅 0 | `confirmed` | `transforms.test.ts:160-249`; `ganji.test.ts:7-90` | cross-file |
| **a11y 핵심 코드에 자동 테스트가 전무하다.** `useFocusTrap`은 `lib/` 아래이지만 `environment:'node'`에서 `document`/`offsetParent`가 없어 테스트 불가. `GlossaryModal`/`GlossaryTooltip`은 `.tsx`라 glob 밖 | `confirmed` | `vitest.config.ts:16-17`; `lib/hooks/useFocusTrap.ts:37-83` | architectural |
| **살아있는 a11y 체크는 jsx-a11y 6개 규칙뿐이고 전부 `warn`이다.** `next lint`에 `--max-warnings=0`이 없어 경고로는 CI가 통과한다. 6개 모두 대비·포커스 순서·`inert`·키보드 해제를 다루지 않는다 | `confirmed` | `.eslintrc.json:2`; `eslint-config-next/index.js:67-78`; `package.json:9` | architectural |
| **게이트가 5개 개별 명령이고 집계 스크립트가 없다.** `typecheck` 스크립트조차 없어 CI가 `npx tsc --noEmit`을 직접 호출한다. 기여자는 5개를 알고 타이핑해야 하며 CI 정의와 로컬 정의가 드리프트할 수 있다 | `confirmed` | `package.json:5-11`; `ci.yml:66` | architectural |
| **`node .ds-css/compile.mjs`가 아무데도 배선돼 있지 않다.** 산문(`web/README.md:177`, `NOTES.md:28`)에만 등장하고 npm script·CI 스텝 어디에도 없다. 출력은 gitignore라 design-sync 드리프트는 완전히 무게이트다 | `confirmed` | grep `compile.mjs`; `.gitignore:35`; `ci.yml:43-74` | architectural |
| **hook 레이어가 전무하다.** `.husky/`·`.pre-commit-config.yaml`·`lint-staged` 모두 없음 | `confirmed` | glob 결과 없음 | architectural |
| **백엔드 테스트 함수 202개 / 20파일.** `manseol/calculator/`는 8개 중 6개 모듈에 전용 테스트가 있으나 `pillar_engine.py`·`interactions.py`는 없고, `manseol/core/`·`manseol/analysis/`(14개 모듈)는 전용 테스트가 하나도 없다 | `confirmed` | grep imports over `tests/`; glob `manseol/**` | cross-file |
| 다만 미커버 모듈은 골든 스냅샷으로 **간접** 실행된다 — `test_manseol_regression.py`가 전체 파이프라인을 돌려 고정 사주(`경오/신사/경진/계미`)를 단언한다. 실재하는 커버리지지만 입력 1개·종단값 단언이라 거칠다 | `plausible` | `test_manseol_regression.py:18-47` | cross-file |
| **coverage가 설정만 되고 측정되지 않는다.** `[tool.coverage.run]`에 6개 패키지가 있으나 CI는 `--cov` 없이 `pytest -q`만 돈다 | `confirmed` | `pyproject.toml:52,82-87`; `ci.yml:29` | architectural |

## Risks / Ambiguities

- **실제 공백은 "CI 없음"보다 좁고 날카롭다.** a11y 이니셔티브가 수동으로 돌린 4개 게이트는 전부 CI에 있고 살아남는다. 살아남지 못하는 것은 **정확히 판별력을 가졌던 부분**이다.
- **`npm run lint`가 CI 로그가 시사하는 것보다 약할 수 있다.** jsx-a11y가 전부 `warn`이라 aria 위반이 들어와도 경고만 찍고 통과할 가능성 — `next lint`의 warning 시 exit code를 확인해야 확정된다.
- **`.ds-css` 컴파일이 가장 취약한 고리다.** `tailwind.config.ts:5`가 수동 동기화를 요구하는 주석을 달고 있는데, 강제 장치가 없고 출력은 gitignore이며 유일한 리마인더가 README 한 줄이다. 이는 "문서화된 관례"이지 게이트가 아니다.
- **import 기준 미커버 ≠ 미테스트.** manseol `core`/`analysis` 지적은 *전용* 테스트 파일 기준이다. 골든이 happy path를 덮으므로, 두 단언 값을 움직이지 않는 변경은 조용히 통과한다.

## Next Local Checks

전부 **제안**이며 현재 상태가 아니다.

1. lint 게이트의 이빨 확인 — 임시로 `aria-hoax="x"`를 넣고 `npm run lint; echo $?`. 0이면 `--max-warnings=0` 추가가 답이다.
2. 집계 게이트 스크립트 `"gate": "npm run lint && tsc --noEmit && vitest run && next build && node .ds-css/compile.mjs"`를 추가하고 CI가 그것을 호출하게 해 정의 드리프트를 원천 차단.
3. `compile.mjs`를 CI에 배선 — 산출물이 gitignore이므로 바이트 크기/해시 단언 여부를 결정해야 한다.
4. **a11y 하네스 repo 편입에 필요한 결정들**(현재 전무):
   - *의존성*: `@playwright/test`를 실제 devDependency로 → `npm ci`에 브라우저 다운로드 추가
   - *fixture*: `web/e2e/fixtures/saju-result.json`. 백엔드 골든(`test_manseol_regression.py:19-27`)과 **같은 입력**에서 파생시켜야 두 골든이 갈라지지 않는다
   - *CI 브라우저*: 세션은 `channel:'chrome'`을 썼는데 `ubuntu-latest`에 없다 → 번들 chromium + `npx playwright install --with-deps chromium`
   - *런타임*: 하네스가 `build && start`를 요구 → `ci.yml:72`의 빌드 재사용 여부 결정
   - *flake 정책*: 재시도 횟수, 초기에는 mypy처럼 `continue-on-error`로 스테이징할지
   - *셀프테스트*: `A11Y_SELFTEST=1` 변이 모드를 CI 스텝으로 보존 — 하네스가 공허하게 통과하지 않음을 증명하는 유일한 장치
5. **playwright 없이 얻는 부분 승리**: `jsdom` + `@testing-library/react`를 넣고 `include`에 `components/**/*.test.tsx`를 추가하면 `useFocusTrap`의 Tab 순환 계약(`:46-70`)이 브라우저 없이 CI에서 단위 테스트 가능해진다. 대비·`inert` 레이아웃은 못 보므로 하네스를 대체하지 않고 보완한다.
6. `manseol/calculator/pillar_engine.py`·`interactions.py`의 전용 테스트 공백 해소.
