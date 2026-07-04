# ForceTeller

사주명리학 기반 AI 운세 분석 플랫폼

## 개요

ForceTeller는 정확한 만세력 계산과 AI 해석을 결합한 사주팔자 분석 서비스입니다. 천문학적 진태양시 보정, 오행 분석, 십성 분포, 대운 흐름, 용신 선정 등 전문적인 사주 분석 기능을 제공하며, 8개의 전문 AI 에이전트를 통해 맞춤형 해석을 제공합니다.

## 프로젝트 구조

```
./
├── api/                          # FastAPI 백엔드
│   ├── routes/
│   │   ├── chat.py               # 채팅/대화 엔드포인트
│   │   ├── manseol.py            # 사주 계산 엔드포인트
│   │   └── analysis.py           # 분석 엔드포인트
│   ├── converters.py             # 데이터 변환 유틸 (enrich_with_analysis)
│   ├── dependencies.py           # 의존성 주입
│   ├── errors.py                 # 오류 응답 헬퍼 (예외 상세 DEBUG 게이팅)
│   ├── formatters.py             # 응답 포맷팅
│   ├── schemas.py                # Pydantic 데이터 모델
│   └── server.py                 # FastAPI 앱 설정
│
├── manseol/                      # 만세력 계산 엔진
│   ├── calculator/               # 사주 계산기
│   │   ├── pillar_engine.py      # 사주팔자(년월일시주) 계산
│   │   ├── ten_gods.py           # 십성(十星) 계산
│   │   ├── shensha.py            # 신살(神殺) 계산
│   │   ├── hidden_stems.py       # 지장간(地藏干) 계산
│   │   ├── twelve_phases.py      # 십이운성(十二運星) 계산
│   │   ├── fortune_cycle.py      # 대운(大運) 계산
│   │   ├── current_fortune.py    # 현재 연운·월운·일운 (단일 진실 공급원)
│   │   └── interactions.py       # 오행/지지 상호작용
│   ├── core/                     # 핵심 유틸리티
│   │   ├── astronomical.py       # PyEphem 천문 계산
│   │   ├── solar_terms.py        # 24절기 계산
│   │   ├── time_correction.py    # 진태양시 보정
│   │   └── calendar_converter.py # 양력/음력 변환
│   ├── data/                     # 참조 데이터
│   │   ├── stems_branches.py     # 천간/지지 데이터
│   │   ├── lunar_data.py         # 음력 데이터
│   │   ├── city_coordinates.py   # 도시 좌표
│   │   ├── korean_names.py       # 한글 이름 데이터
│   │   └── kst_history.py        # 한국 표준시 역사
│   ├── analysis/                 # 해석 엔진
│   │   ├── fortune/analyzer.py   # 운세 분석
│   │   ├── schools/              # 사주 학파
│   │   │   ├── base_interpreter.py
│   │   │   ├── ziping.py         # 자평명리(子平命理)
│   │   │   ├── dts.py            # 적천수(滴天髓)
│   │   │   ├── qtbj.py           # 궁통보감(窮通寶鑑)
│   │   │   ├── shensha.py        # 신살중심(神煞中心)
│   │   │   ├── modern.py         # 현대명리
│   │   │   └── comparator.py     # 학파 비교
│   │   └── yongsin/              # 용신(用神) 분석
│   │       ├── base.py           # 용신 기본 클래스
│   │       ├── strength.py       # 일간 강도
│   │       ├── selector.py       # 용신 선정
│   │       ├── seasonal.py       # 계절 조정
│   │       ├── mediation.py      # 오행 조정
│   │       ├── disease.py        # 건강 지표
│   │       └── recommendations.py
│   ├── models/                   # 데이터 모델
│   │   ├── input_model.py        # 입력 검증
│   │   └── saju_result.py        # 결과 모델
│   ├── output/
│   │   └── json_exporter.py      # JSON 출력
│   └── cli.py                    # CLI 인터페이스
│
├── agents/                       # AI 해석 에이전트 (LangGraph 기반)
│   ├── graph.py                  # LangGraph StateGraph 빌드
│   ├── nodes.py                  # 노드 함수 (supervisor, interpreter, synthesis)
│   ├── state.py                  # TypedDict 기반 상태 정의
│   ├── schemas.py                # Pydantic 응답 스키마
│   ├── llm.py                    # OpenRouter LLM 추상화 (LangChain ChatOpenAI)
│   ├── orchestrator.py           # Orchestrator (모델→그래프 config 주입)
│   ├── agent_configs.py          # 8개 에이전트 설정
│   ├── config.py                 # AgentConfig 데이터클래스
│   └── prompts/
│       └── system_prompts.py     # LLM 시스템 프롬프트
│
├── conversation/                 # 세션 관리
│   ├── session_manager.py        # Session/Message dataclass + 인메모리 매니저(레거시)
│   └── db_session_manager.py     # DB 백엔드 세션 매니저 (영속화, async)
│
├── db/                           # DB 영속화 (SQLAlchemy 2.0 async)
│   ├── base.py                   # 비동기 엔진·세션 팩토리·Base
│   ├── models.py                 # SessionORM, MessageORM
│   └── repository.py             # SessionRepository (async CRUD)
│
├── migrations/                   # Alembic 마이그레이션 (env.py 비동기)
│   └── versions/                 # 0001_initial.py …
│
├── config/                       # 설정
│   ├── settings.py               # Pydantic 환경 설정
│   ├── constants.py              # 도메인 상수
│   ├── logging_config.py         # 로깅 설정
│   └── version.py                # 버전 단일 상수 (__version__, pyproject와 동기)
│
├── utils/
│   ├── llm_client.py             # OpenRouter 클라이언트 (스트리밍/reasoning)
│   └── protocols.py              # 타입 프로토콜 정의
│
├── tests/                        # 테스트 (pytest, unit/integration)
│   ├── unit/                     # 단위 테스트
│   └── integration/              # 통합 테스트 (api/)
│
├── web/                          # Next.js 14 프론트엔드
│   ├── app/
│   │   ├── page.tsx              # 홈 페이지
│   │   ├── layout.tsx            # 루트 레이아웃
│   │   ├── result/page.tsx       # 결과 표시
│   │   └── chat/page.tsx         # 채팅 인터페이스
│   ├── components/
│   │   ├── hero/                 # 랜딩 히어로 섹션
│   │   ├── features/             # 기능 그리드
│   │   ├── layout/               # Sidebar (아이콘 내비게이션)
│   │   ├── result/               # 결과 표시 (13개 컴포넌트)
│   │   ├── chat/                 # 채팅 UI (8개 컴포넌트)
│   │   └── ui/                   # 재사용 UI (9개 컴포넌트)
│   ├── data/
│   │   └── saju-glossary.ts      # 사주 용어 사전
│   ├── stores/
│   │   └── sajuStore.ts          # Zustand 상태관리
│   ├── lib/
│   │   ├── api/                  # API 클라이언트 (client·manseol·chat)
│   │   ├── constants/            # 프론트엔드 상수
│   │   ├── ganji.ts              # 간지(干支) 표시 사전 (인덱스→한글/한자/오행)
│   │   ├── transforms.ts         # 데이터 변환
│   │   └── utils.ts              # 유틸리티
│   ├── types/
│   │   └── saju.ts               # TypeScript 타입
│   ├── next.config.js            # rewrites 프록시 (API_PROXY_TARGET)
│   ├── package.json
│   └── tailwind.config.ts
│
├── main.py                       # CLI 진입점
├── pyproject.toml                # 프로젝트 메타데이터·의존성·도구 설정
├── uv.lock                       # 의존성 잠금 파일 (uv)
└── README.md
```

