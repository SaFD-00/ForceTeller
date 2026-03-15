"""
LangGraph 노드 함수

각 에이전트를 LangGraph 노드 함수로 구현합니다.
노드 함수는 AgentState를 받아 상태 업데이트를 반환합니다.
"""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agents.state import AgentState
from agents.schemas import InterpretationResult, RouterDecision, SynthesisResult
from agents.llm import create_structured_llm, create_llm
from agents.prompts.system_prompts import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    format_saju_context,
)
from agents.agent_configs import AGENT_CONFIGS


# 최대 반복 횟수 (무한 루프 방지)
MAX_ITERATIONS = 10


async def supervisor_node(state: AgentState) -> dict:
    """Supervisor 노드: 다음 에이전트 결정

    사용자 질문과 현재까지의 해석 결과를 분석하여
    다음에 실행할 에이전트를 선택합니다.

    Args:
        state: 현재 그래프 상태

    Returns:
        {"next_agent": str, "messages": list}
    """
    # 반복 횟수 체크
    if state.get("iteration", 0) >= MAX_ITERATIONS:
        return {
            "next_agent": "FINISH",
            "messages": [AIMessage(content="[Supervisor] 최대 반복 횟수 도달")],
        }

    llm = create_structured_llm(RouterDecision, provider="openai")

    # 사용 가능한 에이전트 목록 (synthesis 제외)
    available_agents = [
        f"- {name}: {config.interpretation_focus}"
        for name, config in AGENT_CONFIGS.items()
        if name != "synthesis"
    ]

    # 완료된 해석 목록
    completed = list(state.get("interpretations", {}).keys())

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""{ORCHESTRATOR_SYSTEM_PROMPT}

## 사용 가능한 에이전트
{chr(10).join(available_agents)}

## 선택 규칙
1. 사용자 질문에 가장 적합한 에이전트를 선택하세요.
2. 이미 완료된 에이전트는 다시 선택하지 마세요.
3. 필요한 해석이 모두 완료되면 'synthesis'를 선택하세요.
4. 종합 해석까지 완료되면 'FINISH'를 선택하세요.
"""),
        MessagesPlaceholder("messages"),
        ("human", f"""
현재까지 완료된 해석: {', '.join(completed) if completed else '없음'}

다음 에이전트를 선택하세요.
"""),
    ])

    chain = prompt | llm

    try:
        decision = await chain.ainvoke({
            "messages": state["messages"],
        })

        return {
            "next_agent": decision.next_agent,
            "messages": [AIMessage(content=f"[Supervisor] {decision.reasoning}")],
        }
    except Exception as e:
        # 에러 시 기본값으로 personality 선택
        return {
            "next_agent": "personality" if not completed else "synthesis",
            "error": str(e),
            "messages": [AIMessage(content=f"[Supervisor] 에러 발생, 기본 에이전트 선택: {e}")],
        }


async def interpreter_node(state: AgentState, agent_name: str) -> dict:
    """해석 에이전트 노드 (파라미터화)

    특정 에이전트의 해석을 수행합니다.

    Args:
        state: 현재 상태
        agent_name: 에이전트 이름

    Returns:
        상태 업데이트 딕셔너리
    """
    config = AGENT_CONFIGS.get(agent_name)
    if not config:
        return {
            "error": f"Unknown agent: {agent_name}",
            "messages": [AIMessage(content=f"[Error] 알 수 없는 에이전트: {agent_name}")],
        }

    llm = create_structured_llm(InterpretationResult, provider="openai")

    # 사주 컨텍스트 생성
    saju_context = format_saju_context(state["saju_data"])

    # 마지막 사용자 질문 추출
    user_question = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            user_question = msg.content
            break

    prompt = ChatPromptTemplate.from_messages([
        ("system", config.system_prompt),
        ("human", f"""
{saju_context}

## 사용자 질문
{user_question}

