# Stage: docs-drift — 문서와 코드의 정합성

## Question
문서가 코드의 현재 상태를 정확히 기술하는가? 드리프트한 서술은 어디이고, 그중 무엇이 **해롭게** 오도하는가?

## Evidence

| Source | Why it matters | Check |
|--------|----------------|-------|
| `web/lib/constants/elements.ts:8,14,20,26,32` | 오행 hex 도메인 SSOT | 목 `#16A34A`·화 `#DC2626`·토 `#D97706`·금 `#64748B`·수 `#2563EB` |
| `web/.design-sync/conventions.md:46-47,50` | 디자인 에이전트가 읽는 규칙서 | 토 `#ca8a04`·금 `#71717a`·"하드 오프셋" |
| `web/.design-sync/guidelines/02-oheng-color-system.md:10,18-19,23-28,33` | 오행 색 전용 가이드 | 낡은 hex + "primary 바이올렛" + 원색 텍스트/보더 지시 |
| `web/.design-sync/NOTES.md:73-75` | 동일 드리프트를 이미 인지·정정한 기록 | tokens.css만 고쳤고 산문은 누락 |
| `api/routes/*.py`, `api/server.py:116-128` | 엔드포인트 실체 | 12개 전부 문서와 일치 |

## Findings

| Finding | Verdict | Evidence | Scope |
|---------|---------|----------|-------|
| **`guidelines/02`가 ink 규칙을 정면으로 위반하도록 지시한다.** "테두리 50%", `text-element-fire`, `border-element-fire/30`을 권장하는데 `DESIGN.md:124-126`은 원색 텍스트와 `/50` 보더를 명시적으로 금지한다. **ink 언급 0건.** 이 문서의 독자는 사람이 아니라 디자인 에이전트다 — 에이전트가 이걸 근거로 코드를 생성하면 방금 4라운드에 걸쳐 고친 접근성 회귀가 조용히 재유입된다 | `confirmed` | `guidelines/02:23-28` ↔ `DESIGN.md:124-126` ↔ `globals.css:104-118`(실제는 `*-ink`+`border-border`); `grep -c "ink"` = 0 | architectural |
| **오행 토·금 hex가 두 문서에서 낡았다.** 토 `#ca8a04`(실제 `#D97706`), 금 `#71717a`(실제 `#64748B`) | `confirmed` | `conventions.md:46-47`, `guidelines/02:18-19,33` ↔ `elements.ts:20,26` | cross-file |
| **같은 드리프트를 이미 인지하고 고쳤는데 산문 문서만 놓쳤다.** `NOTES.md:73-75`가 "tokens.css의 `#ca8a04→#d97706`, `#71717a→#64748b` 정정"을 기록하고 `tokens.css:37-38`은 실제로 고쳐져 있다. **반복되는 실패 모드** — 기계가 읽는 파일만 고치고 산문은 남는다 | `confirmed` | `NOTES.md:73-75` ↔ `tokens.css:37-38`(고침) vs `conventions.md:46-47`(안 고침) | architectural |
| **`conventions.md` 자기모순**: `:22`의 상태색 warning `#d97706`(정확)과 `:46`의 오행 토 `#ca8a04`가 충돌한다. `DESIGN.md:136`이 earth == warning으로 못박은 상태 | `confirmed` | `conventions.md:22` vs `:46`; `DESIGN.md:136` | single-case |
| **"primary 바이올렛" — 두 팔레트 전의 잔재.** 현재 primary는 스카이블루 `#49B6E5` | `confirmed` | `guidelines/02:10` ↔ `tailwind.config.ts:25` | single-case |
| **"하드 오프셋 그림자" 서술이 낡았다.** 실제 shadow 3종은 전부 블러 소프트다. `guidelines/01:32`는 반대로 "하드 오프셋은 쓰지 않는다"고 해 두 문서가 모순 | `confirmed` | `README.md:493`·`conventions.md:50` ↔ `tailwind.config.ts:88-93`, `globals.css:39` | cross-file |
| **존재하지 않는 컴포넌트 6종을 4개 문서가 나열한다** — FourPillarsDisplay·PillarCard·FiveElementsChart·TenGodsDistribution·StrengthMeter·FortuneCycleTimeline. 실제 `result/`는 13개이고 이들은 없다 | `confirmed` | `conventions.md:56-59`, `guidelines/01:40`, `guidelines/02:29`, `NOTES.md:111-113` ↔ `components/result/` | cross-file |
| **고아 프리뷰 5개 — 문서가 아니라 코드 이슈다.** `previews/FiveElementsChart.tsx` 등이 사라진 export를 `from "forceteller-web"`으로 import한다. `config.json:22-32`도 5종 override를 유지 | `confirmed` | `previews/{FiveElementsChart,FourPillarsDisplay,StrengthMeter,TenGodsDistribution,FortuneCycleTimeline}.tsx` | architectural |
| **BottomNav·MotionProvider·`lib/hooks/`가 구조 문서에 전무하다.** `layout/`은 "Sidebar"만 나열하고 `lib/` 목록에 `hooks/`가 없다. 전체 `.md` grep에서 BottomNav·MotionProvider가 devlog 제외 0건 | `confirmed` | `README.md:118,126-131,501-502`, `ARCHITECTURE.md:158,163-165` ↔ `layout.tsx:3-5,63,67` | cross-file |
| **"모바일은 사이드바 collapse"가 오도한다.** 모바일에서 Sidebar는 완전히 숨겨지고 BottomNav가 대체한다 | `confirmed` | `guidelines/01:38` ↔ `Sidebar.tsx:13`(`hidden…lg:flex`), `BottomNav.tsx:19`(`lg:hidden`) | single-case |
| **API 엔드포인트 12개가 전부 일치한다** — 경로·메서드·이름 드리프트 0 | `confirmed` | `README.md:339-392`, `ARCHITECTURE.md:140-145` ↔ `manseol.py`·`chat.py`·`analysis.py`·`server.py` | cross-file |
| **실행 명령·버전이 전부 일치한다.** npm scripts 5종 실재, ruff 일원화, vitest 21개 정확, 버전 1.0.0 양쪽 동일 | `confirmed` | `package.json:6-10`, `pyproject.toml:4,55-56,100`, `config/version.py:7` | cross-file |
| **십성 램프 10 hex와 오행 hex가 `DESIGN.md`·`README.md`·`web/README.md`에서 정확하다** | `confirmed` | `DESIGN.md:146-150` ↔ `ElementDistribution.tsx:52-56` | cross-file |
| `NOTES.md:116-121`의 "Bangers 워드마크" 검증 기록이 같은 파일 `:49-53`의 "Bangers 삭제·Delius 교체 완료"와 모순. 다만 해당 섹션 제목이 "2026 tetris 리디자인"이라 **의도된 이력 기록**일 수 있다 | `plausible` | `NOTES.md:116-121` vs `:49-53` | single-case |

