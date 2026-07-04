"""
LangGraph 노드 함수

각 에이전트를 LangGraph 노드 함수로 구현합니다.
노드 함수는 AgentState와 RunnableConfig를 받아 상태 업데이트를 반환합니다.
사용할 모델은 config["configurable"]["model"]로 요청별 주입됩니다.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from agents.agent_configs import AGENT_CONFIGS
from agents.llm import ainvoke_structured, create_structured_llm
from agents.prompts.system_prompts import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    format_saju_context,
)
from agents.schemas import InterpretationResult, RouterDecision, SynthesisResult
from agents.state import AgentState
from config.logging_config import get_logger

logger = get_logger(__name__)

# 최대 반복 횟수 (무한 루프 방지)
MAX_ITERATIONS = 10


def _model_from_config(config: RunnableConfig | None, *, routing: bool = False) -> str | None:
    """RunnableConfig에서 사용할 모델 ID 추출

    Args:
        config: LangGraph가 주입하는 실행 설정
        routing: True면 라우팅(경량) 모델 우선

    Returns:
        모델 ID (없으면 None → 설정 기본값 사용)
    """
    configurable = (config or {}).get("configurable", {}) if config else {}
    if routing:
        return configurable.get("routing_model") or configurable.get("model")
    return configurable.get("model")


async def supervisor_node(state: AgentState, config: RunnableConfig) -> dict:
    """Supervisor 노드: 다음 에이전트 결정

    사용자 질문과 현재까지의 해석 결과를 분석하여
    다음에 실행할 에이전트를 선택합니다.
    """
    # 반복 횟수 체크
    if state.get("iteration", 0) >= MAX_ITERATIONS:
        return {
            "next_agent": "FINISH",
            "messages": [AIMessage(content="[Supervisor] 최대 반복 횟수 도달")],
        }

    llm = create_structured_llm(RouterDecision, model=_model_from_config(config, routing=True))

    # 사용 가능한 에이전트 목록 (synthesis 제외)
    available_agents = [
        f"- {name}: {cfg.interpretation_focus}"
        for name, cfg in AGENT_CONFIGS.items()
        if name != "synthesis"
    ]

    # 완료된 해석 목록
    completed = list(state.get("interpretations", {}).keys())

    system_content = f"""{ORCHESTRATOR_SYSTEM_PROMPT}

## 사용 가능한 에이전트
{chr(10).join(available_agents)}

## 선택 규칙
1. 사용자 질문에 가장 적합한 에이전트를 선택하세요.
2. 이미 완료된 에이전트는 다시 선택하지 마세요.
3. 필요한 해석이 모두 완료되면 'synthesis'를 선택하세요.
4. 종합 해석까지 완료되면 'FINISH'를 선택하세요."""

    human_content = (
        f"현재까지 완료된 해석: {', '.join(completed) if completed else '없음'}\n\n"
        "다음 에이전트를 선택하세요."
    )

    # ChatPromptTemplate를 거치지 않고 메시지를 직접 구성한다.
    # (동적 텍스트의 중괄호가 템플릿 변수로 오인되는 문제 방지)
    messages = [
        SystemMessage(content=system_content),
        *state["messages"],
        HumanMessage(content=human_content),
    ]

    try:
        decision = await ainvoke_structured(llm, messages)
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


async def route_question(question: str, model: str | None = None) -> str:
    """단발 라우팅: 질문에 가장 적합한 인터프리터 에이전트 1개 선택

    스트리밍 채팅 경로처럼 LangGraph 그래프를 거치지 않고
    가벼운 라우팅 모델로 에이전트만 빠르게 결정할 때 사용한다.

    Args:
        question: 사용자 질문
        model: 라우팅에 사용할 모델 ID (None이면 설정 기본값)

    Returns:
        선택된 에이전트 이름 (실패 시 'personality')
    """
    available_agents = [
        f"- {name}: {cfg.interpretation_focus}"
        for name, cfg in AGENT_CONFIGS.items()
        if name != "synthesis"
    ]
    system_content = f"""{ORCHESTRATOR_SYSTEM_PROMPT}

## 사용 가능한 에이전트
{chr(10).join(available_agents)}

