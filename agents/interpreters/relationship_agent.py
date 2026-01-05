"""대인관계/결혼 해석 에이전트"""

from agents.base_agent import BaseAgent
from agents.prompts.system_prompts import RELATIONSHIP_SYSTEM_PROMPT


class RelationshipAgent(BaseAgent):
    """대인관계와 결혼운을 분석하는 에이전트"""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        reasoning_effort: str = "medium"
    ):
        super().__init__(
            name="relationship",
            system_prompt=RELATIONSHIP_SYSTEM_PROMPT,
            llm_provider=llm_provider,
            model=model,
            reasoning_effort=reasoning_effort
        )

    def get_interpretation_focus(self) -> str:
        return "연애, 결혼, 대인관계"
