"""
API 스키마 정의
Pydantic 모델로 요청/응답 스키마 정의
"""

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ============== 공통 스키마 ==============


class CalendarType(str, Enum):
    SOLAR = "solar"
    LUNAR = "lunar"
    LEAP_LUNAR = "leap_lunar"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class InterpretationType(str, Enum):
    FULL = "full"  # 전체 해석
    QUICK = "quick"  # 빠른 단일 해석
    SPECIFIC = "specific"  # 특정 분야 해석


class ModelChoice(str, Enum):
    """OpenRouter 모델 선택지"""

    GPT_OSS_120B = "openai/gpt-oss-120b:free"
    GPT_OSS_20B = "openai/gpt-oss-20b:free"
    GEMMA_4_26B = "google/gemma-4-26b-a4b-it:free"
    GEMMA_4_31B = "google/gemma-4-31b-it:free"
    DEEPSEEK_V4_FLASH = "deepseek/deepseek-v4-flash"
    DEEPSEEK_V4_PRO = "deepseek/deepseek-v4-pro"


# ============== 만세력 API 스키마 ==============


class ManseolRequest(BaseModel):
    """사주 계산 요청"""

    name: str = Field(..., min_length=1, max_length=50, description="이름")
    birth_date: date = Field(..., description="생년월일 (YYYY-MM-DD)")
    birth_time: str | None = Field(None, description="출생시간 (HH:MM)")
    calendar: CalendarType = Field(default=CalendarType.SOLAR, description="달력 유형")
    city: str = Field(default="Seoul", description="출생 도시")
    gender: Gender = Field(..., description="성별")
    jajasi: bool = Field(default=False, description="야자시/조자시 적용")
    longitude: float | None = Field(None, ge=-180, le=180, description="직접 입력 경도")
    apply_time_correction: bool = Field(default=True, description="시간 보정 적용")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "홍길동",
                "birth_date": "1990-05-15",
                "birth_time": "14:30",
                "calendar": "solar",
                "city": "Seoul",
                "gender": "male",
                "jajasi": False,
            }
        }
    )


class ManseolResponse(BaseModel):
    """사주 계산 응답"""

    success: bool = True
    data: dict[str, Any] = Field(..., description="사주 계산 결과")
    error: str | None = None


# ============== 채팅 API 스키마 ==============


class ChatRequest(BaseModel):
    """대화 요청"""

    session_id: str | None = Field(None, description="기존 세션 ID (새 세션은 null)")
    saju_data: dict[str, Any] | None = Field(None, description="새 세션시 사주 데이터")
    message: str = Field(..., min_length=1, max_length=4000, description="사용자 메시지")
    interpretation_type: InterpretationType = Field(
        default=InterpretationType.FULL, description="해석 유형"
    )
    focus: str | None = Field(
        None, description="특정 해석 분야 (personality/career/relationship/health/fortune)"
    )
    model: ModelChoice | None = Field(
        default=None, description="사용할 OpenRouter 모델 (None이면 서버 기본 모델)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": None,
                "saju_data": {"meta": {}, "input": {}, "pillars": {}},
                "message": "제 성격에 대해 알려주세요",
                "interpretation_type": "full",
            }
        }
    )


class ChatResponse(BaseModel):
    """대화 응답"""

    success: bool = True
    session_id: str = Field(..., description="세션 ID")
    message: str = Field(..., description="응답 메시지")
    suggested_questions: list[str] = Field(default_factory=list, description="추천 질문 목록")
    interpretations: dict[str, Any] | None = Field(None, description="해석 결과")
    agents_used: list[str] = Field(default_factory=list, description="사용된 에이전트")
    error: str | None = None


# ============== 세션 API 스키마 ==============


class SessionInfo(BaseModel):
    """세션 정보"""

    session_id: str
    created_at: str
    last_activity: str
    message_count: int
    name: str


class SessionListResponse(BaseModel):
    """세션 목록 응답"""

    success: bool = True
    sessions: list[SessionInfo]
    total: int


class SessionDetailResponse(BaseModel):
    """세션 상세 응답"""

    success: bool = True
    session: dict[str, Any] | None = None
    error: str | None = None


# ============== 상태 API 스키마 ==============


class HealthResponse(BaseModel):
    """헬스체크 응답"""

    status: str = "ok"
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ErrorResponse(BaseModel):
    """에러 응답"""

    success: bool = False
    error: str
    detail: str | None = None


# ============== 분석 API 스키마 ==============


