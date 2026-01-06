"""유파 비교 분석 에이전트"""

from typing import Optional

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import SCHOOL_COMPARE_SYSTEM_PROMPT


class SchoolCompareAgent(BaseAgent):
    """5개 유파의 관점에서 사주를 비교 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="school_compare",
            system_prompt=SCHOOL_COMPARE_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "자평명리, 적천수, 궁통보감, 현대명리, 신살중심 유파별 해석"
