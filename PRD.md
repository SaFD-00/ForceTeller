# ForceTeller: Product Requirements Document

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | ForceTeller |
| 목적 | 천문학적 정밀도의 사주명리 계산과 AI 해석을 결합한 운세 분석 플랫폼 |
| 유형 | Full-Stack Web Application + REST API + CLI |
| 버전 | 1.0.0 |
| 상태 | Production-Ready |
| 라이선스 | Apache License 2.0 |

### 1.1 핵심 가치

| 기존 사주 서비스 | ForceTeller |
|----------------|-------------|
| 표준시 기반 단순 계산 | PyEphem 기반 **진태양시 보정** (경도/균시차/서머타임/KST 역사) |
| 단일 학파 해석 | **5개 학파** 동시 해석 및 비교 (자평/적천수/궁통보감/현대/신살) |
| 고정 템플릿 응답 | **8개 전문 AI 에이전트**가 맞춤 해석 (LangGraph Supervisor 패턴) |
| 1회성 결과 | **멀티턴 대화** 기반 심층 상담 (세션 컨텍스트 유지) |
| 단일 LLM 종속 | **Provider-Agnostic** LLM (OpenAI/Gemini 자유 전환) |

### 1.2 기술적 차별점

| 기술 | 설명 |
|------|------|
| 진태양시 보정 | PyEphem 천문 라이브러리로 경도 보정, 균시차(최대 16분), 서머타임, KST 역사 반영 |
| LangGraph Supervisor | 동적 에이전트 라우팅으로 사용자 질문에 최적화된 에이전트 조합 선택 |
| Pydantic Structured Output | LLM 응답을 Pydantic 모델로 강제하여 타입 안전한 일관된 출력 보장 |
| Provider-Agnostic LLM | OpenAI/Gemini 추상화 계층으로 비용 최적화 및 장애 대응 |
| Hungarian Matching 없는 실시간 계산 | 사주 계산은 순수 알고리즘 기반, LLM 호출 없이 즉시 응답 |

---

## 2. 시스템 아키텍처

### 2.1 3-Layer 계층 구조

```
+------------------+     +------------------+     +------------------+
|   Presentation   |     |   Application    |     |    External      |
|   Next.js 14     | --> |   FastAPI        | --> |   LLM APIs       |
|   (Frontend)     |     |   + LangGraph    |     |  (OpenAI/Gemini) |
+------------------+     +------------------+     +------------------+
                               |
                               v
                    +------------------+
                    |     Domain       |
                    |  Manseol Engine  |
                    | (Saju Calculator)|
                    +------------------+
```

### 2.2 사주 계산 데이터 흐름

```
[User Input]
    │
    v
[API: POST /api/manseol]
    │
    v
[TimeCorrector] ─── PyEphem ─── 진태양시 보정
    │
    v
[PillarEngine] ─── 년/월/일/시주 계산
    │
    ├── ten_gods.py ──────── 십성 계산
    ├── shensha.py ──────── 신살 계산 (49종)
    ├── hidden_stems.py ─── 지장간 계산
    ├── twelve_phases.py ── 십이운성 계산
    ├── fortune_cycle.py ── 대운 계산
    └── interactions.py ─── 오행 상호작용
    │
    v
[SajuResult Model] → [JSON Response]
```

### 2.3 AI 해석 데이터 흐름

```
[User Question]
    │
    v
[API: POST /api/chat]
    │
    v
[SessionManager] ─── 세션 생성/조회, 컨텍스트 빌드
    │
    v
[LangGraph StateGraph]
    │
    ├── supervisor_node ──── 질문 분석 → 에이전트 선택 (RouterDecision)
    ├── interpreter_node ─── 선택된 에이전트 실행 (InterpretationResult)
    ├── (반복: supervisor → interpreter)
    └── synthesis_node ───── 종합 해석 생성 (SynthesisResult)
    │
    v
[Structured Output (Pydantic)] → [JSON Response]
```

### 2.4 핵심 컴포넌트

| 컴포넌트 | 역할 | 기술 |
|---------|------|------|
| Manseol Engine | 사주 계산 (4주, 분석, 대운) | Python, PyEphem |
| Agent Framework | AI 해석 오케스트레이션 | LangGraph, LangChain |
| API Layer | REST API 서비스 | FastAPI, Pydantic |
| Frontend | 웹 UI (입력, 결과, 채팅) | Next.js 14, React 18 |
| Session Manager | 멀티턴 대화 세션 관리 | In-Memory (Python dict) |
| Config Module | 환경 변수 및 설정 관리 | Pydantic Settings |

### 2.5 프로젝트 구조