## 선택 규칙
사용자 질문에 가장 적합한 에이전트 하나를 선택하세요.
synthesis나 FINISH는 선택하지 마세요."""

    llm = create_structured_llm(RouterDecision, model=model)
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=question),
    ]

    try:
        decision = await ainvoke_structured(llm, messages)
        agent = decision.next_agent
        if agent in AGENT_CONFIGS and agent != "synthesis":
            return agent
    except Exception as exc:
        logger.warning("라우팅 결정 실패, 기본 에이전트(personality)로 폴백: %s", exc)
    return "personality"


async def interpreter_node(
    state: AgentState,
    agent_name: str,
    config: RunnableConfig,
) -> dict:
    """해석 에이전트 노드 (파라미터화)

    특정 에이전트의 해석을 수행합니다.
    """
    agent_config = AGENT_CONFIGS.get(agent_name)
    if not agent_config:
        return {
            "error": f"Unknown agent: {agent_name}",
            "messages": [AIMessage(content=f"[Error] 알 수 없는 에이전트: {agent_name}")],
        }

    llm = create_structured_llm(InterpretationResult, model=_model_from_config(config))

    # 사주 컨텍스트 생성
    saju_context = format_saju_context(state["saju_data"])

    # 마지막 사용자 질문 추출
    user_question = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            user_question = msg.content
            break

    human_content = (
        f"{saju_context}\n\n"
        f"## 사용자 질문\n{user_question}\n\n"
        f"## 요청\n{agent_config.interpretation_focus}에 대해 상세히 해석해 주세요."
    )
    messages = [
        SystemMessage(content=agent_config.system_prompt),
        HumanMessage(content=human_content),
    ]

    try:
        result = await ainvoke_structured(llm, messages)

        # 기존 해석에 추가
        interpretations = dict(state.get("interpretations", {}))
        interpretations[agent_name] = result.model_dump()

        return {
            "interpretations": interpretations,
            "current_agent": agent_name,
            "messages": [
                AIMessage(content=f"[{agent_config.display_name}]\n\n{result.interpretation}")
            ],
            "iteration": state.get("iteration", 0) + 1,
        }
    except Exception as e:
        return {
            "error": str(e),
            "current_agent": agent_name,
            "messages": [AIMessage(content=f"[{agent_config.display_name}] 해석 실패: {e}")],
            "iteration": state.get("iteration", 0) + 1,
        }


async def synthesis_node(state: AgentState, config: RunnableConfig) -> dict:
    """종합 해석 노드

    모든 에이전트의 해석 결과를 종합하여
    통합된 인생 해석을 제공합니다.
    """
    agent_config = AGENT_CONFIGS.get("synthesis")
    if not agent_config:
        return {
            "error": "synthesis config not found",
            "next_agent": "FINISH",
        }

    llm = create_structured_llm(SynthesisResult, model=_model_from_config(config))

    # 모든 해석 결과 수집
    interpretations = state.get("interpretations", {})
    if not interpretations:
        return {
            "final_output": "해석 결과가 없습니다.",
            "next_agent": "FINISH",
            "messages": [AIMessage(content="[종합 분석] 해석 결과가 없습니다.")],
        }

    interpretations_summary = "\n\n".join(
        [
            f"### {AGENT_CONFIGS.get(name).display_name if AGENT_CONFIGS.get(name) else name} 해석\n{data.get('interpretation', '')}"
            for name, data in interpretations.items()
        ]
    )

    # 사주 컨텍스트
    saju_context = format_saju_context(state["saju_data"])

    human_content = (
        f"{saju_context}\n\n"
        f"## 각 전문 에이전트의 해석\n{interpretations_summary}\n\n"
        "## 요청\n위 해석들을 종합하여 일관성 있고 균형 잡힌 통합 해석을 제공해 주세요."
    )
    messages = [
        SystemMessage(content=agent_config.system_prompt),
        HumanMessage(content=human_content),
    ]

    try:
        result = await ainvoke_structured(llm, messages)
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

    LangGraph는 (state, config) 시그니처의 노드에 RunnableConfig를 자동 주입한다.
    agent_name은 클로저로 바인딩한다.

    Example:
        >>> personality_node = create_interpreter_node("personality")
        >>> graph.add_node("personality", personality_node)
    """

    async def node(state: AgentState, config: RunnableConfig) -> dict:
        return await interpreter_node(state, agent_name, config)

    return node


def route_to_next(state: AgentState) -> str:
    """다음 노드 결정 라우터

    supervisor_node의 결과(next_agent)를 기반으로 다음 노드를 결정합니다.
    """
    next_agent = state.get("next_agent", "FINISH")

    # 유효한 에이전트인지 확인
    valid_agents = list(AGENT_CONFIGS.keys()) + ["FINISH"]
    if next_agent not in valid_agents:
        return "FINISH"

    return next_agent
