"""
에이전트 설정 데이터 클래스
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentConfig:
    """에이전트 설정 데이터 클래스"""

    name: str
    display_name: str
    system_prompt: str
    interpretation_focus: str
    keywords: list[str] = field(default_factory=list)

    def __post_init__(self):
        # frozen=True이므로 object.__setattr__ 사용
        if not isinstance(self.keywords, tuple):
            object.__setattr__(self, "keywords", list(self.keywords))