## 요청
{config.interpretation_focus}에 대해 상세히 해석해 주세요.
"""),
    ])

    chain = prompt | llm

    try:
        result = await chain.ainvoke({})

        # 기존 해석에 추가
        interpretations = dict(state.get("interpretations", {}))
        interpretations[agent_name] = result.model_dump()

        return {
            "interpretations": interpretations,
            "current_agent": agent_name,
            "messages": [AIMessage(
                content=f"[{config.display_name}]\n\n{result.interpretation}"
            )],
            "iteration": state.get("iteration", 0) + 1,
        }
    except Exception as e:
        return {
            "error": str(e),
            "current_agent": agent_name,
            "messages": [AIMessage(content=f"[{config.display_name}] 해석 실패: {e}")],
            "iteration": state.get("iteration", 0) + 1,
        }


async def synthesis_node(state: AgentState) -> dict:
    """종합 해석 노드

    모든 에이전트의 해석 결과를 종합하여
    통합된 인생 해석을 제공합니다.

    Args:
        state: 현재 상태

    Returns:
        상태 업데이트 딕셔너리
    """
    config = AGENT_CONFIGS.get("synthesis")
    if not config:
        return {
            "error": "synthesis config not found",
            "next_agent": "FINISH",
        }

    llm = create_structured_llm(SynthesisResult, provider="openai")

    # 모든 해석 결과 수집
    interpretations = state.get("interpretations", {})
    if not interpretations:
        return {
            "final_output": "해석 결과가 없습니다.",
            "next_agent": "FINISH",
            "messages": [AIMessage(content="[종합 분석] 해석 결과가 없습니다.")],
        }

    interpretations_summary = "\n\n".join([
        f"### {AGENT_CONFIGS.get(name, {}).display_name if AGENT_CONFIGS.get(name) else name} 해석\n{data.get('interpretation', '')}"
        for name, data in interpretations.items()
    ])

    # 사주 컨텍스트
    saju_context = format_saju_context(state["saju_data"])

    prompt = ChatPromptTemplate.from_messages([
        ("system", config.system_prompt),
        ("human", f"""
{saju_context}

## 각 전문 에이전트의 해석
{interpretations_summary}

## 요청
위 해석들을 종합하여 일관성 있고 균형 잡힌 통합 해석을 제공해 주세요.
"""),
    ])

    chain = prompt | llm

    try:
        result = await chain.ainvoke({})

        return {
            "final_output": result.synthesis,
            "current_agent": "synthesis",
            "next_agent": "FINISH",
            "messages": [AIMessage(content=f"[종합 분석]\n\n{result.synthesis}")],
        }
    except Exception as e:
        return {
            "error": str(e),
            "next_agent": "FINISH",
            "messages": [AIMessage(content=f"[종합 분석] 실패: {e}")],
        }


def create_interpreter_node(agent_name: str):
    """특정 에이전트 이름으로 바인딩된 노드 함수 생성

    LangGraph에서 노드 함수는 단일 인자(state)만 받으므로,
    agent_name을 클로저로 바인딩합니다.

    Args:
        agent_name: 바인딩할 에이전트 이름

    Returns:
        바인딩된 노드 함수

    Example:
        >>> personality_node = create_interpreter_node("personality")
        >>> graph.add_node("personality", personality_node)
    """
    async def node(state: AgentState) -> dict:
        return await interpreter_node(state, agent_name)
    return node


def route_to_next(state: AgentState) -> str:
    """다음 노드 결정 라우터

    supervisor_node의 결과(next_agent)를 기반으로
    다음 노드를 결정합니다.

    Args:
        state: 현재 상태

    Returns:
        다음 노드 이름
    """
    next_agent = state.get("next_agent", "FINISH")

    # 유효한 에이전트인지 확인
    valid_agents = list(AGENT_CONFIGS.keys()) + ["FINISH"]
    if next_agent not in valid_agents:
        return "FINISH"

    return next_agent
