"""
LangGraph 노드 함수 단위 테스트

route_question(단발 라우팅)과 create_initial_state(상태 초기화)를 LLM 호출 없이
검증한다. route_question은 create_structured_llm/ainvoke_structured 두 seam을
모킹해 실제 LLM·네트워크를 완전히 차단한다.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents.nodes import route_question
from agents.schemas import RouterDecision
from agents.state import create_initial_state


class TestRouteQuestion:
    """단발 라우팅: 질문 → 인터프리터 에이전트 1개"""

    async def test_returns_valid_agent(self):
        """RouterDecision이 유효 에이전트를 고르면 그 이름을 반환"""
        decision = RouterDecision(next_agent="career", reasoning="직업 관련 질문")

        with (
            patch("agents.nodes.create_structured_llm", return_value=MagicMock()),
            patch("agents.nodes.ainvoke_structured", new=AsyncMock(return_value=decision)),
        ):
            result = await route_question("직업운이 궁금해요")

        assert result == "career"

    async def test_synthesis_choice_falls_back_to_personality(self):
        """라우터가 synthesis를 고르면(단발 라우팅 대상 아님) personality로 폴백"""
        decision = RouterDecision(next_agent="synthesis", reasoning="종합")

        with (
            patch("agents.nodes.create_structured_llm", return_value=MagicMock()),
            patch("agents.nodes.ainvoke_structured", new=AsyncMock(return_value=decision)),
        ):
            result = await route_question("전체적으로 봐주세요")

        assert result == "personality"

    async def test_unknown_agent_falls_back_to_personality(self):
        """AGENT_CONFIGS에 없는 이름이면 personality로 폴백"""
        decision = RouterDecision(next_agent="does_not_exist", reasoning="?")

        with (
            patch("agents.nodes.create_structured_llm", return_value=MagicMock()),
            patch("agents.nodes.ainvoke_structured", new=AsyncMock(return_value=decision)),
        ):
            result = await route_question("아무거나")

        assert result == "personality"

    async def test_llm_error_falls_back_to_personality(self):
        """LLM 호출이 예외를 던지면 안전하게 personality로 폴백"""
        with (
            patch("agents.nodes.create_structured_llm", return_value=MagicMock()),
            patch(
                "agents.nodes.ainvoke_structured",
                new=AsyncMock(side_effect=Exception("LLM 다운")),
            ),
        ):
            result = await route_question("성격 알려주세요")

        assert result == "personality"

    async def test_model_is_passed_to_create_structured_llm(self):
        """model 인자가 create_structured_llm으로 전달되는지 확인"""
        decision = RouterDecision(next_agent="health", reasoning="건강")

        with (
            patch("agents.nodes.create_structured_llm", return_value=MagicMock()) as mock_create,
            patch("agents.nodes.ainvoke_structured", new=AsyncMock(return_value=decision)),
        ):
            await route_question("건강운은?", model="deepseek/deepseek-v4-flash")

        _, kwargs = mock_create.call_args
        assert kwargs["model"] == "deepseek/deepseek-v4-flash"


class TestCreateInitialState:
    """초기 상태 구조 검증"""

    def test_defaults(self, sample_saju_data):
        """messages 미지정 시 기본 상태 구조"""
        state = create_initial_state(sample_saju_data)

        assert state["messages"] == []
        assert state["saju_data"] is sample_saju_data
        assert state["current_agent"] == ""
        assert state["next_agent"] is None
        assert state["interpretations"] == {}
        assert state["iteration"] == 0
        assert state["final_output"] is None
        assert state["error"] is None

    def test_with_messages(self, sample_saju_data):
        """초기 messages를 전달하면 그대로 담긴다"""
        from langchain_core.messages import HumanMessage

        msgs = [HumanMessage(content="안녕하세요")]
        state = create_initial_state(sample_saju_data, messages=msgs)

        assert state["messages"] == msgs


@pytest.mark.parametrize(
    "chosen",
    ["personality", "career", "relationship", "health", "fortune", "yongsin", "school_compare"],
)
async def test_route_question_accepts_all_interpreter_agents(chosen):
    """synthesis를 제외한 모든 인터프리터 에이전트명이 그대로 통과하는지 확인"""
    decision = RouterDecision(next_agent=chosen, reasoning="test")

    with (
        patch("agents.nodes.create_structured_llm", return_value=MagicMock()),
        patch("agents.nodes.ainvoke_structured", new=AsyncMock(return_value=decision)),
    ):
        result = await route_question("질문")

    assert result == chosen
