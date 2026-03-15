"""
에이전트 팩토리 (LangGraph 호환)

설정 기반으로 에이전트 인스턴스 또는 노드 함수를 생성합니다.

Note:
    LangGraph 기반 구현으로 전환되었습니다.
    기존 AgentFactory는 레거시 호환을 위해 유지되며,
    새 코드는 NodeFactory 또는 agents.nodes 모듈을 직접 사용하세요.
"""

import warnings
from typing import Callable, TYPE_CHECKING

from agents.config import AgentConfig
from agents.agent_configs import AGENT_CONFIGS
from agents.nodes import create_interpreter_node

if TYPE_CHECKING:
    from agents.base_agent import BaseAgent
    from utils.protocols import LLMClientProtocol


class NodeFactory:
    """LangGraph 노드 팩토리

    에이전트 설정을 기반으로 LangGraph 노드 함수를 생성합니다.

    Example:
        >>> factory = NodeFactory()
        >>> personality_node = factory.create_node("personality")
        >>> graph.add_node("personality", personality_node)
    """

    def __init__(self, configs: dict[str, AgentConfig] | None = None):
        """
        Args:
            configs: 에이전트 설정 딕셔너리 (None이면 기본 설정 사용)
        """
        self._configs = configs or AGENT_CONFIGS

    def create_node(self, agent_type: str) -> Callable:
        """에이전트 노드 함수 생성

        Args:
            agent_type: 에이전트 타입

        Returns:
            노드 함수

        Raises:
            ValueError: 알 수 없는 에이전트 타입
        """
        if agent_type not in self._configs:
            available = ", ".join(self._configs.keys())
            raise ValueError(
                f"알 수 없는 에이전트 타입: '{agent_type}'. "
                f"사용 가능한 타입: {available}"
            )

        return create_interpreter_node(agent_type)

    def get_all_types(self) -> list[str]:
        """사용 가능한 모든 에이전트 타입"""
        return list(self._configs.keys())

    def get_config(self, agent_type: str) -> AgentConfig | None:
        """에이전트 설정 조회"""
        return self._configs.get(agent_type)

    def get_keyword_mapping(self) -> dict[str, list[str]]:
        """키워드 매핑 (레거시 호환)"""
        return {
            agent_type: config.keywords
            for agent_type, config in self._configs.items()
        }


# =============================================================================
# Legacy Support (Deprecated)
# =============================================================================

class ConfigurableAgent:
    """설정 기반 에이전트 (Deprecated)

    Deprecated:
        LangGraph 노드 함수 패턴을 사용하세요.
        agents.nodes.create_interpreter_node() 참조.
    """

    def __init__(
        self,
        config: AgentConfig,
        llm_provider: str = "openai",
        model: str | None = None,
        reasoning_effort: str = "medium",
        llm_client: "LLMClientProtocol | None" = None
    ):
        warnings.warn(
            "ConfigurableAgent is deprecated. "
            "Use LangGraph node functions instead. "
            "See agents/nodes.py for examples.",
            DeprecationWarning,
            stacklevel=2
        )

        # 레거시 구현을 위해 BaseAgent 임포트
        from agents.base_agent import BaseAgent as LegacyBaseAgent

        # 내부적으로 레거시 BaseAgent 사용
        class _LegacyAgent(LegacyBaseAgent):
            def __init__(inner_self, config, *args, **kwargs):
                super().__init__(
                    name=config.name,
                    system_prompt=config.system_prompt,
                    *args, **kwargs
                )
                inner_self._config = config

            def get_interpretation_focus(inner_self) -> str:
                return inner_self._config.interpretation_focus

        self._agent = _LegacyAgent(
            config=config,
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
    def keywords(self) -> list[str]:
        return self._config.keywords

    async def interpret(self, *args, **kwargs):
        return await self._agent.interpret(*args, **kwargs)

    async def synthesize(self, *args, **kwargs):
        return await self._agent.synthesize(*args, **kwargs)


class AgentFactory:
    """에이전트 팩토리 (Deprecated)

    Deprecated:
        NodeFactory를 사용하세요.

    Note:
        이 클래스는 레거시 호환성을 위해 유지됩니다.
        새 코드는 NodeFactory 또는 agents.nodes 모듈을 사용하세요.
    """

    def __init__(self, configs: dict[str, AgentConfig] | None = None):
        """
        Args:
            configs: 에이전트 설정 딕셔너리 (None이면 기본 설정 사용)
        """
        warnings.warn(
            "AgentFactory is deprecated. Use NodeFactory instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._configs = configs or AGENT_CONFIGS

    def create(
        self,
        agent_type: str,
        llm_provider: str = "openai",
        model: str | None = None,
        reasoning_effort: str = "medium",
        llm_client: "LLMClientProtocol | None" = None
    ) -> "BaseAgent":
        """에이전트 인스턴스 생성 (Deprecated)

        Deprecated:
            NodeFactory.create_node()을 사용하세요.
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

    def get_all_types(self) -> list[str]:
        """사용 가능한 모든 에이전트 타입 반환"""
        return list(self._configs.keys())

    def get_config(self, agent_type: str) -> AgentConfig | None:
        """에이전트 설정 조회"""
        return self._configs.get(agent_type)

    def get_keywords(self, agent_type: str) -> list[str]:
        """에이전트 키워드 조회"""
        config = self._configs.get(agent_type)
        return config.keywords if config else []

    def get_keyword_mapping(self) -> dict[str, list[str]]:
        """키워드 매핑 딕셔너리 반환"""
        return {
            agent_type: config.keywords
            for agent_type, config in self._configs.items()
        }
