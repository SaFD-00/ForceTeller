# 서비스 완성 패스 — 프로덕션 완결성 갭 마감

- 작성: 2026-07-23
- 카테고리: devlog
- based_on: standalone (goal: "서비스가 완성되었다고 판단될 때까지 진행", subagent 활용)
- commits:
  - `5e5f944` feat(api): IP별 레이트리밋 미들웨어 — 공개 배포 남용·비용 방어선
  - `f4fadd3` fix(a11y): 출생 도시 자동완성을 접근성 ARIA combobox로 전환
  - `fe7d350` chore(models): Pydantic class-based Config → model_config=ConfigDict
  - `be280e7` chore(web): 미사용 의존성 recharts 제거
  - `ebdccc5` docs: 레이트리밋 모듈·recharts 제거를 구조/보안 문서에 반영
  - `0d44526` harden(api): 요청 본문 크기 상한 + message 길이 상한 (검증 후속)
- diffstat: 16 files, +598 −378

## 접근

이미 성숙한 저장소(백엔드 pytest 278, 프론트 lint/tsc/vitest·a11y e2e 전부 GREEN)라
"완성" 판정 기준을 **품질 게이트**가 아니라 **제품 완결성**(실동작 + 프로덕션 배포 차단
요소 제거)에 두었다. 두 정찰 subagent(백엔드/보안, 프론트/UX)를 병렬로 띄워 실재 갭만
매핑하게 하고, 동시에 직접 end-to-end 스모크·실측으로 판정 기준선을 잡았다.

판정 근거는 저장소 스스로 밝힌 미완 지점 — README "알려진 한계"와 직전 분석 devlog의
"남은 것" — 이며, 없는 스코프를 지어내지 않았다.

## Changes

- **레이트리밋(최우선 차단 요소)**: README가 "공개 배포 전 도입 필요"로 지목한 부재를 해소.
  `api/rate_limit.py`에 인메모리 슬라이딩 윈도우 리미터(`time.monotonic` 기반, Lock 보호,
  `max_keys` 메모리 가드) + `client_key`(X-Forwarded-For 신뢰 게이팅) + 이중 버킷 미들웨어.
  전역 60/분, LLM(`/api/chat`·`/api/chat/stream`, OpenRouter 키 소비 표면) 12/분. `/health`
  면제. CORS보다 먼저 등록해 429에도 CORS 헤더가 실린다. 설정 `RATE_LIMIT_*` 6종.
- **도시 자동완성 접근성**: 순수 텍스트 입력 + 떠 있는 button 목록 → ARIA combobox.
  `role=combobox`/`aria-expanded`/`aria-controls`/`aria-autocomplete`/`aria-activedescendant`,
  `ul[role=listbox]` + `li[role=option][aria-selected]`. ArrowUp/Down(순환)·Home/End·Enter·
  Escape 키보드. 활성 옵션을 activedescendant로 가리켜 DOM 포커스는 입력에 머무르므로,
  옵션으로 Tab 이동 시 `onBlur` 200ms 타이머가 옵션을 언마운트하던 결함이 사라진다.
  `e2e/a11y-loading`의 도시 옵션 셀렉터를 `role=option`으로 갱신(button→li 반영).
- **Pydantic 위생**: class-based `Config`(V3 제거 예정) 5곳 → `model_config=ConfigDict`.
  전부 `json_schema_extra`(OpenAPI 예시)만 담아 동작 변화 없음. 경고 6→0.
- **죽은 의존성**: `recharts` 제거(소스 참조 0, 차트는 순수 SVG). 트리셰이킹으로 번들엔
  원래 없었으므로 산출물 크기 불변 — 순수 설치 위생.
- **문서 동기화**: 구조/보안 문서에 `rate_limit.py`·레이트리밋 상세 반영, Recharts 행 제거.

## Why

README "알려진 한계"의 헤드라인이 "인증·레이트리밋 미구현 — 공개 배포 전 도입 필요"였다.
이 서비스는 **익명 사용을 전제한 사주 앱**이라 계정·로그인(인증)은 제품 성격상 두지 않되,
남용·비용 폭주(특히 OpenRouter 키를 소비하는 LLM 엔드포인트)를 막을 **레이트리밋이 실질적
1차 방어선**이다. 따라서 완성의 핵심 차단 요소로 이것을 최우선 처리했다.

