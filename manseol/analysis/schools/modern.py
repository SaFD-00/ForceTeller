"""
현대명리(現代命理) 해석기
현대 사회에 맞게 재해석한 명리학
심리학적 관점과 실용적 조언을 결합
"""

from typing import Any

from ..yongsin.base import (
    WuXing,
    get_sheng_element,
    get_sheng_me_element,
)
from .base_interpreter import BaseSchoolInterpreter, SchoolCode

# 오행별 심리 특성
WUXING_PSYCHOLOGY = {
    WuXing.WOOD: {
        "traits": ["창의성", "성장 지향", "계획성"],
        "strengths": ["새로운 아이디어", "장기 비전", "인내심"],
        "weaknesses": ["완고함", "조급함", "과도한 계획"],
        "career_modern": ["스타트업", "교육 테크", "친환경 산업", "헬스케어"],
    },
    WuXing.FIRE: {
        "traits": ["열정", "리더십", "표현력"],
        "strengths": ["동기 부여", "영감 제공", "네트워킹"],
        "weaknesses": ["급한 성격", "감정 기복", "지속력 부족"],
        "career_modern": ["마케팅", "엔터테인먼트", "소셜 미디어", "이벤트"],
    },
    WuXing.EARTH: {
        "traits": ["안정감", "신뢰성", "현실감"],
        "strengths": ["일관성", "책임감", "중재력"],
        "weaknesses": ["변화 저항", "고집", "느린 적응"],
        "career_modern": ["부동산 테크", "물류", "HR", "프로젝트 관리"],
    },
    WuXing.METAL: {
        "traits": ["분석력", "결단력", "정확성"],
        "strengths": ["논리적 사고", "효율성", "품질 관리"],
        "weaknesses": ["완벽주의", "비판적", "융통성 부족"],
        "career_modern": ["데이터 분석", "핀테크", "법무", "품질 관리"],
    },
    WuXing.WATER: {
        "traits": ["유연성", "지혜", "적응력"],
        "strengths": ["통찰력", "소통 능력", "창의적 해결"],
        "weaknesses": ["우유부단", "감정 과잉", "방향 상실"],
        "career_modern": ["컨설팅", "연구개발", "AI/ML", "글로벌 비즈니스"],
    },
}