## 기술 스택

### 백엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.11+ | 런타임 |
| uv | 0.11+ | 패키지·가상환경 관리 |
| FastAPI | 0.110 | REST API 프레임워크 |
| Pydantic | 2.0 | 데이터 검증 |
| Uvicorn | 0.27 | ASGI 서버 |
| LangGraph | 0.2+ | 에이전트 그래프 (Supervisor 패턴) |
| langchain-core | 0.3+ | 메시지·러너블 추상화 |
| langchain-openai | 0.2+ | OpenRouter 연동 (OpenAI 호환 ChatOpenAI) |
| OpenAI SDK | 1.0+ | OpenRouter Chat Completions 클라이언트 (스트리밍) |
| SQLAlchemy | 2.0+ | 비동기 ORM (세션·대화 영속화) |
| Alembic | 1.13+ | DB 마이그레이션 |
| PyEphem | 4.1 | 천문 계산 |
| Korean-Lunar-Calendar | 0.3 | 음력 변환 |
| Click | 8.0 | CLI 프레임워크 |
| Rich | 13.0 | 터미널 포맷팅 |

### 프론트엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | 14.2 | App Router 프레임워크 |
| React | 18.2 | UI 라이브러리 |
| TypeScript | 5.0 | 타입 안전성 |
| Tailwind CSS | 3.4 | 스타일링 |
| Zustand | 4.5 | 상태관리 |
| Recharts | 2.14 | 데이터 시각화 |
| Framer Motion | 11.0 | 애니메이션 |
| Iconify (@iconify/react) | 5.0 | 아이콘셋 |
| React Markdown | 10.1 | 마크다운 렌더링 (remark-gfm) |
| Vitest | 4.1 | 단위 테스트 (lib 순수 함수) |