class AnalysisType(str, Enum):
    """분석 유형"""

    # 운세 분석 (5가지)
    FORTUNE_GENERAL = "fortune_general"
    FORTUNE_CAREER = "fortune_career"
    FORTUNE_WEALTH = "fortune_wealth"
    FORTUNE_HEALTH = "fortune_health"
    FORTUNE_LOVE = "fortune_love"
    # 용신 분석
    YONGSIN = "yongsin"
    # 유파 비교
    SCHOOL_COMPARE = "school_compare"
    # 특정 용신 방법론
    YONGSIN_METHOD = "yongsin_method"


class YongSinMethodType(str, Enum):
    """용신 분석 방법론"""

    STRENGTH = "strength"  # 강약용신
    SEASONAL = "seasonal"  # 조후용신
    MEDIATION = "mediation"  # 통관용신
    DISEASE = "disease"  # 병약용신


class SchoolCodeType(str, Enum):
    """유파 코드"""

    ZIPING = "ziping"  # 자평명리
    DTS = "dts"  # 적천수
    QTBJ = "qtbj"  # 궁통보감
    MODERN = "modern"  # 현대명리
    SHENSHA = "shensha"  # 신살중심


class AnalysisRequest(BaseModel):
    """분석 요청"""

    session_id: str | None = Field(None, description="기존 세션 ID (새 세션은 null)")
    saju_data: dict[str, Any] | None = Field(None, description="새 세션시 사주 데이터")
    analysis_type: AnalysisType = Field(..., description="분석 유형")
    yongsin_method: YongSinMethodType | None = Field(
        None, description="용신 방법론 (YONGSIN_METHOD 타입일 때 필수)"
    )
    schools: list[SchoolCodeType] | None = Field(
        None, description="비교할 유파 목록 (SCHOOL_COMPARE 타입일 때, None이면 전체)"
    )
    message: str | None = Field(None, max_length=4000, description="추가 질문 메시지")
    model: ModelChoice | None = Field(
        default=None, description="사용할 OpenRouter 모델 (None이면 서버 기본 모델)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "session-123",
                "analysis_type": "fortune_general",
                "message": "올해 운세가 어떤가요?",
            }
        }
    )


class FortuneResult(BaseModel):
    """운세 분석 결과"""

    fortune_type: str
    score: int = Field(..., ge=0, le=100)
    summary: str
    positive: list[str] = Field(default_factory=list)
    negative: list[str] = Field(default_factory=list)
    advice: list[str] = Field(default_factory=list)
    lucky_colors: list[str] = Field(default_factory=list)
    lucky_numbers: list[int] = Field(default_factory=list)
    lucky_directions: list[str] = Field(default_factory=list)


class YongSinResultSchema(BaseModel):
    """용신 분석 결과"""

    primary_yongsin: str
    secondary_yongsin: str | None = None
    xi_sin: list[str] = Field(default_factory=list, description="희신")
    ji_sin: list[str] = Field(default_factory=list, description="기신")
    chou_sin: list[str] = Field(default_factory=list, description="수신")
    day_master_strength: str
    reasoning: str
    method: str
    confidence: float = Field(..., ge=0, le=1)
    recommendations: dict[str, list[str]] = Field(default_factory=dict)


class SchoolInterpretationSchema(BaseModel):
    """유파 해석 결과"""

    school: str
    school_name: str
    yong_sin: str
    geok_guk: str | None = None
    overall: str
    health: str
    wealth: str
    career: str
    relationship: str
    fame: str
    confidence: float = Field(..., ge=0, le=1)
    key_features: list[str] = Field(default_factory=list)


class SchoolComparisonSchema(BaseModel):
    """유파 비교 결과"""

    schools: list[str]
    interpretations: list[SchoolInterpretationSchema]
    consensus: list[dict[str, Any]] = Field(default_factory=list)
    differences: list[dict[str, Any]] = Field(default_factory=list)
    recommendation: str


class AnalysisResponse(BaseModel):
    """분석 응답"""

    success: bool = True
    session_id: str
    analysis_type: str
    message: str = Field(..., description="AI 분석 메시지")
    fortune_result: FortuneResult | None = None
    yongsin_result: YongSinResultSchema | None = None
    school_comparison: SchoolComparisonSchema | None = None
    suggested_questions: list[str] = Field(default_factory=list)
    error: str | None = None


class AnalysisTypesResponse(BaseModel):
    """분석 유형 목록 응답"""

    success: bool = True
    fortune_types: list[dict[str, str]]
    yongsin_methods: list[dict[str, str]]
    school_codes: list[dict[str, str]]
