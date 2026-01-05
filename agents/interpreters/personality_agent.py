"""성격/기질 해석 에이전트"""

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import PERSONALITY_SYSTEM_PROMPT


class PersonalityAgent(BaseAgent):
    """성격과 기질을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="personality",
            system_prompt=PERSONALITY_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "성격, 기질, 성향"
