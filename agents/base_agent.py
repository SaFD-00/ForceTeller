"""
베이스 에이전트 클래스 (레거시 호환 + 마이그레이션 경고)

Note:
    이 모듈은 레거시 호환성을 위해 유지됩니다.
    새로운 코드는 agents/nodes.py의 노드 함수를 사용하세요.

    LangGraph 기반 새 패턴:
    - agents.state: TypedDict 기반 상태 정의
    - agents.schemas: Pydantic 모델 기반 출력 스키마
    - agents.nodes: 노드 함수 구현
    - agents.graph: StateGraph 빌드
"""

import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from agents.prompts.system_prompts import format_saju_context
from config.logging_config import get_logger

if TYPE_CHECKING:
    from utils.protocols import LLMClientProtocol

logger = get_logger(__name__)


@dataclass
class AgentResponse:
    """에이전트 응답 데이터 클래스

    Deprecated:
        InterpretationResult Pydantic 모델 사용을 권장합니다.
        from agents.schemas import InterpretationResult

    Example (새 패턴):
        >>> from agents.schemas import InterpretationResult
        >>> result = InterpretationResult(
        ...     interpretation="해석 내용",
        ...     suggested_questions=["질문1", "질문2"]
        ... )
    """
    agent_name: str
    interpretation: str
    confidence: float = 1.0
    metadata: dict[str, Any] | None = None
    suggested_questions: list[str] = field(default_factory=list)

    def __post_init__(self):
        # 레거시 코드 사용 시 경고
        warnings.warn(
            "AgentResponse is deprecated. "
            "Use InterpretationResult from agents.schemas instead.",
            DeprecationWarning,
            stacklevel=3
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "interpretation": self.interpretation,
            "confidence": self.confidence,
            "metadata": self.metadata or {},
            "suggested_questions": self.suggested_questions or []
        }