```
ForceTeller/
├── PRD.md                          # 본 문서
├── README.md                       # 설치/실행 가이드
├── ARCHITECTURE.md                 # 아키텍처 상세
├── main.py                         # CLI 진입점 (Click)
├── requirements.txt                # Python 의존성
├── requirements-dev.txt            # 개발용 의존성
├── Dockerfile                      # Docker 빌드
├── .env.example                    # 환경변수 템플릿
├── pytest.ini                      # 테스트 설정
│
├── api/                            # FastAPI 백엔드
│   ├── server.py                   # FastAPI 앱 설정
│   ├── schemas.py                  # Pydantic 요청/응답 모델
│   ├── routes/
│   │   ├── manseol.py              # 사주 계산 엔드포인트
│   │   ├── chat.py                 # 채팅 엔드포인트
│   │   └── analysis.py             # 분석 엔드포인트
│   ├── converters.py               # 데이터 변환 유틸
│   ├── formatters.py               # 응답 포맷팅
│   └── dependencies.py             # 의존성 주입
│
├── manseol/                        # 만세력 계산 엔진
│   ├── calculator/                 # 사주 계산기
│   │   ├── pillar_engine.py        # 사주팔자 계산
│   │   ├── ten_gods.py             # 십성 계산
│   │   ├── shensha.py              # 신살 계산
│   │   ├── hidden_stems.py         # 지장간 계산
│   │   ├── twelve_phases.py        # 십이운성 계산
│   │   ├── fortune_cycle.py        # 대운 계산
│   │   └── interactions.py         # 오행 상호작용
│   ├── core/                       # 천문 계산
│   │   ├── astronomical.py         # PyEphem 진태양시
│   │   ├── solar_terms.py          # 24절기 계산
│   │   ├── time_correction.py      # 시간 보정
│   │   └── calendar_converter.py   # 양력/음력 변환
│   ├── analysis/                   # 해석 엔진
│   │   ├── schools/                # 5개 학파
│   │   │   ├── base_interpreter.py
│   │   │   ├── ziping.py           # 자평파
│   │   │   ├── dts.py              # 적천수
│   │   │   ├── qtbj.py             # 궁통보감
│   │   │   ├── modern.py           # 현대 학파
│   │   │   ├── shensha.py          # 신살파
│   │   │   └── comparator.py       # 학파 비교
│   │   ├── yongsin/                # 용신 분석
│   │   │   ├── base.py
│   │   │   ├── strength.py         # 강약용신
│   │   │   ├── seasonal.py         # 조후용신
│   │   │   ├── mediation.py        # 통관용신
│   │   │   ├── disease.py          # 병약용신
│   │   │   ├── selector.py         # 용신 선정
│   │   │   └── recommendations.py
│   │   └── fortune/analyzer.py     # 운세 분석
│   ├── data/                       # 참조 데이터
│   │   ├── stems_branches.py       # 천간/지지
│   │   ├── lunar_data.py           # 음력 데이터
│   │   ├── city_coordinates.py     # 도시 좌표
│   │   ├── korean_names.py         # 한글 이름
│   │   └── kst_history.py          # KST 역사
│   ├── models/                     # 데이터 모델
│   │   ├── input_model.py          # 입력 검증
│   │   └── saju_result.py          # 결과 모델
│   ├── output/json_exporter.py     # JSON 출력
│   └── cli.py                      # 만세력 전용 CLI
│
├── agents/                         # AI 에이전트 (LangGraph)
│   ├── graph.py                    # StateGraph 빌드
│   ├── nodes.py                    # 노드 함수
│   ├── state.py                    # AgentState 정의
│   ├── schemas.py                  # Pydantic 응답 스키마
│   ├── llm.py                      # LLM 추상화
│   ├── factory.py                  # NodeFactory / AgentFactory
│   ├── agent_configs.py            # 8개 에이전트 설정
│   ├── config.py                   # AgentConfig 데이터클래스
│   ├── orchestrator.py             # Orchestrator (레거시 호환)
│   └── prompts/system_prompts.py   # 시스템 프롬프트
│
├── conversation/                   # 세션 관리
│   ├── session_manager.py          # 멀티턴 세션 핸들링
│   └── context_builder.py          # 대화 컨텍스트
│
├── config/                         # 설정
│   ├── settings.py                 # Pydantic 환경 설정
│   ├── constants.py                # 도메인 상수 (627줄)
│   └── logging_config.py           # 로깅 설정
│
├── utils/                          # 유틸리티
│   ├── llm_client.py               # OpenAI/Gemini 클라이언트
│   └── protocols.py                # 타입 프로토콜
│
├── tests/                          # 테스트
│   ├── unit/                       # 단위 테스트
│   ├── integration/                # 통합 테스트
│   └── e2e/                        # E2E 테스트
│
└── web/                            # Next.js 14 프론트엔드
    ├── app/
    │   ├── page.tsx                 # 홈 (입력 폼)
    │   ├── layout.tsx              # 루트 레이아웃
    │   ├── result/page.tsx         # 결과 표시
    │   ├── chat/page.tsx           # 채팅 인터페이스
    │   └── providers.tsx           # 앱 프로바이더
    ├── components/
    │   ├── hero/                   # 랜딩 히어로 (3개)
    │   ├── features/               # 기능 그리드 (2개)
    │   ├── result/                 # 결과 표시 (14개)
    │   ├── chat/                   # 채팅 UI (10개)
    │   └── ui/                     # 재사용 UI (8개)
    ├── stores/sajuStore.ts         # Zustand 상태관리
    ├── lib/
    │   ├── api/                    # API 클라이언트
    │   ├── constants/              # 프론트엔드 상수
    │   ├── transforms.ts           # 데이터 변환
    │   └── utils.ts                # 유틸리티
    ├── types/saju.ts               # TypeScript 타입 (37+)
    ├── data/saju-glossary.ts       # 사주 용어 사전
    ├── package.json
    └── tailwind.config.ts
```

---

## 3. 도메인 엔진 상세 (만세력)

### 3.1 진태양시 보정 알고리즘

사주 계산의 정확도는 출생 시간에 의존하며, 표준시와 진태양시 사이에 최대 **46분**의 오차가 발생할 수 있다.

```
T_saju = T_clock − T_DST + ΔT_longitude + E(균시차)
```

| 보정 항목 | 설명 | 최대 오차 |
|----------|------|----------|
| 경도 보정 (ΔT_longitude) | 출생 도시의 경도와 표준자오선(135°E) 차이를 시간으로 변환 | ~30분 |
| 균시차 (E) | 지구 공전 궤도 이심률과 자전축 경사에 의한 시간 편차 | ~16분 |
| 서머타임 (T_DST) | 역사적 서머타임 적용 기간 보정 | 60분 |
| KST 역사 | 한국 표준시 변경 이력 반영 (1908~현재) | 30분 |

구현: `manseol/core/astronomical.py` (PyEphem), `manseol/core/time_correction.py`

### 3.2 사주 4주 계산

| 주(柱) | 계산 기준 | 구현 |
|--------|----------|------|
| 년주(年柱) | 입춘(立春) 기준 연도 전환 | 절기 계산 + 60갑자 순환 |
| 월주(月柱) | 절기(節氣) 기준 월 전환 + 오호둔월법(五虎遁月法) | 24절기 테이블 |
| 일주(日柱) | 갑자일(甲子日) 기준 60갑자 순환 | 율리안일수 계산 |
| 시주(時柱) | 오서둔시법(五鼠遁時法) + 진태양시 보정 | 2시간 단위 12지지 |

구현: `manseol/calculator/pillar_engine.py`

**자시(子時) 구분**:
- **조자시(早子時)**: 23:00~00:00을 당일로 처리
- **야자시(夜子時)**: 23:00~00:00을 익일로 처리 (사용자 선택)

### 3.3 분석 모듈

