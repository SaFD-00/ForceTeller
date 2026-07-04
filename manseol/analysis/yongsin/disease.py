"""
병약용신(病藥用神) 알고리즘
사주의 불균형(병)을 진단하고 치료(약) 오행 선정
Reference: fortuneteller/src/lib/yongsin/disease_algorithm.ts
"""

from typing import Any

from .base import (
    DayMasterStrength,
    WuXing,
    YongSinAlgorithm,
    YongSinMethod,
    YongSinRecommendations,
    YongSinResult,
    get_day_master_strength_from_score,
    get_ke_me_element,
    get_sheng_me_element,
    get_wuxing_attributes,
)


class DiseaseYongSinAlgorithm(YongSinAlgorithm):
    """
    병약용신 알고리즘

    원리:
    - 사주의 불균형(病)을 찾아 그것을 치료하는 오행(藥)을 용신으로 선정
    - 과다한 오행이 병(病), 그것을 극하거나 설기하는 오행이 약(藥)
    - 부족한 오행이 병이면, 그것을 보충하는 오행이 약
    """

    @property
    def name(self) -> str:
        return "병약용신"

    @property
    def description(self) -> str:
        return "사주의 불균형(病)을 진단하고 그것을 치료하는 오행(藥)을 선정합니다."

    def select(self, saju_data: dict[str, Any]) -> YongSinResult:
        """용신 선정"""
        # 오행 분포 확인
        wuxing_count = self._get_wuxing_count(saju_data)

        # 일간 강약
        strength = self._get_day_master_strength(saju_data)

        # 병(病) 진단: 과다하거나 부족한 오행
        disease_element, disease_type = self._diagnose_disease(wuxing_count)

        # 약(藥) 선정: 병을 치료하는 오행
        medicine_element = self._find_medicine(disease_element, disease_type, wuxing_count)

        return self._create_result(
            medicine_element, disease_element, disease_type, wuxing_count, strength
        )

    def calculate_applicability(self, saju_data: dict[str, Any]) -> float:
        """
        병약용신의 적용 적합도 계산
        오행 불균형이 심할수록 적합도 높음
        """
        wuxing_count = self._get_wuxing_count(saju_data)

        # 불균형 정도 계산
        total = sum(wuxing_count.values())
        avg = total / 5 if total > 0 else 1.6

        # 편차 계산
        variance = 0
        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            variance += (count - avg) ** 2

        variance /= 5

        # 편차가 클수록 적합도 높음 (0~2 -> 0.4~1.0)
        applicability = 0.4 + min(0.6, variance * 0.3)

        return min(1.0, applicability)

    def _get_wuxing_count(self, saju_data: dict[str, Any]) -> dict[str, int]:
        """오행 개수 추출"""
        five_elements = saju_data.get("five_elements_analysis", {})
        distribution = five_elements.get("distribution", {})

        result = {}
        for element in WuXing:
            element_data = distribution.get(element.value, {})
            result[element.value] = element_data.get("count", 0)

        return result

    def _get_day_master_strength(self, saju_data: dict[str, Any]) -> DayMasterStrength:
        """일간 강약 추출"""
        strength_info = saju_data.get("strength_analysis", {})
        score = strength_info.get("score", 50)
        return get_day_master_strength_from_score(score)

    def _diagnose_disease(self, wuxing_count: dict[str, int]) -> tuple:
        """
        병(病) 진단

        Returns:
            (병이 되는 오행, 병의 유형: 'excess' 또는 'deficiency')
        """
        total = sum(wuxing_count.values())
        avg = total / 5 if total > 0 else 1.6

        max_element = None
        max_count = 0
        min_element = None
        min_count = float("inf")

        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            if count > max_count:
                max_count = count
                max_element = element
            if count < min_count:
                min_count = count
                min_element = element

        # 과다 vs 부족 중 더 심한 쪽이 병
        excess_severity = max_count - avg
        deficiency_severity = avg - min_count

        if excess_severity >= deficiency_severity and excess_severity > 0.5:
            return (max_element, "excess")
        elif deficiency_severity > 0.5:
            return (min_element, "deficiency")
        else:
            # 균형 상태면 가장 약한 오행을 부족으로 진단
            return (min_element, "deficiency")

    def _find_medicine(
        self, disease_element: WuXing, disease_type: str, wuxing_count: dict[str, int]
    ) -> WuXing:
        """
        약(藥) 선정

        - 과다(excess): 병을 극하거나 설기하는 오행이 약
        - 부족(deficiency): 병을 생하거나 보충하는 오행이 약
        """
        if disease_type == "excess":
            # 과다한 오행을 극하는 오행이 약
            return get_ke_me_element(disease_element)
        else:
            # 부족한 오행을 생하는 오행이 약
            return get_sheng_me_element(disease_element)

    def _create_result(
        self,
        medicine: WuXing,
        disease: WuXing,
        disease_type: str,
        wuxing_count: dict[str, int],
        strength: DayMasterStrength,
    ) -> YongSinResult:
        """결과 생성"""
        primary_yongsin = medicine

        # 희신: 약(용신)을 돕는 오행
        xi_sin = [medicine]
        medicine_producer = get_sheng_me_element(medicine)
        if medicine_producer != disease:
            xi_sin.append(medicine_producer)

        # 기신: 병을 악화시키는 오행
        ji_sin = []
        if disease_type == "excess":
            # 과다할 때 기신은 병을 생하는 오행
            disease_producer = get_sheng_me_element(disease)
            ji_sin.append(disease_producer)
            ji_sin.append(disease)  # 병 자체도 기신
        else:
            # 부족할 때 기신은 병을 극하는 오행
            disease_attacker = get_ke_me_element(disease)
            ji_sin.append(disease_attacker)

        # 수신: 용신을 극하는 오행
        chou_sin = [get_ke_me_element(medicine)]

        # 설명 생성
        if disease_type == "excess":
            reasoning = (
                f"사주 내 {disease.value} 오행이 과다하여 불균형(病)이 발생합니다. "
                f"{medicine.value} 오행이 {disease.value}을(를) 극(克)하여 과다한 기운을 억제하므로, "
                f"이를 약(藥)으로 삼아 용신으로 선정합니다."
            )
        else:
            reasoning = (
                f"사주 내 {disease.value} 오행이 부족하여 불균형(病)이 발생합니다. "
                f"{medicine.value} 오행이 {disease.value}을(를) 생(生)하여 부족한 기운을 보충하므로, "
                f"이를 약(藥)으로 삼아 용신으로 선정합니다."
            )

        recommendations = self._generate_recommendations(primary_yongsin, None, ji_sin)

        return YongSinResult(
            primary_yongsin=primary_yongsin,
            secondary_yongsin=disease if disease_type == "deficiency" else None,
            xi_sin=xi_sin,
            ji_sin=ji_sin,
            chou_sin=chou_sin,
            day_master_strength=strength,
            reasoning=reasoning,
            method=YongSinMethod.DISEASE,
            confidence=0.80,
            recommendations=recommendations,
        )

    def _generate_recommendations(
        self, primary: WuXing, secondary: WuXing | None, ji_sin: list[WuXing]
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
            cautions.append(f"{ji.value} 오행({ji_colors})의 과다한 영향을 피하세요")

        return YongSinRecommendations(
            colors=list(set(colors))[:5],
            directions=list(set(directions))[:3],
            careers=list(set(careers))[:8],
            activities=list(set(activities))[:6],
            cautions=cautions[:6],
        )
