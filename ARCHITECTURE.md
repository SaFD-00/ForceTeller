# ForceTeller Architecture

## System Overview

ForceTeller는 사주명리학 기반 AI 운세 분석 플랫폼입니다. 크게 세 개의 주요 계층으로 구성됩니다:

1. **Presentation Layer**: Next.js 14 프론트엔드
2. **Application Layer**: FastAPI 백엔드 + LangGraph 에이전트
3. **Domain Layer**: 만세력 계산 엔진

```
+------------------+     +------------------+     +------------------+
|   Next.js 14     |     |    FastAPI       |     |   LLM APIs       |
|   (Frontend)     | --> |    (Backend)     | --> |  (OpenRouter)    |
+------------------+     +------------------+     +------------------+
                               |
                               v
                    +------------------+
                    |  Manseol Engine  |
                    | (Saju Calculator)|
                    +------------------+
```

## Core Components

### 1. Manseol Engine (`manseol/`)

천문학적 정확도의 사주 계산 엔진입니다.

```
manseol/
├── calculator/           # 사주 계산기
│   ├── pillar_engine.py  # 년월일시주 계산
│   ├── ten_gods.py       # 십성 계산
│   ├── shensha.py        # 신살 계산
│   └── fortune_cycle.py  # 대운 계산
├── core/                 # 천문 계산
│   ├── astronomical.py   # PyEphem 기반 진태양시
│   ├── solar_terms.py    # 24절기
│   └── time_correction.py
└── analysis/             # 해석 엔진
    ├── yongsin/          # 용신 분석
    └── schools/          # 학파별 해석
```

**Key Features:**
- PyEphem 기반 진태양시 보정
- 경도/균시차/서머타임 자동 계산
- 양력/음력/윤달 완벽 지원
- 5개 학파 해석 비교

### 2. AI Agent Framework (`agents/`)

LangGraph 기반 멀티에이전트 시스템입니다.

```
agents/
├── graph.py          # StateGraph 빌드
├── nodes.py          # 노드 함수
├── state.py          # AgentState (TypedDict)
├── schemas.py        # Pydantic 스키마
├── llm.py            # OpenRouter LLM 추상화
├── orchestrator.py   # 그래프 실행 + 모델 주입
└── agent_configs.py  # 8개 에이전트 설정
```

#### Agent Graph Architecture (Supervisor Pattern)

```
                    +-----------+
                    |   START   |
                    +-----+-----+
                          |
                          v
                    +-----------+
           +------->| supervisor|<--------+
           |        +-----+-----+         |
           |              |               |
           |   +----------+----------+    |
           |   |          |          |    |
           v   v          v          v    |
    +----------+ +----------+ +----------+|
    |personality| | career   | | health  ||
    +-----+----+ +-----+----+ +----+-----+|
          |            |           |      |
          +------------+-----------+------+
                       |
                       v
                 +-----------+
                 | synthesis |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 |    END    |
                 +-----------+
```

**Agents (8 types):**
| Agent | Focus |
|-------|-------|
| personality | 성격, 기질, 성향 |
| career | 직업, 재물, 사업 |
| relationship | 연애, 결혼, 대인관계 |
| health | 건강, 체질 |
| fortune | 대운, 세운, 시기 |
| yongsin | 용신, 희신, 기신 |
| school_compare | 유파별 해석 비교 |
| synthesis | 종합 해석 |

#### State Management

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # 메시지 누적
    saju_data: dict[str, Any]          # 사주 데이터 (불변)
    current_agent: str                  # 현재 에이전트
    next_agent: Optional[str]           # 다음 에이전트 (라우팅)
    interpretations: dict[str, dict]    # 해석 결과 누적
    iteration: int                      # 반복 카운터
    final_output: Optional[str]         # 최종 출력
    error: Optional[str]                # 에러 정보
