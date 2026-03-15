"""
LangGraph StateGraph 빌드

ForceTeller의 에이전트 그래프를 구성하고 컴파일합니다.
Supervisor 패턴을 사용하여 동적 라우팅을 구현합니다.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agents.state import AgentState
from agents.nodes import (
    supervisor_node,
    synthesis_node,
    create_interpreter_node,
    route_to_next,
)
from agents.agent_configs import AGENT_CONFIGS


def build_forceteller_graph() -> StateGraph:
    """ForceTeller 메인 그래프 빌드

    Supervisor Pattern:
    START -> supervisor -> {agent} -> supervisor -> ... -> synthesis -> END

    Flow:
    1. START에서 supervisor로 이동
    2. supervisor가 다음 에이전트 결정
    3. 해석 에이전트 실행 후 다시 supervisor로
    4. 모든 해석 완료 시 synthesis 실행
    5. synthesis 완료 후 END

    Returns:
        구성된 StateGraph (컴파일 전)
    """
    graph = StateGraph(AgentState)

    # 1. 노드 추가
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("synthesis", synthesis_node)

    # 해석 에이전트 노드들 (synthesis 제외)
    interpreter_agents = [
        name for name in AGENT_CONFIGS.keys()
        if name != "synthesis"
    ]

    for agent_name in interpreter_agents:
        graph.add_node(agent_name, create_interpreter_node(agent_name))

    # 2. 엣지 정의

    # START -> supervisor
    graph.add_edge(START, "supervisor")

    # supervisor -> 각 에이전트 (조건부 엣지)
    # route_to_next 함수가 next_agent 값을 반환
    routing_map = {name: name for name in interpreter_agents}
    routing_map["synthesis"] = "synthesis"
    routing_map["FINISH"] = END

    graph.add_conditional_edges(
        "supervisor",
        route_to_next,
        routing_map
    )

    # 각 해석 에이전트 -> supervisor (다음 결정을 위해)
    for agent_name in interpreter_agents:
        graph.add_edge(agent_name, "supervisor")

    # synthesis -> END
    graph.add_edge("synthesis", END)

    return graph


def compile_graph(
    checkpointer: bool = True,
    interrupt_before: list[str] | None = None,
):
    """그래프 컴파일

    Args:
        checkpointer: 체크포인터 사용 여부 (대화 상태 저장)
        interrupt_before: 인터럽트 지점 노드들 (human-in-the-loop)

    Returns:
        컴파일된 그래프 (실행 가능)

    Example:
        >>> graph = compile_graph()
        >>> result = await graph.ainvoke(initial_state, config={"configurable": {"thread_id": "1"}})
    """
    graph = build_forceteller_graph()

    memory = MemorySaver() if checkpointer else None

    return graph.compile(
        checkpointer=memory,
        interrupt_before=interrupt_before,
    )


# 기본 컴파일된 그래프 (싱글톤, lazy initialization)
_compiled_graph = None


def get_graph():
    """컴파일된 그래프 가져오기 (lazy singleton)

    처음 호출 시 그래프를 컴파일하고 캐시합니다.
    이후 호출에서는 캐시된 그래프를 반환합니다.

    Returns:
        컴파일된 그래프

    Example:
        >>> graph = get_graph()
        >>> result = await graph.ainvoke(state)
    """
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = compile_graph()
    return _compiled_graph


def reset_graph():
    """그래프 캐시 초기화

    테스트나 설정 변경 시 사용합니다.
    """
    global _compiled_graph
    _compiled_graph = None


def visualize_graph() -> str:
    """그래프 구조 시각화 (ASCII)

    Returns:
        그래프 구조를 나타내는 ASCII 문자열
    """
    interpreter_agents = [
        name for name in AGENT_CONFIGS.keys()
        if name != "synthesis"
    ]

    agents_str = ", ".join(interpreter_agents)

    return f"""
    ┌─────────────────────────────────────────────┐
    │           ForceTeller Agent Graph           │
    ├─────────────────────────────────────────────┤
    │                                             │
    │  START                                      │
    │    │                                        │
    │    ▼                                        │
    │  ┌─────────────┐                            │
    │  │  supervisor │◄────────────────┐          │
    │  └──────┬──────┘                 │          │
    │         │                        │          │
    │    ┌────┴────┐                   │          │
    │    ▼         ▼                   │          │
    │  ┌───┐   ┌───────────────────┐   │          │
    │  │...│   │ interpreter nodes │───┘          │
    │  │   │   │ ({agents_str})│          │
    │  └───┘   └───────────────────┘              │
    │    │                                        │
    │    ▼                                        │
    │  ┌───────────┐                              │
    │  │ synthesis │                              │
    │  └─────┬─────┘                              │
    │        │                                    │
    │        ▼                                    │
    │       END                                   │
    │                                             │
    └─────────────────────────────────────────────┘
    """