| 모듈 | 설명 | 파일 |
|------|------|------|
| 오행 분석 | 목/화/토/금/수 분포 및 균형 | `interactions.py` |
| 십성 분포 | 비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인 | `ten_gods.py` |
| 십이운성 | 각 오행별 12단계 생명 주기 (태, 양, 장생, ..., 묘) | `twelve_phases.py` |
| 신살 | 천을귀인, 문창귀인 등 49종 길흉신 | `shensha.py` |
| 지장간 | 지지 속 숨은 천간 분석 | `hidden_stems.py` |
| 대운 | 10년 주기 운세 흐름 (순행/역행) | `fortune_cycle.py` |
| 오행 상호작용 | 삼합, 육합, 육충, 형, 원진, 상생, 상극 | `interactions.py` |

### 3.4 용신 분석 시스템

4가지 용신 선정 알고리즘을 `YongSinSelector`가 통합 관리:

| 방법론 | 설명 | 파일 |
|--------|------|------|
| 강약용신(强弱用神) | 일간 강약에 따른 용신 선정 | `yongsin/strength.py` |
| 조후용신(調候用神) | 계절(월지)에 따른 오행 조절 | `yongsin/seasonal.py` |
| 통관용신(通關用神) | 충돌하는 오행 간 중재자 선정 | `yongsin/mediation.py` |
| 병약용신(病藥用神) | 사주의 병(病)을 치료하는 약(藥) 선정 | `yongsin/disease.py` |

### 3.5 학파별 해석 프레임워크

`BaseSchoolInterpreter` 추상 클래스를 Template Method 패턴으로 구현:

| 학파 | 코드 | 핵심 특징 | 파일 |
|------|------|----------|------|
| 자평명리(子平命理) | `ziping` | 전통적 격국론, 용신론 중심 | `schools/ziping.py` |
| 적천수(滴天髓) | `dts` | 일간 중심, 대주파 해석 | `schools/dts.py` |
| 궁통보감(窮通寶鑑) | `qtbj` | 조후용신 중심, 계절론 | `schools/qtbj.py` |
| 현대명리 | `modern` | 현대적 재해석, 실용 중심 | `schools/modern.py` |
| 신살 중심 | `shensha` | 신살 배합 중심 해석 | `schools/shensha.py` |

학파 비교: `schools/comparator.py` — 5개 학파의 해석을 병렬 실행 후 합의/차이점 분석

### 3.6 도메인 상수

`config/constants.py` (627줄)에 정의된 핵심 데이터:

| 상수 | 내용 |
|------|------|
| 오행(五行) | 목/화/토/금/수 정의, 속성, 색상, 방위 |
| 천간(天干) | 갑~계 10간, 오행/음양 매핑 |
| 지지(地支) | 자~해 12지, 오행/음양/동물 매핑 |
| 육십갑자 | 60갑자 전체 조합 및 각 비유 |
| 24절기 | 입춘~대한, 양력 날짜 범위 |
| 십성 관계 | 일간 기준 10신 산출 테이블 |
| 신살 정의 | 길신/흉신 목록 및 설명 |
| 상생/상극 | 오행 생극 관계 정의 |
| 형충회합 | 삼합, 육합, 육충, 형, 원진 관계 |

---

## 4. 서버 상세 (FastAPI)

### 4.1 앱 구조

| 파일 | 역할 |
|------|------|
| `api/server.py` | `create_app()` 팩토리, CORS 미들웨어, 전역 예외 핸들러, 라우터 등록 |
| `api/dependencies.py` | 의존성 주입 (SessionManager, Settings 인스턴스) |
| `api/converters.py` | 백엔드 SajuResult → API 응답 변환 |
| `api/formatters.py` | 응답 포맷팅 유틸리티 |

### 4.2 라우트 모듈

| 라우터 | 파일 | 엔드포인트 수 | 역할 |
|--------|------|-------------|------|
| `manseol_router` | `routes/manseol.py` | 4 | 사주 계산, 도시 검색 |
| `chat_router` | `routes/chat.py` | 5 | AI 대화, 세션 관리 |
| `analysis_router` | `routes/analysis.py` | 2 | 상세 분석, 분석 유형 조회 |

### 4.3 요청/응답 스키마

#### Enum 타입

| Enum | 값 | 용도 |
|------|-----|------|
| `CalendarType` | solar, lunar, leap_lunar | 달력 유형 |
| `Gender` | male, female | 성별 |
| `InterpretationType` | full, quick, specific | 해석 유형 |
| `LLMProvider` | openai, gemini | LLM 제공자 |
| `AnalysisType` | fortune_general, fortune_career, fortune_wealth, fortune_health, fortune_love, yongsin, school_compare, yongsin_method | 분석 유형 (8종) |
| `YongSinMethodType` | strength, seasonal, mediation, disease | 용신 방법론 (4종) |
| `SchoolCodeType` | ziping, dts, qtbj, modern, shensha | 학파 코드 (5종) |

#### 주요 모델

| 모델 | 방향 | 핵심 필드 |
|------|------|----------|
| `ManseolRequest` | 요청 | name, birth_date, birth_time, calendar, city, gender, jajasi |
| `ManseolResponse` | 응답 | success, data(사주 계산 결과), error |
| `ChatRequest` | 요청 | session_id, saju_data, message, interpretation_type, focus, llm_provider |
| `ChatResponse` | 응답 | session_id, message, suggested_questions, interpretations, agents_used |
| `AnalysisRequest` | 요청 | analysis_type, yongsin_method, schools, message, llm_provider |
| `AnalysisResponse` | 응답 | analysis_type, message, fortune_result, yongsin_result, school_comparison |
| `ErrorResponse` | 응답 | success(false), error, detail |

---

## 5. 클라이언트 상세 (Next.js)

### 5.1 기술 스택

| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | ^14.2.0 | App Router 프레임워크 |
| React | ^18.2.0 | UI 라이브러리 |
| TypeScript | ^5.0.0 | 타입 안전성 |
| Tailwind CSS | ^3.4.0 | 유틸리티 퍼스트 스타일링 |
| Zustand | ^4.5.0 | 경량 상태관리 |
| React Query | ^5.60.0 | 서버 상태 관리 및 데이터 페칭 |
| Recharts | ^2.14.0 | 데이터 시각화 (오행 차트, 강도 그래프) |
| Framer Motion | ^11.0.0 | 애니메이션 |
| Iconify | ^5.0.0 | Solar 아이콘셋 |
| React Markdown | ^10.1.0 | AI 응답 마크다운 렌더링 |

### 5.2 페이지 구성

| 페이지 | 경로 | 설명 |
|--------|------|------|
| 홈 | `/` | 사주 입력 폼 (이름, 생년월일, 시간, 성별, 도시, 달력 유형) |
| 결과 | `/result` | 사주 계산 결과 시각화 (4주, 오행, 십성, 대운 등) |
| 채팅 | `/chat` | AI 대화형 상담 인터페이스 |

