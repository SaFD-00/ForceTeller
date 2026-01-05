"""용신 분석 에이전트"""

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import YONGSIN_SYSTEM_PROMPT


class YongsinAgent(BaseAgent):
    """용신, 희신, 기신을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="yongsin",
            system_prompt=YONGSIN_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "용신, 희신, 기신, 개운법"
