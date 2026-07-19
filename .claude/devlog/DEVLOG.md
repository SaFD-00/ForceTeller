# DEVLOG

프로젝트에 실제로 적용된 변경의 기록. 최신 항목이 위에 온다.

## 2026-07-19 — 분석 후속: S-1~S-8 전건 반영

`/workflow:analyze`가 도출한 8개 제안을 전부 반영했다. 접근성 이니셔티브가 `/result` 데스크톱 안에서만
완결됐다는 것이 분석의 헤드라인이었고, 이번에 채팅·오버레이·홈까지 넓히면서 회귀를 자동으로 되돌릴
경로(디자인 에이전트용 문서)와 회귀를 못 잡던 게이트 공백(하네스가 저장소 밖)을 함께 막았다.

- based_on: S-1~S-8 ← `.claude/analysis/2026-07-19_16-43-29/solutions.md`
- changes: 36 files, +2184 −558 / `3ca1e93` `52e6703` `9a61e5d` `a0dcff1` `0832fd5` `dae0d9c` `41f6c59` `f80bac7`
- why: P1 두 건의 성격이 달랐다 — S-2는 지금 해를 끼치고(로딩 점 대비 1:1로 비가시, 스트리밍 답변 SR 무음),
  S-1은 증상이 없지만 다음 디자인 작업에서 회귀를 되돌린다. S-5는 CI가 4게이트를 돌면서도 접근성 회귀를
  하나도 못 잡는 공백을 메웠다
- verification: `npm run gate` exit 0(Tests 30) · `npm run e2e` 4종 PASS · 셀프테스트 exit 0(변이 7건 검출) ·
  번들 chromium(CI 조건)에서도 PASS · 로딩 점 1:1 → 6.38:1 실측 · 토큰 패리티·CI 가드·lint 전부 위반을
  주입해 실제로 잡는지 확인 후 원복
- category: devlog
- companion: [.claude/devlog/2026-07-19_18-01-16_analysis-p1-p3-followthrough.md](./2026-07-19_18-01-16_analysis-p1-p3-followthrough.md)

## 2026-07-19 — 접근성 마감 라운드: 오버레이 계약 확립과 검증 하네스 봉합

직전 tier-2 검증이 남긴 잔여 결함 4건을 마감했다. 검증 하네스를 먼저 고친 것은 신뢰할 수 없는 게이트로
새 작업을 판정하면 의미가 없기 때문이고, 그 과정에서 대비 측정 함수가 한 번도 작동한 적 없었다는 사실이
드러났다.

- based_on: standalone (직전 tier-2 검증 지목 사항)
- changes: 7 files, +145 −77 / `418ed46` `3527633` `271264b` `0b4d275` /
  모달 portal+inert·overflow·exit 복원, 툴팁 document Escape·죽은 경로 제거, 십성 aria 통일, 문서 정합
- why: 모달 배경 미봉쇄(aria-modal만으로 불완전), hover 툴팁 키보드 미해제(1.4.13), 호출부 0건인
  `onDetailClick` 죽은 경로, 화살표·범례를 단언하지 않아 화살촉이 깨져도 PASS를 내던 하네스
- verification: `tsc/lint/test/build/compile.mjs` 전부 통과 · 프로덕션 빌드 실측 `VERDICT: PASS` exit 0 ·
  셀프테스트 exit 1(변이 4종 포착) · 코드를 되돌린 discriminator로 P1 4건·P2 2건 FAIL 확인(공허 통과 아님)
- category: devlog
- companion: [.claude/devlog/2026-07-19_16-41-23_a11y-overlay-contract.md](./2026-07-19_16-41-23_a11y-overlay-contract.md)
