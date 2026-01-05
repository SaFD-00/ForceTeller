# ForceTeller

사주명리학 기반 AI 운세 분석 플랫폼

## 개요

ForceTeller는 정확한 만세력 계산과 AI 해석을 결합한 사주팔자 분석 서비스입니다. 천문학적 진태양시 보정, 오행 분석, 십성 분포, 대운 흐름, 용신 선정 등 전문적인 사주 분석 기능을 제공하며, 8개의 전문 AI 에이전트를 통해 맞춤형 해석을 제공합니다.

## 프로젝트 구조

```
ForceTeller/
├── api/                          # FastAPI 백엔드
│   ├── routes/
│   │   ├── chat.py               # 채팅/대화 엔드포인트
│   │   ├── manseol.py            # 사주 계산 엔드포인트
│   │   └── analysis.py           # 분석 엔드포인트
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
│   │   └── kst_history.py        # 한국 표준시 역사
│   ├── analysis/                 # 해석 엔진
│   │   ├── fortune/analyzer.py   # 운세 분석
│   │   ├── schools/              # 사주 학파
│   │   │   ├── base_interpreter.py
│   │   │   ├── dts.py            # 대주파(大主派)
│   │   │   ├── ziping.py         # 자평파(子平派)
│   │   │   ├── qtbj.py           # 기운투부(起運途步)
│   │   │   ├── shensha.py        # 신살파
│   │   │   ├── modern.py         # 현대 학파
│   │   │   └── comparator.py     # 학파 비교
│   │   └── yongsin/              # 용신(用神) 분석
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
├── agents/                       # AI 해석 에이전트
│   ├── interpreters/             # 8개 전문 에이전트
│   │   ├── personality_agent.py  # 성격/특성 분석
│   │   ├── career_agent.py       # 직업/재물 분석
│   │   ├── relationship_agent.py # 인연/궁합 분석
│   │   ├── health_agent.py       # 건강/체질 분석
│   │   ├── fortune_agent.py      # 운세/시운 분석
│   │   ├── yongsin_agent.py      # 용신 분석
│   │   ├── school_compare_agent.py # 학파 비교
│   │   └── synthesis_agent.py    # 종합 분석
│   ├── base_agent.py             # 추상 기본 클래스
│   ├── orchestrator.py           # 에이전트 라우팅/조율
│   ├── prompts/
│   │   └── system_prompts.py     # LLM 시스템 프롬프트
│   └── schemas.py                # 에이전트 응답 모델
│
├── conversation/                 # 세션 관리
│   ├── session_manager.py        # 멀티턴 세션 핸들링
│   └── context_builder.py        # 대화 컨텍스트
│
├── config/                       # 설정
│   ├── settings.py               # Pydantic 환경 설정
│   └── constants.py              # 도메인 상수 (627줄)
│
├── utils/
│   └── llm_client.py             # OpenAI/Gemini 클라이언트
│
├── web/                          # Next.js 14 프론트엔드
│   ├── app/
│   │   ├── page.tsx              # 홈 페이지
│   │   ├── layout.tsx            # 루트 레이아웃
│   │   ├── result/page.tsx       # 결과 표시
│   │   ├── chat/page.tsx         # 채팅 인터페이스
│   │   └── providers.tsx         # 앱 프로바이더
│   ├── components/
│   │   ├── hero/                 # 랜딩 히어로 섹션
│   │   ├── features/             # 기능 그리드
│   │   ├── result/               # 결과 표시 (17개 컴포넌트)
│   │   ├── chat/                 # 채팅 UI (9개 컴포넌트)
│   │   └── ui/                   # 재사용 UI (7개 컴포넌트)
│   ├── stores/
│   │   └── sajuStore.ts          # Zustand 상태관리
│   ├── lib/
│   │   ├── api/                  # API 클라이언트
│   │   ├── constants/            # 프론트엔드 상수
│   │   └── utils.ts              # 유틸리티
│   ├── types/
│   │   └── saju.ts               # TypeScript 타입
│   ├── package.json
│   └── tailwind.config.ts
│
├── main.py                       # CLI 진입점
├── requirements.txt              # Python 의존성
└── README.md
```

## 기술 스택

