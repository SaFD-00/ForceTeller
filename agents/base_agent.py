"""
베이스 에이전트 클래스
모든 해석 에이전트의 기본 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from utils.llm_client import LLMClient
from agents.prompts.system_prompts import format_saju_context
from agents.schemas import get_interpretation_schema


@dataclass
class AgentResponse:
    """에이전트 응답 데이터 클래스"""
    agent_name: str
    interpretation: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    suggested_questions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "agent_name": self.agent_name,
            "interpretation": self.interpretation,
            "confidence": self.confidence,
            "metadata": self.metadata or {},
            "suggested_questions": self.suggested_questions or []
        }


class BaseAgent(ABC):
    """해석 에이전트 기본 클래스"""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        """
        Args:
            name: 에이전트 이름
            system_prompt: 시스템 프롬프트
            llm_provider: LLM 제공자 ("openai" | "gemini")
            model: 모델명 (None이면 기본값)
            reasoning_effort: 추론 강도 (OpenAI) / thinking_level (Gemini)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.llm_provider = llm_provider
        self.model = model
        self.reasoning_effort = reasoning_effort

        self.llm_client = LLMClient(provider=llm_provider)

    @abstractmethod
    def get_interpretation_focus(self) -> str:
        """해석 초점 반환 (서브클래스에서 구현)"""
        pass

    async def interpret(
        self,
        saju_data: Dict,
        user_question: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> AgentResponse:
        """
        사주 해석 수행

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
            # Structured Outputs 스키마 설정 (OpenAI만 지원)
            response_schema = None
            if self.llm_provider == "openai":
                schema = get_interpretation_schema()
                response_schema = {
                    "name": "agent_interpretation",
                    "schema": schema
                }
                print(f"[DEBUG Agent] 스키마: {schema}")

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

            print(f"[DEBUG Agent] 응답 타입: {type(response)}")

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

    async def answer_question(
        self,
        saju_data: Dict,
        question: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> AgentResponse:
        """
        특정 질문에 대한 답변

        Args:
            saju_data: 사주 계산 결과
            question: 사용자 질문
            conversation_history: 대화 이력

        Returns:
            AgentResponse
        """
        return await self.interpret(
            saju_data=saju_data,
            user_question=question,
            conversation_history=conversation_history
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', provider='{self.llm_provider}')"
