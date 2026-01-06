"""
Orchestrator 단위 테스트
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

from agents.orchestrator import Orchestrator
from agents.base_agent import AgentResponse
from agents.factory import AgentFactory
from agents.agent_configs import AGENT_CONFIGS


def create_mock_agent(name: str = "test", interpretation: str = "테스트 해석"):
    """테스트용 모킹된 에이전트 생성"""
    mock_response = AgentResponse(
        agent_name=name,
        interpretation=interpretation,
        confidence=1.0,
        metadata={"provider": "openai"},
        suggested_questions=["다음 질문"]
    )

    mock_agent = MagicMock()
    mock_agent.interpret = AsyncMock(return_value=mock_response)
    mock_agent.synthesize = AsyncMock(return_value=mock_response)
    return mock_agent


def create_orchestrator_with_mock_agents():
    """모킹된 에이전트가 주입된 Orchestrator 생성"""
    # Orchestrator 생성 (use_llm_routing=False로 LLMClient 생성 방지)
    orchestrator = Orchestrator.__new__(Orchestrator)
    orchestrator.llm_provider = "openai"
    orchestrator.model = None
    orchestrator.use_llm_routing = False
    orchestrator._agents = {}

    # AgentFactory 설정
    orchestrator._factory = AgentFactory()

    # 키워드 매핑 설정 (팩토리에서 가져옴)
    orchestrator.KEYWORD_MAPPING = orchestrator._factory.get_keyword_mapping()

    # 모든 에이전트에 대해 mock 주입
    agent_names = ["personality", "career", "relationship", "health",
                   "fortune", "synthesis", "yongsin", "school_compare"]
    for name in agent_names:
        orchestrator._agents[name] = create_mock_agent(name)

    return orchestrator


class TestOrchestratorKeywordSelection:
    """키워드 기반 에이전트 선택 테스트"""

    @pytest.fixture
    def orchestrator(self):
        """테스트용 오케스트레이터"""
        return create_orchestrator_with_mock_agents()

    def test_select_personality_agent(self, orchestrator):
        """성격 관련 키워드로 personality 에이전트 선택"""
        questions = ["성격에 대해", "기질이 어떤", "장단점은"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "personality" in agents

    def test_select_career_agent(self, orchestrator):
        """직업 관련 키워드로 career 에이전트 선택"""
        questions = ["직업운은 어떤", "취업 시기", "사업 운세", "재물운"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "career" in agents

    def test_select_relationship_agent(self, orchestrator):
        """연애/결혼 관련 키워드로 relationship 에이전트 선택"""
        questions = ["연애운은", "결혼은 언제", "배우자 궁합", "대인관계"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "relationship" in agents

    def test_select_health_agent(self, orchestrator):
        """건강 관련 키워드로 health 에이전트 선택"""
        questions = ["건강 운세", "체질이 어떤", "아픈 곳이 있을"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "health" in agents

    def test_select_fortune_agent(self, orchestrator):
        """운세 관련 키워드로 fortune 에이전트 선택"""
        questions = ["올해 운세", "대운은 어떤", "내년은 어떤", "앞으로의 미래"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "fortune" in agents

    def test_select_yongsin_agent(self, orchestrator):
        """용신 관련 키워드로 yongsin 에이전트 선택"""
        questions = ["용신이 뭔", "희신 기신", "개운법", "신강인"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "yongsin" in agents

    def test_select_school_compare_agent(self, orchestrator):
        """유파 비교 관련 키워드로 school_compare 에이전트 선택"""
        questions = ["유파별 해석", "자평명리", "적천수로", "궁통보감"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            assert "school_compare" in agents

    def test_select_multiple_agents(self, orchestrator):
        """여러 키워드가 포함된 질문에서 다중 에이전트 선택"""
        question = "성격과 직업운은 어떤"
        agents = orchestrator._select_agents_by_keyword(question)

        assert "personality" in agents
        assert "career" in agents

    def test_select_default_agents_for_full_request(self, orchestrator):
        """전체 해석 요청 시 기본 에이전트 세트 선택"""
        questions = [
            "전체적으로",
            "종합 해석",
            "모두",
        ]

        default_agents = ["personality", "career", "relationship", "fortune"]

        for question in questions:
            agents = orchestrator._select_agents_by_keyword(question)
            for agent in default_agents:
                assert agent in agents

    def test_select_default_agents_when_no_keyword_matches(self, orchestrator):
        """키워드 매칭이 없을 때 기본 에이전트 선택"""
        question = "그냥"  # 특정 키워드 없음
        agents = orchestrator._select_agents_by_keyword(question)

        # 기본 에이전트가 선택되어야 함
        assert len(agents) > 0


class TestOrchestratorAgentManagement:
    """에이전트 관리 테스트"""

    def test_get_agent_returns_cached_instance(self):
        """에이전트 인스턴스 캐시 반환"""
        orchestrator = create_orchestrator_with_mock_agents()

        agent1 = orchestrator._get_agent("personality")
        agent2 = orchestrator._get_agent("personality")

        assert agent1 is agent2
        assert agent1 is not None

    def test_get_nonexistent_agent(self):
        """존재하지 않는 에이전트 요청"""
        orchestrator = create_orchestrator_with_mock_agents()
        agent = orchestrator._get_agent("nonexistent")
        assert agent is None


class TestOrchestratorRouteAndInterpret:
    """route_and_interpret 메서드 테스트"""

    @pytest.fixture
    def orchestrator(self):
        """테스트용 오케스트레이터"""
        return create_orchestrator_with_mock_agents()

    @pytest.mark.asyncio
    async def test_route_and_interpret_returns_correct_structure(self, orchestrator, sample_saju_data):
        """route_and_interpret가 올바른 구조의 결과를 반환"""
        result = await orchestrator.route_and_interpret(
            saju_data=sample_saju_data,
            question="성격 분석",
            include_synthesis=False
        )

        assert "agents_used" in result
        assert "interpretations" in result
        assert "synthesis" in result
        assert "routing_info" in result

    @pytest.mark.asyncio
    async def test_route_and_interpret_uses_keyword_routing(self, orchestrator, sample_saju_data):
        """키워드 기반 라우팅 사용 확인"""
        result = await orchestrator.route_and_interpret(
            saju_data=sample_saju_data,
            question="성격 분석",
            include_synthesis=False
        )

        assert "personality" in result["agents_used"]
        assert result["routing_info"]["reasoning"] == "키워드 기반 선택"

    @pytest.mark.asyncio
    async def test_route_and_interpret_with_conversation_history(self, orchestrator, sample_saju_data):
        """대화 이력과 함께 라우팅"""
        history = [
            {"role": "user", "content": "이전 질문"},
            {"role": "assistant", "content": "이전 응답"}
        ]

        result = await orchestrator.route_and_interpret(
            saju_data=sample_saju_data,
            question="성격 분석",
            conversation_history=history,
            include_synthesis=False
        )

        assert result is not None
        assert "interpretations" in result

    @pytest.mark.asyncio
    async def test_route_and_interpret_handles_agent_error(self, sample_saju_data):
        """에이전트 에러 처리"""
        # 에러를 발생시키는 에이전트가 있는 오케스트레이터 생성
        orchestrator = create_orchestrator_with_mock_agents()

        # personality 에이전트가 에러를 발생시키도록 설정
        orchestrator._agents["personality"].interpret = AsyncMock(
            side_effect=Exception("에이전트 에러")
        )

        result = await orchestrator.route_and_interpret(
            saju_data=sample_saju_data,
            question="성격 분석",
            include_synthesis=False
        )

        # 에러가 발생해도 결과가 반환되어야 함
        assert "interpretations" in result
        assert "personality" in result["interpretations"]
        assert "error" in result["interpretations"]["personality"]

    @pytest.mark.asyncio
    async def test_route_and_interpret_with_synthesis(self, orchestrator, sample_saju_data):
        """종합 해석 포함 테스트"""
        # 전체 해석 트리거 키워드 사용
        result = await orchestrator.route_and_interpret(
            saju_data=sample_saju_data,
            question="전체적으로 분석",
            include_synthesis=True
        )

        assert "synthesis" in result
        # 여러 에이전트가 사용되었으므로 synthesis가 있어야 함
        assert len(result["agents_used"]) > 1


class TestOrchestratorInterpretFull:
    """interpret_full 메서드 테스트"""

    @pytest.fixture
    def orchestrator(self):
        """테스트용 오케스트레이터"""
        return create_orchestrator_with_mock_agents()

    @pytest.mark.asyncio
    async def test_interpret_full_uses_all_default_agents(self, orchestrator, sample_saju_data):
        """전체 해석 시 기본 에이전트 사용"""
        result = await orchestrator.interpret_full(saju_data=sample_saju_data)

        # 기본 에이전트들이 사용되어야 함
        expected_agents = ["personality", "career", "relationship", "fortune"]
        for agent in expected_agents:
            assert agent in result["agents_used"]


class TestOrchestratorQuickInterpret:
    """quick_interpret 메서드 테스트"""

    @pytest.fixture
    def orchestrator(self):
        """테스트용 오케스트레이터"""
        return create_orchestrator_with_mock_agents()

    @pytest.mark.asyncio
    async def test_quick_interpret_with_valid_focus(self, orchestrator, sample_saju_data):
        """유효한 focus로 빠른 해석"""
        response = await orchestrator.quick_interpret(
            saju_data=sample_saju_data,
            focus="personality"
        )

        assert isinstance(response, AgentResponse)
        assert response.confidence > 0

    @pytest.mark.asyncio
    async def test_quick_interpret_with_invalid_focus(self, orchestrator, sample_saju_data):
        """유효하지 않은 focus로 빠른 해석"""
        response = await orchestrator.quick_interpret(
            saju_data=sample_saju_data,
            focus="invalid_agent"
        )

        assert response.confidence == 0.0
        assert "찾을 수 없습니다" in response.interpretation


class TestOrchestratorLLMRouting:
    """LLM 기반 라우팅 테스트"""

    @pytest.mark.asyncio
    async def test_llm_routing_parses_response(self):
        """LLM 라우팅 응답 파싱"""
        mock_llm_client = MagicMock()
        mock_llm_client.chat = AsyncMock(
            return_value='{"agents": ["personality", "career"], "reasoning": "테스트"}'
        )

        # LLM 라우팅이 활성화된 오케스트레이터 생성
        orchestrator = Orchestrator.__new__(Orchestrator)
        orchestrator.llm_provider = "openai"
        orchestrator.model = None
        orchestrator.use_llm_routing = True
        orchestrator.llm_client = mock_llm_client
        orchestrator._agents = {}
        orchestrator._factory = AgentFactory()
        orchestrator.KEYWORD_MAPPING = orchestrator._factory.get_keyword_mapping()

        result = await orchestrator._select_agents_by_llm("성격과 직업운")

        assert "agents" in result
        assert "reasoning" in result
        assert "personality" in result["agents"]
        assert "career" in result["agents"]

    @pytest.mark.asyncio
    async def test_llm_routing_fallback_on_parse_error(self):
        """LLM 응답 파싱 실패 시 키워드 기반으로 폴백"""
        mock_llm_client = MagicMock()
        mock_llm_client.chat = AsyncMock(return_value="유효하지 않은 JSON")

        orchestrator = Orchestrator.__new__(Orchestrator)
        orchestrator.llm_provider = "openai"
        orchestrator.model = None
        orchestrator.use_llm_routing = True
        orchestrator.llm_client = mock_llm_client
        orchestrator._agents = {}
        orchestrator._factory = AgentFactory()
        orchestrator.KEYWORD_MAPPING = orchestrator._factory.get_keyword_mapping()

        result = await orchestrator._select_agents_by_llm("성격 분석")

        # 키워드 기반으로 폴백되어야 함
        assert "agents" in result
        assert "파싱 실패" in result["reasoning"]

    @pytest.mark.asyncio
    async def test_llm_routing_fallback_on_exception(self):
        """LLM 호출 예외 시 키워드 기반으로 폴백"""
        mock_llm_client = MagicMock()
        mock_llm_client.chat = AsyncMock(side_effect=Exception("API 에러"))

        orchestrator = Orchestrator.__new__(Orchestrator)
        orchestrator.llm_provider = "openai"
        orchestrator.model = None
        orchestrator.use_llm_routing = True
        orchestrator.llm_client = mock_llm_client
        orchestrator._agents = {}
        orchestrator._factory = AgentFactory()
        orchestrator.KEYWORD_MAPPING = orchestrator._factory.get_keyword_mapping()

        result = await orchestrator._select_agents_by_llm("성격 분석")

        # 키워드 기반으로 폴백되어야 함
        assert "agents" in result
        assert "실패" in result["reasoning"]
