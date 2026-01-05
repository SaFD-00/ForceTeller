"""건강 해석 에이전트"""

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import HEALTH_SYSTEM_PROMPT


class HealthAgent(BaseAgent):
    """건강 체질을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="health",
            system_prompt=HEALTH_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "건강 체질, 취약 부위, 건강 관리"