### 5.3 컴포넌트 체계 (37개)

#### 결과 표시 컴포넌트 (14개)

| 컴포넌트 | 역할 |
|---------|------|
| `FourPillarsDisplay` | 사주팔자 4주 시각화 (메인) |
| `PillarCard` | 개별 주(柱) 카드 |
| `PillarTable` | 주별 테이블 표시 |
| `PentagonChart` | 오행 오각형 강도 차트 |
| `StrengthMeter` | 일간 강약 미터 |
| `FiveElementsChart` | 오행 분포 바 차트 |
| `ElementDistribution` | 오행 균형 분석 |
| `TenGodsDistribution` | 십성 분포 차트 |
| `YongshinCard` | 용신/희신/기신 카드 |
| `ShenshaDetailCard` | 신살 상세 정보 |
| `InteractionsTabs` | 오행 상호작용 탭 (합/충/형) |
| `FortuneCycleTimeline` | 대운 타임라인 |
| `FortuneCycleSlider` | 대운 슬라이더 |
| `StrengthDistributionChart` | 강도 분포 차트 |

#### 채팅 컴포넌트 (10개)

| 컴포넌트 | 역할 |
|---------|------|
| `ChatContainer` | 메인 채팅 컨테이너 |
| `MessageList` | 메시지 목록 |
| `MessageBubble` | 개별 메시지 버블 |
| `ChatInput` | 사용자 입력 필드 |
| `MarkdownRenderer` | AI 응답 마크다운 렌더링 |
| `ReasoningDisplay` | AI 추론 과정 표시 |
| `SuggestedQuestions` | 추천 질문 버튼 |
| `AnalysisButtons` | 빠른 분석 버튼 (성격/직업/건강 등) |
| `AgentSelector` | 에이전트 직접 선택 |
| `ChatHeader` | 채팅 헤더 (세션 정보) |

#### 히어로/기능 컴포넌트 (5개)

| 컴포넌트 | 역할 |
|---------|------|
| `HeroSection` | 랜딩 히어로 섹션 |
| `SajuInputForm` | 사주 입력 폼 |
| `HeroBackground` | 배경 애니메이션 |
| `FeatureGrid` | 기능 소개 그리드 |
| `FeatureCard` | 개별 기능 카드 |

#### 공통 UI 컴포넌트 (8개)

| 컴포넌트 | 역할 |
|---------|------|
| `Button` | 버튼 (다양한 variant) |
| `Input` | 입력 필드 |
| `GlassCard` | 글래스모피즘 카드 |
| `Icon` | Iconify 아이콘 래퍼 |
| `ElementBadge` | 오행 배지 (색상 매핑) |
| `GlossaryTooltip` | 용어 툴팁 |
| `GlossaryModal` | 용어 사전 모달 |
| `LoadingOverlay` | 로딩 오버레이 |

### 5.4 상태 관리

| Store | 파일 | Persist | 핵심 상태 |
|-------|------|---------|----------|
| `useSajuStore` | `stores/sajuStore.ts` | localStorage (`saju-storage`) | 사주 결과, 로딩 상태, 에러 |
| `useChatStore` | `stores/sajuStore.ts` | 미적용 (세션 내 한정) | 세션 ID, 메시지 목록, 로딩 |

### 5.5 오행 디자인 시스템

| 오행 | 한자 | 색상 코드 | Tailwind | 의미 |
|------|------|-----------|----------|------|
| 목(木) | 木 | `#22c55e` | green-500 | 성장, 창조 |
| 화(火) | 火 | `#ef4444` | red-500 | 열정, 활동 |
| 토(土) | 土 | `#eab308` | yellow-500 | 안정, 중재 |
| 금(金) | 金 | `#a1a1aa` | zinc-400 | 결단, 정의 |
| 수(水) | 水 | `#3b82f6` | blue-500 | 지혜, 유연 |

---

## 6. AI 에이전트 상세 (LangGraph)

### 6.1 Supervisor 패턴

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

### 6.2 AgentState 정의

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # 메시지 히스토리 (자동 누적)
    saju_data: dict[str, Any]          # 사주 데이터 (불변)
    current_agent: str                  # 현재 실행 중인 에이전트
    next_agent: Optional[str]           # 다음 에이전트 (라우팅 결정)
    interpretations: dict[str, dict]    # 각 에이전트 해석 결과 누적
    iteration: int                      # 반복 카운터 (무한 루프 방지)
    final_output: Optional[str]         # 최종 종합 출력
    error: Optional[str]                # 에러 정보
```

### 6.3 에이전트 설정 (8종)

| 에이전트 | 표시명 | 해석 영역 | 키워드 |
|---------|--------|----------|--------|
| `personality` | 성격 분석 | 성격, 기질, 성향 | 성격, 기질, 성향, 특성, 장단점, 강점, 약점 |
| `career` | 직업/재물 분석 | 직업, 재물, 사업 | 직업, 일, 직장, 취업, 사업, 재물, 돈, 부, 투자, 경력 |
| `relationship` | 대인관계 분석 | 연애, 결혼, 대인관계 | 연애, 결혼, 배우자, 인연, 이성, 사랑, 대인관계, 친구, 가족 |
| `health` | 건강 분석 | 건강, 체질 | 건강, 질병, 아픈, 체질, 몸, 운동, 음식 |
| `fortune` | 운세 분석 | 운세, 시기, 흐름 | 운세, 대운, 올해, 내년, 언제, 시기, 때, 미래, 앞으로 |
| `yongsin` | 용신 분석 | 용신, 희신, 기신 | 용신, 희신, 기신, 개운, 강약, 신강, 신약 |
| `school_compare` | 유파 비교 분석 | 유파별 해석 비교 | 유파, 비교, 자평, 적천수, 궁통보감, 현대명리, 신살 |
| `synthesis` | 종합 분석 | 종합 해석 | 종합, 전체, 모두, 전반 |

### 6.4 노드 함수

| 노드 | 입력 | 출력 (Structured) | 역할 |
|------|------|-------------------|------|
| `supervisor_node` | 사용자 질문 + 사주 데이터 | `RouterDecision` (next_agent, reasoning) | 질문 분석 → 최적 에이전트 선택 |
| `interpreter_node` | 사주 데이터 + 에이전트 프롬프트 | `InterpretationResult` (interpretation, confidence, suggested_questions) | 선택된 에이전트가 해석 수행 |
| `synthesis_node` | 모든 해석 결과 | `SynthesisResult` (synthesis, key_points, final_questions) | 종합 해석 생성 |

### 6.5 LLM 추상화

```python
def create_llm(provider: str = "openai", ...) -> BaseChatModel:
    if provider == "openai":
        return ChatOpenAI(model=model, ...)
    elif provider == "google":
        return ChatGoogleGenerativeAI(model=model, ...)
