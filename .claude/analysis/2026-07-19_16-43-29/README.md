# 분석: 접근성·디자인 시스템 이니셔티브 종료 후 현재 상태

> **Scope**: 정적 코드 분석 + 4개 stage 병렬 조사 + 오케스트레이터 직접 재검산 9건.
> **브라우저 실측은 이번 분석에서 수행하지 않았다** — 지난 라운드의 `/result` 데스크톱 실측이 최신 측정치다.

**Headline:** 4라운드 이니셔티브는 `/result` **데스크톱 뷰포트 안에서만** 완결됐다. 나머지 두 라우트는 손대지 않았고, 그중 채팅 로딩 점은 `bg-muted` 위 `bg-muted`(대비 1:1)로 **지금 모든 사용자에게 보이지 않으며**, `aria-live`가 repo 전역 0건이라 제품의 핵심 인터랙션인 스트리밍 답변이 스크린리더에 전혀 전달되지 않는다. 더 시급한 것은 `web/.design-sync/guidelines/02`가 **디자인 에이전트에게 ink 규칙 위반을 지시**하고 있다는 점이다(ink 언급 0건, `text-element-fire`·`border-element-*/30` 권장, 낡은 hex) — 방금 고친 회귀를 자동으로 되돌리는 경로다.

## Index

| 문서 | 내용 |
|------|------|
| [`_current-vs-baseline.md`](./_current-vs-baseline.md) | **정본 수치 SSoT** — 검증 인프라·테스트·도달 범위·정합 수치 |
| [`gap-stage1-a11y-reach.md`](./gap-stage1-a11y-reach.md) | 접근성 이니셔티브가 닿은 곳과 안 닿은 곳 |
| [`gap-stage2-design-drift.md`](./gap-stage2-design-drift.md) | 디자인 시스템의 드리프트 내성 |
| [`gap-stage3-test-gate.md`](./gap-stage3-test-gate.md) | 검증 체계의 지속가능성 |
| [`gap-stage4-docs-drift.md`](./gap-stage4-docs-drift.md) | 문서-코드 정합성 |
| [`solutions.md`](./solutions.md) | **제안** — S-1~S-8, P1/P2/P3 + honest ceiling |
| [`verification.md`](./verification.md) | claim audit — 재검산 9건 + 이 분석의 한계 |

## Stage Verdicts

| Stage | 핵심 판정 | Verdict | Scope |
|-------|----------|---------|-------|
| a11y-reach | 이니셔티브 전체가 `components/result/*`에만 착지 — 3라우트 중 2개에 렌더되는 채팅은 아무것도 못 받음 | `confirmed` | architectural |
| a11y-reach | 채팅 로딩 점 `bg-muted` on `bg-muted` = 1:1, 완전 비가시 | `confirmed` | cross-page |
| a11y-reach | `aria-live` repo 전역 0건 — 스트리밍 답변·에러가 SR에 무음 | `confirmed` | cross-page |
| a11y-reach | 오버레이 3개 중 계약 준수 1개. 모바일 오버레이는 "검증된 페이지"에 있으면서 `isMobile` 게이트로 실측을 빠져나감 | `confirmed` | architectural |
| design-drift | 규칙 위반 4종 스윕 전부 0건 — 규율은 지켜지고 있다 | `confirmed` | cross-file |
| design-drift | 그러나 기계적 강제는 2개뿐이고 나머지는 산문. 실패 모드가 이미 발생(`animation-delay-*` 미정의 출하) | `confirmed` | architectural |
| test-gate | **CI가 존재하고 프론트 4게이트를 전부 블로킹 실행한다 — "CI 없음"이라는 사전 전제는 틀렸다** | `contradicted` | architectural |
| test-gate | 그러나 판별력을 가졌던 a11y 하네스는 저장소에 없다. revert 6건을 tsc·lint·test·build 중 무엇도 못 잡는다 | `confirmed` | architectural |
| docs-drift | `guidelines/02`가 ink 규칙 위반을 지시(ink 언급 0건) — 회귀 자동 재유입 경로 | `confirmed` | architectural |
| docs-drift | API 엔드포인트 12개·실행 명령·버전은 전부 일치 — 이쪽 드리프트 0 | `confirmed` | cross-file |

## Honesty / Limits

- **이번 분석은 브라우저를 띄우지 않았다.** 채팅 관련 findings 전부가 코드 읽기 기반이며, `/chat`의 populated 상태는 **아무도 렌더한 적이 없다**. `solutions.md`의 S-2는 고치기 전에 실측이 선행돼야 한다.
- **합성 알파 대비를 계산하지 않았다.** `bg-muted` on `bg-muted`(1:1)만 색 동일성으로 확정했다. 다른 조합의 "괜찮다"는 판단은 토큰 주석 근거이지 실측이 아니다.
- **`@iconify/react`의 기본 `aria-hidden` 동작이 미확정이다.** 붙인다면 스피너 완전 은닉(더 나쁨), 안 붙인다면 앱 전역 장식 아이콘이 이름 없는 그래픽 — 어느 쪽이든 결함이나 고칠 방향이 갈린다.
- **`components/result/*` 13개를 전문 읽지 않았다** — 검증된 표면이라 import만 추적했다. 그 안의 회귀는 여기 나타나지 않는다.
- **pytest 278개 주장을 검증하지 않았다** — 테스트 함수 202개 + parametrize 전개 가능성. 실행 없이 확정 불가라 드리프트로 보고하지 않았다.
- **단일 사례를 승격하지 않았다.** `LoadingOverlay`·모바일 오버레이는 각각 `single-case`로 두되, "오버레이 계약이 1곳에만 적용됐다"는 3개 전수 확인 근거로 `architectural`로 올렸다.
- 이 분석은 **코드를 수정하지 않았고 Notion에 업로드하지 않았다.**
