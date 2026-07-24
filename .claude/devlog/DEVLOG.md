# DEVLOG

프로젝트에 실제로 적용된 변경의 기록. 최신 항목이 위에 온다.

## 2026-07-24 — 만세력·채팅 프롬프트 인터넷 대조 검증 패스

검증 subagent 2종(Workflow 병렬)이 외부 기준을 먼저 확보한 뒤 로컬 실측과 대조했다. README가
후속 과제로 남겼던 "절기 ~9h 오프셋"은 UTC/KST 변환 누락(−9h)과 J2000 분점 황경(세차 드리프트,
연도별 −3.2h~+7.8h)의 **합성**으로 규명 — 2024년엔 상쇄돼 −1.2h로 보였다. 프롬프트는 도메인
오류·안전 가드·인젝션 방어를 OWASP·Anthropic 모범사례 기준으로 마감했다.

- based_on: standalone (사용자 요청: 만세력·채팅 프롬프트 검증·업데이트, 인터넷 검색, subagent 활용)
- changes: 8 files, +381 −52 / `a8984ff` `f433ceb`
- why: 절기 오프셋이 연도 가변이라 절기 경계 부근 출생의 년·월주가 실제로 틀리고 있었다
  (1990-02-04 10:00 → 경오·무인 오판, 정정 후 기사·정축). 프롬프트엔 존재하지 않는 상극
  "화극수", 비표준 용어 "수신(讐神)", 안전·인젝션 공백이 실측됐다
- verification: KASI/역서 절입 12건 ±0.7분 · 기준 명식 9케이스·일진 앵커 7건 일치 · pytest 333(+33) ·
  ruff 전건 · 메인 세션이 입춘 4개 연도·경계 명식 CLI 직접 실측 + 전체 diff 육안 검수
- category: devlog
- companion: [.claude/devlog/2026-07-24_10-52-36_manseol-prompt-verification.md](./2026-07-24_10-52-36_manseol-prompt-verification.md)

## 2026-07-23 — 서비스 완성 패스: 프로덕션 완결성 갭 마감

성숙한 저장소(전 게이트 GREEN)에서 "완성"의 남은 축은 제품 완결성이었다 — 실동작 + 공개
배포 차단 요소 제거. 정찰 subagent 2종(백엔드/보안·프론트/UX)으로 실재 갭을 매핑하고 직접
end-to-end 실측으로 판정했다. README "알려진 한계"·직전 분석 "남은 것"이 지목한 지점만 닫았다.

- based_on: standalone (goal: 서비스 완성까지 진행, subagent 활용)
- changes: 16 files, +598 −378 / `5e5f944` `f4fadd3` `fe7d350` `be280e7` `ebdccc5` `0d44526`
- why: README 헤드라인 미완이 "레이트리밋 미구현 — 공개 배포 전 필수"였다. 익명 사주 앱이라
  인증은 성격상 제외하되, OpenRouter 키 소비 표면을 지키는 레이트리밋을 1차 방어선으로 최우선
  구현. 콤보박스는 직전 분석이 코드 추론으로 남긴 결함이 실측상 키보드 선택 불가로 확인돼 마감.
  독립 verifier subagent가 지목한 요청 본문 무제한 WARNING을 후속으로 마감(크기 상한·길이 상한)
- verification: pytest 300(+22) · 라이브 429+Retry-After·413 · a11y e2e 4종 PASS·selftest 변이 7건 ·
  콤보박스 키보드 라이브 9/9 · Pydantic 경고 6→0 · recharts 번들 불변 · 무데이터 진입 빈 상태 실측 ·
  verifier 독립 판정 "production-complete, no hard BLOCKERs"
- category: devlog
- companion: [.claude/devlog/2026-07-23_23-27-19_service-completion-pass.md](./2026-07-23_23-27-19_service-completion-pass.md)

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
