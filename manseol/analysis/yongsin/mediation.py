"""
통관용신(通關用神) 알고리즘
충돌하는 오행 사이를 중재하는 오행 선정
Reference: fortuneteller/src/lib/yongsin/mediation_algorithm.ts
"""

from typing import Dict, Any, Optional, List, Tuple
from .base import (
    YongSinAlgorithm,
    YongSinResult,
    YongSinRecommendations,
    YongSinMethod,
    WuXing,
    DayMasterStrength,
    get_wuxing_attributes,
    str_to_wuxing,
    get_day_master_strength_from_score,
    KE_MAP,
)


# 상극 관계에서 통관 역할을 하는 오행
# A극B 관계에서 통관용신은 A가 생하고 B를 생하는 오행
MEDIATION_MAP: Dict[Tuple[WuXing, WuXing], WuXing] = {
    # 목극토 -> 화가 통관 (목생화, 화생토)
    (WuXing.WOOD, WuXing.EARTH): WuXing.FIRE,
    # 화극금 -> 토가 통관 (화생토, 토생금)
    (WuXing.FIRE, WuXing.METAL): WuXing.EARTH,
    # 토극수 -> 금이 통관 (토생금, 금생수)
    (WuXing.EARTH, WuXing.WATER): WuXing.METAL,
    # 금극목 -> 수가 통관 (금생수, 수생목)
    (WuXing.METAL, WuXing.WOOD): WuXing.WATER,
    # 수극화 -> 목이 통관 (수생목, 목생화)
    (WuXing.WATER, WuXing.FIRE): WuXing.WOOD,
}


