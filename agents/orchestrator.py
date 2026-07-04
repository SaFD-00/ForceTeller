"""
오케스트레이터 (LangGraph 기반)

에이전트 선택 및 조율을 담당합니다.
사용할 모델은 그래프 실행 config로 주입되어 각 노드로 전달됩니다.
"""

import uuid
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage

from agents.graph import get_graph
from agents.state import AgentState, create_initial_state
from config.settings import settings


class Orchestrator:
    """LangGraph 기반 오케스트레이터

    Supervisor 패턴으로 에이전트를 동적 선택/실행합니다.

    Attributes:
        model: 사용할 OpenRouter 모델 ID (None이면 설정 기본값)
        graph: 컴파일된 LangGraph (싱글톤)

    Example:
        >>> orchestrator = Orchestrator()
        >>> result = await orchestrator.route_and_interpret(
        ...     saju_data=saju_data,
        ...     question="제 성격은 어떤가요?"
        ... )
    """

    def __init__(self, model: str | None = None):
        """
        Args:
            model: OpenRouter 모델 ID (None이면 설정 기본값)
        """
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

        Args:
            saju_data: 사주 계산 결과
            question: 사용자 질문
            conversation_history: 대화 이력 (선택적)
            include_synthesis: 종합 해석 포함 여부
            thread_id: 대화 스레드 ID (체크포인팅용)

        Returns:
            {"agents_used": [...], "interpretations": {...},
             "synthesis": {...}, "routing_info": {...}}
        """
        messages: list = []

        # 대화 히스토리 변환 (최근 N개)
        if conversation_history:
            for msg in conversation_history[-settings.CONVERSATION_HISTORY_LIMIT :]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

        # 사용자 질문 추가
        messages.append(HumanMessage(content=question))

        # 초기 상태 구성
        initial_state = create_initial_state(saju_data=saju_data, messages=messages)

        # 그래프 실행 설정 (모델을 노드로 전달)
        config = {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4()),
                "model": self.model,
                "routing_model": settings.OPENROUTER_ROUTING_MODEL,
            }
        }

        # 그래프 실행
        result = await self.graph.ainvoke(initial_state, config=config)

        return self._format_result(result, include_synthesis)

    def _format_result(
        self,
        state: AgentState,
        include_synthesis: bool = True,
    ) -> dict[str, Any]:
        """LangGraph 결과를 API 응답 형식으로 변환"""
        interpretations = state.get("interpretations", {})
        agents_used = list(interpretations.keys())

        result = {
            "agents_used": agents_used,
            "interpretations": interpretations,
            "synthesis": None,
            "routing_info": {
                "agents": agents_used,
                "reasoning": "LangGraph Supervisor 패턴 기반 동적 라우팅",
            },
        }

        if include_synthesis and state.get("final_output"):
            result["synthesis"] = {
                "agent_name": "synthesis",
                "interpretation": state.get("final_output"),
                "confidence": 1.0,
                "suggested_questions": [],
            }

        if state.get("error"):
            result["error"] = state.get("error")

        return result
