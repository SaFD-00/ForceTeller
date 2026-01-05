"""
조후용신(調候用神) 알고리즘
계절의 한(寒)/난(暖)/조(燥)/습(濕)을 조절하는 오행 선정
Reference: fortuneteller/src/lib/yongsin/seasonal_algorithm.ts
"""

from typing import Dict, Any, Optional
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
)


# 절기별 계절 매핑
SOLAR_TERM_SEASON: Dict[str, str] = {
    # 봄 (목)
    "입춘": "봄", "우수": "봄", "경칩": "봄", "춘분": "봄", "청명": "봄", "곡우": "봄",
    # 여름 (화)
    "입하": "여름", "소만": "여름", "망종": "여름", "하지": "여름", "소서": "여름", "대서": "여름",
    # 가을 (금)
    "입추": "가을", "처서": "가을", "백로": "가을", "추분": "가을", "한로": "가을", "상강": "가을",
    # 겨울 (수)
    "입동": "겨울", "소설": "겨울", "대설": "겨울", "동지": "겨울", "소한": "겨울", "대한": "겨울",
}

# 계절별 조후 필요 오행
SEASONAL_ADJUSTMENT: Dict[str, Dict[str, WuXing]] = {
    "봄": {
        "needs": WuXing.FIRE,   # 봄은 아직 찬 기운이 있어 火로 따뜻하게
        "avoid": WuXing.WATER,  # 水는 더 춥게 만듦
        "season_element": WuXing.WOOD,
    },
    "여름": {
        "needs": WuXing.WATER,  # 여름은 더워서 水로 시원하게
        "avoid": WuXing.FIRE,   # 火는 더 뜨겁게 만듦
        "season_element": WuXing.FIRE,
    },
    "가을": {
        "needs": WuXing.WATER,  # 가을은 건조해서 水로 습윤하게
        "avoid": WuXing.FIRE,   # 火는 더 건조하게 만듦
        "season_element": WuXing.METAL,
    },
    "겨울": {
        "needs": WuXing.FIRE,   # 겨울은 추워서 火로 따뜻하게
        "avoid": WuXing.WATER,  # 水는 더 춥게 만듦
        "season_element": WuXing.WATER,
    },
}

# 월지별 계절
MONTH_BRANCH_SEASON: Dict[str, str] = {
    "인": "봄", "묘": "봄", "진": "봄",      # 1-3월
    "사": "여름", "오": "여름", "미": "여름",  # 4-6월
    "신": "가을", "유": "가을", "술": "가을",  # 7-9월
    "해": "겨울", "자": "겨울", "축": "겨울",  # 10-12월
}


