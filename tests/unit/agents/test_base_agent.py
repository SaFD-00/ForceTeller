"""
BaseAgent 단위 테스트
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

from agents.base_agent import BaseAgent, AgentResponse


# 테스트용 구체 에이전트 클래스
class TestableAgent(BaseAgent):
    """테스트용 구체 에이전트"""

    def get_interpretation_focus(self) -> str:
        return "테스트 해석 초점"


class TestAgentResponse:
    """AgentResponse 클래스 테스트"""

    def test_response_creation(self):
        """응답 생성 테스트"""
        response = AgentResponse(
            agent_name="test_agent",
            interpretation="테스트 해석 결과"
        )

        assert response.agent_name == "test_agent"
        assert response.interpretation == "테스트 해석 결과"
        assert response.confidence == 1.0
        assert response.metadata is None
        assert response.suggested_questions == []

    def test_response_with_all_fields(self):
        """모든 필드가 있는 응답 생성"""
        response = AgentResponse(
            agent_name="personality",
            interpretation="성격 분석 결과",
            confidence=0.9,
            metadata={"provider": "openai", "model": "gpt-4"},
            suggested_questions=["직업운은?", "연애운은?"]
        )

        assert response.confidence == 0.9
        assert response.metadata["provider"] == "openai"
        assert len(response.suggested_questions) == 2

    def test_response_to_dict(self):
        """응답 딕셔너리 변환"""
        response = AgentResponse(
            agent_name="career",
            interpretation="직업 분석",
            confidence=0.8,
            metadata={"focus": "career"},
            suggested_questions=["질문1"]
        )

        result = response.to_dict()

        assert result["agent_name"] == "career"
        assert result["interpretation"] == "직업 분석"
        assert result["confidence"] == 0.8
        assert result["metadata"] == {"focus": "career"}
        assert result["suggested_questions"] == ["질문1"]

    def test_response_to_dict_with_none_metadata(self):
        """metadata가 None일 때 딕셔너리 변환"""
        response = AgentResponse(
            agent_name="test",
            interpretation="결과"
        )

        result = response.to_dict()

        assert result["metadata"] == {}
        assert result["suggested_questions"] == []


class TestBaseAgent:
    """BaseAgent 클래스 테스트"""

    @pytest.fixture
    def mock_llm_client(self):
        """LLMClient 모킹"""
        with patch('agents.base_agent.LLMClient') as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def agent(self, mock_llm_client):
        """테스트용 에이전트"""
        return TestableAgent(
            name="test_agent",
            system_prompt="테스트 시스템 프롬프트",
            llm_provider="openai"
        )

    def test_agent_creation(self, agent):
        """에이전트 생성 테스트"""
        assert agent.name == "test_agent"
        assert agent.system_prompt == "테스트 시스템 프롬프트"
        assert agent.llm_provider == "openai"
        assert agent.reasoning_effort == "medium"

    def test_agent_creation_with_custom_settings(self, mock_llm_client):
        """커스텀 설정으로 에이전트 생성"""
        agent = TestableAgent(
            name="custom",
            system_prompt="커스텀 프롬프트",
            llm_provider="gemini",
            model="gemini-pro",
            reasoning_effort="high"
        )

        assert agent.llm_provider == "gemini"
        assert agent.model == "gemini-pro"
        assert agent.reasoning_effort == "high"

    def test_get_interpretation_focus(self, agent):
        """해석 초점 반환 테스트"""
        focus = agent.get_interpretation_focus()

        assert focus == "테스트 해석 초점"

    def test_agent_repr(self, agent):
        """에이전트 문자열 표현"""
        repr_str = repr(agent)

        assert "TestableAgent" in repr_str
        assert "test_agent" in repr_str
        assert "openai" in repr_str

    @pytest.mark.asyncio
    async def test_interpret_success(self, agent, sample_saju_data, mock_llm_response):
        """interpret 메서드 성공 테스트"""
        # LLM 응답 모킹
        agent.llm_client.chat = AsyncMock(return_value=mock_llm_response)

        response = await agent.interpret(
            saju_data=sample_saju_data,
            user_question="성격에 대해 알려주세요"
        )

        assert isinstance(response, AgentResponse)
        assert response.agent_name == "test_agent"
        assert response.interpretation == mock_llm_response["interpretation"]
        assert response.confidence == 1.0
        assert response.suggested_questions == mock_llm_response["suggested_questions"]

        # LLM이 호출되었는지 확인
        agent.llm_client.chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_interpret_without_question(self, agent, sample_saju_data, mock_llm_response):
        """질문 없이 interpret 호출"""
        agent.llm_client.chat = AsyncMock(return_value=mock_llm_response)

        response = await agent.interpret(saju_data=sample_saju_data)

        # 호출된 메시지 확인
        call_args = agent.llm_client.chat.call_args
        messages = call_args.kwargs.get('messages', call_args.args[0] if call_args.args else [])

        # 사용자 메시지에 해석 초점이 포함되어 있는지 확인
        user_message = next(m for m in messages if m['role'] == 'user')
        assert "테스트 해석 초점" in user_message['content']

    @pytest.mark.asyncio
    async def test_interpret_with_conversation_history(
        self, agent, sample_saju_data, mock_llm_response
    ):
        """대화 이력과 함께 interpret 호출"""
        agent.llm_client.chat = AsyncMock(return_value=mock_llm_response)

        history = [
            {"role": "user", "content": "이전 질문"},
            {"role": "assistant", "content": "이전 응답"}
        ]

        response = await agent.interpret(
            saju_data=sample_saju_data,
            user_question="새 질문",
            conversation_history=history
        )

        # 대화 이력이 포함되었는지 확인
        call_args = agent.llm_client.chat.call_args
        messages = call_args.kwargs.get('messages', call_args.args[0] if call_args.args else [])

        # 대화 이력 메시지 수 확인 (system + history(2) + user = 4)
        assert len(messages) == 4

    @pytest.mark.asyncio
    async def test_interpret_with_long_history(
        self, agent, sample_saju_data, mock_llm_response
    ):
        """긴 대화 이력 (최근 10개만 사용)"""
        agent.llm_client.chat = AsyncMock(return_value=mock_llm_response)

        # 15개의 대화 이력
        history = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"메시지 {i}"}
            for i in range(15)
        ]

        await agent.interpret(
            saju_data=sample_saju_data,
            conversation_history=history
        )

        call_args = agent.llm_client.chat.call_args
        messages = call_args.kwargs.get('messages', call_args.args[0] if call_args.args else [])

        # system(1) + 최근 history(10) + user(1) = 12
        assert len(messages) == 12

    @pytest.mark.asyncio
    async def test_interpret_error_handling(self, agent, sample_saju_data):
        """interpret 에러 처리 테스트"""
        agent.llm_client.chat = AsyncMock(side_effect=Exception("API 오류"))

        response = await agent.interpret(saju_data=sample_saju_data)

        assert response.confidence == 0.0
        assert "오류" in response.interpretation
        assert response.metadata.get("error") == "API 오류"

    @pytest.mark.asyncio
    async def test_interpret_text_response(self, agent, sample_saju_data):
        """텍스트 응답 처리 (dict가 아닌 경우)"""
        agent.llm_client.chat = AsyncMock(return_value="단순 텍스트 응답")

        response = await agent.interpret(saju_data=sample_saju_data)

        assert response.interpretation == "단순 텍스트 응답"
        assert response.suggested_questions == []

    @pytest.mark.asyncio
    async def test_answer_question(self, agent, sample_saju_data, mock_llm_response):
        """answer_question 메서드 테스트"""
        agent.llm_client.chat = AsyncMock(return_value=mock_llm_response)

        response = await agent.answer_question(
            saju_data=sample_saju_data,
            question="질문입니다"
        )

        assert isinstance(response, AgentResponse)
        agent.llm_client.chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_interpret_openai_with_schema(self, sample_saju_data, mock_llm_response):
        """OpenAI 프로바이더에서 스키마 사용 확인"""
        with patch('agents.base_agent.LLMClient') as mock_class:
            mock_instance = MagicMock()
            mock_instance.chat = AsyncMock(return_value=mock_llm_response)
            mock_class.return_value = mock_instance

            agent = TestableAgent(
                name="test",
                system_prompt="프롬프트",
                llm_provider="openai"
            )

            await agent.interpret(saju_data=sample_saju_data)

            # response_schema가 전달되었는지 확인
            call_kwargs = mock_instance.chat.call_args.kwargs
            assert "response_schema" in call_kwargs
            assert call_kwargs["response_schema"] is not None

    @pytest.mark.asyncio
    async def test_interpret_gemini_without_schema(self, sample_saju_data, mock_llm_response):
        """Gemini 프로바이더에서는 스키마 없음"""
        with patch('agents.base_agent.LLMClient') as mock_class:
            mock_instance = MagicMock()
            mock_instance.chat = AsyncMock(return_value=mock_llm_response)
            mock_class.return_value = mock_instance

            agent = TestableAgent(
                name="test",
                system_prompt="프롬프트",
                llm_provider="gemini"
            )

            await agent.interpret(saju_data=sample_saju_data)

            # thinking_level이 전달되었는지 확인
            call_kwargs = mock_instance.chat.call_args.kwargs
            assert "thinking_level" in call_kwargs


class TestBaseAgentAbstract:
    """BaseAgent 추상 클래스 테스트"""

    def test_cannot_instantiate_base_agent(self):
        """BaseAgent는 직접 인스턴스화할 수 없음"""
        with pytest.raises(TypeError):
            BaseAgent(
                name="test",
                system_prompt="프롬프트"
            )

    def test_must_implement_get_interpretation_focus(self):
        """get_interpretation_focus는 반드시 구현해야 함"""
        # 구현하지 않은 서브클래스
        class IncompleteAgent(BaseAgent):
            pass

        with pytest.raises(TypeError):
            IncompleteAgent(name="test", system_prompt="프롬프트")