### 백엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.11+ | 런타임 |
| FastAPI | 0.110 | REST API 프레임워크 |
| Pydantic | 2.0 | 데이터 검증 |
| Uvicorn | 0.27 | ASGI 서버 |
| OpenAI SDK | 1.0+ | GPT 통합 |
| Google GenAI SDK | - | Gemini 통합 |
| PyEphem | 4.1 | 천문 계산 |
| Korean-Lunar-Calendar | 0.3 | 음력 변환 |
| Click | 8.0 | CLI 프레임워크 |
| Rich | 13.0 | 터미널 포맷팅 |

### 프론트엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | 14.2 | App Router 프레임워크 |
| React | 18.3 | UI 라이브러리 |
| TypeScript | 5.0 | 타입 안전성 |
| Tailwind CSS | 3.4 | 스타일링 |
| Zustand | 4.5 | 상태관리 |
| Recharts | 2.14 | 데이터 시각화 |
| Framer Motion | 11.0 | 애니메이션 |
| React Query | 5.60 | 데이터 페칭 |
| Iconify | 5.0 | Solar 아이콘셋 |
| React Markdown | 10.1 | 마크다운 렌더링 |

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

### 3. 학파별 해석
- **자평파(子平派)**: 전통적 자평명리
- **대주파(大主派)**: 대주 중심 해석
- **기운투부파**: 기운 흐름 분석
- **신살파**: 신살 중심 해석
- **현대 학파**: 현대적 재해석

### 4. AI 에이전트 (8종)

| 에이전트 | 분석 영역 |
|----------|-----------|
| PersonalityAgent | 성격, 특성, 장단점 |
| CareerAgent | 직업, 재물, 적성 |
| RelationshipAgent | 인연, 궁합, 결혼 시기 |
| HealthAgent | 건강, 체질, 질병 취약점 |
| FortuneAgent | 운세, 시운, 길일 |
| YongsinAgent | 용신 분석 및 조언 |
| SchoolCompareAgent | 학파별 해석 비교 |
| SynthesisAgent | 종합 분석 |

### 5. 대화형 상담
- 멀티턴 대화 지원
- 세션 기반 컨텍스트 유지
- 사주 데이터 기반 맞춤 해석
- 후속 질문 자동 추천
- OpenAI/Gemini 선택 가능

## 시작하기

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- OpenAI API Key 또는 Google Gemini API Key

### 백엔드 설치 및 실행

```bash
# Conda 환경 생성 및 활성화
conda create -n forceteller python=3.11 -y
conda activate forceteller

# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일 편집 (API 키 설정)

# 서버 실행
python -m api.server
# 또는
uvicorn api.server:app --reload --host 0.0.0.0 --port 1118
```

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
python main.py cli --name "홍길동" --birth-date "1990-01-15" --birth-time "14:30" --gender male

# 대화형 모드
python main.py interactive

# 서버 실행
python main.py server --host 0.0.0.0 --port 1118 --reload

# 시스템 정보
python main.py info
```

## API 엔드포인트

### 만세력 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/manseol` | 사주 계산 |
| POST | `/api/manseol/quick` | 빠른 계산 |
| GET | `/api/manseol/cities` | 도시 목록 |
| GET | `/api/manseol/city/{name}` | 도시 정보 |

**사주 계산 요청 예시:**
```json
{
  "name": "홍길동",
  "birth_date": "1990-01-15",
  "birth_time": "14:30",
  "calendar_type": "solar",
  "city": "Seoul",
  "gender": "male",
  "jajasi": false
}
```

### 채팅 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/chat` | AI 대화 |
| GET | `/api/chat/sessions` | 세션 목록 |
| GET | `/api/chat/sessions/{id}` | 세션 상세 |
| DELETE | `/api/chat/sessions/{id}` | 세션 삭제 |
| POST | `/api/chat/sessions/{id}/clear` | 대화 기록 삭제 |

**채팅 요청 예시:**
```json
{
  "session_id": "uuid",
  "saju_data": { ... },
  "message": "제 적성에 맞는 직업은 무엇인가요?",
  "interpretation_type": "SPECIFIC"
}
```

### 분석 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/analysis` | 상세 분석 |

### 시스템 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 헬스 체크 |
| GET | `/` | API 정보 |

## 환경 변수

### 백엔드 (.env)

