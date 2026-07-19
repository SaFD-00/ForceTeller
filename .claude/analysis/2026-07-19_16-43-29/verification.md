# Verification — claim audit

Phase 2 stage worker의 주장을 최종 결론으로 승격하기 전에 오케스트레이터가 직접 재검산한 기록.

## 재검산한 주장

| # | 주장 | 출처 | 재검산 방법 | 결과 |
|---|------|------|-------------|------|
| 1 | CI가 없다 (**내 브리프의 전제**) | 오케스트레이터 | `.github/workflows/ci.yml` 직접 읽기 | **반박됨.** `frontend` job이 lint(63)·`tsc --noEmit`(66)·`npm test`(69)·`npm run build`(72) 4개를 전부 실행하고 블로킹한다. 내 전제가 틀렸다 |
| 2 | 채팅 로딩 점이 `bg-muted` on `bg-muted`로 비가시 | stage a11y | `MessageList.tsx:110-114` 직접 읽기 | **확인.** 컨테이너 `:110` `bg-muted`, 점 `:112-114`도 `bg-muted`(`#EDF4FA`). 동일색 = 1:1 |
| 3 | `aria-live` 0건 | stage a11y | `grep -rn "aria-live\|role=\"status\"\|role=\"alert\"\|sr-only" web/app web/components` | **확인.** 0건 |
| 4 | `Icon`이 `aria-label`을 드롭 | stage a11y | `Icon.tsx:6-21` 직접 읽기 | **확인.** `IconProps = {name, size, className}`, rest spread 없음 → 호출자가 넘긴 `aria-label`이 DOM에 도달하지 못함 |
| 5 | design-sync 문서에 낡은 오행 hex | stage docs-code | `grep -rn "ca8a04\|71717a" web/.design-sync/` ↔ `elements.ts:20,26` | **확인.** `conventions.md:46-47`, `guidelines/02:18-19,33`이 `#ca8a04`/`#71717a`. 코드는 `#D97706`/`#64748B` |
| 6 | guidelines/02가 ink 규칙 위반을 지시 | stage docs-code | 파일 8-35행 읽기 + `grep -c "ink"` | **확인.** ink 언급 **0건**. `text-element-fire`·`border-element-fire/30`·"테두리 50%"를 권장. "primary 바이올렛"이라는 두 팔레트 전 잔재까지 있음 |
| 7 | 고아 프리뷰 5개 | stage docs-code | `ls previews/` ↔ `ls components/result/` | **확인.** `FiveElementsChart`·`FourPillarsDisplay`·`StrengthMeter`·`TenGodsDistribution`·`FortuneCycleTimeline`이 previews에 있으나 `components/result/`에 없음 |
| 8 | `/result`에 미검증 모바일 오버레이 | stage a11y | `result/page.tsx:509` 읽기 | **확인.** `isChatOpen && isMobile` 게이트. 데스크톱 뷰포트(1280×1000)로 실측했으므로 마운트된 적 없음 |
| 9 | `LoadingOverlay`가 계약 미준수 | stage a11y | `grep`으로 role/aria/portal/trap 확인 | **확인.** `fixed inset-0`(25행)만 있고 role·aria·portal·focus trap **전부 0건** |

## Audit 체크리스트

1. **핵심 수치를 원천에서 재계산했는가?** — 예. 대비 주장은 토큰 hex 동일성(`bg-muted` on `bg-muted`)으로 판정했고, grep 개수는 전부 직접 실행했다. 단, **합성 알파 대비 수치는 이번 분석에서 계산하지 않았다**(아래 한계 참조).
2. **자동 요약·worker 보고를 그대로 복사하지 않았는가?** — 위 9건을 직접 재검산했다. 재검산하지 않은 worker 주장은 보고서에서 verdict를 낮춰 표기했다.
3. **단일 사례를 보편 원인으로 승격하지 않았는가?** — `LoadingOverlay`·모바일 오버레이는 각각 `single-case`로 유지했다. 다만 "오버레이 계약이 1곳에만 적용됐다"는 것은 3개 오버레이 전수 확인에 근거하므로 `architectural`로 올렸다.
4. **결론이 evidence scope를 넘지 않는가?** — `/chat`의 populated 상태는 **아무도 렌더한 적이 없다**. 해당 findings는 코드 읽기 기반이며 그렇게 명시했다.
5. **방법론 권고를 현재 결과처럼 쓰지 않았는가?** — `solutions.md`의 모든 항목은 제안이며 현재 상태와 분리했다. a11y 하네스 repo 편입은 "결정 필요 사항"으로만 적었다.
6. **Notion 업로드를 실행하지 않았는가?** — 하지 않았다.

## 이 분석의 한계 (정직하게)

- **합성 알파 대비를 계산하지 않았다.** stage a11y가 `bg-primary/10 text-accent` 같은 조합을 "괜찮다"고 한 것은 토큰 주석 근거이지 실측이 아니다. `bg-muted` on `bg-muted`(1:1)만 색 동일성으로 확정했다.
- **`/chat`·`/`를 브라우저로 렌더하지 않았다.** 지난 4라운드의 실측은 전부 `/result` 데스크톱 뷰포트였다. 채팅 관련 findings 전부가 코드 읽기 기반이다.
- **`@iconify/react`의 기본 `aria-hidden` 동작을 확인하지 못했다.** Iconify가 기본으로 `aria-hidden="true"`를 붙이면 스피너가 완전 은닉(더 나쁨)이고, 안 붙이면 앱 전역의 장식 아이콘이 전부 이름 없는 그래픽으로 읽힌다. **어느 쪽이든 결함이지만 어느 쪽인지 미확정.**
- **`BirthInfoForm`의 200ms `onBlur` 키보드 트랩은 코드 추론이다.** Tab + `setTimeout` 언마운트의 포커스 거동은 타이밍·브라우저 의존이라 실제 키 입력으로 확인해야 한다.
- **pytest 278개 주장을 검증하지 않았다.** 테스트 함수는 202개이고 `parametrize` 전개로 278이 될 수 있으나 실행 없이 확정 불가 — 드리프트로 보고하지 않았다.
- **`components/result/*` 13개 파일을 전문 읽지 않았다.** 검증된 표면이라 import만 추적했다. 그 안의 회귀는 이 분석에 나타나지 않는다.