```

| 기능 | 설명 |
|------|------|
| `create_llm()` | Provider별 LLM 인스턴스 생성 |
| `create_structured_llm()` | Pydantic 모델 기반 구조화된 출력 LLM 생성 |
| `create_llm_with_fallback()` | Primary → Fallback 체인 구성 |
| `invoke_with_retry()` | tenacity 기반 재시도 (3회, exponential backoff) |

---

## 7. 모듈 상세 요구사항

### 7.1 세션 관리 (`conversation/`)

| 항목 | 값 |
|------|-----|
| 저장소 | In-Memory (Python dict) |
| 최대 세션 수 | 100 (설정 가능, `MAX_SESSIONS`) |
| 세션 타임아웃 | 60분 (`SESSION_TIMEOUT_MINUTES`) |
| 대화 히스토리 제한 | 저장: 20건 (`SESSION_MAX_HISTORY`), LLM 전달: 10건 (`CONVERSATION_HISTORY_LIMIT`) |
| 정리 정책 | LRU, 20% 일괄 삭제 (`SESSION_CLEANUP_PERCENTAGE`) |
| 세션 데이터 | session_id, saju_data, messages[], created_at, last_activity, name |

### 7.2 컨텍스트 빌더 (`conversation/context_builder.py`)

대화 히스토리와 사주 데이터를 결합하여 LLM에 전달할 메시지 시퀀스를 구성:
- System prompt (에이전트별 역할 정의)
- 사주 데이터 요약 (4주, 오행 분포, 용신 등)
- 최근 N개 대화 히스토리

### 7.3 설정 모듈 (`config/settings.py`)

Pydantic `BaseSettings` 기반 환경 변수 관리:

```python
class Settings(BaseSettings):
    # API 키
    OPENAI_API_KEY: Optional[str]
    GOOGLE_API_KEY: Optional[str]
    # LLM 설정
    DEFAULT_LLM_PROVIDER: str = "openai"
    OPENAI_MODEL: str = "gpt-5-nano"
    GEMINI_MODEL: str = "gemini-3-flash-preview"
    # 서버 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    # 세션 설정
    MAX_SESSIONS: int = 100
    SESSION_TIMEOUT_MINUTES: int = 60
    # ... (전체 30+ 설정 항목)
```

---

## 8. API 명세

### 8.1 만세력 API

#### `POST /api/manseol` — 사주 계산

**요청**:
```json
{
  "name": "홍길동",
  "birth_date": "1990-05-15",
  "birth_time": "14:30",
  "calendar": "solar",
  "city": "Seoul",
  "gender": "male",
  "jajasi": false,
  "apply_time_correction": true
}
```

**응답**: 4주 + 오행 분포 + 십성 + 신살 + 대운 + 지장간 + 십이운성 + 용신 + 시간 보정 정보

#### `POST /api/manseol/quick` — 빠른 계산 (Query Params)

#### `GET /api/manseol/cities?q={query}` — 도시 검색 (다국어 지원)

#### `GET /api/manseol/city/{name}` — 도시 좌표 조회

### 8.2 채팅 API

#### `POST /api/chat` — AI 대화

**요청**:
```json
{
  "session_id": null,
  "saju_data": { "meta": {}, "input": {}, "pillars": {} },
  "message": "제 성격에 대해 알려주세요",
  "interpretation_type": "full",
  "focus": null,
  "llm_provider": "openai"
}
```

**응답**:
```json
{
  "success": true,
  "session_id": "uuid-...",
  "message": "사주 분석 결과...",
  "suggested_questions": ["직업 적성은?", "올해 운세는?"],
  "interpretations": { "personality": { ... } },
  "agents_used": ["personality"]
}
```

#### `GET /api/chat/sessions` — 세션 목록

#### `GET /api/chat/sessions/{id}` — 세션 상세

#### `DELETE /api/chat/sessions/{id}` — 세션 삭제

#### `POST /api/chat/sessions/{id}/clear` — 대화 기록 삭제

### 8.3 분석 API

#### `POST /api/analysis` — 상세 분석

8가지 `AnalysisType`에 따른 분석 실행:
- 운세 분석 (5종): `fortune_general`, `fortune_career`, `fortune_wealth`, `fortune_health`, `fortune_love`
- 용신 분석: `yongsin` (4가지 방법론 선택 가능)
- 유파 비교: `school_compare` (5개 학파 비교)

#### `GET /api/analysis/types` — 분석 유형 목록

### 8.4 시스템 API

| 엔드포인트 | 응답 |
|-----------|------|
| `GET /health` | `{"status": "ok", "version": "1.0.0", "timestamp": "..."}` |
| `GET /` | API 정보 |

### 8.5 에러 응답

```json
{
  "success": false,
  "error": "에러 메시지",
  "detail": "상세 정보 (선택)"
}
```

| HTTP 상태 | 상황 |
|-----------|------|
| 400 | 잘못된 요청 (날짜 형식, 필수 필드 누락) |
| 404 | 세션/도시 미발견 |
| 422 | Pydantic 검증 실패 |
| 500 | 서버 내부 오류 (LLM 호출 실패 등) |

---

## 9. 설정 파일

### 9.1 백엔드 환경 변수 (`.env`)

```env
# LLM API 키
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# LLM 설정
DEFAULT_LLM_PROVIDER=openai          # openai | gemini
OPENAI_MODEL=gpt-5-nano             # gpt-5.2 | gpt-5-nano | gpt-5-mini
GEMINI_MODEL=gemini-3-flash-preview  # gemini-3-pro-preview | gemini-3-flash-preview

# OpenAI 상세 설정
OPENAI_REASONING_EFFORT=none         # none | low | medium | high | xhigh
OPENAI_TEXT_VERBOSITY=medium         # low | medium | high
OPENAI_MAX_TOKENS=4096

