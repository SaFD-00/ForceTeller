"""
에이전트 응답 스키마 정의
OpenAI Structured Outputs 용
"""

from typing import List


def get_interpretation_schema() -> dict:
    """
    Structured Outputs용 JSON 스키마 반환

    OpenAI Structured Outputs 요구사항:
    - additionalProperties: false 필수
    - 모든 properties가 required에 포함
    - minItems, maxItems 등 일부 키워드 미지원
    """
    return {
        "type": "object",
        "properties": {
            "interpretation": {
                "type": "string",
                "description": "사주 해석 내용. 마크다운 형식으로 작성하되, 서두 인사나 불필요한 문구 없이 바로 본론부터 시작."
            },
            "suggested_questions": {
                "type": "array",
                "description": "사용자가 이어서 할 수 있는 추천 질문 3개. 현재 해석 내용과 관련된 구체적인 질문으로 작성.",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["interpretation", "suggested_questions"],
        "additionalProperties": False
    }
