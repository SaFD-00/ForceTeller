"""직업/재물 해석 에이전트"""

from typing import Optional

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import CAREER_SYSTEM_PROMPT


class CareerAgent(BaseAgent):
    """직업과 재물운을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="career",
            system_prompt=CAREER_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "직업 적성, 재물운, 사업운"
