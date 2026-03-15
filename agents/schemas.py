"""
에이전트 응답 스키마 정의

Pydantic 기반 통합 스키마로 모든 LLM Provider에서 동일한 구조화된 출력을 사용합니다.
"""

from typing import Optional
from pydantic import BaseModel, Field


class InterpretationResult(BaseModel):
    """에이전트 해석 결과 스키마

    모든 해석 에이전트가 반환하는 표준 응답 형식입니다.
    LangChain의 with_structured_output()과 함께 사용됩니다.
    """
    interpretation: str = Field(
        description="사주 해석 내용. 마크다운 형식으로 작성하되, "
                    "서두 인사나 불필요한 문구 없이 바로 본론부터 시작."
    )
    confidence: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="해석 신뢰도 (0.0 ~ 1.0)"
    )
    suggested_questions: list[str] = Field(
        default_factory=list,
        description="사용자가 이어서 할 수 있는 추천 질문 3개. "
                    "현재 해석 내용과 관련된 구체적인 질문으로 작성."
    )


class RouterDecision(BaseModel):
    """Supervisor 라우팅 결정

    Supervisor 노드가 다음 에이전트를 선택할 때 사용하는 스키마입니다.
    """
    next_agent: str = Field(
        description="다음 실행할 에이전트 이름. "
                    "선택 가능: personality, career, relationship, health, "
                    "fortune, yongsin, school_compare, synthesis, FINISH"
    )
    reasoning: str = Field(
        description="에이전트 선택 이유"
    )


class SynthesisResult(BaseModel):
    """종합 해석 결과

    Synthesis 에이전트가 반환하는 종합 해석 스키마입니다.
    """
    synthesis: str = Field(
        description="종합 해석 내용. 각 에이전트의 해석을 통합하여 "
                    "일관성 있고 균형 잡힌 인생 해석을 제공."
    )
    key_insights: list[str] = Field(
        default_factory=list,
        description="핵심 인사이트 요약 (3-5개)"
    )
    suggested_questions: list[str] = Field(
        default_factory=list,
        description="추가 탐색 질문"
    )


# Legacy compatibility - deprecated
def get_interpretation_schema() -> dict:
    """
    Structured Outputs용 JSON 스키마 반환

    Deprecated: InterpretationResult Pydantic 모델 사용을 권장합니다.

    OpenAI Structured Outputs 요구사항:
    - additionalProperties: false 필수
    - 모든 properties가 required에 포함
    - minItems, maxItems 등 일부 키워드 미지원
    """
    import warnings
    warnings.warn(
        "get_interpretation_schema() is deprecated. "
        "Use InterpretationResult Pydantic model instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return {
        "type": "object",
        "properties": {
            "interpretation": {
                "type": "string",
                "description": "사주 해석 내용. 마크다운 형식으로 작성하되, "
                               "서두 인사나 불필요한 문구 없이 바로 본론부터 시작."
            },
            "suggested_questions": {
                "type": "array",
                "description": "사용자가 이어서 할 수 있는 추천 질문 3개. "
                               "현재 해석 내용과 관련된 구체적인 질문으로 작성.",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["interpretation", "suggested_questions"],
        "additionalProperties": False
    }
