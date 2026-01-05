"""대운/세운 해석 에이전트"""

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import FORTUNE_SYSTEM_PROMPT


class FortuneAgent(BaseAgent):
    """대운과 세운을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="fortune",
            system_prompt=FORTUNE_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "대운, 세운, 시기별 운세"
