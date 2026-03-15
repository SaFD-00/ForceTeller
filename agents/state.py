"""
LangGraph 상태 정의

에이전트 그래프의 상태를 TypedDict로 정의합니다.
add_messages reducer를 사용하여 메시지를 자동 누적합니다.
"""

from typing import Annotated, Optional, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """에이전트 그래프 상태

    LangGraph StateGraph에서 사용하는 상태 정의입니다.
    Annotated를 사용하여 reducer 함수를 지정합니다.

    Attributes:
        messages: 메시지 히스토리 (add_messages reducer로 자동 누적)
        saju_data: 사주 데이터 (불변)
        current_agent: 현재 실행 중인 에이전트 이름
        next_agent: 다음에 실행할 에이전트 이름
        interpretations: 각 에이전트의 해석 결과 누적
        iteration: 반복 카운터 (무한 루프 방지)
        final_output: 최종 종합 출력
        error: 에러 정보
    """
    # 메시지 히스토리 (자동 누적)
    messages: Annotated[list[BaseMessage], add_messages]

    # 사주 데이터 (불변)
    saju_data: dict[str, Any]

    # 현재 에이전트 정보
    current_agent: str

    # 라우팅 결정
    next_agent: Optional[str]

    # 해석 결과 누적
    interpretations: dict[str, dict]

    # 반복 카운터
    iteration: int

    # 최종 출력
    final_output: Optional[str]

    # 에러 정보
    error: Optional[str]


def create_initial_state(
    saju_data: dict[str, Any],
    messages: list[BaseMessage] | None = None
) -> AgentState:
    """초기 상태 생성

    Args:
        saju_data: 사주 데이터
        messages: 초기 메시지 (선택적)

    Returns:
        초기화된 AgentState
    """
    return AgentState(
        messages=messages or [],
        saju_data=saju_data,
        current_agent="",
        next_agent=None,
        interpretations={},
        iteration=0,
        final_output=None,
        error=None,
    )