## Risks / Ambiguities

- **`web/.design-sync/**`의 독자는 사람이 아니라 디자인 에이전트다.** 이것이 이 stage에서 가장 중요한 사실이다. 낡은 hex와 ink 위반 지시가 남아 있으면, 다음 디자인 작업이 `#ca8a04`와 `text-element-fire`를 생성해 **접근성 회귀를 자동으로 재유입**시킨다. 사람이 읽는 문서의 오타와는 위험도가 다르다.
- **`TenGodsDistribution`은 타입으로는 실재한다**(`web/types/saju.ts`). `conventions.md:65`가 props 타입으로 언급한 것은 정확하고 `:57`이 `result/` 컴포넌트로 나열한 것만 틀렸다. **일괄 삭제하면 안 된다.**
- **고아 프리뷰 5개가 design-sync 빌드를 실제로 깨뜨리는지는 빌드를 돌려야 확정된다.** import 대상이 부재하는 것은 확정이다.
- pytest 278개 주장은 실행 없이 확정 불가라 드리프트로 보고하지 않았다(테스트 함수 202개 + parametrize 전개 가능).

## Next Local Checks

1. `conventions.md:46-47`, `guidelines/02:18-19,33`의 토·금 hex 정정 — `NOTES.md:73-75`가 이미 정한 방향과 동일.
2. **`guidelines/02` 전면 개정** — ink 토큰 도입, `border-border` 규칙, "테두리 50%"·`border-element-*/30` 삭제, "바이올렛"→"스카이".
3. `README.md:493`·`conventions.md:50`의 "하드 오프셋" → "소프트 페이퍼 그림자".
4. 부재 컴포넌트 6종 제거(4개 문서 + `config.json:22-32`). `types/saju.ts`의 동명 타입은 보존.
5. `previews/` 고아 5개 삭제 여부 판단 — design-sync 빌드로 실패 재현 후 결정.
6. `README.md`·`ARCHITECTURE.md`에 BottomNav·MotionProvider·`lib/hooks/` 추가.
7. `guidelines/01:38`의 "사이드바 collapse" → "lg 미만에서 Sidebar 숨김 + BottomNav".