```env
# LLM API 키
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# LLM 설정
DEFAULT_LLM_PROVIDER=openai          # openai | gemini
OPENAI_MODEL=gpt-5.2                 # gpt-5.2 | gpt-5.2-pro | gpt-5-mini | gpt-5-nano | gpt-5.1-codex-max
GEMINI_MODEL=gemini-3-pro-preview    # gemini-3-pro-preview | gemini-3-flash-preview | gemini-3-pro-image-preview

# OpenAI 설정
OPENAI_REASONING_EFFORT=none         # low | medium | high
OPENAI_TEXT_VERBOSITY=medium         # low | medium | high
OPENAI_MAX_TOKENS=4096

# Gemini 설정
GEMINI_THINKING_LEVEL=medium         # minimal | low | medium | high
GEMINI_MAX_TOKENS=4096

# 서버 설정
API_HOST=0.0.0.0
API_PORT=1118
DEBUG=false

# 세션 설정
SESSION_MAX_HISTORY=20
SESSION_TIMEOUT_MINUTES=60

# 만세력 설정
DEFAULT_CITY=Seoul
USE_TRUE_SOLAR_TIME=true
```

### 프론트엔드 (web/.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:1118
```

## 오행 색상 시스템

| 오행 | 한자 | 색상 코드 | 의미 |
|------|------|-----------|------|
| 목(木) | 木 | `#22c55e` (Green) | 성장, 창조 |
| 화(火) | 火 | `#ef4444` (Red) | 열정, 활동 |
| 토(土) | 土 | `#eab308` (Yellow) | 안정, 중재 |
| 금(金) | 金 | `#a1a1aa` (Gray) | 결단, 정의 |
| 수(水) | 水 | `#3b82f6` (Blue) | 지혜, 유연 |

## 프론트엔드 컴포넌트

### 결과 표시 컴포넌트 (17개)
- `FourPillarsDisplay` - 사주팔자 시각화
- `PillarCard`, `PillarTable` - 주별 카드/테이블
- `PentagonChart` - 오각형 강도 차트
- `StrengthMeter` - 일간 강도 미터
- `FiveElementsChart` - 오행 분포 차트
- `ElementDistribution` - 오행 균형
- `TenGodsDistribution` - 십성 분포
- `YongshinCard` - 용신 정보
- `ShenshaDetailCard` - 신살 정보
- `InteractionsTabs` - 오행 상호작용
- `FortuneCycleTimeline` - 대운 타임라인
- `FortuneCycleSlider` - 대운 슬라이더
- `StrengthDistributionChart` - 강도 분포

### 채팅 컴포넌트 (9개)
- `ChatContainer` - 메인 채팅 컨테이너
- `MessageList`, `MessageBubble` - 메시지 표시
- `ChatInput` - 사용자 입력
- `MarkdownRenderer` - 마크다운 렌더링
- `SuggestedQuestions` - 추천 질문
- `AnalysisButtons` - 빠른 분석 버튼
- `AgentSelector` - 에이전트 선택

### UI 컴포넌트 (7개)
- `Button`, `Input` - 기본 입력
- `GlassCard` - 글래스모피즘 카드
- `Icon` - 아이콘 래퍼
- `ElementBadge` - 오행 배지
- `GlossaryTooltip`, `GlossaryModal` - 용어 설명
- `LoadingOverlay` - 로딩 상태

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
[사용자] → [Vercel (Next.js)] → [Railway (FastAPI)]
                                      ↓
                              [OpenAI/Gemini API]
```

- **프론트엔드**: Vercel (Next.js 최적화, 무료 티어)
- **백엔드**: Railway (월 $5 크레딧 무료)

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
5. Variables 탭에서 환경 변수 추가:
   ```
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   DEFAULT_LLM_PROVIDER=openai
   OPENAI_MODEL=gpt-5-nano
   CORS_ORIGINS=https://your-app.vercel.app
   ```
6. Settings → Networking → **Generate Domain** 클릭
7. 생성된 도메인 복사 (예: `forceteller-xxx.railway.app`)

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
docker run -p 1118:1118 \
  -e OPENAI_API_KEY=sk-... \
  -e GOOGLE_API_KEY=... \
  forceteller-api
```

### 환경 변수 (프로덕션)

| 변수 | 설명 | 예시 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-...` |
| `GOOGLE_API_KEY` | Google Gemini API 키 | `AI...` |
| `CORS_ORIGINS` | 허용할 프론트엔드 도메인 | `https://your-app.vercel.app` |
| `NEXT_PUBLIC_API_URL` | 백엔드 API URL | `https://api.railway.app` |

### 예상 비용

| 서비스 | 무료 티어 |
|--------|-----------|
| Vercel | 100GB 대역폭/월, 무제한 배포 |
| Railway | $5 크레딧/월 (약 500시간) |

## 라이선스

Apache License 2.0 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
