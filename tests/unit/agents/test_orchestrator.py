"""
Orchestrator 단위 테스트 (LangGraph 기반)

Orchestrator는 LangGraph StateGraph를 감싸는 얇은 래퍼다.
모델 ID를 그래프 실행 config로 주입하고, 그래프 결과를 API 형식으로 변환한다.
"""

import pytest
from unittest.mock import AsyncMock, patch

from agents.orchestrator import Orchestrator
from config.settings import settings


class TestOrchestratorInit:
    """초기화 및 모델 보관 테스트"""

    def test_default_model_is_none(self):
        """모델 미지정 시 None (노드에서 설정 기본값 사용)"""
        orch = Orchestrator()
        assert orch.model is None
        assert orch.graph is not None

    def test_explicit_model_is_stored(self):
        """명시적 모델 ID가 보관되는지 확인"""
        orch = Orchestrator(model="deepseek/deepseek-v4-pro")
        assert orch.model == "deepseek/deepseek-v4-pro"


class TestOrchestratorConfigInjection:
    """그래프 실행 config로 모델이 주입되는지 테스트"""

    @pytest.mark.asyncio
    async def test_route_and_interpret_injects_model_into_config(self, sample_saju_data):
        """route_and_interpret가 그래프에 model/routing_model을 주입하는지 확인"""
        orch = Orchestrator(model="google/gemma-4-31b-it:free")

        fake_state = {
            "interpretations": {"personality": {"interpretation": "테스트", "suggested_questions": []}},
            "final_output": "종합 해석",
        }

        with patch.object(orch.graph, "ainvoke", new=AsyncMock(return_value=fake_state)) as mock_ainvoke:
            result = await orch.route_and_interpret(
                saju_data=sample_saju_data,
                question="성격이 궁금해요",
            )

        # 그래프가 호출되고 config에 모델이 들어갔는지 확인
        mock_ainvoke.assert_awaited_once()
        _, kwargs = mock_ainvoke.call_args
        configurable = kwargs["config"]["configurable"]
        assert configurable["model"] == "google/gemma-4-31b-it:free"
        assert configurable["routing_model"] == settings.OPENROUTER_ROUTING_MODEL
        assert "thread_id" in configurable

        # 결과 구조 확인
        assert result["agents_used"] == ["personality"]
        assert result["synthesis"]["interpretation"] == "종합 해석"

    @pytest.mark.asyncio
    async def test_thread_id_is_passed_through(self, sample_saju_data):
        """thread_id가 config로 전달되는지 확인"""
        orch = Orchestrator()
        with patch.object(orch.graph, "ainvoke", new=AsyncMock(return_value={})) as mock_ainvoke:
            await orch.route_and_interpret(
                saju_data=sample_saju_data,
                question="질문",
                thread_id="thread-123",
            )
        _, kwargs = mock_ainvoke.call_args
        assert kwargs["config"]["configurable"]["thread_id"] == "thread-123"


class TestOrchestratorFormatResult:
    """_format_result 변환 테스트"""

    def test_format_result_structure(self):
        """결과가 API 호환 구조를 갖는지 확인"""
        orch = Orchestrator()
        state = {
            "interpretations": {"career": {"interpretation": "직업 해석"}},
            "final_output": None,
        }
        result = orch._format_result(state, include_synthesis=True)

        assert result["agents_used"] == ["career"]
        assert result["interpretations"] == state["interpretations"]
        assert result["synthesis"] is None
        assert "routing_info" in result

    def test_format_result_includes_synthesis(self):
        """final_output이 있으면 synthesis가 채워지는지 확인"""
        orch = Orchestrator()
        state = {"interpretations": {}, "final_output": "통합 해석"}
        result = orch._format_result(state, include_synthesis=True)

        assert result["synthesis"]["agent_name"] == "synthesis"
        assert result["synthesis"]["interpretation"] == "통합 해석"

    def test_format_result_propagates_error(self):
        """state에 error가 있으면 결과에 포함되는지 확인"""
        orch = Orchestrator()
        state = {"interpretations": {}, "final_output": None, "error": "LLM 실패"}
        result = orch._format_result(state)

        assert result["error"] == "LLM 실패"
