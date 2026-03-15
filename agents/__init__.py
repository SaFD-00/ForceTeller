"""
해석 에이전트 모듈

LangGraph 기반 에이전트 프레임워크를 제공합니다.

새 패턴 (권장):
    >>> from agents.graph import get_graph
    >>> from agents.orchestrator import Orchestrator
    >>>
    >>> orchestrator = Orchestrator()
    >>> result = await orchestrator.route_and_interpret(saju_data, question)

레거시 패턴 (deprecated):
    >>> from agents import BaseAgent, PersonalityAgent  # deprecated
"""

# =============================================================================
# New LangGraph-based exports (Recommended)
# =============================================================================

from agents.orchestrator import Orchestrator
from agents.state import AgentState, create_initial_state
from agents.schemas import InterpretationResult, RouterDecision, SynthesisResult
from agents.llm import create_llm, create_structured_llm, create_llm_with_fallback
from agents.nodes import (
    supervisor_node,
    interpreter_node,
    synthesis_node,
    create_interpreter_node,
    route_to_next,
)
from agents.graph import (
    build_forceteller_graph,
    compile_graph,
    get_graph,
    reset_graph,
)
from agents.factory import NodeFactory
from agents.config import AgentConfig
from agents.agent_configs import AGENT_CONFIGS, get_agent_config, get_all_agent_types

# =============================================================================
# Legacy exports (Deprecated - for backward compatibility)
# =============================================================================

from agents.base_agent import BaseAgent, AgentResponse
from agents.factory import AgentFactory, ConfigurableAgent

# Legacy interpreter imports (deprecated)
try:
    from agents.interpreters import (
        PersonalityAgent,
        CareerAgent,
        RelationshipAgent,
        HealthAgent,
        FortuneAgent,
        SynthesisAgent,
    )
except ImportError:
    # interpreters 모듈이 없는 경우 (새 설치)
    PersonalityAgent = None
    CareerAgent = None
    RelationshipAgent = None
    HealthAgent = None
    FortuneAgent = None
    SynthesisAgent = None


__all__ = [
    # New (Recommended)
    "Orchestrator",
    "AgentState",
    "create_initial_state",
    "InterpretationResult",
    "RouterDecision",
    "SynthesisResult",
    "create_llm",
    "create_structured_llm",
    "create_llm_with_fallback",
    "supervisor_node",
    "interpreter_node",
    "synthesis_node",
    "create_interpreter_node",
    "route_to_next",
    "build_forceteller_graph",
    "compile_graph",
    "get_graph",
    "reset_graph",
    "NodeFactory",
    "AgentConfig",
    "AGENT_CONFIGS",
    "get_agent_config",
    "get_all_agent_types",
    # Legacy (Deprecated)
    "BaseAgent",
    "AgentResponse",
    "AgentFactory",
    "ConfigurableAgent",
    "PersonalityAgent",
    "CareerAgent",
    "RelationshipAgent",
    "HealthAgent",
    "FortuneAgent",
    "SynthesisAgent",
]