```

### 3. API Layer (`api/`)

FastAPI 기반 REST API입니다.

```
api/
├── routes/
│   ├── chat.py       # 채팅 엔드포인트
│   ├── manseol.py    # 사주 계산 엔드포인트
│   └── analysis.py   # 분석 엔드포인트
├── schemas.py        # Pydantic 모델
└── server.py         # FastAPI 앱
```

**Endpoints:**
- `POST /api/manseol` - 사주 계산 (`api/converters.py:enrich_with_analysis`로 용신 4방법·개운법·5학파·운세점수를 응답에 보강. interactions·sewun은 json_exporter가 직접 산출)
- `POST /api/chat` - AI 대화
- `POST /api/chat/stream` - 스트리밍 대화 (focus 지정 시 에이전트별 프롬프트, 없으면 `agents.nodes.route_question`의 RouterDecision 라우팅 → `agent_selected` SSE 이벤트로 출처·신뢰도 전달)
- `POST /api/analysis` - 상세 분석

> **계산 vs 분석 분리:** 결정론 계산(사주팔자·상호작용·세운)은 `manseol/output/json_exporter.py`에서, 해석 라이브러리(용신·유파·운세) 조립은 API 계층의 `enrich_with_analysis`에서 `SajuDataConverter.to_analysis_format` 입력으로 수행한다. `/api/manseol` 응답 `data`는 `Dict`이므로 스키마 변경 없이 키를 주입해 노출한다.

### 4. Frontend (`web/`)

Next.js 14 App Router 기반 프론트엔드입니다.

```
web/
├── app/              # App Router
├── components/
│   ├── result/       # 결과 표시 (14개)
│   ├── chat/         # 채팅 UI (10개)
│   └── ui/           # 재사용 UI (8개)
├── stores/
│   └── sajuStore.ts  # Zustand 상태관리
├── lib/
│   └── api/          # API 클라이언트
├── .design-sync/     # claude.ai/design 디자인시스템 동기화 (synth-entry 번들)
└── .ds-css/          # design-sync용 Tailwind v3 정적 CSS 컴파일
```

**Key Design:**
- **컴포넌트 순수 props-driven**: result/chat 컴포넌트 대부분이 store 비결합 → 프리뷰·재사용·테스트 용이.
- **UI 테마(tetris-refined 블록)**: [typeui.sh `tetris`](https://www.typeui.sh/design-skills/tetris) 기반 — 쿨블루 배경 + 비비드 퍼플 강조 + 딥네이비 잉크 + 하드 오프셋(솔리드) 그림자 + 1.5px 블록 테두리. 폰트 Pretendard(본문)·Bangers(라틴 디스플레이)·JetBrains Mono(숫자·간지). 브랜드 마스코트 **"별이"**(`components/ui/Mascot.tsx`, 별·달 점성술사)가 채팅 아바타·로딩·설명봇·로고에 재사용된다.
- **design-sync**: 앱을 DS 패키지처럼 synth-entry로 번들해 claude.ai/design에 게시한다(업로드는 별도 승인 단계). process shim·next/navigation no-op stub·framer-motion skipAnimations로 정적 헤드리스 렌더를 보정. 상세 재현 노트는 `web/.design-sync/NOTES.md`.

### 5. Persistence Layer (`db/`)

SQLAlchemy 2.0 비동기 기반 영속화 계층입니다. 세션·대화·사주결과가
서버 재시작과 TTL을 넘어 유지됩니다.

```
db/
├── base.py        # 비동기 엔진·async_sessionmaker·Base·init_models
├── models.py      # SessionORM, MessageORM (JSON 컬럼, PG=JSONB variant)
└── repository.py  # SessionRepository (async CRUD, dataclass↔ORM 변환)

conversation/
└── db_session_manager.py  # DBSessionManager (SessionManagerProtocol async 구현)

migrations/        # Alembic (env.py 비동기, versions/0001_initial.py)
```

**Key Design:**
- **DB 단일 진실원천**: 인메모리 캐시 없음. 엔드포인트가 받은 `Session` 객체를 직접 변형한 뒤
  `await sm.save_session(session)`로 명시적 flush 해야 영속된다(chat 3곳·analysis 1곳).
- **Postgres(배포) + SQLite(로컬) 동일 코드**: `settings.DATABASE_URL`로 전환
  (`sqlite+aiosqlite:///...` / `postgresql+asyncpg://...`). JSON 컬럼은 PG에서 JSONB variant.
- **`Session`/`Message` dataclass 유지**: `conversation.context_builder`·프롬프트 빌드는 무변경.
  `DBSessionManager`는 DB row ↔ dataclass 변환만 담당.
- **스키마**: `sessions`(session_id PK, saju_data/interpretation_cache/metadata JSON, created_at, last_activity 인덱스),
  `messages`(id PK, session_id FK ON DELETE CASCADE, seq, role, content, metadata, timestamp).
- **마이그레이션**: 운영은 Alembic(`alembic upgrade head`, Docker CMD에 포함)이 진실원천.
  `init_models()`(create_all)는 로컬·테스트 부트스트랩용.

```
api/routes/{chat,analysis}  --await-->  DBSessionManager  -->  SessionRepository
                                                                     |
                                              SQLAlchemy async (asyncpg / aiosqlite)
```

