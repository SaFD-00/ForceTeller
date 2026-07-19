# DEVLOG

프로젝트에 실제로 적용된 변경의 기록. 최신 항목이 위에 온다.

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