## 주요 기능

### 1. 만세력 계산
- **사주팔자 산출**: 년주, 월주, 일주, 시주 정확 계산
- **진태양시 보정**:
  - 경도 보정 (도시별 좌표)
  - 균시차(均時差) 계산
  - 서머타임 적용
  - 한국 표준시 역사 반영
- **달력 지원**: 양력, 음력, 윤달 완벽 지원
- **자시 구분**: 조자시/야자시 옵션

### 2. 사주 분석
| 분석 항목 | 설명 |
|-----------|------|
| 오행 분석 | 목/화/토/금/수 분포 및 균형 |
| 십성 분포 | 비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인 |
| 십이운성 | 각 오행별 12단계 생명 주기 |
| 신강/신약 | 일간 강도 분석 |
| 용신 | 용신/희신/기신 선정 |
| 대운 | 10년 주기 운세 흐름 |
| 신살 | 천을귀인, 문창귀인 등 길흉신 분석 |
| 지장간 | 지지 속 숨은 천간 분석 |

### 3. 학파별 해석 (5대 유파)
- **자평명리(子平命理)**: 일간 중심 강약 분석과 격국론 (연해자평)
- **적천수(滴天髓)**: 오행의 생극제화와 통변성정 (체용론)
- **궁통보감(窮通寶鑑)**: 월령과 조후 중심 해석 (난강망 계열)
- **현대명리**: 심리학적 관점의 실용적 재해석
- **신살중심(神煞中心)**: 신살 배합 중심의 길흉 판단

### 4. AI 에이전트 (8종, LangGraph Supervisor 패턴)

| 에이전트 | 분석 영역 |
|----------|-----------|
| personality | 성격, 특성, 장단점 |
| career | 직업, 재물, 적성 |
| relationship | 인연, 궁합, 결혼 시기 |
| health | 건강, 체질, 질병 취약점 |
| fortune | 운세, 시운, 길일 |
| yongsin | 용신 분석 및 조언 |
| school_compare | 학파별 해석 비교 |
| synthesis | 종합 분석 |

### 5. 대화형 상담
- 멀티턴 대화 지원
- 세션 기반 컨텍스트 유지
- 사주 데이터 기반 맞춤 해석
- 후속 질문 자동 추천
- 스트리밍 응답에 **에이전트별 전문 프롬프트 라우팅**(focus 지정 시 해당 에이전트, 없으면 RouterDecision 자동 선택)과 **출처·신뢰도 배지** 노출
- 스트리밍 시 현재 연/월/일운을 **매 메시지 서버 재계산**(절기 기반 월운). 세션 저장 스냅샷의 프론트 근사 대신 백엔드 단일 진실 공급원 사용
- 모든 해석 하단에 **면책 고지(Disclaimer)** 상시 표시 (참고용 콘텐츠 안내)
- 답변 생성 중 자동 스크롤은 **사용자가 채팅 하단(생성 영역)에 있을 때만** 동작(채팅 컨테이너 한정) — 사주 결과 등 다른 창이 끌려 내려가지 않음
- OpenRouter 6개 모델 지원 (gpt-oss / gemma-4 / deepseek-v4)