## Data Flow

### 1. Saju Calculation Flow

```
[User Input]
    |
    v
[API: /api/manseol]
    |
    v
[Manseol Engine]
    |
    +-- pillar_engine.py --> 사주팔자 계산
    +-- ten_gods.py --> 십성 계산
    +-- shensha.py --> 신살 계산
    +-- fortune_cycle.py --> 대운 계산
    |
    v
[SajuResult Model]
    |
    v
[JSON Response]
```

### 2. AI Interpretation Flow

```
[User Question]
    |
    v
[API: /api/chat]
    |
    v
[Orchestrator]
    |
    v
[LangGraph StateGraph]
    |
    +-- supervisor_node --> 에이전트 선택
    +-- interpreter_node --> 해석 수행
    +-- synthesis_node --> 종합 해석
    |
    v
[Structured Output (Pydantic)]
    |
    v
[JSON Response]
```

## Key Design Decisions

### 1. LangGraph Supervisor Pattern

**Why:**
- 동적 에이전트 선택이 필요
- 사용자 질문에 따라 다른 에이전트 조합
- 종합 해석을 위한 멀티 에이전트 협업

**Benefits:**
- 상태 기반 제어 흐름
- 체크포인팅을 통한 대화 지속
- 구조화된 출력 보장

### 2. Pydantic Structured Output

**Why:**
- LLM 응답의 일관성 보장
- 타입 안전한 데이터 처리
- 모든 OpenRouter 모델 공통 스키마 (json_schema 강제 + tenacity 재시도)

**Schemas:**
```python
class InterpretationResult(BaseModel):
    interpretation: str
    confidence: float
    suggested_questions: list[str]

class RouterDecision(BaseModel):
    next_agent: str
    reasoning: str
```

### 3. OpenRouter 단일 게이트웨이 (Model-Agnostic LLM Layer)

**Why:**
- OpenRouter는 OpenAI 호환 API → 하나의 클라이언트로 6개 모델 전환
- 무료 모델(gpt-oss, gemma-4) 기본 → 비용 0
- 모델 폴백 체인으로 장애 대응

**Implementation:**
```python
def create_llm(model: str | None = None, temperature: float = 0.7) -> BaseChatModel:
    return ChatOpenAI(
        model=model or settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,  # https://openrouter.ai/api/v1
        ...
    )
```

요청별 모델은 API → Orchestrator → LangGraph `config["configurable"]["model"]` 로
각 노드에 주입된다. 스트리밍은 `utils/llm_client.OpenRouterClient`(AsyncOpenAI)가
`delta.reasoning`을 읽어 reasoning/output을 분리 전송한다.

### 4. True Solar Time Correction

**Why:**
- 사주 계산의 정확도는 출생 시간에 의존
- 도시별 경도 차이 → 최대 30분 오차
- 균시차 → 최대 16분 오차

**Implementation:**
- PyEphem 천문 라이브러리
- 도시별 좌표 데이터베이스
- 한국 표준시 역사 반영

## Scalability Considerations

### Current Architecture (Single Instance)

```
[Vercel] --> [Railway (Single)] --> [OpenRouter]
```

### Future Architecture (Multi-Instance)

세션이 DB에 영속되므로(무상태 API), 다중 인스턴스로 수평 확장이 가능합니다.

```
                    +-------------+
                    | Load Balancer|
                    +------+------+
                           |
           +---------------+---------------+
           |               |               |
    +------+------+ +------+------+ +------+------+
    | API Pod 1   | | API Pod 2   | | API Pod 3   |
    +------+------+ +------+------+ +------+------+
           |               |               |
           +---------------+---------------+
                           |
                    +------+------+
                    | PostgreSQL  |
                    | (Sessions)  |   ← 영속화 (현재 토대 구축 완료)
                    +-------------+
                    (+ Redis 캐시는 후속 선택)
```

## Security Considerations

1. **API Key Protection**: 환경 변수로 관리
2. **CORS**: 허용 도메인 명시적 설정
3. **Rate Limiting**: API 요청 제한 (미구현)
4. **Input Validation**: Pydantic 스키마 검증

## Dependencies

### Backend
- Python 3.11+
- FastAPI 0.110+
- LangGraph 0.x
- LangChain 0.3+
- PyEphem 4.1+
- SQLAlchemy 2.0+ (async) · Alembic 1.13+
- asyncpg (PostgreSQL) · aiosqlite (SQLite) · greenlet

### Frontend
- Node.js 18+
- Next.js 14.2+
- React 18.3+
- TypeScript 5.0+