# Gemini 상세 설정
GEMINI_THINKING_LEVEL=low            # minimal | low | medium | high
GEMINI_MAX_TOKENS=4096

# 서버 설정
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
CORS_ORIGINS=*                       # 콤마 구분 도메인 목록

# 세션 설정
SESSION_MAX_HISTORY=20
SESSION_TIMEOUT_MINUTES=60
MAX_SESSIONS=100
SESSION_CLEANUP_PERCENTAGE=0.2
CONVERSATION_HISTORY_LIMIT=10

# 에이전트 설정
DEFAULT_REASONING_EFFORT=medium

# 로깅 설정
LOG_LEVEL=INFO

# 만세력 설정
DEFAULT_CITY=Seoul
USE_TRUE_SOLAR_TIME=true
```

### 9.2 프론트엔드 환경 변수 (`web/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 9.3 Docker 설정

```dockerfile
FROM python:3.11-slim
# ephem 빌드를 위한 gcc 설치
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.4 테스트 설정 (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## 10. CLI 인터페이스

`main.py` (Click 프레임워크) 기반 4개 명령어:

### 10.1 사주 계산

```bash
python main.py cli \
  --name "홍길동" \
  --birth-date "1990-01-15" \
  --birth-time "14:30" \
  --gender male \
  [--city Seoul] \
  [--calendar solar] \
  [--jajasi] \
  [--output result.json] \
  [--format json|text]
```

### 10.2 서버 실행

```bash
python main.py server \
  [--host 0.0.0.0] \
  [--port 8000] \
  [--reload]
```

### 10.3 대화형 모드

```bash
python main.py interactive
```

Rich 기반 터미널 UI로 실시간 사주 계산 + AI 대화 루프 제공.

### 10.4 시스템 정보

```bash
python main.py info
```

LLM Provider 상태, API 키 유효성, 설정 값 등 시스템 정보 출력.

### 10.5 만세력 전용 CLI

```bash
python -m manseol.cli [옵션]
```

`manseol/cli.py`에서 독립 실행 가능한 계산 전용 인터페이스 제공.

---

## 11. 비기능 요구사항

### 11.1 에러 처리

| 전략 | 구현 |
|------|------|
| 전역 예외 핸들러 | FastAPI `@app.exception_handler` — 모든 미처리 예외를 `ErrorResponse`로 변환 |
| LLM 재시도 | tenacity: 3회, exponential backoff (2^n초) |
| Provider 폴백 | `create_llm_with_fallback()` — Primary 실패 시 다른 Provider 자동 전환 |
| 입력 검증 | Pydantic 모델로 모든 API 입력을 스키마 수준에서 검증 |

### 11.2 로깅

| 항목 | 설정 |
|------|------|
| 레벨 | 환경변수 `LOG_LEVEL` (기본: INFO) |
| 포맷 | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |
| 외부 라이브러리 | httpx, openai, langchain 등 WARNING 이상만 출력 |

### 11.3 보안

| 항목 | 구현 |
|------|------|
| API 키 | 환경 변수로 관리, `.env` 파일 git-ignore |
| CORS | `CORS_ORIGINS` 환경변수로 허용 도메인 명시적 설정 |
| 입력 검증 | Pydantic 필드 레벨 검증 (min_length, max_length, ge, le 등) |
| 민감 데이터 | 로그에 API 키, 사용자 개인정보 출력 방지 |

### 11.4 세션 관리 정책

| 항목 | 값 | 설정 |
|------|-----|------|
| 최대 동시 세션 | 100 | `MAX_SESSIONS` |
| 세션 타임아웃 | 60분 | `SESSION_TIMEOUT_MINUTES` |
| 대화 히스토리 저장 | 20건 | `SESSION_MAX_HISTORY` |
| LLM 전달 히스토리 | 10건 | `CONVERSATION_HISTORY_LIMIT` |
| 정리 방식 | LRU 20% 일괄 삭제 | `SESSION_CLEANUP_PERCENTAGE` |

### 11.5 확장성 고려

**현재 (Single Instance)**:
```
[Vercel] → [Railway (Single)] → [OpenAI/Gemini]
```

**미래 (Multi-Instance)**:
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
                |    Redis    |
                |  (Sessions) |
                +-------------+
```

---

## 12. 테스트

### 12.1 테스트 전략

| 계층 | 프레임워크 | 경로 | 목적 |
|------|----------|------|------|
| Unit | pytest | `tests/unit/` | 개별 모듈 단위 검증 |
| Integration | pytest | `tests/integration/` | 모듈 간 연동 검증 |
| E2E | pytest | `tests/e2e/` | 전체 워크플로우 검증 |

### 12.2 현재 테스트 커버리지

| 모듈 | 테스트 파일 수 | 주요 대상 |
|------|-------------|----------|
| `agents/` | 4 | AgentFactory, Orchestrator, 노드 함수 |
| `api/` | 3 | Dependencies, Formatters, Converters |
| `config/` | 1 | Settings 로드, 환경 변수 |
| `conversation/` | 1 | SessionManager |
| `utils/` | 1 | LLM Client |
| **합계** | **10** | |

### 12.3 커버리지 갭

| 미비 영역 | 상태 | 우선순위 |
|----------|------|---------|
| `manseol/` 전체 | 테스트 없음 (빈 디렉토리) | **P0** — 핵심 계산 엔진 |
| `e2e/` | 빈 디렉토리 | P1 — 전체 흐름 검증 |
| Frontend | 테스트 없음 | P2 — 컴포넌트 렌더링 |

---

## 13. 의존성

### 13.1 시스템 요구사항

| 항목 | 버전 |
|------|------|
| Python | 3.11+ |
| Node.js | 18+ |
| gcc | ephem 빌드용 (Docker 환경) |

### 13.2 백엔드 패키지

#### 도메인 / 천문 계산

| 패키지 | 버전 | 용도 |
|--------|------|------|
| ephem | ≥4.1.0 | PyEphem 천문 계산 (진태양시) |
| korean-lunar-calendar | ≥0.3.1 | 양력/음력 변환 |
| geonamescache | ≥2.0.0 | 도시 좌표 데이터 |

#### 데이터 모델링

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pydantic | ≥2.0 | 데이터 검증 |
| pydantic-settings | ≥2.0 | 환경 변수 관리 |
| python-dateutil | ≥2.8.2 | 날짜 처리 |

#### AI / LLM