class SeasonalYongSinAlgorithm(YongSinAlgorithm):
    """
    조후용신 알고리즘 (궁통보감 방식)

    원리:
    - 계절의 한난조습을 조절하는 오행을 용신으로 선정
    - 봄/겨울(寒): 火가 필요
    - 여름/가을(暖/燥): 水가 필요
    """

    @property
    def name(self) -> str:
        return "조후용신"

    @property
    def description(self) -> str:
        return "계절의 한난조습(寒暖燥濕)을 조절하여 사주의 균형을 맞추는 오행을 선정합니다. 궁통보감 방식입니다."

    def select(self, saju_data: Dict[str, Any]) -> YongSinResult:
        """용신 선정"""
        # 계절 파악
        season = self._get_season(saju_data)
        season_adj = SEASONAL_ADJUSTMENT.get(season, SEASONAL_ADJUSTMENT["봄"])

        # 일간 오행
        day_stem_element = self._get_day_stem_element(saju_data)

        # 일간 강약
        strength = self._get_day_master_strength(saju_data)

        # 조후용신 선정
        primary_yongsin = season_adj["needs"]
        avoid_element = season_adj["avoid"]
        season_element = season_adj["season_element"]

        # 희신: 용신을 생하는 오행
        xi_sin = [primary_yongsin]
        if primary_yongsin == WuXing.FIRE:
            xi_sin.append(WuXing.WOOD)  # 목생화
        elif primary_yongsin == WuXing.WATER:
            xi_sin.append(WuXing.METAL)  # 금생수

        # 기신: 피해야 할 오행
        ji_sin = [avoid_element]
        if avoid_element == WuXing.FIRE:
            ji_sin.append(WuXing.WOOD)
        elif avoid_element == WuXing.WATER:
            ji_sin.append(WuXing.METAL)

        # 수신: 용신을 극하는 오행
        chou_sin = []
        if primary_yongsin == WuXing.FIRE:
            chou_sin.append(WuXing.WATER)  # 수극화
        elif primary_yongsin == WuXing.WATER:
            chou_sin.append(WuXing.EARTH)  # 토극수

        # 보조 용신: 용신을 생하는 오행
        secondary_yongsin = xi_sin[1] if len(xi_sin) > 1 else None

        # 계절별 특성 설명
        season_desc = {
            "봄": "아직 한기가 남아있는",
            "여름": "더운 기운이 가득한",
            "가을": "건조한 기운이 있는",
            "겨울": "추운 기운이 강한",
        }

        adjustment_desc = {
            WuXing.FIRE: "따뜻하게 하는 화(火)",
            WuXing.WATER: "시원하고 습윤하게 하는 수(水)",
        }

        reasoning = (
            f"{season_desc.get(season, season)} {season}에 태어났으므로, "
            f"계절의 기운을 조절하기 위해 "
            f"{adjustment_desc.get(primary_yongsin, primary_yongsin.value)} 기운을 용신으로 삼습니다."
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
            method=YongSinMethod.SEASONAL,
            confidence=0.80,
            recommendations=recommendations,
        )

    def calculate_applicability(self, saju_data: Dict[str, Any]) -> float:
        """
        조후용신의 적용 적합도 계산
        계절 특성이 강할수록 적합도 높음
        """
        season = self._get_season(saju_data)
        wuxing_count = self._get_wuxing_count(saju_data)

        season_adj = SEASONAL_ADJUSTMENT.get(season, SEASONAL_ADJUSTMENT["봄"])
        season_element = season_adj["season_element"]

        # 계절 오행이 사주에 많을수록 적합도 높음
        season_count = wuxing_count.get(season_element.value, 0)

        # 0~4 -> 0.5~0.9
        applicability = 0.5 + (season_count * 0.1)

        # 극단적인 계절(여름/겨울)일수록 더 적합
        if season in ["여름", "겨울"]:
            applicability += 0.1

        return min(1.0, applicability)

    def _get_season(self, saju_data: Dict[str, Any]) -> str:
        """계절 파악"""
        # 절기로 판단
        solar_term = saju_data.get("solar_term", "")
        if solar_term in SOLAR_TERM_SEASON:
            return SOLAR_TERM_SEASON[solar_term]

        # 월지로 판단
        four_pillars = saju_data.get("four_pillars", {})
        month_pillar = four_pillars.get("month", {})
        month_branch = month_pillar.get("branch", "")

        if month_branch in MONTH_BRANCH_SEASON:
            return MONTH_BRANCH_SEASON[month_branch]

        # 생월로 판단
        birth_date = saju_data.get("input", {}).get("birth_date", "")
        if birth_date:
            try:
                month = int(birth_date.split("-")[1])
                if month in [3, 4, 5]:
                    return "봄"
                elif month in [6, 7, 8]:
                    return "여름"
                elif month in [9, 10, 11]:
                    return "가을"
                else:
                    return "겨울"
            except (IndexError, ValueError):
                pass

        return "봄"  # 기본값

    def _get_day_stem_element(self, saju_data: Dict[str, Any]) -> WuXing:
        """일간 오행 추출"""
        day_master = saju_data.get("day_master_analysis", {})
        if day_master:
            element_str = day_master.get("element", "목")
            return str_to_wuxing(element_str) or WuXing.WOOD

        four_pillars = saju_data.get("four_pillars", {})
        day_pillar = four_pillars.get("day", {})
        element_str = day_pillar.get("stem_element", "목")
        return str_to_wuxing(element_str) or WuXing.WOOD

    def _get_day_master_strength(self, saju_data: Dict[str, Any]) -> DayMasterStrength:
        """일간 강약 추출"""
        strength_info = saju_data.get("strength_analysis", {})
        score = strength_info.get("score", 50)
        return get_day_master_strength_from_score(score)

    def _get_wuxing_count(self, saju_data: Dict[str, Any]) -> Dict[str, int]:
        """오행 개수 추출"""
        five_elements = saju_data.get("five_elements_analysis", {})
        distribution = five_elements.get("distribution", {})

        result = {}
        for element in WuXing:
            element_data = distribution.get(element.value, {})
            result[element.value] = element_data.get("count", 0)

        return result

    def _generate_recommendations(
        self,
        primary: WuXing,
        secondary: Optional[WuXing],
        ji_sin: list
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
            cautions.append(f"{ji.value} 오행({ji_colors})은 피하세요")

        return YongSinRecommendations(
            colors=list(set(colors))[:5],
            directions=list(set(directions))[:3],
            careers=list(set(careers))[:8],
            activities=list(set(activities))[:6],
            cautions=cautions[:6],
        )
