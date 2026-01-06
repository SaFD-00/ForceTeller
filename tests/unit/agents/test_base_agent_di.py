"""
BaseAgent 의존성 주입 테스트
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from agents.base_agent import BaseAgent, AgentResponse
from utils.protocols import LLMClientProtocol


class DITestableAgent(BaseAgent):
    """DI 테스트용 구체 에이전트"""

    def get_interpretation_focus(self) -> str:
        return "DI 테스트 해석 초점"


class TestBaseAgentDependencyInjection:
    """BaseAgent 의존성 주입 테스트"""

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM 클라이언트"""
        mock = MagicMock(spec=LLMClientProtocol)
        mock.chat = AsyncMock(return_value={
            "interpretation": "DI 테스트 응답",
            "suggested_questions": ["질문1", "질문2"]
        })
        return mock

    def test_agent_accepts_injected_llm_client(self, mock_llm_client):
        """에이전트가 주입된 LLM 클라이언트를 받아들이는지 확인"""
        agent = DITestableAgent(
            name="di_test",
            system_prompt="테스트 프롬프트",
            llm_client=mock_llm_client
        )

        assert agent.llm_client is mock_llm_client
        assert agent.name == "di_test"

    def test_agent_creates_default_llm_client_when_not_injected(self):
        """LLM 클라이언트가 주입되지 않으면 기본값을 생성하는지 확인"""
        # LLMClient 생성을 모킹
        with pytest.MonkeyPatch.context() as mp:
            mock_llm_class = MagicMock()
            mock_llm_instance = MagicMock()
            mock_llm_class.return_value = mock_llm_instance

            # 임포트 시 실제 LLMClient 대신 mock 사용
            import utils.llm_client
            mp.setattr(utils.llm_client, "LLMClient", mock_llm_class)

            agent = DITestableAgent(
                name="no_di_test",
                system_prompt="테스트 프롬프트",
                llm_provider="openai"
            )

            # LLMClient가 생성되었는지 확인
            mock_llm_class.assert_called_once_with(provider="openai")

    @pytest.mark.asyncio
    async def test_interpret_uses_injected_client(self, mock_llm_client, sample_saju_data):
        """interpret 메서드가 주입된 클라이언트를 사용하는지 확인"""
        agent = DITestableAgent(
            name="di_test",
            system_prompt="테스트 프롬프트",
            llm_provider="openai",
            llm_client=mock_llm_client
        )

        response = await agent.interpret(
            saju_data=sample_saju_data,
            user_question="테스트 질문"
        )

        # 주입된 클라이언트의 chat 메서드가 호출되었는지 확인
        mock_llm_client.chat.assert_called_once()
        assert isinstance(response, AgentResponse)
        assert response.interpretation == "DI 테스트 응답"
        assert response.suggested_questions == ["질문1", "질문2"]

    @pytest.mark.asyncio
    async def test_interpret_without_question(self, mock_llm_client, sample_saju_data):
        """질문 없이 interpret 호출 시 해석 초점 사용"""
        agent = DITestableAgent(
            name="di_test",
            system_prompt="테스트 프롬프트",
            llm_client=mock_llm_client
        )

        await agent.interpret(saju_data=sample_saju_data)

        # chat 호출 확인
        call_args = mock_llm_client.chat.call_args
        messages = call_args.kwargs.get('messages', call_args.args[0] if call_args.args else [])

        # 사용자 메시지에 해석 초점이 포함되어 있는지 확인
        user_message = next(m for m in messages if m['role'] == 'user')
        assert "DI 테스트 해석 초점" in user_message['content']

    @pytest.mark.asyncio
    async def test_interpret_error_handling(self, sample_saju_data):
        """interpret 에러 처리 테스트"""
        mock_client = MagicMock()
        mock_client.chat = AsyncMock(side_effect=Exception("테스트 에러"))

        agent = DITestableAgent(
            name="error_test",
            system_prompt="프롬프트",
            llm_client=mock_client
        )

        response = await agent.interpret(saju_data=sample_saju_data)

        assert response.confidence == 0.0
        assert "오류" in response.interpretation
        assert response.metadata.get("error") == "테스트 에러"

    @pytest.mark.asyncio
    async def test_answer_question_uses_injected_client(self, mock_llm_client, sample_saju_data):
        """answer_question 메서드가 주입된 클라이언트를 사용하는지 확인"""
        agent = DITestableAgent(
            name="di_test",
            system_prompt="테스트 프롬프트",
            llm_client=mock_llm_client
        )

        response = await agent.answer_question(
            saju_data=sample_saju_data,
            question="질문입니다"
        )

        mock_llm_client.chat.assert_called_once()
        assert isinstance(response, AgentResponse)

    def test_multiple_agents_with_same_client(self, mock_llm_client):
        """여러 에이전트가 같은 클라이언트를 공유할 수 있는지 확인"""
        agent1 = DITestableAgent(
            name="agent1",
            system_prompt="프롬프트1",
            llm_client=mock_llm_client
        )

        agent2 = DITestableAgent(
            name="agent2",
            system_prompt="프롬프트2",
            llm_client=mock_llm_client
        )

        # 같은 클라이언트 인스턴스를 공유
        assert agent1.llm_client is agent2.llm_client
        assert agent1.llm_client is mock_llm_client

    def test_agent_preserves_other_parameters(self, mock_llm_client):
        """DI 시에도 다른 파라미터가 보존되는지 확인"""
        agent = DITestableAgent(
            name="param_test",
            system_prompt="시스템 프롬프트",
            llm_provider="gemini",
            model="custom-model",
            reasoning_effort="high",
            llm_client=mock_llm_client
        )

        assert agent.name == "param_test"
        assert agent.system_prompt == "시스템 프롬프트"
        assert agent.llm_provider == "gemini"
        assert agent.model == "custom-model"
        assert agent.reasoning_effort == "high"
        assert agent.llm_client is mock_llm_client


class TestBaseAgentProtocolCompliance:
    """BaseAgent가 LLMClientProtocol을 올바르게 사용하는지 테스트"""

    def test_injected_client_implements_protocol(self):
        """주입된 클라이언트가 프로토콜을 구현하는지 확인"""
        mock_client = MagicMock()
        mock_client.chat = AsyncMock(return_value="응답")
        mock_client.chat_stream = AsyncMock()

        # runtime_checkable 프로토콜 확인
        assert isinstance(mock_client, LLMClientProtocol)

        agent = DITestableAgent(
            name="protocol_test",
            system_prompt="프롬프트",
            llm_client=mock_client
        )

        assert agent.llm_client is mock_client
