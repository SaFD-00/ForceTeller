"""
적천수(滴天髓) 해석기
청나라 임철초의 저서
오행의 생극제화와 통변성정을 깊이 다룸
"""

from typing import Any

from ..yongsin.base import (
    WuXing,
    get_ke_element,
    get_ke_me_element,
    get_sheng_element,
    get_sheng_me_element,
)
from .base_interpreter import BaseSchoolInterpreter, SchoolCode


class DTSInterpreter(BaseSchoolInterpreter):
    """적천수 해석기"""

    @property
    def school_code(self) -> SchoolCode:
        return SchoolCode.DTS

    def determine_yong_sin(self, saju_data: dict[str, Any]) -> WuXing:
        """
        적천수 방식의 용신 결정
        오행의 순환과 조화를 중시
        """
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)
        strength = self._get_strength_level(saju_data)

        # 적천수는 오행의 흐름을 중시
        # 막힌 곳을 뚫어주는 통관용신 개념 적용

        # 상극 관계의 오행들 확인
        strong_elements = [e for e, v in balance.items() if v > 0.25]

        if len(strong_elements) >= 2:
            # 충돌하는 오행이 있으면 통관용신 찾기
            for elem1 in strong_elements:
                for elem2 in strong_elements:
                    if get_ke_element(elem1) == elem2:
                        # 통관 역할을 하는 오행 찾기
                        mediator = get_sheng_element(elem1)
                        if get_sheng_element(mediator) == elem2:
                            return mediator

        # 기본 강약 분석
        if strength in ["very_strong", "strong"]:
            return get_sheng_element(day_element)
        elif strength in ["weak", "very_weak"]:
            return get_sheng_me_element(day_element)
        else:
            weakest = min(balance, key=balance.get)
            return weakest

    def determine_geok_guk(self, saju_data: dict[str, Any]) -> str | None:
        """적천수는 격국보다 오행 흐름을 중시"""
        balance = self._get_wuxing_balance(saju_data)

        # 오행 흐름 상태 판단
        strong_count = len([v for v in balance.values() if v > 0.25])
        weak_count = len([v for v in balance.values() if v < 0.1])

        if strong_count == 0 and weak_count == 0:
            return "중화격"
        elif strong_count >= 2:
            return "편중격"
        elif weak_count >= 2:
            return "결핍격"
        else:
            return "보통격"

    def interpret_health(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석 - 적천수 관점"""
        self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        health_text = "적천수에서는 오행의 순환이 막히면 병이 생긴다고 봅니다. "

        # 막힌 흐름 찾기
        blocked = []
        for elem in WuXing:
            if balance.get(elem, 0) < 0.1:
                prev_elem = get_sheng_me_element(elem)
                if balance.get(prev_elem, 0) > 0.2:
                    blocked.append(f"{prev_elem.value}→{elem.value}")

        if blocked:
            health_text += f"오행 흐름이 {', '.join(blocked[:2])} 구간에서 막혀 있습니다. "
        else:
            health_text += "오행의 흐름이 비교적 원활합니다. "

        health_text += f"{yong_sin.value} 오행을 보강하여 기의 순환을 돕습니다."

        return health_text

    def interpret_wealth(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석 - 적천수 관점"""
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)
        strength = self._get_strength_level(saju_data)

        wealth_text = "적천수에서 재물은 오행 흐름의 결과입니다. "

        # 재성으로 흐르는 기운 분석
        wealth_element = get_ke_element(day_element)
        food_element = get_sheng_element(day_element)  # 식상

        food_ratio = balance.get(food_element, 0)
        wealth_ratio = balance.get(wealth_element, 0)

        if food_ratio > 0.15 and wealth_ratio > 0.15:
            wealth_text += "식상생재(食傷生財)의 흐름이 있어 재물 획득이 순조롭습니다. "
        elif strength in ["strong", "very_strong"]:
            wealth_text += "일간이 강하니 적극적으로 재물을 추구할 수 있습니다. "
        else:
            wealth_text += "재물을 얻으려면 먼저 자신을 강화해야 합니다. "

        wealth_text += f"{yong_sin.value} 관련 투자와 활동이 유리합니다."

        return wealth_text

    def interpret_career(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석 - 적천수 관점"""
        day_element = self._get_day_stem_element(saju_data)
        self._get_wuxing_balance(saju_data)

        career_text = "적천수에서는 오행의 성정(性情)으로 적성을 파악합니다. "

        # 일간의 성정
        element_natures = {
            WuXing.WOOD: "목은 인자하고 곧아 교육, 의료, 환경 분야가 좋습니다.",
            WuXing.FIRE: "화는 밝고 예리하여 예술, IT, 홍보 분야가 적합합니다.",
            WuXing.EARTH: "토는 신의가 있어 부동산, 중개, 농업이 어울립니다.",
            WuXing.METAL: "금은 결단력이 있어 금융, 법률, 기계 분야가 좋습니다.",
            WuXing.WATER: "수는 지혜로워 연구, 유통, 서비스업이 적합합니다.",
        }

        career_text += element_natures.get(day_element, "")

        return career_text

    def interpret_relationship(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석 - 적천수 관점"""
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        rel_text = "적천수에서 관계는 오행의 상생상극으로 봅니다. "

        # 비겁(같은 오행) 분석
        same_ratio = balance.get(day_element, 0)
        if same_ratio > 0.25:
            rel_text += "비겁이 강하여 형제, 친구와의 인연이 깊습니다. 경쟁도 있을 수 있습니다. "
        elif same_ratio < 0.1:
            rel_text += "비겁이 약하여 독립적인 성향이지만, 도움받기 어려울 수 있습니다. "

        # 관성 분석
        official = get_ke_me_element(day_element)
        if balance.get(official, 0) > 0.2:
            rel_text += "관성이 있어 상사, 윗사람과의 관계가 중요합니다. "

        rel_text += f"{yong_sin.value} 오행의 사람과 좋은 인연입니다."

        return rel_text

    def interpret_fame(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석 - 적천수 관점"""
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        fame_text = "적천수에서 명예는 오행의 조화에서 비롯됩니다. "

        # 인성과 관성의 조화
        seal_element = get_sheng_me_element(day_element)
        official_element = get_ke_me_element(day_element)

        seal_ratio = balance.get(seal_element, 0)
        official_ratio = balance.get(official_element, 0)

        if seal_ratio > 0.15 and official_ratio > 0.15:
            fame_text += "관인상생(官印相生)의 좋은 구조로 학문과 명예를 얻을 수 있습니다. "
        elif official_ratio > 0.2:
            fame_text += "관성이 강하여 사회적 지위를 얻을 기회가 있습니다. "
        elif seal_ratio > 0.2:
            fame_text += "인성이 강하여 학문이나 기술로 명성을 얻습니다. "
        else:
            fame_text += "실력을 쌓아 점진적으로 인정받는 것이 좋습니다. "

        return fame_text

    def calculate_confidence(self, saju_data: dict[str, Any]) -> float:
        """신뢰도 계산 - 적천수"""
        base = 0.72

        # 오행 정보 완성도
        wuxing_count = saju_data.get("wuxing_count", {})
        if len(wuxing_count) == 5:
            base += 0.08

        # 기둥 정보 완성도
        for pillar in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]:
            if saju_data.get(pillar):
                base += 0.02

        return min(0.9, base)

    def extract_key_features(self, saju_data: dict[str, Any], yong_sin: WuXing) -> list[str]:
        """핵심 특징 추출"""
        day_element = self._get_day_stem_element(saju_data)
        geok_guk = self.determine_geok_guk(saju_data)

        features = [
            f"용신: {yong_sin.value}",
            f"일간 성정: {day_element.value}",
            f"오행 상태: {geok_guk}",
            "해석 기준: 오행 순환과 통변성정",
        ]

        return features