### 6. 결과 노출 (Phase 1 배선)
계산 엔진에 구현돼 있던 자산을 결과/응답에 노출:
- **합·충·형·파·해·공망** 상호작용 (천간합/충극, 지지 육합·삼합·방합·반합, 충/형/파/해, 공망)
- **세운(연운)**: 올해부터 향후 6년간 연도별 운세(간지·십성·12운성)
- **용신 4방법 비교**(강약/조후/통관/병약) + **개운법**(색/방위/직업/활동/생활습관)
- **5학파 비교 해석** + 학파 일치도(신뢰도) 배지
- **운세 유형별 점수**(종합/직업/재물/건강/애정) 대시보드
- **평생운 흐름**(10년 대운 내러티브) 리포트
- **현재 운세**(`current_fortune`) 및 슬라이더용 범위(`fortune_ranges`): 서버 KST 시각 기준 연/월/일운을 단일 진실 공급원으로 산출 (절기 기반, 프론트 재계산 제거)
- 출생시간 **시간 미상(時不知)** 입력 지원

## 시작하기

### 사전 요구사항
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (패키지·가상환경 관리)
- Node.js 18+
- OpenRouter API Key (https://openrouter.ai/keys)

### 백엔드 설치 및 실행

```bash
# uv 설치 (최초 1회, 이미 설치되어 있으면 생략)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경(.venv) 생성 + 의존성 설치 (dev 포함, 잠금 파일 기준)
uv sync

# 환경 설정
cp .env.example .env
# .env 파일 편집 (API 키 설정)

# DB 마이그레이션 (스키마 생성). DATABASE_URL 미설정 시 로컬 SQLite(./forceteller.db) 사용
uv run alembic upgrade head

# 서버 실행 (uv run은 .venv를 자동 활성화)
uv run python -m api.server
# 또는
uv run uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

> `uv sync`가 프로젝트 루트에 `.venv`를 생성합니다. 셸에서 직접 활성화하려면 `source .venv/bin/activate`를 사용하세요.
>
> **DB 영속화**: 세션·대화·사주결과가 DB에 영속되어 서버 재시작에도 유지됩니다.
> 로컬은 SQLite(기본), 배포는 `DATABASE_URL`에 PostgreSQL을 주입하세요
> (`postgresql+asyncpg://user:pass@host:5432/db`). 서버 기동 시 누락 테이블은 자동 생성되며,
> 스키마 변경 이력 관리는 Alembic(`alembic upgrade head` / `alembic revision --autogenerate`)을 사용합니다.

### 개발 (테스트·코드 품질)

```bash
# dev 의존성은 uv sync 시 기본 포함 (프로덕션만 원하면 uv sync --no-dev)
uv run pytest              # 테스트 실행 (278개)
uv run ruff check .        # 린트 (ruff로 일원화)
uv run ruff format .       # 포맷 (--check로 검사만)
uv run mypy .              # 타입 체크 (CI 비차단)

# 프론트엔드 (web/)
cd web && npm run lint     # ESLint
cd web && npm test         # Vitest 단위 테스트 (21개)

# 의존성 추가/제거
uv add <패키지>            # 런타임 의존성
uv add --dev <패키지>      # 개발 의존성
```

> 린트·포맷은 ruff로 일원화했습니다(black/isort 제거). CI는 `ruff check`·
> `ruff format --check`를 차단 게이트로, mypy는 정보성(비차단)으로 실행합니다.

### 프론트엔드 설치 및 실행

```bash
cd web

# 의존성 설치
npm install

# 환경 설정
cp .env.example .env.local
# NEXT_PUBLIC_API_URL 설정

# 개발 서버 실행
npm run dev
```

### CLI 사용

```bash
# 사주 계산
uv run python main.py cli --name "홍길동" --birth-date "1990-01-15" --birth-time "14:30" --gender male

# 대화형 모드
uv run python main.py interactive

# 서버 실행
uv run python main.py server --host 0.0.0.0 --port 8000 --reload

# 시스템 정보
uv run python main.py info
```

## API 엔드포인트

### 만세력 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/manseol` | 사주 계산 (응답 `data`에 결정론 계산으로 interactions·sewun·current_fortune·fortune_ranges, 분석 보강으로 yongsin_comparison·yongsin_recommendations·school_comparison·fortune_scores 포함) |
| POST | `/api/manseol/quick` | 빠른 계산 (쿼리 파라미터: name·birth_date·gender·birth_time) |
| GET | `/api/manseol/cities` | 도시 목록 (한글/영어 검색) |
| GET | `/api/manseol/city/{name}` | 도시 정보 |

**사주 계산 요청 예시:**
```json
{
  "name": "홍길동",
  "birth_date": "1990-01-15",
  "birth_time": "14:30",
  "calendar": "solar",
  "city": "Seoul",
  "gender": "male",
  "jajasi": false
}
```

### 채팅 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/chat` | AI 대화 (Supervisor 동적 라우팅) |
| POST | `/api/chat/stream` | 스트리밍 대화 (SSE, reasoning·출처/신뢰도 배지, 월운 서버 재계산) |
| GET | `/api/chat/sessions` | 세션 목록 |
| GET | `/api/chat/sessions/{id}` | 세션 상세 |
| DELETE | `/api/chat/sessions/{id}` | 세션 삭제 |
| POST | `/api/chat/sessions/{id}/clear` | 대화 기록 삭제 |

**채팅 요청 예시:** (`focus`는 선택 — 지정 시 해당 전문 에이전트, 생략 시 자동 라우팅)
```json
{
  "session_id": "uuid",
  "saju_data": { ... },
  "message": "제 적성에 맞는 직업은 무엇인가요?",
  "focus": "career"
}
```

### 분석 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/analysis` | 상세 분석 |
| GET | `/api/analysis/types` | 분석 유형·용신 방법·학파 코드 목록 |

### 시스템 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 헬스 체크 |
| GET | `/` | API 정보 |

## 환경 변수

### 백엔드 (.env)

```env
# OpenRouter API 키 (https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-...

# LLM 설정 (OpenRouter 단일 게이트웨이)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-oss-120b:free          # 기본 해석 모델
OPENROUTER_ROUTING_MODEL=openai/gpt-oss-20b:free   # 라우팅(경량) 모델
OPENROUTER_FALLBACK_MODEL=google/gemma-4-31b-it:free
OPENROUTER_MAX_TOKENS=4096
OPENROUTER_REASONING_EFFORT=medium                 # low | medium | high
OPENROUTER_TEMPERATURE=0.7

# 지원 모델: openai/gpt-oss-120b:free, openai/gpt-oss-20b:free,
#           google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free,
#           deepseek/deepseek-v4-flash, deepseek/deepseek-v4-pro
# OPENROUTER_ALLOWED_MODELS=...  # 요청 허용 모델 화이트리스트(콤마). 기본=지원 6종

# 서버 설정
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false                  # true일 때만 예외 상세를 응답에 노출
CORS_ORIGINS=*               # 콤마 구분 도메인. "*"이면 자격증명(credentials) 차단

# DB 영속화 (선택) — 미설정 시 로컬 SQLite. 배포 시 PostgreSQL 주입
# DATABASE_URL=postgresql+asyncpg://user:password@host:5432/forceteller

# 세션 설정
SESSION_MAX_HISTORY=20
SESSION_TIMEOUT_MINUTES=60      # 세션 TTL(분). 경과 시 조회 불가·정리
MAX_SESSIONS=100               # 인메모리 매니저 최대 동시 세션
SESSION_CLEANUP_PERCENTAGE=0.2 # 상한 초과 시 정리 비율
CONVERSATION_HISTORY_LIMIT=10  # LLM에 전달할 최근 대화 턴 수

# 로깅 설정
LOG_LEVEL=INFO                 # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# 만세력 설정
DEFAULT_CITY=Seoul
USE_TRUE_SOLAR_TIME=true
```

### 프론트엔드 (web/.env.local)

```env
# 런타임: 클라이언트가 호출할 백엔드 절대 URL. 배포 시 백엔드 도메인으로 오버라이드.
# 비워두면 동일 출처(/api/*)로 요청하고 아래 rewrite 프록시를 탄다.
NEXT_PUBLIC_API_URL=http://localhost:8000

# 빌드타임: next.config.js의 rewrites() 프록시 대상. NEXT_PUBLIC_API_URL을 비워
# 동일 출처로 호출할 때 /api/* 요청이 이 주소로 전달된다. 기본값 http://localhost:8000.
# API_PROXY_TARGET=http://localhost:8000
```

## 오행 색상 시스템

Tetris 디자인 시스템에 맞춘 오행별 시맨틱 색상(`web/lib/constants/elements.ts`):

| 오행 | 한자 | 색상 코드 | 의미 |
|------|------|-----------|------|
| 목(木) | 木 | `#16A34A` (Green) | 성장, 창조 |
| 화(火) | 火 | `#DC2626` (Red) | 열정, 활동 |
| 토(土) | 土 | `#D97706` (Amber) | 안정, 중재 |
| 금(金) | 金 | `#64748B` (Slate) | 결단, 정의 |
| 수(水) | 水 | `#2563EB` (Blue) | 지혜, 유연 |

## 프론트엔드 컴포넌트

### 결과 표시 컴포넌트 (13개, `components/result/`)
- `YearlyFortune` - 세운(연도별 운세) 카드
- `LuckyGuideCard` - 용신 개운법(색/방위/직업/생활)
- `SchoolComparison` - 5학파 일치도·비교 탭
- `FortuneScoreDashboard` - 운세 유형별 점수
- `LifetimeReport` - 평생운(10년 대운) 내러티브
- `PillarTable` - 사주팔자 주별 테이블
- `PentagonChart` - 오각형 강도 차트
- `ElementDistribution` - 오행 분포·균형
- `YongshinCard` - 용신 정보
- `ShenshaDetailCard` - 신살 정보
- `InteractionsTabs` - 오행 상호작용
- `FortuneCycleSlider` - 대운/현재 운세 슬라이더
- `StrengthDistributionChart` - 강도 분포

### 채팅 컴포넌트 (8개, `components/chat/`)
- `ChatContainer` - 메인 채팅 컨테이너
- `MessageList`, `MessageBubble` - 메시지 표시
- `ChatInput` - 사용자 입력
- `MarkdownRenderer` - 마크다운 렌더링
- `ReasoningDisplay` - AI 추론 과정 표시
- `SuggestedQuestions` - 추천 질문
- `AgentSelector` - 에이전트 선택

### UI 컴포넌트 (9개, `components/ui/`)
- `Button`, `Input` - 기본 입력
- `GlassCard` - 카드 표면 컨테이너
- `Icon` - 아이콘 래퍼
- `ElementBadge` - 오행 배지
- `GlossaryTooltip`, `GlossaryModal` - 용어 설명
- `Disclaimer` - 면책 고지 (결과·채팅 하단 상시)
- `LoadingOverlay` - 로딩 상태

### 레이아웃 컴포넌트 (`components/layout/`)
- `Sidebar` - 좌측 아이콘 내비게이션 (홈/결과/채팅)

> UI 테마: **Tetris 디자인 시스템** (블록 게임 감성의 고대비·놀이적 스타일,
> Bangers/JetBrains Mono 타이포). 토큰·팔레트는 [DESIGN.md](DESIGN.md) 참조.

## 데이터 상수 (config/constants.py)

프로젝트에서 사용하는 주요 상수들:

- **오행(五行)**: 목, 화, 토, 금, 수 정의 및 속성
- **천간(天干)**: 갑, 을, 병, 정, 무, 기, 경, 신, 임, 계
- **지지(地支)**: 자, 축, 인, 묘, 진, 사, 오, 미, 신, 유, 술, 해
- **오행 상생/상극**: 생극 관계 정의
- **육십갑자(六十甲子)**: 60갑자 및 각 조합의 비유
- **24절기**: 입춘부터 대한까지
- **신살 정의**: 길신/흉신 목록 및 설명
- **귀인성(貴人星)**: 천을귀인, 문창귀인 등

## 배포

### 배포 아키텍처

```
[사용자] → [Vercel (Next.js)] → [Railway (FastAPI)] → [OpenRouter API]
                                      ↓
                                [PostgreSQL (Railway)]  ← 세션·대화 영속화
```

- **프론트엔드**: Vercel (Next.js 최적화, 무료 티어)
- **백엔드**: Railway (월 $5 크레딧 무료)
- **DB**: Railway 관리형 PostgreSQL (세션·대화 영속). Docker 기동 시 `alembic upgrade head` 자동 실행.

### 1단계: GitHub 레포지토리 준비

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/forceteller.git
git push -u origin main
```

### 2단계: Railway 백엔드 배포

1. [railway.app](https://railway.app) 접속 → GitHub 로그인
2. **New Project** → **Deploy from GitHub repo** 선택
3. forceteller 레포지토리 선택
4. Settings에서 설정:
   - **Root Directory**: 프로젝트 루트 경로
   - **Build Command**: 자동 감지 (Dockerfile 사용)
5. **PostgreSQL 추가**: 프로젝트에서 **New** → **Database** → **Add PostgreSQL**.
   생성되면 같은 프로젝트의 서비스에서 `DATABASE_URL`을 참조할 수 있습니다.
6. Variables 탭에서 환경 변수 추가:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   OPENROUTER_MODEL=openai/gpt-oss-120b:free
   CORS_ORIGINS=https://your-app.vercel.app
   # PostgreSQL 플러그인의 연결 문자열을 asyncpg 드라이버 형식으로 지정
   DATABASE_URL=postgresql+asyncpg://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}
   ```
   > Railway 기본 `DATABASE_URL`은 `postgresql://` 스킴이라 그대로 쓰면 동기 드라이버를 찾습니다.
   > 반드시 `postgresql+asyncpg://` 형식으로 지정하세요. 컨테이너 기동 시 `alembic upgrade head`가 자동 실행됩니다.
7. Settings → Networking → **Generate Domain** 클릭
8. 생성된 도메인 복사 (예: `forceteller-xxx.railway.app`)

### 3단계: Vercel 프론트엔드 배포

1. [vercel.com](https://vercel.com) 접속 → GitHub 로그인
2. **Add New Project** → forceteller 레포지토리 선택
3. 설정:
   - **Root Directory**: `web` (또는 프론트엔드 경로)
   - **Framework Preset**: Next.js (자동 감지)
4. Environment Variables 추가:
   ```
   NEXT_PUBLIC_API_URL=https://forceteller-xxx.railway.app
   ```
5. **Deploy** 클릭

### Docker 로컬 실행

```bash
# 이미지 빌드
docker build -t forceteller-api .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e OPENROUTER_API_KEY=sk-or-v1-... \
  forceteller-api
```

### 환경 변수 (프로덕션)

| 변수 | 설명 | 예시 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API 키 | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | 기본 해석 모델 | `openai/gpt-oss-120b:free` |
| `CORS_ORIGINS` | 허용할 프론트엔드 도메인 | `https://your-app.vercel.app` |
| `NEXT_PUBLIC_API_URL` | 백엔드 API URL | `https://api.railway.app` |

### 예상 비용

| 서비스 | 무료 티어 |
|--------|-----------|
| Vercel | 100GB 대역폭/월, 무제한 배포 |
| Railway | $5 크레딧/월 (약 500시간) |
| OpenRouter | `:free` 모델(gpt-oss, gemma-4)은 무료 / deepseek-v4는 종량제 |

## 알려진 한계

- **인증·레이트리밋 미구현**: 현재 API는 인증 및 요청 제한이 없다. 공개 배포 전 도입 필요.
- **절기 경계 판정의 시스템 오프셋**: 천문 계산에 쓰는 ephem이 naive datetime을 UTC로 해석하므로, 엔진이 KST로 다루는 시각과 사이에 약 9시간의 오프셋이 존재한다. 절기 경계 부근(예: 입춘·소한) 출생·현행 시각에서 간지 판정이 어긋날 수 있다. 다만 출생 계산과 현행(current_fortune) 계산이 **동일한 규약**을 쓰므로 서비스 내부적으로는 자기 일관적이며, 절대 정합화는 후속 과제다.
- **지장간은 월률분야 표준표 채택**: 지장간(여기·중기·본기) 및 각 분야 배분은 여러 유파 표가 존재하나 본 프로젝트는 월률분야 표준표를 단일 기준으로 채택한다(왕지 자·묘·유는 여기+본기 2개).

## 라이선스

Apache License 2.0 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