class MediationYongSinAlgorithm(YongSinAlgorithm):
    """
    통관용신 알고리즘

    원리:
    - 사주 내 충돌하는 오행(상극 관계) 사이를 중재하는 오행을 용신으로 선정
    - A극B 관계에서 A를 설기하고 B를 생하는 오행이 통관
    - 예: 목극토 관계에서 화(火)가 통관 (목생화, 화생토)
    """

    @property
    def name(self) -> str:
        return "통관용신"

    @property
    def description(self) -> str:
        return "사주 내 충돌하는 오행 사이를 중재하여 조화를 이루는 오행을 선정합니다."

    def select(self, saju_data: Dict[str, Any]) -> YongSinResult:
        """용신 선정"""
        # 오행 분포 확인
        wuxing_count = self._get_wuxing_count(saju_data)

        # 강한 오행들 찾기
        strong_elements = self._find_strong_elements(wuxing_count)

        # 상극 관계 찾기
        conflicts = self._find_conflicts(strong_elements)

        # 일간 강약
        strength = self._get_day_master_strength(saju_data)

        if conflicts:
            # 가장 심한 충돌에 대한 통관용신 선정
            conflict = conflicts[0]
            primary_yongsin = MEDIATION_MAP.get(conflict)

            if primary_yongsin:
                return self._create_mediation_result(
                    primary_yongsin,
                    conflict,
                    wuxing_count,
                    strength
                )

        # 충돌이 없으면 가장 약한 오행 보강 (강약용신 방식)
        return self._fallback_to_weakest(wuxing_count, strength)

    def calculate_applicability(self, saju_data: Dict[str, Any]) -> float:
        """
        통관용신의 적용 적합도 계산
        상극 관계가 있을수록 적합도 높음
        """
        wuxing_count = self._get_wuxing_count(saju_data)
        strong_elements = self._find_strong_elements(wuxing_count)
        conflicts = self._find_conflicts(strong_elements)

        if not conflicts:
            return 0.3  # 충돌이 없으면 낮은 적합도

        # 충돌 수에 따라 적합도 증가
        applicability = 0.5 + (len(conflicts) * 0.15)

        # 충돌 강도도 고려
        for c1, c2 in conflicts:
            count1 = wuxing_count.get(c1.value, 0)
            count2 = wuxing_count.get(c2.value, 0)
            intensity = min(count1, count2) / 4  # 0~1 정규화
            applicability += intensity * 0.1

        return min(1.0, applicability)

    def _get_wuxing_count(self, saju_data: Dict[str, Any]) -> Dict[str, int]:
        """오행 개수 추출"""
        five_elements = saju_data.get("five_elements_analysis", {})
        distribution = five_elements.get("distribution", {})

        result = {}
        for element in WuXing:
            element_data = distribution.get(element.value, {})
            result[element.value] = element_data.get("count", 0)

        return result

    def _find_strong_elements(self, wuxing_count: Dict[str, int]) -> List[WuXing]:
        """강한 오행 찾기 (평균 이상)"""
        total = sum(wuxing_count.values())
        avg = total / 5 if total > 0 else 1.6

        strong = []
        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            if count >= avg:
                strong.append(element)

        return strong

    def _find_conflicts(self, strong_elements: List[WuXing]) -> List[Tuple[WuXing, WuXing]]:
        """상극 관계 찾기"""
        conflicts = []

        for e1 in strong_elements:
            for e2 in strong_elements:
                if e1 != e2 and KE_MAP.get(e1) == e2:
                    conflicts.append((e1, e2))

        return conflicts

    def _get_day_master_strength(self, saju_data: Dict[str, Any]) -> DayMasterStrength:
        """일간 강약 추출"""
        strength_info = saju_data.get("strength_analysis", {})
        score = strength_info.get("score", 50)
        return get_day_master_strength_from_score(score)

    def _create_mediation_result(
        self,
        primary_yongsin: WuXing,
        conflict: Tuple[WuXing, WuXing],
        wuxing_count: Dict[str, int],
        strength: DayMasterStrength
    ) -> YongSinResult:
        """통관용신 결과 생성"""
        attacker, victim = conflict

        # 희신: 통관용신을 생하는 오행
        xi_sin = [primary_yongsin]

        # 기신: 충돌을 일으키는 오행 (둘 다)
        ji_sin = [attacker, victim]

        # 수신: 통관용신을 극하는 오행
        chou_sin = []
        for element, target in KE_MAP.items():
            if target == primary_yongsin:
                chou_sin.append(element)
                break

        reasoning = (
            f"사주 내 {attacker.value}과 {victim.value}의 상극 관계가 있어 충돌이 발생합니다. "
            f"{primary_yongsin.value} 오행이 {attacker.value}의 기운을 받아 {victim.value}을 생하므로, "
            f"두 오행을 중재하는 통관용신으로 {primary_yongsin.value}을(를) 선정합니다."
        )

        recommendations = self._generate_recommendations(primary_yongsin, None, ji_sin)

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=None,
            xi_sin=xi_sin,
            ji_sin=ji_sin,
            chou_sin=chou_sin,
            day_master_strength=strength,
            reasoning=reasoning,
            method=YongSinMethod.MEDIATION,
            confidence=0.85,
            recommendations=recommendations,
        )

    def _fallback_to_weakest(
        self,
        wuxing_count: Dict[str, int],
        strength: DayMasterStrength
    ) -> YongSinResult:
        """충돌이 없을 때 가장 약한 오행 보강"""
        min_element = WuXing.WOOD
        min_count = float('inf')

        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            if count < min_count:
                min_count = count
                min_element = element

        primary_yongsin = min_element

        reasoning = (
            f"사주 내 뚜렷한 상극 충돌이 없으므로, "
            f"가장 약한 오행인 {primary_yongsin.value}을(를) 보강하여 균형을 맞춥니다."
        )

        recommendations = self._generate_recommendations(primary_yongsin, None, [])

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=None,
            xi_sin=[primary_yongsin],
            ji_sin=[],
            chou_sin=[],
            day_master_strength=strength,
            reasoning=reasoning,
            method=YongSinMethod.MEDIATION,
            confidence=0.65,  # 폴백이므로 낮은 신뢰도
            recommendations=recommendations,
        )

    def _generate_recommendations(
        self,
        primary: WuXing,
        secondary: Optional[WuXing],
        ji_sin: List[WuXing]
    ) -> YongSinRecommendations:
        """용신 기반 추천 정보 생성"""
        primary_attrs = get_wuxing_attributes(primary)

        colors = list(primary_attrs.get("colors", []))
        directions = list(primary_attrs.get("directions", []))
        careers = list(primary_attrs.get("careers", []))
        activities = list(primary_attrs.get("activities", []))

        # 기신 주의사항 생성
        cautions = []
        for ji in ji_sin[:2]:
            ji_attrs = get_wuxing_attributes(ji)
            ji_colors = ", ".join(ji_attrs.get("colors", [])[:2])
            cautions.append(f"{ji.value} 오행({ji_colors})의 과다한 영향을 피하세요")

        return YongSinRecommendations(
            colors=list(set(colors))[:5],
            directions=list(set(directions))[:3],
            careers=list(set(careers))[:8],
            activities=list(set(activities))[:6],
            cautions=cautions[:6],
        )