콤보박스는 직전 분석이 코드 추론으로만 남겨 둔 결함으로, 실측 결과 키보드로는 사실상 도시를
선택할 수 없었다(옵션 Tab 진입 → 입력 blur → 200ms 후 옵션 언마운트). 접근성 기준선(키보드
우선, 항상 보이는 포커스)에 정면으로 어긋나 IMPORTANT로 처리했다.

## Verification

각 변경을 직접 재실행·실측으로 확정했다(에이전트 자가보고 불신, 클린 상태 재검).

- **레이트리밋**: `pytest 295 passed`(신규 17: 윈도우 슬라이딩·키 격리·경계 만료·메모리
  가드 단위 + 429 실발동·버킷 분리·health 면제·비활성 통합). 라이브 서버 — 한도 3에서
  4번째 `HTTP 429` + `Retry-After: 60` + JSON 본문, `/health` 5연속 200(면제) 확인.
- **콤보박스**: `npm run gate` exit 0(lint·tsc·vitest 30·build·css compile), a11y e2e 4종
  `VERDICT: PASS`, selftest 변이 7건 검출. 프로덕션 서버 대상 키보드 내비 라이브 9/9 PASS
  (role·listbox·ArrowDown→activedescendant·aria-selected·Escape·Enter 선택="서울, 대한민국").
- **Pydantic**: ruff format/check 통과, pytest 295, `PydanticDeprecated` 경고 6→0.
- **recharts**: 전수 검색 소스 참조 0, gate exit 0, 번들 크기 불변.
- **직접 스모크(회귀 아님을 실증)**: 만세력 CLI 사주명식 정상 산출, API `/api/manseol`이
  14개 데이터 키 전체 반환, `/result`·`/chat` 무데이터 직접 진입 시 빈 상태 + "홈으로 가기"
  (JS 에러 0), iconify 아이콘 23개 중 21개 `aria-hidden=true`·2개 `aria-label`(장식/의미 분리
  올바름 — devlog 열린 질문 해소).

## 독립 검증 게이트 (verifier subagent)

완성 판정 전 verifier subagent를 동기 실행해 6커밋을 독립 재검증했다(에이전트 자가보고
불신, 클린 상태 재실행). 결과: **"Production-complete / shippable — no hard BLOCKERs"**,
8게이트 GREEN 독립 재확인, 레이트리밋 슬라이딩 윈도우 수학·동시성(Lock, await 없는 임계
구역)·CORS-on-429 런타임 확인, 콤보박스 ARIA·선택 경로 정상, 시크릿 누출 없음.

지목한 실재 WARNING 1건(LLM 경로 요청 본문 무제한, `api/schemas.py`)을 후속 커밋
`0d44526`으로 마감했다 — `RequestSizeLimitMiddleware`(Content-Length 512KB 상한, 413) +
`message` max_length=4000 + 콤보박스 Enter 상한 가드. pytest 300 passed, 라이브 413 확인.

## 남은 것 (정직하게)

- **인증 미구현은 의도**. 익명 사주 앱이라 계정을 두지 않았다. 사용자별 쿼터·감사 로그가
  필요해지면 재검토. 지금은 레이트리밋이 방어선.
- **레이트리밋은 프로세스 로컬**. 단일 인스턴스(Railway 무료 티어)엔 충분하나, 수평 확장 시
  인스턴스마다 독립 카운터 → 정밀 제한은 Redis 백엔드가 후속 과제.
- **절기 경계 ~9h 시스템 오프셋**은 그대로. 출생·현행 계산이 동일 규약이라 서비스 내부
  자기 일관적이며, 절대 정합화는 후속(README 알려진 한계 유지).
- **스크린리더 수동 낭독 품질**은 여전히 기계 판정 불가 — DOM 계약까지만 실측.
- **httpx StarletteDeprecation** 1건은 FastAPI TestClient 내부(서드파티), 우리 코드 아님.

## Provenance

- Snapshot: [2026-07-23_23-27-19_service-completion-pass.sync-snapshot.json](./2026-07-23_23-27-19_service-completion-pass.sync-snapshot.json)
