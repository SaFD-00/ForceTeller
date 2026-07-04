"""
궁통보감(窮通寶鑑) 해석기
명나라 여춘태의 저서
월령과 조후(調候)를 중시하는 계절 중심 해석
"""

from typing import Any

from ..yongsin.base import WuXing
from .base_interpreter import BaseSchoolInterpreter, SchoolCode

# 월령별 조후 용신 (계절과 일간에 따른 필요 오행)
SEASONAL_YONGSIN = {
    # 봄 (인묘진 - 1, 2, 3월)
    "spring": {
        WuXing.WOOD: WuXing.FIRE,  # 목 → 화로 설기
        WuXing.FIRE: WuXing.WOOD,  # 화 → 목의 생조
        WuXing.EARTH: WuXing.FIRE,  # 토 → 화로 온기
        WuXing.METAL: WuXing.FIRE,  # 금 → 화로 따뜻하게
        WuXing.WATER: WuXing.FIRE,  # 수 → 화로 온기 보충
    },
    # 여름 (사오미 - 4, 5, 6월)
    "summer": {
        WuXing.WOOD: WuXing.WATER,  # 목 → 수로 윤택
        WuXing.FIRE: WuXing.WATER,  # 화 → 수로 제어
        WuXing.EARTH: WuXing.WATER,  # 토 → 수로 조습
        WuXing.METAL: WuXing.WATER,  # 금 → 수로 세척
        WuXing.WATER: WuXing.METAL,  # 수 → 금으로 생조
    },
    # 가을 (신유술 - 7, 8, 9월)
    "autumn": {
        WuXing.WOOD: WuXing.WATER,  # 목 → 수로 생조
        WuXing.FIRE: WuXing.WOOD,  # 화 → 목으로 생조
        WuXing.EARTH: WuXing.FIRE,  # 토 → 화로 온기
        WuXing.METAL: WuXing.FIRE,  # 금 → 화로 단련
        WuXing.WATER: WuXing.METAL,  # 수 → 금으로 생조
    },
    # 겨울 (해자축 - 10, 11, 12월)
    "winter": {
        WuXing.WOOD: WuXing.FIRE,  # 목 → 화로 온기
        WuXing.FIRE: WuXing.WOOD,  # 화 → 목으로 생조
        WuXing.EARTH: WuXing.FIRE,  # 토 → 화로 온기
        WuXing.METAL: WuXing.FIRE,  # 금 → 화로 온기
        WuXing.WATER: WuXing.FIRE,  # 수 → 화로 따뜻하게
    },
}

# 지지와 계절 매핑
BRANCH_TO_SEASON = {
    "인": "spring",
    "묘": "spring",
    "진": "spring",
    "사": "summer",
    "오": "summer",
    "미": "summer",
    "신": "autumn",
    "유": "autumn",
    "술": "autumn",
    "해": "winter",
    "자": "winter",
    "축": "winter",
}