| 패키지 | 버전 | 용도 |
|--------|------|------|
| langchain | ≥0.3.0 | LLM 추상화 |
| langchain-core | ≥0.3.0 | 핵심 인터페이스 |
| langchain-openai | ≥0.2.0 | OpenAI 통합 |
| langchain-google-genai | ≥2.0.0 | Gemini 통합 |
| langgraph | ≥0.2.0 | 에이전트 그래프 |
| openai | ≥1.0 | OpenAI SDK (legacy) |
| google-genai | ≥0.5.0 | Google GenAI SDK (legacy) |

#### HTTP / 서버

| 패키지 | 버전 | 용도 |
|--------|------|------|
| fastapi | ≥0.110.0 | REST API 프레임워크 |
| uvicorn | ≥0.27.0 | ASGI 서버 |
| httpx | ≥0.25 | 비동기 HTTP 클라이언트 |
| aiofiles | ≥23.0 | 비동기 파일 I/O |

#### CLI / 유틸

| 패키지 | 버전 | 용도 |
|--------|------|------|
| click | ≥8.0 | CLI 프레임워크 |
| rich | ≥13.0 | 터미널 포맷팅 |
| tenacity | ≥8.2.0 | 재시도 로직 |
| python-dotenv | ≥1.0 | .env 파일 로드 |

### 13.3 프론트엔드 패키지

#### Production

| 패키지 | 버전 | 용도 |
|--------|------|------|
| next | ^14.2.0 | App Router 프레임워크 |
| react | ^18.2.0 | UI 라이브러리 |
| react-dom | ^18.2.0 | React DOM 렌더링 |
| zustand | ^4.5.0 | 상태 관리 |
| @tanstack/react-query | ^5.60.0 | 서버 상태 관리 |
| recharts | ^2.14.0 | 데이터 시각화 |
| framer-motion | ^11.0.0 | 애니메이션 |
| @iconify/react | ^5.0.0 | Solar 아이콘셋 |
| react-markdown | ^10.1.0 | 마크다운 렌더링 |
| remark-gfm | ^4.0.1 | GFM 마크다운 확장 |
| clsx | ^2.1.0 | 조건부 CSS 클래스 |
| tailwind-merge | ^2.5.0 | Tailwind 클래스 병합 |

#### Development

| 패키지 | 버전 | 용도 |
|--------|------|------|
| typescript | ^5.0.0 | 타입 체크 |
| tailwindcss | ^3.4.0 | CSS 프레임워크 |
| eslint | ^8.0.0 | 린팅 |
| eslint-config-next | ^14.2.0 | Next.js ESLint 규칙 |
| postcss | ^8.4.0 | CSS 전처리 |
| autoprefixer | ^10.4.0 | CSS 벤더 프리픽스 |

---

## 14. 배포 아키텍처

### 14.1 배포 구성도

```
[사용자] → [Vercel (Next.js)] → [Railway (FastAPI)] → [OpenAI/Gemini API]
```

### 14.2 프론트엔드 (Vercel)

| 항목 | 값 |
|------|-----|
| 플랫폼 | Vercel |
| Root Directory | `web` |
| Framework | Next.js (자동 감지) |
| 환경 변수 | `NEXT_PUBLIC_API_URL=https://forceteller-xxx.railway.app` |
| 무료 티어 | 100GB 대역폭/월, 무제한 배포 |

### 14.3 백엔드 (Railway)

| 항목 | 값 |
|------|-----|
| 플랫폼 | Railway |
| 빌드 | Dockerfile 기반 |
| 환경 변수 | OPENAI_API_KEY, GOOGLE_API_KEY, CORS_ORIGINS, DEFAULT_LLM_PROVIDER 등 |
| Networking | Generate Domain → `forceteller-xxx.railway.app` |
| 무료 티어 | $5 크레딧/월 (~500시간) |

### 14.4 Docker 로컬 실행

```bash
# 이미지 빌드
docker build -t forceteller-api .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -e GOOGLE_API_KEY=... \
  forceteller-api
```

### 14.5 예상 비용

| 서비스 | 비용 | 비고 |
|--------|------|------|
| Vercel | 무료 | 100GB 대역폭/월 |
| Railway | $5/월 크레딧 | ~500시간 |
| OpenAI API | 종량제 | gpt-5-nano 기본 (저비용) |
| Google GenAI API | 종량제 | 대안 Provider |

---

## 15. 리스크 및 완화 방안

| 리스크 | 영향 | 완화 방안 | 현황 |
|--------|------|----------|------|
| LLM API 의존성 | 외부 API 장애 시 해석 기능 중단 | Provider 폴백 체인 (OpenAI → Gemini), tenacity 재시도 | ✅ 구현됨 |
| In-Memory 세션 | 서버 재시작 시 전체 세션 손실 | Redis 전환 계획 (미래) | ⚠️ 현재 제한 |
| LLM 비용 증가 | 사용량 증가 시 비용 부담 | gpt-5-nano 기본, 경량 모델 우선 설정 | ✅ 설정됨 |
| 도메인 정확성 | 사주 계산 오류 가능성 | PyEphem 천문 라이브러리 기반, 단위 테스트 필요 | ⚠️ 테스트 부족 |
| API 키 노출 | 보안 사고 | 환경 변수 관리, .gitignore, CORS 제한 | ✅ 구현됨 |
| 확장성 한계 | 동시 100세션 초과 불가 | Multi-Pod + Redis 아키텍처 전환 | ⚠️ 미구현 |
| Rate Limiting 부재 | DDoS/남용 취약 | API 레벨 Rate Limiting 추가 필요 | ⚠️ 미구현 |
| Manseol 테스트 부재 | 계산 오류 미탐지 | 핵심 엔진 단위 테스트 작성 필수 | ⚠️ 미구현 |

---

## 16. 향후 확장 방향

### 16.1 기능 확장

| 방향 | 설명 | 기대 효과 |
|------|------|----------|
| 궁합 분석 | 두 사주 간 궁합(상성) 비교 분석 | 사용자 참여도 증가 |
| 날짜별 운세 | 특정 날짜의 길흉 분석 (택일) | 실용적 가치 강화 |
| 이벤트 알림 | 대운/세운 변환 시점 알림 | 리텐션 향상 |
| 사주 공유 | 결과 이미지/링크 공유 기능 | 바이럴 성장 |

### 16.2 기술 확장

