"""
시스템 프롬프트 불변식 테스트

모든 해석 에이전트 프롬프트에 공통 가드레일(안전 경계·입력 처리 원칙)이
포함되어 있는지, 그리고 도메인 오류로 확인되어 수정한 표기(화극수,
수신(讐神))가 재유입되지 않는지 고정한다.
"""

from agents.agent_configs import AGENT_CONFIGS
from agents.prompts.system_prompts import (
    COMMON_GUARDRAILS,
    HEALTH_SYSTEM_PROMPT,
    ORCHESTRATOR_SYSTEM_PROMPT,
    YONGSIN_SYSTEM_PROMPT,
)


class TestCommonGuardrails:
    """공통 가드레일 포함 여부"""

    def test_guardrails_block_has_required_sections(self):
        assert "## 안전 경계" in COMMON_GUARDRAILS
        assert "## 입력 처리 원칙" in COMMON_GUARDRAILS
        # 위기 대응: 자살예방 상담전화 109 (2024-01 통합, 24시간)
        assert "109" in COMMON_GUARDRAILS

    def test_every_agent_prompt_includes_guardrails(self):
        for name, cfg in AGENT_CONFIGS.items():
            assert "## 안전 경계" in cfg.system_prompt, f"{name}: 안전 경계 누락"
            assert "## 입력 처리 원칙" in cfg.system_prompt, f"{name}: 입력 처리 원칙 누락"

    def test_orchestrator_prompt_prioritizes_system_rules(self):
        """라우터도 사용자 메시지를 데이터로만 취급해야 한다"""
        assert "분류 대상 데이터" in ORCHESTRATOR_SYSTEM_PROMPT


class TestDomainCorrections:
    """수정된 도메인 오류의 재유입 방지"""

    def test_health_prompt_has_no_hwa_geuk_su(self):
        """상극은 수극화·화극금이며 '화극수'는 오행 상극 순서에 없다"""
        assert "화극수" not in HEALTH_SYSTEM_PROMPT
        assert "화다수건" in HEALTH_SYSTEM_PROMPT

    def test_yongsin_prompt_uses_standard_gushin_term(self):
        """기신을 생조하는 오행의 표준 용어는 구신(仇神)이다"""
        assert "수신(讐神)" not in YONGSIN_SYSTEM_PROMPT
        assert "구신(仇神)" in YONGSIN_SYSTEM_PROMPT
        assert "한신(閑神)" in YONGSIN_SYSTEM_PROMPT
