"""종합 해석 에이전트"""

from typing import Dict, List, Optional
from agents.base_agent import BaseAgent, AgentResponse
from agents.prompts.system_prompts import SYNTHESIS_SYSTEM_PROMPT, format_saju_context
from agents.schemas import get_interpretation_schema
from config.logging_config import get_logger

logger = get_logger(__name__)


class SynthesisAgent(BaseAgent):
    """종합 해석을 담당하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        reasoning_effort: str = "medium"  # gpt-5.2-chat-latest는 medium까지만 지원
    ):
        super().__init__(
            name="synthesis",
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "종합 해석, 인생 전망"

    async def synthesize(
        self,
        saju_data: Dict,
        agent_responses: List[AgentResponse],
        user_question: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> AgentResponse:
        """
        다른 에이전트들의 해석을 종합

        Args:
            saju_data: 사주 계산 결과
            agent_responses: 다른 에이전트들의 응답 목록
            user_question: 사용자 질문
            conversation_history: 대화 이력

        Returns:
            종합 해석 AgentResponse
        """
        # 사주 컨텍스트
        saju_context = format_saju_context(saju_data)

        # 다른 에이전트 해석 정리
        interpretations_summary = "\n\n".join([
            f"### {resp.agent_name.upper()} 에이전트 해석\n{resp.interpretation}"
            for resp in agent_responses
            if resp.confidence > 0
        ])

        # 메시지 구성
        messages = []

        messages.append({
            "role": "system",
            "content": self.system_prompt
        })

        if conversation_history:
            messages.extend(conversation_history[-10:])

        user_content = f"""
{saju_context}

## 각 전문 에이전트의 해석

{interpretations_summary}

## 요청
위 해석들을 종합하여 일관성 있고 균형 잡힌 통합 해석을 제공해 주세요.
"""

        if user_question:
            user_content += f"\n\n특히 다음 질문에 초점을 맞춰주세요: {user_question}"

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
                    "synthesized_from": [r.agent_name for r in agent_responses],
                    "provider": self.llm_provider
                },
                suggested_questions=suggested_questions
            )

        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                interpretation=f"종합 해석 중 오류: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                suggested_questions=[]
            )