class BaseAgent(ABC):
    """해석 에이전트 기본 클래스

    Deprecated:
        LangGraph 노드 함수 패턴을 사용하세요.
        from agents.nodes import create_interpreter_node

    Example (새 패턴):
        >>> from agents.nodes import create_interpreter_node
        >>> personality_node = create_interpreter_node("personality")
        >>> # LangGraph에서 사용
        >>> graph.add_node("personality", personality_node)
    """

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm_provider: str = "openai",
        model: str | None = None,
        reasoning_effort: str = "medium",
        llm_client: "LLMClientProtocol | None" = None
    ):
        """
        Deprecated:
            LangGraph 노드 함수 패턴을 사용하세요.

        Args:
            name: 에이전트 이름
            system_prompt: 시스템 프롬프트
            llm_provider: LLM 제공자 ("openai" | "gemini")
            model: 모델명 (None이면 기본값)
            reasoning_effort: 추론 강도 (OpenAI) / thinking_level (Gemini)
            llm_client: LLM 클라이언트 (DI용, None이면 자동 생성)
        """
        warnings.warn(
            "BaseAgent is deprecated. Use LangGraph node functions instead. "
            "See agents/nodes.py for examples.",
            DeprecationWarning,
            stacklevel=2
        )

        self.name = name
        self.system_prompt = system_prompt
        self.llm_provider = llm_provider
        self.model = model
        self.reasoning_effort = reasoning_effort

        # 의존성 주입: llm_client가 제공되면 사용, 아니면 새로 생성
        if llm_client is not None:
            self.llm_client = llm_client
        else:
            from utils.llm_client import LLMClient
            self.llm_client = LLMClient(provider=llm_provider)

    @abstractmethod
    def get_interpretation_focus(self) -> str:
        """해석 초점 반환 (서브클래스에서 구현)"""
        pass

    async def interpret(
        self,
        saju_data: dict,
        user_question: str | None = None,
        conversation_history: list[dict] | None = None
    ) -> AgentResponse:
        """
        사주 해석 수행 (Deprecated)

        Deprecated:
            agents.nodes.interpreter_node() 사용을 권장합니다.

        Args:
            saju_data: 사주 계산 결과 딕셔너리
            user_question: 사용자 질문 (없으면 전체 해석)
            conversation_history: 이전 대화 내역

        Returns:
            AgentResponse 객체
        """
        # 사주 컨텍스트 생성
        saju_context = format_saju_context(saju_data)

        # 메시지 구성
        messages = []

        # 시스템 프롬프트
        messages.append({
            "role": "system",
            "content": self.system_prompt
        })

        # 대화 이력 추가
        if conversation_history:
            messages.extend(conversation_history[-10:])  # 최근 10개

        # 사주 컨텍스트 + 질문
        user_content = f"{saju_context}\n\n"

        if user_question:
            user_content += f"## 사용자 질문\n{user_question}\n\n"
        else:
            user_content += f"## 요청\n{self.get_interpretation_focus()}에 대해 상세히 해석해 주세요.\n\n"

        messages.append({
            "role": "user",
            "content": user_content
        })

        # LLM 호출
        try:
            # 레거시 스키마 사용 (deprecated)
            from agents.schemas import get_interpretation_schema

            response_schema = None
            if self.llm_provider == "openai":
                schema = get_interpretation_schema()
                response_schema = {
                    "name": "agent_interpretation",
                    "schema": schema
                }
                logger.debug(f"스키마: {schema}")

            if self.llm_provider == "openai":
                response = await self.llm_client.chat(
                    messages=messages,
                    model=self.model,
                    reasoning_effort=self.reasoning_effort,
                    response_schema=response_schema
                )
            else:
                response = await self.llm_client.chat(
                    messages=messages,
                    model=self.model,
                    thinking_level=self.reasoning_effort
                )

            logger.debug(f"응답 타입: {type(response)}")

            # Structured Outputs 응답 처리 (dict) 또는 일반 텍스트 응답
            if isinstance(response, dict):
                interpretation = response.get("interpretation", "")
                suggested_questions = response.get("suggested_questions", [])
            else:
                interpretation = response if isinstance(response, str) else str(response)
                suggested_questions = []

            return AgentResponse(
                agent_name=self.name,
                interpretation=interpretation,
                confidence=1.0,
                metadata={
                    "provider": self.llm_provider,
                    "model": self.model or "default",
                    "focus": self.get_interpretation_focus()
                },
                suggested_questions=suggested_questions
            )

        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                interpretation=f"해석 중 오류가 발생했습니다: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                suggested_questions=[]
            )

    async def synthesize(
        self,
        saju_data: dict,
        agent_responses: list[AgentResponse],
        user_question: str | None = None,
        conversation_history: list[dict] | None = None
    ) -> AgentResponse:
        """
        여러 에이전트 응답 종합 (Deprecated)

        Deprecated:
            agents.nodes.synthesis_node() 사용을 권장합니다.
        """
        # 종합 컨텍스트 구성
        saju_context = format_saju_context(saju_data)

        interpretations_summary = "\n\n".join([
            f"### {r.agent_name} 해석\n{r.interpretation}"
            for r in agent_responses
        ])

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
{saju_context}

## 각 전문 에이전트의 해석
{interpretations_summary}

## 요청
위 해석들을 종합하여 일관성 있고 균형 잡힌 통합 해석을 제공해 주세요.
"""}
        ]

        try:
            response = await self.llm_client.chat(
                messages=messages,
                model=self.model
            )

            interpretation = response if isinstance(response, str) else str(response)

            return AgentResponse(
                agent_name=self.name,
                interpretation=interpretation,
                confidence=1.0,
                metadata={"synthesized_from": [r.agent_name for r in agent_responses]},
                suggested_questions=[]
            )

        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                interpretation=f"종합 해석 중 오류: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                suggested_questions=[]
            )

    async def answer_question(
        self,
        saju_data: dict,
        question: str,
        conversation_history: list[dict] | None = None
    ) -> AgentResponse:
        """
        특정 질문에 대한 답변 (Deprecated)
        """
        return await self.interpret(
            saju_data=saju_data,
            user_question=question,
            conversation_history=conversation_history
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', provider='{self.llm_provider}')"