class ModernInterpreter(BaseSchoolInterpreter):
    """현대명리 해석기"""

    @property
    def school_code(self) -> SchoolCode:
        return SchoolCode.MODERN

    def determine_yong_sin(self, saju_data: dict[str, Any]) -> WuXing:
        """
        현대명리 방식의 용신 결정
        심리적 균형과 현실적 조화를 중시
        """
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)
        strength = self._get_strength_level(saju_data)

        # 현대적 관점: 부족한 오행보다 활용 가능한 오행 중심
        # 너무 약한 오행은 활용하기 어려움

        # 1. 적당히 있지만 부족한 오행 찾기 (0.1 ~ 0.2 사이)
        moderate_weak = [e for e, v in balance.items() if 0.08 < v < 0.18]

        if moderate_weak:
            # 그 중 일간과 상생 관계인 것 우선
            for elem in moderate_weak:
                if get_sheng_me_element(day_element) == elem:
                    return elem
                if get_sheng_element(day_element) == elem:
                    return elem
            return moderate_weak[0]

        # 2. 기본 강약 분석
        if strength in ["very_strong", "strong"]:
            return get_sheng_element(day_element)
        elif strength in ["weak", "very_weak"]:
            return get_sheng_me_element(day_element)
        else:
            # 중화: 일간을 돕는 오행
            return get_sheng_me_element(day_element)

    def interpret_health(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석 - 현대명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        self._get_wuxing_balance(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})

        health_text = "현대명리에서는 심신의 균형을 중시합니다. "

        # 심리적 건강 분석
        traits = psychology.get("traits", [])
        weaknesses = psychology.get("weaknesses", [])

        if traits:
            health_text += (
                f"{day_element.value} 성향으로 {', '.join(traits[:2])}의 특성이 있습니다. "
            )

        if weaknesses:
            health_text += f"스트레스 시 {', '.join(weaknesses[:2])}에 주의하세요. "

        # 현대적 건강 조언
        health_advice = {
            WuXing.WOOD: "정기적인 야외 활동과 스트레칭으로 기분 전환을 하세요.",
            WuXing.FIRE: "충분한 휴식과 명상으로 에너지를 조절하세요.",
            WuXing.EARTH: "규칙적인 식사와 루틴으로 안정감을 유지하세요.",
            WuXing.METAL: "호흡 운동과 정리정돈으로 마음을 다스리세요.",
            WuXing.WATER: "충분한 수분 섭취와 수면으로 에너지를 충전하세요.",
        }

        health_text += health_advice.get(yong_sin, "")

        return health_text

    def interpret_wealth(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석 - 현대명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        strength = self._get_strength_level(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})

        wealth_text = "현대명리에서 재물은 자신의 강점 활용과 관련됩니다. "

        strengths = psychology.get("strengths", [])
        careers = psychology.get("career_modern", [])

        if strengths:
            wealth_text += f"당신의 강점인 {', '.join(strengths[:2])}을 활용하세요. "

        # 현대적 재물 조언
        if strength in ["strong", "very_strong"]:
            wealth_text += "적극적인 투자와 사업 확장에 유리합니다. "
        elif strength in ["weak", "very_weak"]:
            wealth_text += "안정적인 저축과 점진적 투자가 적합합니다. "
        else:
            wealth_text += "균형 잡힌 포트폴리오가 좋습니다. "

        if careers:
            wealth_text += f"추천 분야: {', '.join(careers[:3])}."

        return wealth_text

    def interpret_career(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석 - 현대명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})
        yongsin_psychology = WUXING_PSYCHOLOGY.get(yong_sin, {})

        career_text = "현대명리에서는 개인의 성향과 시대 흐름을 고려합니다. "

        # 일간 기반 적성
        traits = psychology.get("traits", [])
        careers = psychology.get("career_modern", [])

        if traits:
            career_text += f"{day_element.value} 성향으로 {', '.join(traits[:2])}이 강점입니다. "

        if careers:
            career_text += f"적합한 현대 직업: {', '.join(careers[:3])}. "

        # 용신 기반 추가 적성
        yongsin_careers = yongsin_psychology.get("career_modern", [])
        if yongsin_careers:
            career_text += f"보완 분야: {', '.join(yongsin_careers[:2])}."

        return career_text

    def interpret_relationship(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석 - 현대명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})

        rel_text = "현대명리에서 관계는 심리적 호환성을 중시합니다. "

        traits = psychology.get("traits", [])
        strengths = psychology.get("strengths", [])
        weaknesses = psychology.get("weaknesses", [])

        if traits:
            rel_text += f"당신은 {', '.join(traits[:2])}의 성향으로 관계에 접근합니다. "

        if strengths:
            rel_text += f"{', '.join(strengths[:2])}이 관계의 강점입니다. "

        if weaknesses:
            rel_text += f"관계에서 {', '.join(weaknesses[:1])}에 주의하면 좋습니다. "

        # 상생 관계 추천
        compatible = get_sheng_me_element(day_element)
        rel_text += f"{compatible.value} 성향의 사람과 좋은 시너지를 냅니다."

        return rel_text

    def interpret_fame(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석 - 현대명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        self._get_strength_level(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})

        fame_text = "현대 사회에서 명예는 전문성과 영향력입니다. "

        strengths = psychology.get("strengths", [])

        if strengths:
            fame_text += f"당신의 {', '.join(strengths[:2])}을 통해 인정받을 수 있습니다. "

        # SNS 시대 조언
        fame_advice = {
            WuXing.WOOD: "블로그나 유튜브로 지식을 공유하세요.",
            WuXing.FIRE: "소셜 미디어에서 영향력을 발휘하세요.",
            WuXing.EARTH: "꾸준한 콘텐츠로 신뢰를 쌓으세요.",
            WuXing.METAL: "전문 분야에서 권위를 확립하세요.",
            WuXing.WATER: "네트워킹으로 인맥을 넓히세요.",
        }

        fame_text += fame_advice.get(yong_sin, "")

        return fame_text

    def calculate_confidence(self, saju_data: dict[str, Any]) -> float:
        """신뢰도 계산 - 현대명리"""
        base = 0.75

        # 오행 정보 완성도
        wuxing_count = saju_data.get("wuxing_count", {})
        if len(wuxing_count) == 5:
            base += 0.08

        # 강약 분석 정보
        if saju_data.get("day_master_strength"):
            base += 0.07

        return min(0.93, base)

    def extract_key_features(self, saju_data: dict[str, Any], yong_sin: WuXing) -> list[str]:
        """핵심 특징 추출"""
        day_element = self._get_day_stem_element(saju_data)
        psychology = WUXING_PSYCHOLOGY.get(day_element, {})
        traits = psychology.get("traits", [])

        features = [
            f"용신: {yong_sin.value}",
            f"핵심 성향: {', '.join(traits[:2]) if traits else day_element.value}",
            "해석 기준: 심리학적 관점 + 현대 적용",
            "특징: 실용적 조언 중심",
        ]

        return features
