# 접근성 마감 라운드 — 오버레이 계약 확립과 검증 하네스 봉합

- 작성: 2026-07-19
- 카테고리: devlog
- based_on: standalone (직전 tier-2 검증이 지목한 잔여 결함 목록)
- analysis_dir: none
- commits:
  - `418ed46` fix(a11y): 용어 모달 portal+inert 배경 봉쇄, overflow·exit 애니메이션 복원
  - `3527633` fix(a11y): 툴팁 Escape 를 document 수준으로 승격, 도달 불가 상세보기 경로 제거
  - `271264b` fix(a11y): 십성 도넛 aria 를 범례와 동일 집합(0% 포함 10개)으로 통일
  - `0b4d275` docs(a11y): 오버레이 접근성 계약·실측 게이트 문서화 + mascot 가이드 드리프트 정정
- diffstat: 7 files, +145 −77

## Changes

- Files: `web/components/ui/GlossaryModal.tsx`, `web/components/ui/GlossaryTooltip.tsx`,
  `web/components/result/ElementDistribution.tsx`, `web/lib/hooks/useFocusTrap.ts`(주석),
  `DESIGN.md`, `web/README.md`, `web/.design-sync/guidelines/03-mascot.md`
- 저장소 밖: 검증 하네스 `a11y-verify.mjs`(세션 scratchpad, 커밋 대상 아님)
- Summary:
  - **모달**: portal(`data-glossary-portal`) 도입 + 열림 중 body 직계 자식에 `inert` 부여(기존 inert 값은
    Map으로 보존 후 복원). body overflow는 열기 전 인라인 값 저장·복원. 마지막 `entry`를 내부 캐시해
    exit 애니메이션 복구. 호출부 5곳 무수정.
  - **툴팁**: Escape를 `document` 수준 리스너로 승격(`isOpen`일 때만 부착), 닫을 때 포커스 비이동.
    `onDetailClick`·"자세히 보기" 버튼·`escapeRef` 가드 제거, timeout 언마운트 cleanup 추가.
  - **차트**: 십성 `aria-label`에서 `>0` 필터 제거 — 오행·범례와 동일한 10개 집합.
  - **문서**: DESIGN.md에 "오버레이 접근성 계약" 6항목 신설, web/README.md에 a11y 실측 게이트 절차 추가,
    03-mascot.md의 기존 드리프트(Modal이 Mascot을 쓴다는 서술) 정정.

## Why

직전 tier-2 검증이 4건을 남겼다: (1) 모달 배경이 `aria-hidden`/`inert` 미처리, (2) hover로 연 툴팁을
키보드로 닫을 수 없음(WCAG 1.4.13), (3) `onDetailClick`이 호출부 0건인 죽은 경로, (4) 검증 하네스가
화살표·범례를 계산만 하고 단언하지 않아 **화살촉이 전부 깨져도 PASS**가 나는 상태.

순서를 (4) 먼저로 잡았다 — 신뢰할 수 없는 게이트로 새 작업을 판정하면 의미가 없기 때문이다. 그 과정에서
`bgAtPoint`가 **한 번도 작동한 적이 없다**는 것이 드러났다: `elementsFromPoint`는 뷰포트 좌표인데 차트는
y≈1601, 뷰포트는 1000이라 스택이 항상 비었고 조용히 흰색을 반환했다. 흰색은 어두운 텍스트에 관대한
방향이라 false PASS를 만들 수 있었다. `scrollIntoViewIfNeeded` + 스택 길이 단언으로 고쳤다.

(3)은 배선이 아니라 **제거**를 택했다. `GlossaryModal`은 헤딩 버튼 5개 경로로 이미 살아 있어 고아화가 없고,
배선하면 두 호출부에 모달 상태를 신설하고 `useFocusTrap`의 소멸-폴백이 실경로가 되는 등 마감 라운드에
기능 표면을 여는 일이 된다.