class QTBJInterpreter(BaseSchoolInterpreter):
    """궁통보감 해석기"""

    @property
    def school_code(self) -> SchoolCode:
        return SchoolCode.QTBJ

    def _get_season(self, saju_data: dict[str, Any]) -> str:
        """월령에서 계절 추출"""
        month_pillar = saju_data.get("month_pillar", {})
        branch = month_pillar.get("branch", "자")
        return BRANCH_TO_SEASON.get(branch, "winter")

    def determine_yong_sin(self, saju_data: dict[str, Any]) -> WuXing:
        """
        궁통보감 방식의 용신 결정 (조후용신)
        월령(계절)과 일간의 관계로 결정
        """
        day_element = self._get_day_stem_element(saju_data)
        season = self._get_season(saju_data)

        # 조후 용신 테이블에서 찾기
        seasonal_table = SEASONAL_YONGSIN.get(season, {})
        yong_sin = seasonal_table.get(day_element)

        if yong_sin:
            return yong_sin

        # 기본값: 계절 반대 성질
        if season in ["summer"]:
            return WuXing.WATER
        else:
            return WuXing.FIRE

    def determine_geok_guk(self, saju_data: dict[str, Any]) -> str | None:
        """궁통보감의 조후 상태 판단"""
        self._get_season(saju_data)
        self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        # 조후 상태 확인
        yong_sin = self.determine_yong_sin(saju_data)
        yong_sin_ratio = balance.get(yong_sin, 0)

        if yong_sin_ratio > 0.2:
            return "조후득력격"  # 조후가 잘 맞음
        elif yong_sin_ratio < 0.05:
            return "조후실격"  # 조후가 맞지 않음
        else:
            return "조후중화격"  # 보통

    def interpret_health(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석 - 궁통보감 관점"""
        season = self._get_season(saju_data)
        day_element = self._get_day_stem_element(saju_data)
        self._get_wuxing_balance(saju_data)

        season_names = {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"}
        season_name = season_names.get(season, "")

        health_text = (
            f"궁통보감에서는 {season_name}에 태어난 {day_element.value} 일간의 건강을 중시합니다. "
        )

        # 계절별 건강 조언
        seasonal_health = {
            "spring": "봄에는 간담 기능이 활발하니 화를 다스려야 합니다.",
            "summer": "여름에는 심장에 열이 오르기 쉬우니 수분 섭취가 중요합니다.",
            "autumn": "가을에는 폐 기능이 예민하니 호흡기 관리가 필요합니다.",
            "winter": "겨울에는 신장이 약해지기 쉬우니 보온에 신경 쓰세요.",
        }

        health_text += seasonal_health.get(season, "")
        health_text += f" {yong_sin.value} 오행으로 몸의 균형을 맞추세요."

        return health_text

    def interpret_wealth(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석 - 궁통보감 관점"""
        season = self._get_season(saju_data)
        balance = self._get_wuxing_balance(saju_data)

        season_names = {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"}
        season_name = season_names.get(season, "")

        wealth_text = f"궁통보감에서 {season_name} 출생자의 재물운은 조후의 영향을 받습니다. "

        yong_sin_ratio = balance.get(yong_sin, 0)

        if yong_sin_ratio > 0.15:
            wealth_text += (
                f"{yong_sin.value} 오행이 있어 계절의 부조화를 보완하고 재물운이 순탄합니다. "
            )
        else:
            wealth_text += f"{yong_sin.value} 오행이 부족하여 재물 획득에 노력이 필요합니다. "

        # 계절별 재물 조언
        seasonal_wealth = {
            "spring": "성장하는 시기처럼 장기 투자가 유리합니다.",
            "summer": "열기가 있을 때 적극적으로 움직이되 냉정함을 유지하세요.",
            "autumn": "수확의 시기처럼 결실을 거두는 투자가 좋습니다.",
            "winter": "저축하고 준비하는 시기로 보수적 투자가 유리합니다.",
        }

        wealth_text += seasonal_wealth.get(season, "")

        return wealth_text

    def interpret_career(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석 - 궁통보감 관점"""
        self._get_season(saju_data)
        self._get_day_stem_element(saju_data)

        career_text = "궁통보감에서는 계절과 조후로 직업 적성을 봅니다. "

        # 용신 기반 직업 추천
        yongsin_careers = {
            WuXing.WOOD: "교육, 환경, 의료, 출판 분야가 적합합니다.",
            WuXing.FIRE: "IT, 광고, 요리, 에너지 분야가 좋습니다.",
            WuXing.EARTH: "부동산, 건설, 농업, 컨설팅이 어울립니다.",
            WuXing.METAL: "금융, 기계, 법률, 자동차 분야가 적합합니다.",
            WuXing.WATER: "무역, 유통, 연구, 서비스업이 좋습니다.",
        }

        career_text += f"조후용신이 {yong_sin.value}이므로 "
        career_text += yongsin_careers.get(yong_sin, "다양한 분야에서 활동할 수 있습니다.")

        return career_text

    def interpret_relationship(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석 - 궁통보감 관점"""
        season = self._get_season(saju_data)
        day_element = self._get_day_stem_element(saju_data)

        season_names = {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"}
        season_name = season_names.get(season, "")

        rel_text = f"{season_name}에 태어나 {day_element.value}의 성정을 가집니다. "

        # 계절별 관계 특성
        seasonal_rel = {
            "spring": "성장하는 기운으로 새로운 관계에 적극적입니다. 인내심을 기르면 좋습니다.",
            "summer": "열정적이고 사교적이지만, 급한 성격을 조절하면 좋습니다.",
            "autumn": "차분하고 신중하며, 깊은 관계를 선호합니다.",
            "winter": "내성적이지만 신뢰를 쌓으면 깊은 우정을 나눕니다.",
        }

        rel_text += seasonal_rel.get(season, "")
        rel_text += f" {yong_sin.value} 오행의 사람과 좋은 관계를 맺습니다."

        return rel_text

    def interpret_fame(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석 - 궁통보감 관점"""
        geok_guk = self.determine_geok_guk(saju_data)
        self._get_season(saju_data)

        fame_text = "궁통보감에서 명예는 조후의 적절함에서 옵니다. "

        if geok_guk == "조후득력격":
            fame_text += "조후가 잘 맞아 사회적으로 인정받기 쉽습니다. "
            fame_text += "타고난 운의 흐름을 잘 활용하세요."
        elif geok_guk == "조후실격":
            fame_text += "조후가 맞지 않아 노력으로 보완해야 합니다. "
            fame_text += f"{yong_sin.value} 관련 활동으로 균형을 맞추면 명예를 얻습니다."
        else:
            fame_text += "적당한 조후로 꾸준한 노력이 성과를 냅니다."

        return fame_text

    def calculate_confidence(self, saju_data: dict[str, Any]) -> float:
        """신뢰도 계산 - 궁통보감"""
        base = 0.7

        # 월령 정보가 있으면 신뢰도 상승 (조후 판단의 핵심)
        if saju_data.get("month_pillar"):
            base += 0.15

        # 오행 정보 완성도
        wuxing_count = saju_data.get("wuxing_count", {})
        if len(wuxing_count) == 5:
            base += 0.05

        return min(0.92, base)

    def extract_key_features(self, saju_data: dict[str, Any], yong_sin: WuXing) -> list[str]:
        """핵심 특징 추출"""
        season = self._get_season(saju_data)
        geok_guk = self.determine_geok_guk(saju_data)

        season_names = {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"}

        features = [
            f"조후용신: {yong_sin.value}",
            f"출생 계절: {season_names.get(season, season)}",
            f"조후 상태: {geok_guk}",
            "해석 기준: 월령 중심 조후 분석",
        ]

        return features
