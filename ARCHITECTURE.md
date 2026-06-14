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
- `POST /api/manseol` - 사주 계산
- `POST /api/chat` - AI 대화
- `POST /api/analysis` - 상세 분석

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
└── lib/
    └── api/          # API 클라이언트
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
                    |   Redis     |
                    | (Sessions)  |
                    +-------------+
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

### Frontend
- Node.js 18+
- Next.js 14.2+
- React 18.3+
- TypeScript 5.0+