| 방향 | 설명 | 우선순위 |
|------|------|---------|
| Redis 세션 | In-Memory → Redis 전환 | P0 |
| 데이터베이스 | 사용자/세션/분석 이력 영속화 | P1 |
| Rate Limiting | API 레벨 요청 제한 | P1 |
| 스트리밍 응답 | LLM 응답 실시간 스트리밍 (SSE) | P2 |
| 캐싱 | 동일 사주 계산 결과 캐싱 | P2 |

### 16.3 AI 고도화

| 방향 | 설명 |
|------|------|
| Fine-tuned 모델 | 사주명리 전문 Fine-tuned LLM |
| RAG 기반 문헌 참조 | 고전 명리학 문헌을 RAG로 참조하여 해석 근거 강화 |
| 에이전트 추가 | 택일, 풍수, 관상 등 전문 영역 에이전트 확장 |
| 다국어 지원 | 영어/중국어/일본어 해석 지원 |

### 16.4 플랫폼 확장

| 방향 | 설명 |
|------|------|
| 모바일 앱 | React Native 기반 iOS/Android 앱 |
| 카카오톡 챗봇 | 카카오 채널 연동 AI 상담 |
| 웹 PWA | 오프라인 지원 Progressive Web App |

---

## 17. 용어 정리

### 사주 기초

| 용어 | 설명 |
|------|------|
| 사주명리학(四柱命理學) | 생년월일시의 네 기둥(四柱)으로 운명을 분석하는 동양 철학 |
| 사주팔자(四柱八字) | 년/월/일/시의 4주, 각 주는 천간+지지로 구성 (총 8자) |
| 천간(天干) | 갑(甲), 을(乙), 병(丙), 정(丁), 무(戊), 기(己), 경(庚), 신(辛), 임(壬), 계(癸) — 10간 |
| 지지(地支) | 자(子), 축(丑), 인(寅), 묘(卯), 진(辰), 사(巳), 오(午), 미(未), 신(申), 유(酉), 술(戌), 해(亥) — 12지 |
| 오행(五行) | 목(木), 화(火), 토(土), 금(金), 수(水) — 만물을 구성하는 5가지 기운 |
| 음양(陰陽) | 만물의 상반되는 두 성질 (천간/지지 각각 음양 구분) |
| 육십갑자(六十甲子) | 천간(10) × 지지(12)의 최소공배수 60개 간지 조합 |
| 일간(日干) | 일주의 천간, 사주 해석의 중심 (= 나 자신) |

### 사주 분석

| 용어 | 설명 |
|------|------|
| 십성(十星)/십신(十神) | 일간 기준 다른 천간/지지와의 관계: 비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인 |
| 십이운성(十二運星) | 오행의 12단계 생명 주기: 태, 양, 장생, 목욕, 관대, 건록, 제왕, 쇠, 병, 사, 묘, 절 |
| 신살(神殺) | 사주 배합에서 나타나는 길흉 지표 (천을귀인, 문창귀인, 역마살 등) |
| 지장간(地藏干) | 지지 속에 숨어 있는 천간 (각 지지에 1~3개) |
| 격국(格局) | 사주의 구조적 유형 분류 |
| 신강/신약(身强/身弱) | 일간의 힘이 강한지 약한지 여부 |

### 시간 계산

| 용어 | 설명 |
|------|------|
| 진태양시(眞太陽時) | 실제 태양의 위치에 기반한 시간 (표준시와 최대 ~46분 차이) |
| 균시차(均時差) | 지구 공전 궤도 이심률과 자전축 기울기에 의한 시간 편차 |
| 경도보정(經度補正) | 출생지 경도와 표준자오선 간 시차 보정 |
| 24절기(二十四節氣) | 태양의 황경에 따른 24개 시간 구분 (입춘, 우수, 경칩, ...) |
| 조자시/야자시 | 23:00~00:00의 처리 방식 (당일/익일) |

### 용신 체계

| 용어 | 설명 |
|------|------|
| 용신(用神) | 사주의 균형을 맞추기 위해 가장 필요한 오행 |
| 희신(喜神) | 용신을 돕는 오행 |
| 기신(忌神) | 용신을 방해하는 오행 |
| 수신(讐神) | 기신을 돕는 오행 |
| 강약용신 | 일간 강약에 따른 용신 선정 |
| 조후용신 | 계절(출생 월)에 따른 오행 조절 |
| 통관용신 | 충돌하는 두 오행 사이의 중재자 |
| 병약용신 | 사주의 병(결함)을 치료하는 약(해결책) |

### 학파

| 용어 | 설명 |
|------|------|
| 자평명리(子平命理) | 서자평이 체계화한 전통적 격국/용신론 중심 해석 |
| 적천수(滴天髓) | 일간 중심의 대주파(大主派) 해석 |
| 궁통보감(窮通寶鑑) | 조후용신 중심의 계절론적 해석 |
| 현대명리 | 전통 이론을 현대적으로 재해석한 실용적 접근 |
| 신살 중심 | 사주 내 신살 배합 중심의 길흉 판단 |

### 상호작용

| 용어 | 설명 |
|------|------|
| 상생(相生) | 오행이 서로 돕는 관계 (목→화→토→금→수→목) |
| 상극(相剋) | 오행이 서로 제압하는 관계 (목→토→수→화→금→목) |
| 삼합(三合) | 지지 3개가 결합하여 특정 오행을 형성 |
| 육합(六合) | 지지 2개의 조합 |
| 육충(六冲) | 지지 간 충돌 관계 |
| 형(刑) | 지지 간 형벌 관계 |
| 원진(怨嗔) | 지지 간 원한 관계 |

### 기술 용어

| 용어 | 설명 |
|------|------|
| LangGraph | LangChain 기반 상태 기반 에이전트 그래프 프레임워크 |
| Supervisor Pattern | 중앙 관리자가 하위 에이전트를 동적으로 선택/실행하는 패턴 |
| Structured Output | LLM 출력을 Pydantic 모델로 강제하여 일관된 JSON 응답 보장 |
| Provider-Agnostic | 특정 LLM Provider에 종속되지 않는 추상화된 인터페이스 |
| PyEphem | Python 천문 계산 라이브러리 (항성/행성 위치, 일출/일몰 계산) |
| StateGraph | LangGraph의 핵심 데이터 구조, 노드와 엣지로 에이전트 흐름 정의 |
| Zustand | React용 경량 상태 관리 라이브러리 |
| App Router | Next.js 14의 파일 시스템 기반 라우팅 방식 |
