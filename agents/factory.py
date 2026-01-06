"""
에이전트 팩토리

설정 기반으로 에이전트 인스턴스를 생성합니다.
"""

from typing import Optional, List, Dict, TYPE_CHECKING

from agents.base_agent import BaseAgent
from agents.config import AgentConfig
from agents.agent_configs import AGENT_CONFIGS

if TYPE_CHECKING:
    from utils.protocols import LLMClientProtocol


class ConfigurableAgent(BaseAgent):
    """설정 기반 에이전트

    AgentConfig를 받아서 동작하는 범용 에이전트 클래스입니다.
    """

    def __init__(
        self,
        config: AgentConfig,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        reasoning_effort: str = "medium",
        llm_client: Optional["LLMClientProtocol"] = None
    ):
        super().__init__(
            name=config.name,
            system_prompt=config.system_prompt,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort,
            llm_client=llm_client
        )
        self._config = config

    def get_interpretation_focus(self) -> str:
        return self._config.interpretation_focus

    @property
    def display_name(self) -> str:
        return self._config.display_name

    @property
    def keywords(self) -> List[str]:
        return self._config.keywords


class AgentFactory:
    """에이전트 팩토리

    설정 파일을 기반으로 에이전트 인스턴스를 생성합니다.
    """

    def __init__(self, configs: Optional[Dict[str, AgentConfig]] = None):
        """
        Args:
            configs: 에이전트 설정 딕셔너리 (None이면 기본 설정 사용)
        """
        self._configs = configs or AGENT_CONFIGS

    def create(
        self,
        agent_type: str,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        reasoning_effort: str = "medium",
        llm_client: Optional["LLMClientProtocol"] = None
    ) -> BaseAgent:
        """에이전트 인스턴스 생성

        Args:
            agent_type: 에이전트 타입 (예: "personality", "career")
            llm_provider: LLM 제공자 ("openai" | "gemini")
            model: 모델명 (None이면 기본값)
            reasoning_effort: 추론 강도
            llm_client: 주입할 LLM 클라이언트 (테스트용)

        Returns:
            생성된 에이전트 인스턴스

        Raises:
            ValueError: 잘못된 에이전트 타입
        """
        config = self._configs.get(agent_type)
        if config is None:
            available = ", ".join(self._configs.keys())
            raise ValueError(
                f"알 수 없는 에이전트 타입: '{agent_type}'. "
                f"사용 가능한 타입: {available}"
            )

        return ConfigurableAgent(
            config=config,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort,
            llm_client=llm_client
        )

    def get_all_types(self) -> List[str]:
        """사용 가능한 모든 에이전트 타입 반환"""
        return list(self._configs.keys())

    def get_config(self, agent_type: str) -> Optional[AgentConfig]:
        """에이전트 설정 조회"""
        return self._configs.get(agent_type)

    def get_keywords(self, agent_type: str) -> List[str]:
        """에이전트 키워드 조회"""
        config = self._configs.get(agent_type)
        return config.keywords if config else []

    def get_keyword_mapping(self) -> dict[str, List[str]]:
        """키워드 매핑 딕셔너리 반환 (Orchestrator 호환용)"""
        return {
            agent_type: config.keywords
            for agent_type, config in self._configs.items()
        }
