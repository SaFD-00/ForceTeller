# 분석 후속 — S-1~S-8 전건 반영

- 작성: 2026-07-19
- 카테고리: devlog
- based_on: `.claude/analysis/2026-07-19_16-43-29/solutions.md` S-1~S-8 (P1 2건, P2 3건, P3 3건 전부)
- analysis_dir: `.claude/analysis/2026-07-19_16-43-29`
- commits:
  - `3ca1e93` fix(a11y): 채팅 표면의 사용자 직격 결함 3건 — 로딩 점 비가시·라이브 리전·입력 이름 (S-2)
  - `52e6703` docs(design-sync): 디자인 에이전트 가이드가 지시하던 접근성 회귀 차단 (S-1)
  - `9a61e5d` fix(a11y): 나머지 오버레이 2개에 계약 적용 + 로딩 오버레이가 안 뜨던 버그 (S-3)
  - `a0dcff1` test+ci: 디자인 규칙을 산문에서 기계적 강제로 전환 (S-4)
  - `0832fd5` test(e2e): a11y 실측 하네스를 저장소로 편입하고 CI에 배선 (S-5)
  - `dae0d9c` fix(a11y): Tailwind 애니메이션에 prefers-reduced-motion 커버리지 추가 (S-7)
  - `41f6c59` ci: 게이트를 집계 스크립트로 통합 + lint warning 이 실제로 차단하게 (S-8)
  - `f80bac7` docs: 구조 문서에 신규 디렉터리 반영 + 고아 프리뷰·죽은 참조 정리 (S-6)
- diffstat: 36 files, +2184 −558

## Changes

- **S-1 회귀 재유입 차단**: `web/.design-sync/guidelines/02` 전면 개정(ink 규칙 도입, 원색 텍스트·`/50` 보더 금지 명시), 낡은 오행 hex 정정, "primary 바이올렛"·"하드 오프셋" 잔재 제거
- **S-2 채팅 3건**: 로딩 점 `bg-muted`→`muted-foreground`(1:1 → 6.38:1), 완료 메시지 전용 `aria-live` 리전 + 로딩 `role="status"` + 에러 `role="alert"`, textarea `useId`+`htmlFor` 라벨
- **S-3 오버레이**: 모바일 채팅에 전체 계약, `LoadingOverlay`에 축소 계약(트랩 없음). `useOverlayPortal` 훅 추출. **선존 버그 동봉** — `setError`가 `isLoading:false`를 함께 세팅하는데 `BirthInfoForm`이 `setLoading(true)` 다음에 호출해 오버레이가 프로덕션에서 한 번도 뜬 적이 없었다
- **S-4 기계적 강제**: 토큰 패리티 테스트 9건(미러 3곳 일치 단언, `tokens.css` 누락 11키 보충), `animation-delay-*` 죽은 클래스 제거, CI grep 가드 2종
- **S-5 하네스 편입**: `web/e2e/` 4종 + fixture, `@playwright/test` devDependency, CI 4스텝(`continue-on-error` 스테이징, 셀프테스트 포함)
- **S-6 문서**: 구조 문서에 `BottomNav`·`MotionProvider`·`lib/hooks/`·`web/e2e/` 추가, 고아 프리뷰 5개 삭제, 죽은 참조 제거, "Vitest 21개"→30개
- **S-7 reduced-motion**: `globals.css`에 `@media (prefers-reduced-motion: reduce)` — 정지가 아니라 주기 연장
- **S-8 게이트**: `npm run gate` 집계 스크립트 + CI가 그것을 호출, `lint`에 `--max-warnings=0`

## Why

분석이 P1으로 꼽은 두 건이 성격이 달랐다. S-2는 **지금 사용자에게 해를 끼치는 것**(로딩 점이 안 보여 앱이 멈춘 것처럼 보임, 스트리밍 답변이 SR에 무음)이고, S-1은 **회귀를 자동 재유입시키는 것**(디자인 에이전트가 읽는 문서가 방금 고친 규칙을 반대로 지시)이다. 후자는 지금 증상이 없지만 다음 작업에서 되돌린다.

S-5가 P2 중 가장 중요했다. CI는 이미 4게이트를 블로킹 실행하지만 **판별력을 가졌던 것은 거기 없었다** — 하네스가 세션 임시 디렉터리에만 있어 세션이 끝나면 사라졌다.

## Verification

각 단계마다 오케스트레이터가 직접 재실행:

- `npm run gate` (lint→typecheck→test→build→compile.mjs) → exit 0, Tests 30 passed
- `npm run e2e` → 4종 전부 `VERDICT: PASS`, exit 0
- `npm run e2e:selftest` → exit 0 (변이 7건 검출 = 하네스가 공허하지 않음)
- `PW_CHANNEL= node e2e/a11y-result.mjs` → 번들 chromium(CI 조건)에서도 PASS

**실측이 코드 추론을 확정한 지점**: `/chat`을 프로덕션 빌드로 렌더해(스트림을 무응답으로 묶어 로딩 상태 노출) 로딩 점이 `rgb(237,244,250)` 위 `rgb(237,244,250)`으로 정확히 1:1임을 확인했다. 수정 후 6.38:1.

**판별력 확인(공허 통과가 아님을 실증)**:
- 토큰 패리티: `tokens.css`의 `--ft-color-accent`를 변조 → FAIL → 원복 → PASS
- CI 가드: `text-primary`와 `card rounded-xl`을 주입 → 각각 매치 → 원복
- lint: `aria-hoax` 주입 시 warning만 내고 **exit 0**이었음을 확인 → `--max-warnings=0` 추가 근거
- 오버레이: `GlossaryModal`을 HEAD로 되돌려 P1 4건 FAIL, 툴팁 리스너 제거로 P2 2건 FAIL

## 남은 것 (정직하게)

- **CI 실행은 미검증**. 로컬에서 번들 chromium과 백엔드 부재를 각각·동시에 모의했지만 `ubuntu-latest`의 **한글 폰트 부재**는 재현하지 못했다(macOS엔 한글 폰트가 항상 있다). `continue-on-error` 스테이징의 직접적 이유이며, 첫 CI 로그를 보고 핀 조정 여부를 판단해야 한다.
- **스크린리더 수동 검증 부재**. `aria-live` 배치는 DOM 계약(리전 선존재, 스트리밍 노드를 리전 밖에 배치)까지만 실측했다. 실제 VoiceOver/NVDA 낭독 품질은 기계 판정 불가.
- **홈·입력 폼의 나머지 표면 미실측**. `BirthInfoForm`의 도시 자동완성이 콤보박스가 아니고 `onBlur` 200ms 타이머로 키보드 이동 중 옵션이 언마운트되는 문제는 코드 추론 상태로 남았다.
- `@iconify/react`의 기본 `aria-hidden` 동작 미확정 — 어느 쪽이든 결함이나 고칠 방향이 갈린다.
- `recharts`가 `package.json`에 있으나 실사용 0건 — 제거는 동작 변경이라 손대지 않았다.

## Provenance

- Analysis hub: [README.md](../analysis/2026-07-19_16-43-29/README.md)
- Solutions: [solutions.md](../analysis/2026-07-19_16-43-29/solutions.md)
- Snapshot: [2026-07-19_18-01-16_analysis-p1-p3-followthrough.sync-snapshot.json](./2026-07-19_18-01-16_analysis-p1-p3-followthrough.sync-snapshot.json)
