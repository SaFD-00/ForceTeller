"""
API 스키마 정의
Pydantic 모델로 요청/응답 스키마 정의
"""

from datetime import date, time, datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


# ============== 공통 스키마 ==============

class CalendarType(str, Enum):
    SOLAR = "solar"
    LUNAR = "lunar"
    LEAP_LUNAR = "leap_lunar"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class InterpretationType(str, Enum):
    FULL = "full"           # 전체 해석
    QUICK = "quick"         # 빠른 단일 해석
    SPECIFIC = "specific"   # 특정 분야 해석


class LLMProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"


# ============== 만세력 API 스키마 ==============

class ManseolRequest(BaseModel):
    """사주 계산 요청"""
    name: str = Field(..., min_length=1, max_length=50, description="이름")
    birth_date: date = Field(..., description="생년월일 (YYYY-MM-DD)")
    birth_time: Optional[str] = Field(None, description="출생시간 (HH:MM)")
    calendar: CalendarType = Field(default=CalendarType.SOLAR, description="달력 유형")
    city: str = Field(default="Seoul", description="출생 도시")
    gender: Gender = Field(..., description="성별")
    jajasi: bool = Field(default=False, description="야자시/조자시 적용")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="직접 입력 경도")
    apply_time_correction: bool = Field(default=True, description="시간 보정 적용")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "birth_date": "1990-05-15",
                "birth_time": "14:30",
                "calendar": "solar",
                "city": "Seoul",
                "gender": "male",
                "jajasi": False
            }
        }


class ManseolResponse(BaseModel):
    """사주 계산 응답"""
    success: bool = True
    data: Dict[str, Any] = Field(..., description="사주 계산 결과")
    error: Optional[str] = None


# ============== 채팅 API 스키마 ==============

class ChatRequest(BaseModel):
    """대화 요청"""
    session_id: Optional[str] = Field(None, description="기존 세션 ID (새 세션은 null)")
    saju_data: Optional[Dict[str, Any]] = Field(None, description="새 세션시 사주 데이터")
    message: str = Field(..., min_length=1, description="사용자 메시지")
    interpretation_type: InterpretationType = Field(
        default=InterpretationType.FULL,
        description="해석 유형"
    )
    focus: Optional[str] = Field(
        None,
        description="특정 해석 분야 (personality/career/relationship/health/fortune)"
    )
    llm_provider: LLMProvider = Field(
        default=LLMProvider.OPENAI,
        description="LLM 제공자"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": None,
                "saju_data": {"meta": {}, "input": {}, "pillars": {}},
                "message": "제 성격에 대해 알려주세요",
                "interpretation_type": "full"
            }
        }


class ChatResponse(BaseModel):
    """대화 응답"""
    success: bool = True
    session_id: str = Field(..., description="세션 ID")
    message: str = Field(..., description="응답 메시지")
    suggested_questions: List[str] = Field(default_factory=list, description="추천 질문 목록")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="해석 결과")
    agents_used: List[str] = Field(default_factory=list, description="사용된 에이전트")
    error: Optional[str] = None


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
    sessions: List[SessionInfo]
    total: int


class SessionDetailResponse(BaseModel):
    """세션 상세 응답"""
    success: bool = True
    session: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


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
    detail: Optional[str] = None


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
    STRENGTH = "strength"      # 강약용신
    SEASONAL = "seasonal"      # 조후용신
    MEDIATION = "mediation"    # 통관용신
    DISEASE = "disease"        # 병약용신


class SchoolCodeType(str, Enum):
    """유파 코드"""
    ZIPING = "ziping"        # 자평명리
    DTS = "dts"              # 적천수
    QTBJ = "qtbj"            # 궁통보감
    MODERN = "modern"        # 현대명리
    SHENSHA = "shensha"      # 신살중심


class AnalysisRequest(BaseModel):
    """분석 요청"""
    session_id: Optional[str] = Field(None, description="기존 세션 ID (새 세션은 null)")
    saju_data: Optional[Dict[str, Any]] = Field(None, description="새 세션시 사주 데이터")
    analysis_type: AnalysisType = Field(..., description="분석 유형")
    yongsin_method: Optional[YongSinMethodType] = Field(
        None,
        description="용신 방법론 (YONGSIN_METHOD 타입일 때 필수)"
    )
    schools: Optional[List[SchoolCodeType]] = Field(
        None,
        description="비교할 유파 목록 (SCHOOL_COMPARE 타입일 때, None이면 전체)"
    )
    message: Optional[str] = Field(
        None,
        description="추가 질문 메시지"
    )
    llm_provider: LLMProvider = Field(
        default=LLMProvider.OPENAI,
        description="LLM 제공자"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session-123",
                "analysis_type": "fortune_general",
                "message": "올해 운세가 어떤가요?"
            }
        }


class FortuneResult(BaseModel):
    """운세 분석 결과"""
    fortune_type: str
    score: int = Field(..., ge=0, le=100)
    summary: str
    positive: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)
    advice: List[str] = Field(default_factory=list)
    lucky_colors: List[str] = Field(default_factory=list)
    lucky_numbers: List[int] = Field(default_factory=list)
    lucky_directions: List[str] = Field(default_factory=list)


class YongSinResultSchema(BaseModel):
    """용신 분석 결과"""
    primary_yongsin: str
    secondary_yongsin: Optional[str] = None
    xi_sin: List[str] = Field(default_factory=list, description="희신")
    ji_sin: List[str] = Field(default_factory=list, description="기신")
    chou_sin: List[str] = Field(default_factory=list, description="수신")
    day_master_strength: str
    reasoning: str
    method: str
    confidence: float = Field(..., ge=0, le=1)
    recommendations: Dict[str, List[str]] = Field(default_factory=dict)


class SchoolInterpretationSchema(BaseModel):
    """유파 해석 결과"""
    school: str
    school_name: str
    yong_sin: str
    geok_guk: Optional[str] = None
    overall: str
    health: str
    wealth: str
    career: str
    relationship: str
    fame: str
    confidence: float = Field(..., ge=0, le=1)
    key_features: List[str] = Field(default_factory=list)


class SchoolComparisonSchema(BaseModel):
    """유파 비교 결과"""
    schools: List[str]
    interpretations: List[SchoolInterpretationSchema]
    consensus: List[Dict[str, Any]] = Field(default_factory=list)
    differences: List[Dict[str, Any]] = Field(default_factory=list)
    recommendation: str


class AnalysisResponse(BaseModel):
    """분석 응답"""
    success: bool = True
    session_id: str
    analysis_type: str
    message: str = Field(..., description="AI 분석 메시지")
    fortune_result: Optional[FortuneResult] = None
    yongsin_result: Optional[YongSinResultSchema] = None
    school_comparison: Optional[SchoolComparisonSchema] = None
    suggested_questions: List[str] = Field(default_factory=list)
    error: Optional[str] = None


class AnalysisTypesResponse(BaseModel):
    """분석 유형 목록 응답"""
    success: bool = True
    fortune_types: List[Dict[str, str]]
    yongsin_methods: List[Dict[str, str]]
    school_codes: List[Dict[str, str]]
