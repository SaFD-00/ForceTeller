"""
에이전트 설정 정의

모든 에이전트의 설정을 중앙에서 관리합니다.
새 에이전트를 추가하려면 이 파일에 설정만 추가하면 됩니다.
"""

from agents.config import AgentConfig
from agents.prompts.system_prompts import (
    PERSONALITY_SYSTEM_PROMPT,
    CAREER_SYSTEM_PROMPT,
    RELATIONSHIP_SYSTEM_PROMPT,
    HEALTH_SYSTEM_PROMPT,
    FORTUNE_SYSTEM_PROMPT,
    YONGSIN_SYSTEM_PROMPT,
    SCHOOL_COMPARE_SYSTEM_PROMPT,
    SYNTHESIS_SYSTEM_PROMPT,
)


AGENT_CONFIGS = {
    "personality": AgentConfig(
        name="personality",
        display_name="성격 분석",
        system_prompt=PERSONALITY_SYSTEM_PROMPT,
        interpretation_focus="성격, 기질, 성향",
        keywords=["성격", "기질", "성향", "특성", "장단점", "강점", "약점"],
    ),

    "career": AgentConfig(
        name="career",
        display_name="직업/재물 분석",
        system_prompt=CAREER_SYSTEM_PROMPT,
        interpretation_focus="직업, 재물, 사업",
        keywords=["직업", "일", "직장", "취업", "사업", "재물", "돈", "부", "투자", "경력"],
    ),

    "relationship": AgentConfig(
        name="relationship",
        display_name="대인관계 분석",
        system_prompt=RELATIONSHIP_SYSTEM_PROMPT,
        interpretation_focus="연애, 결혼, 대인관계",
        keywords=["연애", "결혼", "배우자", "인연", "이성", "사랑", "대인관계", "친구", "가족"],
    ),

    "health": AgentConfig(
        name="health",
        display_name="건강 분석",
        system_prompt=HEALTH_SYSTEM_PROMPT,
        interpretation_focus="건강, 체질",
        keywords=["건강", "질병", "아픈", "체질", "몸", "운동", "음식"],
    ),

    "fortune": AgentConfig(
        name="fortune",
        display_name="운세 분석",
        system_prompt=FORTUNE_SYSTEM_PROMPT,
        interpretation_focus="운세, 시기, 흐름",
        keywords=["운세", "대운", "올해", "내년", "언제", "시기", "때", "미래", "앞으로"],
    ),

    "yongsin": AgentConfig(
        name="yongsin",
        display_name="용신 분석",
        system_prompt=YONGSIN_SYSTEM_PROMPT,
        interpretation_focus="용신, 희신, 기신",
        keywords=["용신", "희신", "기신", "개운", "강약", "신강", "신약"],
    ),

    "school_compare": AgentConfig(
        name="school_compare",
        display_name="유파 비교 분석",
        system_prompt=SCHOOL_COMPARE_SYSTEM_PROMPT,
        interpretation_focus="유파별 해석 비교",
        keywords=["유파", "비교", "자평", "적천수", "궁통보감", "현대명리", "신살"],
    ),

    "synthesis": AgentConfig(
        name="synthesis",
        display_name="종합 분석",
        system_prompt=SYNTHESIS_SYSTEM_PROMPT,
        interpretation_focus="종합 해석",
        keywords=["종합", "전체", "모두", "전반"],
    ),
}


def get_agent_config(agent_type: str) -> AgentConfig | None:
    """에이전트 설정 조회"""
    return AGENT_CONFIGS.get(agent_type)


def get_all_agent_types() -> list[str]:
    """모든 에이전트 타입 목록"""
    return list(AGENT_CONFIGS.keys())


def get_keyword_mapping() -> dict[str, list[str]]:
    """키워드 매핑 딕셔너리 반환 (Orchestrator 호환용)"""
    return {
        agent_type: config.keywords
        for agent_type, config in AGENT_CONFIGS.items()
    }
