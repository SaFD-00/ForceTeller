"""
오케스트레이터 (LangGraph 기반)

에이전트 선택 및 조율을 담당합니다.
기존 인터페이스를 유지하면서 내부 구현을 LangGraph로 전환했습니다.
"""

import uuid
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage

from agents.graph import get_graph
from agents.state import AgentState, create_initial_state


class Orchestrator:
    """LangGraph 기반 오케스트레이터

    기존 인터페이스 호환성을 유지하면서 내부 구현을 LangGraph StateGraph로 전환했습니다.

    Attributes:
        llm_provider: LLM 제공자 (openai, google)
        model: 사용할 모델명
        graph: 컴파일된 LangGraph

    Example:
        >>> orchestrator = Orchestrator()
        >>> result = await orchestrator.route_and_interpret(
        ...     saju_data=saju_data,
        ...     question="제 성격은 어떤가요?"
        ... )
    """

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str | None = None,
        use_llm_routing: bool = True,  # LangGraph는 항상 LLM 라우팅 사용
    ):
        """
        Args:
            llm_provider: LLM 제공자 (openai, google)
            model: 모델명 (None이면 기본값)
            use_llm_routing: LLM 기반 라우팅 (LangGraph에서는 항상 True)
        """
        self.llm_provider = llm_provider
        self.model = model
        self.graph = get_graph()

    async def route_and_interpret(
        self,
        saju_data: dict,
        question: str,
        conversation_history: list[dict] | None = None,
        include_synthesis: bool = True,
        thread_id: str | None = None,
    ) -> dict[str, Any]:
        """질문을 분석하여 적절한 에이전트로 라우팅하고 해석 수행

        LangGraph StateGraph를 사용하여 자동으로 에이전트를 선택하고 실행합니다.
        Supervisor 패턴을 사용하여 동적 라우팅을 수행합니다.

        Args:
            saju_data: 사주 계산 결과
            question: 사용자 질문
            conversation_history: 대화 이력 (선택적)
            include_synthesis: 종합 해석 포함 여부
            thread_id: 대화 스레드 ID (체크포인팅용)

        Returns:
            {
                "agents_used": [...],
                "interpretations": {...},
                "synthesis": {...},
                "routing_info": {...}
            }
        """
        # 초기 메시지 구성
        messages: list = []

        # 대화 히스토리 변환
        if conversation_history:
            for msg in conversation_history[-10:]:  # 최근 10개만
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

        # 사용자 질문 추가
        messages.append(HumanMessage(content=question))

        # 초기 상태 구성
        initial_state = create_initial_state(
            saju_data=saju_data,
            messages=messages,
        )

        # 그래프 실행 설정
        config = {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4())
            }
        }

        # 그래프 실행
        result = await self.graph.ainvoke(initial_state, config=config)

        # 결과 변환 (기존 형식 호환)
        return self._format_result(result, include_synthesis)

    def _format_result(
        self,
        state: AgentState,
        include_synthesis: bool = True
    ) -> dict[str, Any]:
        """LangGraph 결과를 기존 API 형식으로 변환

        Args:
            state: 그래프 실행 결과 상태
            include_synthesis: 종합 해석 포함 여부

        Returns:
            기존 API 호환 형식의 결과
        """
        interpretations = state.get("interpretations", {})
        agents_used = list(interpretations.keys())

        result = {
            "agents_used": agents_used,
            "interpretations": interpretations,
            "synthesis": None,
            "routing_info": {
                "agents": agents_used,
                "reasoning": "LangGraph Supervisor 패턴 기반 동적 라우팅",
            }
        }

        # 종합 해석 추가
        if include_synthesis and state.get("final_output"):
            result["synthesis"] = {
                "agent_name": "synthesis",
                "interpretation": state.get("final_output"),
                "confidence": 1.0,
                "suggested_questions": [],
            }

        # 에러 정보 추가
        if state.get("error"):
            result["error"] = state.get("error")

        return result

    async def interpret_full(
        self,
        saju_data: dict,
        conversation_history: list[dict] | None = None
    ) -> dict[str, Any]:
        """전체 해석 수행

        모든 관련 에이전트를 사용하여 종합적인 사주 해석을 수행합니다.

        Args:
            saju_data: 사주 계산 결과
            conversation_history: 대화 이력

        Returns:
            전체 해석 결과
        """
        return await self.route_and_interpret(
            saju_data=saju_data,
            question="전체적으로 사주를 분석해 주세요. "
                     "성격, 직업, 대인관계, 건강, 운세를 종합적으로 해석해 주세요.",
            conversation_history=conversation_history,
            include_synthesis=True
        )

    async def quick_interpret(
        self,
        saju_data: dict,
        focus: str = "personality"
    ) -> dict[str, Any]:
        """빠른 단일 해석

        특정 영역에 집중한 빠른 해석을 수행합니다.

        Args:
            saju_data: 사주 계산 결과
            focus: 해석 초점 (personality, career, relationship 등)

        Returns:
            단일 영역 해석 결과
        """
        focus_mapping = {
            "personality": "제 성격과 기질에 대해 알려주세요.",
            "career": "직업운과 재물운에 대해 알려주세요.",
            "relationship": "연애운과 대인관계에 대해 알려주세요.",
            "health": "건강운에 대해 알려주세요.",
            "fortune": "올해와 앞으로의 운세에 대해 알려주세요.",
            "yongsin": "용신과 개운법에 대해 알려주세요.",
        }

        question = focus_mapping.get(focus, f"{focus}에 대해 해석해 주세요.")

        return await self.route_and_interpret(
            saju_data=saju_data,
            question=question,
            include_synthesis=False
        )

    async def continue_conversation(
        self,
        saju_data: dict,
        question: str,
        thread_id: str,
        conversation_history: list[dict] | None = None,
    ) -> dict[str, Any]:
        """대화 계속하기

        이전 대화를 이어서 새로운 질문에 답변합니다.
        thread_id를 통해 이전 상태를 복원합니다.

        Args:
            saju_data: 사주 계산 결과
            question: 새로운 질문
            thread_id: 이전 대화의 thread_id
            conversation_history: 추가 대화 이력

        Returns:
            해석 결과
        """
        return await self.route_and_interpret(
            saju_data=saju_data,
            question=question,
            conversation_history=conversation_history,
            thread_id=thread_id,
            include_synthesis=True
        )
