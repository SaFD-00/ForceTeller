"""
강약용신(强弱用神) 알고리즘
일간의 강약을 기준으로 보충/억제할 오행 선정
Reference: fortuneteller/src/lib/yongsin/strength_algorithm.ts
"""

from typing import Dict, Any, List
from .base import (
    YongSinAlgorithm,
    YongSinResult,
    YongSinRecommendations,
    YongSinMethod,
    WuXing,
    DayMasterStrength,
    get_sheng_element,
    get_sheng_me_element,
    get_ke_element,
    get_ke_me_element,
    get_wuxing_attributes,
    str_to_wuxing,
    get_day_master_strength_from_score,
)


class StrengthYongSinAlgorithm(YongSinAlgorithm):
    """
    강약용신 알고리즘

    원리:
    - 일간이 강하면: 설기(洩)하거나 극(克)하는 오행이 용신
      - 식상(설기): 일간이 생하는 오행
      - 재성(극): 일간이 극하는 오행
    - 일간이 약하면: 생(生)하거나 동일 오행이 용신
      - 인성(생기): 일간을 생하는 오행
      - 비겁(동류): 일간과 같은 오행
    """

    @property
    def name(self) -> str:
        return "강약용신"

    @property
    def description(self) -> str:
        return "일간의 강약을 기준으로 부족한 기운을 보충하거나 과한 기운을 억제하는 오행을 선정합니다."

    def select(self, saju_data: Dict[str, Any]) -> YongSinResult:
        """용신 선정"""
        # 일간 오행 추출
        day_stem_element_str = self._get_day_stem_element(saju_data)
        day_stem_element = str_to_wuxing(day_stem_element_str) or WuXing.WOOD

        # 일간 강약 판단
        strength_info = saju_data.get("strength_analysis", {})
        strength_score = strength_info.get("score", 50)
        strength_level = strength_info.get("level", "중화")

        day_master_strength = self._convert_strength_level(strength_level, strength_score)

        # 용신 선정
        if day_master_strength in [DayMasterStrength.VERY_STRONG, DayMasterStrength.STRONG]:
            # 일간이 강함 → 설(洩), 극(克)하는 오행이 용신
            result = self._select_for_strong_day_master(day_stem_element, day_master_strength)
        elif day_master_strength in [DayMasterStrength.WEAK, DayMasterStrength.VERY_WEAK]:
            # 일간이 약함 → 생(生)하거나 동일 오행이 용신
            result = self._select_for_weak_day_master(day_stem_element, day_master_strength)
        else:
            # 중화 → 가장 약한 오행 보강
            result = self._select_for_medium_day_master(saju_data, day_stem_element)

        return result

    def calculate_applicability(self, saju_data: Dict[str, Any]) -> float:
        """
        강약용신의 적용 적합도 계산
        일간 강약이 명확할수록 적합도 높음
        """
        strength_info = saju_data.get("strength_analysis", {})
        score = strength_info.get("score", 50)

        # 중화(40~60)에서 멀수록 적합도 높음
        distance_from_medium = abs(score - 50)

        # 0~50 -> 0.5~1.0
        applicability = 0.5 + (distance_from_medium / 100)
        return min(1.0, applicability)

    def _get_day_stem_element(self, saju_data: Dict[str, Any]) -> str:
        """일간 오행 추출"""
        # saju_data 구조에 따라 접근 방식 조정
        day_master = saju_data.get("day_master_analysis", {})
        if day_master:
            return day_master.get("element", "목")

        # 대안: four_pillars에서 추출
        four_pillars = saju_data.get("four_pillars", {})
        day_pillar = four_pillars.get("day", {})
        return day_pillar.get("stem_element", "목")

    def _convert_strength_level(self, level_str: str, score: int) -> DayMasterStrength:
        """문자열 강약 레벨을 enum으로 변환"""
        level_map = {
            "신강": DayMasterStrength.STRONG,
            "매우 신강": DayMasterStrength.VERY_STRONG,
            "신약": DayMasterStrength.WEAK,
            "매우 신약": DayMasterStrength.VERY_WEAK,
            "중화": DayMasterStrength.MEDIUM,
        }

        if level_str in level_map:
            return level_map[level_str]

        # 점수로 판단
        return get_day_master_strength_from_score(score)

    def _select_for_strong_day_master(
        self,
        day_stem_element: WuXing,
        strength: DayMasterStrength
    ) -> YongSinResult:
        """강한 일간을 위한 용신 선정"""
        # 식상으로 설기 (일간이 생하는 오행)
        sheng_element = get_sheng_element(day_stem_element)
        # 재성으로 일간의 힘을 빼냄 (일간이 극하는 오행)
        ke_element = get_ke_element(day_stem_element)

        primary_yongsin = sheng_element
        secondary_yongsin = ke_element

        xi_sin = [sheng_element, ke_element]
        # 비겁(동류)과 인성(나를 생하는)은 기신
        ji_sin = [day_stem_element, get_sheng_me_element(day_stem_element)]
        # 인성은 수신 (용신인 식상을 극함)
        chou_sin = [get_sheng_me_element(day_stem_element)]

        intensity = "매우 " if strength == DayMasterStrength.VERY_STRONG else ""
        reasoning = (
            f"일간({day_stem_element.value})이 {intensity}강하므로, "
            f"일간의 힘을 설(洩)하거나 소모시키는 "
            f"{sheng_element.value}(식상)과 {ke_element.value}(재성)을 용신으로 삼습니다."
        )

        recommendations = self._generate_recommendations(primary_yongsin, secondary_yongsin, ji_sin)

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=secondary_yongsin,
            xi_sin=xi_sin,
            ji_sin=ji_sin,
            chou_sin=chou_sin,
            day_master_strength=strength,
            reasoning=reasoning,
            method=YongSinMethod.STRENGTH,
            confidence=0.85,
            recommendations=recommendations,
        )

    def _select_for_weak_day_master(
        self,
        day_stem_element: WuXing,
        strength: DayMasterStrength
    ) -> YongSinResult:
        """약한 일간을 위한 용신 선정"""
        # 인성으로 생기 (나를 생하는 오행)
        sheng_me_element = get_sheng_me_element(day_stem_element)
        # 비겁으로 돕기 (나와 같은 오행)
        same_element = day_stem_element

        primary_yongsin = sheng_me_element
        secondary_yongsin = same_element

        xi_sin = [sheng_me_element, same_element]
        # 재성(내가 극하는)과 관성(나를 극하는)은 기신
        ji_sin = [get_ke_element(day_stem_element), get_ke_me_element(day_stem_element)]
        # 재성은 수신 (용신인 인성을 극함)
        chou_sin = [get_ke_element(day_stem_element)]

        intensity = "매우 " if strength == DayMasterStrength.VERY_WEAK else ""
        reasoning = (
            f"일간({day_stem_element.value})이 {intensity}약하므로, "
            f"일간을 생(生)하는 {sheng_me_element.value}(인성)과 "
            f"일간과 같은 {same_element.value}(비겁)을 용신으로 삼습니다."
        )

        recommendations = self._generate_recommendations(primary_yongsin, secondary_yongsin, ji_sin)

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=secondary_yongsin,
            xi_sin=xi_sin,
            ji_sin=ji_sin,
            chou_sin=chou_sin,
            day_master_strength=strength,
            reasoning=reasoning,
            method=YongSinMethod.STRENGTH,
            confidence=0.85,
            recommendations=recommendations,
        )

    def _select_for_medium_day_master(
        self,
        saju_data: Dict[str, Any],
        day_stem_element: WuXing
    ) -> YongSinResult:
        """중화 일간을 위한 용신 선정 (가장 약한 오행 보강)"""
        wuxing_count = self._get_wuxing_count(saju_data)
        weakest_element = self._find_weakest(wuxing_count)

        primary_yongsin = weakest_element
        secondary_yongsin = get_sheng_element(weakest_element)

        xi_sin = [weakest_element, get_sheng_element(weakest_element)]
        ji_sin = [get_ke_element(weakest_element)]
        chou_sin = [get_ke_me_element(weakest_element)]

        reasoning = (
            f"사주가 중화되어 있으므로, "
            f"가장 약한 오행인 {weakest_element.value}을(를) 보강하여 균형을 맞춥니다."
        )

        recommendations = self._generate_recommendations(primary_yongsin, secondary_yongsin, ji_sin)

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=secondary_yongsin,
            xi_sin=xi_sin,
            ji_sin=ji_sin,
            chou_sin=chou_sin,
            day_master_strength=DayMasterStrength.MEDIUM,
            reasoning=reasoning,
            method=YongSinMethod.STRENGTH,
            confidence=0.75,  # 중화일 때는 약간 낮은 신뢰도
            recommendations=recommendations,
        )

    def _get_wuxing_count(self, saju_data: Dict[str, Any]) -> Dict[str, int]:
        """오행 개수 추출"""
        five_elements = saju_data.get("five_elements_analysis", {})
        distribution = five_elements.get("distribution", {})

        result = {}
        for element in WuXing:
            element_data = distribution.get(element.value, {})
            result[element.value] = element_data.get("count", 0)

        return result

    def _find_weakest(self, wuxing_count: Dict[str, int]) -> WuXing:
        """가장 약한 오행 찾기"""
        min_element = WuXing.WOOD
        min_count = float('inf')

        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            if count < min_count:
                min_count = count
                min_element = element

        return min_element

    def _generate_recommendations(
        self,
        primary: WuXing,
        secondary: WuXing,
        ji_sin: List[WuXing]
    ) -> YongSinRecommendations:
        """용신 기반 추천 정보 생성"""
        primary_attrs = get_wuxing_attributes(primary)
        secondary_attrs = get_wuxing_attributes(secondary) if secondary else {}

        colors = list(primary_attrs.get("colors", []))
        if secondary_attrs:
            colors.extend(secondary_attrs.get("colors", [])[:2])

        directions = list(primary_attrs.get("directions", []))
        if secondary_attrs:
            directions.extend(secondary_attrs.get("directions", [])[:1])

        careers = list(primary_attrs.get("careers", []))
        if secondary_attrs:
            careers.extend(secondary_attrs.get("careers", [])[:3])

        activities = list(primary_attrs.get("activities", []))
        if secondary_attrs:
            activities.extend(secondary_attrs.get("activities", [])[:2])

        # 기신 주의사항 생성
        cautions = []
        for ji in ji_sin[:2]:
            ji_attrs = get_wuxing_attributes(ji)
            ji_colors = ", ".join(ji_attrs.get("colors", [])[:2])
            ji_directions = ", ".join(ji_attrs.get("directions", []))
            cautions.append(f"{ji.value} 오행({ji_colors})은 피하세요")
            if ji_directions:
                cautions.append(f"{ji_directions} 방향 이동은 신중하게")

        return YongSinRecommendations(
            colors=list(set(colors))[:5],
            directions=list(set(directions))[:3],
            careers=list(set(careers))[:8],
            activities=list(set(activities))[:6],
            cautions=cautions[:6],
        )
