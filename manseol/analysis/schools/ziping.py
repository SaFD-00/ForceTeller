"""
자평명리(子平命理) 해석기
송나라 서자평이 정립한 전통 명리학의 기초
일간 중심의 강약 분석과 격국론을 중시
"""

from typing import Any, Dict, List, Optional

from ..yongsin.base import (
    WuXing,
    get_sheng_element,
    get_sheng_me_element,
    get_ke_element,
    get_ke_me_element,
)
from .base_interpreter import BaseSchoolInterpreter, SchoolCode


# 격국 정의
GEOK_GUK_TYPES = {
    # 정격 (正格)
    "정관격": "관성이 투출하여 일간을 도와줌",
    "편관격": "편관이 강하여 권위와 통솔력",
    "정인격": "정인이 월령을 차지하여 학문과 명예",
    "편인격": "편인이 강하여 창의력과 독특함",
    "식신격": "식신이 왕성하여 재능과 표현력",
    "상관격": "상관이 강하여 예술성과 반골기질",
    "정재격": "정재가 왕성하여 안정적 재물",
    "편재격": "편재가 강하여 사업적 재능",
    # 특별격
    "건록격": "월령에 비겁이 있어 자립심 강함",
    "양인격": "양인이 있어 결단력과 추진력",
}


class ZipingInterpreter(BaseSchoolInterpreter):
    """자평명리 해석기"""

    @property
    def school_code(self) -> SchoolCode:
        return SchoolCode.ZIPING

    def determine_yong_sin(self, saju_data: Dict[str, Any]) -> WuXing:
        """
        자평명리 방식의 용신 결정
        일간의 강약을 기준으로 결정
        """
        day_element = self._get_day_stem_element(saju_data)
        strength = self._get_strength_level(saju_data)

        if strength in ["very_strong", "strong"]:
            # 강한 일간: 설기(식상) 또는 극하는 오행(재성)
            return get_sheng_element(day_element)
        elif strength in ["weak", "very_weak"]:
            # 약한 일간: 생해주는 오행(인성) 또는 같은 오행(비겁)
            return get_sheng_me_element(day_element)
        else:
            # 중화: 가장 약한 오행 보강
            balance = self._get_wuxing_balance(saju_data)
            weakest = min(balance, key=balance.get)
            return weakest

    def determine_geok_guk(self, saju_data: Dict[str, Any]) -> Optional[str]:
        """격국 판단 (자평명리의 핵심)"""
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)
        strength = self._get_strength_level(saju_data)

        # 월령 오행 확인 (간략화된 버전)
        month_pillar = saju_data.get("month_pillar", {})
        month_element = month_pillar.get("branch_element", day_element.value)

        # 격국 판단 로직 (간략화)
        if month_element == day_element.value:
            return "건록격"

        # 관성 격국
        ke_me = get_ke_me_element(day_element)
        if balance.get(ke_me, 0) > 0.25:
            return "정관격" if strength in ["medium", "strong"] else "편관격"

        # 인성 격국
        sheng_me = get_sheng_me_element(day_element)
        if balance.get(sheng_me, 0) > 0.25:
            return "정인격"

        # 식상 격국
        sheng = get_sheng_element(day_element)
        if balance.get(sheng, 0) > 0.25:
            return "식신격" if strength in ["strong", "very_strong"] else "상관격"

        # 재성 격국
        ke = get_ke_element(day_element)
        if balance.get(ke, 0) > 0.25:
            return "정재격"

        return "보통격"

    def interpret_health(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석 - 자평명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        weak_elements = [e for e, v in balance.items() if v < 0.15]
        strong_elements = [e for e, v in balance.items() if v > 0.3]

        health_text = f"자평명리에서는 일간({day_element.value})의 균형을 중시합니다. "

        if weak_elements:
            weak_names = [e.value for e in weak_elements]
            health_text += f"{', '.join(weak_names)} 오행이 부족하여 관련 장기에 주의가 필요합니다. "

        if strong_elements:
            strong_names = [e.value for e in strong_elements]
            health_text += f"{', '.join(strong_names)} 오행이 과다하여 조절이 필요합니다. "

        health_text += f"{yong_sin.value} 오행을 보강하면 건강 균형에 도움이 됩니다."

        return health_text

    def interpret_wealth(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석 - 자평명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        strength = self._get_strength_level(saju_data)
        wealth_element = get_ke_element(day_element)  # 재성
        balance = self._get_wuxing_balance(saju_data)

        wealth_text = f"자평명리에서 재성은 {wealth_element.value}입니다. "

        wealth_ratio = balance.get(wealth_element, 0)
        if wealth_ratio > 0.25:
            wealth_text += "재성이 왕성하여 재물 복이 있습니다. "
            if strength in ["weak", "very_weak"]:
                wealth_text += "다만 일간이 약하여 재물을 감당하기 어려울 수 있습니다. "
        elif wealth_ratio < 0.1:
            wealth_text += "재성이 약하여 재물 축적에 노력이 필요합니다. "
        else:
            wealth_text += "재성이 적당하여 안정적인 재물운입니다. "

        wealth_text += f"{yong_sin.value} 관련 분야에서 재물 기회를 찾으세요."

        return wealth_text

    def interpret_career(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석 - 자평명리 관점"""
        geok_guk = self.determine_geok_guk(saju_data)
        day_element = self._get_day_stem_element(saju_data)

        career_text = f"격국이 {geok_guk}로, "

        career_by_geok = {
            "정관격": "공무원, 관리직, 대기업 등 안정적인 직업이 적합합니다.",
            "편관격": "군인, 경찰, 외과의사 등 권위와 결단력이 필요한 분야가 좋습니다.",
            "정인격": "교육, 학문, 연구직 등 지적 분야에서 성공할 수 있습니다.",
            "편인격": "예술, 종교, 철학 등 독창적인 분야가 어울립니다.",
            "식신격": "요리, 예술, 교육 등 창작과 표현의 분야가 좋습니다.",
            "상관격": "예술가, 방송인, 변호사 등 언변과 표현력이 중요한 분야입니다.",
            "정재격": "금융, 회계, 사업 등 안정적 재물 관리 분야가 적합합니다.",
            "편재격": "무역, 투자, 사업 등 역동적인 재물 분야가 좋습니다.",
            "건록격": "자영업, 전문직 등 독립적인 분야에서 성공합니다.",
        }

        career_text += career_by_geok.get(geok_guk, "다양한 분야에서 능력을 발휘할 수 있습니다.")

        return career_text

    def interpret_relationship(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석 - 자평명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        strength = self._get_strength_level(saju_data)

        rel_text = f"일간 {day_element.value}의 성향으로, "

        if strength in ["strong", "very_strong"]:
            rel_text += "주도적인 성격으로 리더십이 있습니다. "
            rel_text += "다만 타인의 의견을 경청하려 노력해야 합니다. "
        elif strength in ["weak", "very_weak"]:
            rel_text += "협조적이고 유연한 성격입니다. "
            rel_text += "자신의 의견을 적극적으로 표현하면 좋습니다. "
        else:
            rel_text += "균형 잡힌 대인관계를 유지할 수 있습니다. "

        rel_text += f"{yong_sin.value} 오행의 사람과 좋은 인연이 있습니다."

        return rel_text

    def interpret_fame(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석 - 자평명리 관점"""
        day_element = self._get_day_stem_element(saju_data)
        official_element = get_ke_me_element(day_element)  # 관성
        balance = self._get_wuxing_balance(saju_data)

        fame_text = f"관성({official_element.value})이 명예와 사회적 지위를 나타냅니다. "

        official_ratio = balance.get(official_element, 0)
        if official_ratio > 0.2:
            fame_text += "관성이 적당하여 사회적 인정을 받을 수 있습니다. "
        elif official_ratio < 0.1:
            fame_text += "관성이 약하여 명예보다 실리를 추구하는 편입니다. "
        else:
            fame_text += "관성이 중간으로 적당한 사회적 활동이 좋습니다. "

        return fame_text

    def calculate_confidence(self, saju_data: Dict[str, Any]) -> float:
        """신뢰도 계산 - 자평명리"""
        # 자평명리는 전통적 방법으로 기본 신뢰도 높음
        base = 0.75

        # 오행 정보가 충분할수록 신뢰도 상승
        wuxing_count = saju_data.get("wuxing_count", {})
        if len(wuxing_count) == 5:
            base += 0.1

        # 강약 정보가 있으면 신뢰도 상승
        if saju_data.get("day_master_strength"):
            base += 0.05

        return min(0.95, base)

    def extract_key_features(
        self,
        saju_data: Dict[str, Any],
        yong_sin: WuXing
    ) -> List[str]:
        """핵심 특징 추출"""
        geok_guk = self.determine_geok_guk(saju_data)
        strength = self._get_strength_level(saju_data)

        features = [
            f"용신: {yong_sin.value}",
            f"격국: {geok_guk}",
            f"일간 강약: {strength}",
            "해석 기준: 일간 중심 강약 분석",
        ]

        return features