(1)에서 `inert`는 배경이 다이얼로그의 형제여야 걸 수 있어 portal이 전제였다. 여기서 **effect 선언 순서
의존**이 생겼다 — React는 cleanup을 선언 순서로 실행하므로 inert 해제가 포커스 복원보다 먼저 돌아야
복원 대상이 focusable하다. 뒤집으면 조용히 포커스가 body로 낙하한다. 코드 주석과 DESIGN.md 양쪽에 남겼다.

## Verification

게이트(전부 오케스트레이터가 직접 재실행):

- `npx tsc --noEmit` → exit 0
- `npm run lint` → ✔ No ESLint warnings or errors
- `npm test` → Test Files 2 passed, Tests 21 passed
- `npm run build` → ✓ Compiled successfully
- `node .ds-css/compile.mjs` → wrote ds-compiled.css (48939 bytes)

브라우저 실측(프로덕션 빌드 `npm run build && PORT=3456 npm run start`, Playwright channel 'chrome',
mock 주입, 알파 합성 후 대비 계산):

- `node a11y-verify.mjs` → `VERDICT: PASS`, exit 0
- 양성 단언 라인: ARROWS / LEGEND / GUARD / ARIA-OHENG / ARIA-TENGOD / ARIA-PENTAGON / SWEEP / DONUT /
  CONTRAST / TABS / P1-INERT / P1-OVERFLOW / P1-EXITANIM / P1-INERT-RESTORE / P1-FOCUSRETURN /
  P2-KBD-ESC / P2-HOVER-ESC / P2-NO-DETAIL-BTN / P3
- `A11Y_SELFTEST=1 node a11y-verify.mjs` → `VERDICT: FAIL (7건)`, exit 1 — 주입한 변이 4종(marker 제거,
  aria 위조, 범례 항목 제거, % 텍스트 제거)을 전부 포착

판별력 확인(공허 통과가 아님을 실증):

- `GlossaryModal.tsx`만 HEAD로 되돌려 재빌드 → P1 4건 FAIL(포탈 부재, inert 미적용 8개, exit 즉시 detach,
  overflow "unset") → 복원 후 PASS
- 툴팁 document 리스너만 제거해 재빌드 → P2 3건 중 2건 FAIL → 복원 후 PASS

문서-코드 정합:

- `grep -n "inert" DESIGN.md` → 신규 소절 존재
- inert effect(60행) < `useFocusTrap`(79행) — 문서가 요구한 선언 순서가 코드에서 지켜짐
- 모달 Escape가 실제로 `document.addEventListener`(90행)임을 확인
- `grep -rn "onDetailClick" web --include="*.tsx"` → 0건
- `grep -rn "GlossaryModal" web/.design-sync/guidelines/03-mascot.md` → 0건

## 남은 것 (이번 범위 밖)

- **하네스가 저장소 밖에 있다** — a11y 실측 스크립트는 세션 scratchpad 소산이라 세션이 끝나면 CI가 회귀를
  못 잡는다. repo 편입에는 playwright devDependency·fixture 커밋·CI 브라우저 실행시간·flake 정책이라는
  결정 사항이 걸려 있다. 다음 라운드 1순위.
- **결과 페이지 외 표면 미실측** — 홈·입력 폼·채팅은 이 수준의 기계 실측을 받지 않았다.
- **스크린리더 수동 검증 부재** — aria 문구의 낭독 품질·순서는 기계 판정 불가.
- `useFocusTrap`의 "저장 요소 소멸 시 body 낙하" 폴백 — 현재 모든 호출부의 트리거가 존속하는 헤딩 버튼이라
  실경로가 없어 주석 문서화로 갈음.

## Provenance

- Analysis hub: none (standalone record 모드)
- Snapshot: [2026-07-19_16-41-23_a11y-overlay-contract.sync-snapshot.json](./2026-07-19_16-41-23_a11y-overlay-contract.sync-snapshot.json)
