"""
AgentFactory 단위 테스트
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

from agents.config import AgentConfig
from agents.factory import AgentFactory
from agents.base_agent import BaseAgent, AgentResponse
from utils.protocols import LLMClientProtocol


class TestAgentConfig:
    """AgentConfig 데이터 클래스 테스트"""

    def test_config_creation(self):
        """기본 설정 생성"""
        config = AgentConfig(
            name="test",
            display_name="테스트 에이전트",
            system_prompt="테스트 프롬프트",
            interpretation_focus="테스트 해석",
            keywords=["테스트", "시험"]
        )

        assert config.name == "test"
        assert config.display_name == "테스트 에이전트"
        assert config.system_prompt == "테스트 프롬프트"
        assert config.interpretation_focus == "테스트 해석"
        assert config.keywords == ["테스트", "시험"]

    def test_config_immutable_fields(self):
        """설정 필드가 올바른 타입인지 확인"""
        config = AgentConfig(
            name="personality",
            display_name="성격 분석",
            system_prompt="성격 분석 프롬프트",
            interpretation_focus="성격, 기질, 성향",
            keywords=["성격", "기질"]
        )

        assert isinstance(config.name, str)
        assert isinstance(config.keywords, list)


class TestAgentFactory:
    """AgentFactory 클래스 테스트"""

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM 클라이언트"""
        mock = MagicMock(spec=LLMClientProtocol)
        mock.chat = AsyncMock(return_value={
            "interpretation": "팩토리 테스트 해석",
            "suggested_questions": ["질문1"]
        })
        return mock

    @pytest.fixture
    def factory(self):
        """AgentFactory 인스턴스"""
        return AgentFactory()

    def test_factory_has_all_agent_types(self, factory):
        """팩토리가 모든 에이전트 타입을 지원하는지 확인"""
        expected_types = [
            "personality",
            "career",
            "relationship",
            "health",
            "fortune",
            "yongsin",
            "school_compare",
            "synthesis"
        ]

        available_types = factory.get_all_types()

        for agent_type in expected_types:
            assert agent_type in available_types

    def test_create_personality_agent(self, factory, mock_llm_client):
        """성격 에이전트 생성"""
        agent = factory.create("personality", llm_client=mock_llm_client)

        assert isinstance(agent, BaseAgent)
        assert agent.name == "personality"
        assert agent.llm_client is mock_llm_client

    def test_create_career_agent(self, factory, mock_llm_client):
        """직업 에이전트 생성"""
        agent = factory.create("career", llm_client=mock_llm_client)

        assert isinstance(agent, BaseAgent)
        assert agent.name == "career"

    def test_create_all_agent_types(self, factory, mock_llm_client):
        """모든 에이전트 타입 생성 가능"""
        for agent_type in factory.get_all_types():
            agent = factory.create(agent_type, llm_client=mock_llm_client)

            assert isinstance(agent, BaseAgent)
            assert agent.name == agent_type

    def test_create_invalid_agent_type_raises_error(self, factory, mock_llm_client):
        """잘못된 타입 에러 처리"""
        with pytest.raises(ValueError) as exc_info:
            factory.create("invalid_type", llm_client=mock_llm_client)

        assert "invalid_type" in str(exc_info.value)

    def test_create_agent_with_custom_provider(self, factory, mock_llm_client):
        """커스텀 provider로 에이전트 생성"""
        agent = factory.create(
            "personality",
            llm_provider="gemini",
            llm_client=mock_llm_client
        )

        assert agent.llm_provider == "gemini"

    def test_create_agent_without_llm_client(self, factory):
        """LLM 클라이언트 없이 에이전트 생성 (자동 생성)"""
        # 실제 LLM 클라이언트 생성을 막기 위해 mock 사용
        with pytest.MonkeyPatch.context() as mp:
            mock_llm_class = MagicMock()
            mock_llm_instance = MagicMock()
            mock_llm_class.return_value = mock_llm_instance

            import utils.llm_client
            mp.setattr(utils.llm_client, "LLMClient", mock_llm_class)

            agent = factory.create("personality", llm_provider="openai")

            assert agent is not None
            mock_llm_class.assert_called_once_with(provider="openai")

    def test_get_config(self, factory):
        """에이전트 설정 조회"""
        config = factory.get_config("personality")

        assert config is not None
        assert config.name == "personality"
        assert "성격" in config.interpretation_focus
        assert len(config.keywords) > 0

    def test_get_config_invalid_type(self, factory):
        """잘못된 타입 설정 조회"""
        config = factory.get_config("invalid")

        assert config is None

    def test_get_keywords(self, factory):
        """에이전트 키워드 조회"""
        keywords = factory.get_keywords("personality")

        assert isinstance(keywords, list)
        assert "성격" in keywords

    @pytest.mark.asyncio
    async def test_created_agent_can_interpret(self, factory, mock_llm_client, sample_saju_data):
        """생성된 에이전트가 해석을 수행할 수 있는지 확인"""
        agent = factory.create("personality", llm_client=mock_llm_client)

        response = await agent.interpret(saju_data=sample_saju_data)

        assert isinstance(response, AgentResponse)
        mock_llm_client.chat.assert_called_once()

    def test_factory_returns_new_instance_each_time(self, factory, mock_llm_client):
        """팩토리가 매번 새 인스턴스를 반환하는지 확인"""
        agent1 = factory.create("personality", llm_client=mock_llm_client)
        agent2 = factory.create("personality", llm_client=mock_llm_client)

        assert agent1 is not agent2


class TestAgentConfigCollection:
    """에이전트 설정 컬렉션 테스트"""

    @pytest.fixture
    def factory(self):
        return AgentFactory()

    def test_all_agents_have_required_fields(self, factory):
        """모든 에이전트가 필수 필드를 가지고 있는지 확인"""
        for agent_type in factory.get_all_types():
            config = factory.get_config(agent_type)

            assert config.name, f"{agent_type}에 name이 없음"
            assert config.display_name, f"{agent_type}에 display_name이 없음"
            assert config.system_prompt, f"{agent_type}에 system_prompt가 없음"
            assert config.interpretation_focus, f"{agent_type}에 interpretation_focus가 없음"
            assert config.keywords, f"{agent_type}에 keywords가 없음"

    def test_agent_names_match_config_keys(self, factory):
        """에이전트 이름이 설정 키와 일치하는지 확인"""
        for agent_type in factory.get_all_types():
            config = factory.get_config(agent_type)
            assert config.name == agent_type

    def test_no_duplicate_keywords_across_agents(self, factory):
        """에이전트 간 키워드 중복이 합리적인 수준인지 확인"""
        # 중복이 허용되지만 동일한 키워드가 너무 많은 에이전트에 걸쳐 있으면 안 됨
        keyword_count = {}

        for agent_type in factory.get_all_types():
            config = factory.get_config(agent_type)
            for keyword in config.keywords:
                if keyword not in keyword_count:
                    keyword_count[keyword] = []
                keyword_count[keyword].append(agent_type)

        # 키워드가 3개 이상의 에이전트에 중복되면 경고
        for keyword, agents in keyword_count.items():
            assert len(agents) <= 3, f"키워드 '{keyword}'가 너무 많은 에이전트에 중복됨: {agents}"
