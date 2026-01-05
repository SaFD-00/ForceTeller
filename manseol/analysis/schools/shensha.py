"""
신살중심(神煞中心) 해석기
신살(神煞)을 중심으로 길흉을 판단하는 전통적 접근법
특정 조합과 패턴으로 운명을 해석
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


# 주요 신살 정의
SHENSHA_DEFINITIONS = {
    # 길신 (吉神)
    "천을귀인": {
        "type": "길신",
        "meaning": "귀인의 도움을 받음",
        "effect": "어려울 때 도움을 받고, 위기를 넘김",
        "areas": ["인간관계", "직업", "위기 극복"],
    },
    "문창귀인": {
        "type": "길신",
        "meaning": "학문과 문서의 길신",
        "effect": "학업 성취, 시험 합격, 문서 관련 성공",
        "areas": ["학업", "시험", "자격증"],
    },
    "태극귀인": {
        "type": "길신",
        "meaning": "근본의 귀인",
        "effect": "기초가 튼튼하고, 끈기가 있음",
        "areas": ["기초 역량", "지속력"],
    },
    "천덕귀인": {
        "type": "길신",
        "meaning": "하늘의 덕",
        "effect": "덕망이 있고, 흉한 일이 길하게 바뀜",
        "areas": ["명예", "덕망", "흉화 해소"],
    },
    "월덕귀인": {
        "type": "길신",
        "meaning": "월의 덕",
        "effect": "매월 행운이 따르고, 안정적",
        "areas": ["안정", "월별 운"],
    },
    "역마": {
        "type": "중성",
        "meaning": "이동과 변화의 살",
        "effect": "이사, 출장, 여행이 많음. 변화가 잦음",
        "areas": ["이동", "해외", "변화"],
    },
    "화개": {
        "type": "길신",
        "meaning": "예술과 종교의 별",
        "effect": "예술적 감각, 종교심, 고독한 성향",
        "areas": ["예술", "종교", "철학"],
    },
    "식신": {
        "type": "길신",
        "meaning": "식복과 재능",
        "effect": "먹을 복이 있고, 표현력이 좋음",
        "areas": ["식복", "재능", "자녀"],
    },
    # 흉신 (凶神)
    "양인": {
        "type": "흉신",
        "meaning": "날카로운 칼날",
        "effect": "결단력이 있으나 강함이 과해 다칠 수 있음",
        "areas": ["건강", "사고", "결단"],
    },
    "겁살": {
        "type": "흉신",
        "meaning": "강도의 살",
        "effect": "재물 손실, 다툼에 주의",
        "areas": ["재물", "분쟁"],
    },
    "도화": {
        "type": "중성",
        "meaning": "이성과 매력의 살",
        "effect": "이성 관계 활발, 매력적이나 풍류에 빠질 수 있음",
        "areas": ["연애", "매력", "예술"],
    },
    "백호": {
        "type": "흉신",
        "meaning": "흰 호랑이",
        "effect": "사고, 수술, 혈광에 주의",
        "areas": ["건강", "사고"],
    },
    "공망": {
        "type": "흉신",
        "meaning": "비어있는 망",
        "effect": "노력해도 성과가 적을 수 있음, 공허함",
        "areas": ["성과", "허무"],
    },
}


class ShenshaInterpreter(BaseSchoolInterpreter):
    """신살중심 해석기"""

    @property
    def school_code(self) -> SchoolCode:
        return SchoolCode.SHENSHA

    def _analyze_shensha(self, saju_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """신살 분석 (간략화된 버전)"""
        day_stem = saju_data.get("day_pillar", {}).get("stem", "갑")
        day_branch = saju_data.get("day_pillar", {}).get("branch", "자")
        balance = self._get_wuxing_balance(saju_data)
        strength = self._get_strength_level(saju_data)

        gilsin = []   # 길신
        hyungsin = [] # 흉신

        # 간단한 신살 판단 로직
        # 실제로는 더 복잡한 천간지지 조합으로 판단

        # 귀인 판단 (예시: 오행 균형이 좋으면 천을귀인)
        balance_variance = sum((v - 0.2) ** 2 for v in balance.values())
        if balance_variance < 0.02:
            gilsin.append("천을귀인")

        # 문창 판단 (예시: 목/수 오행이 적당하면)
        if 0.15 < balance.get(WuXing.WOOD, 0) < 0.3:
            gilsin.append("문창귀인")

        if 0.15 < balance.get(WuXing.WATER, 0) < 0.3:
            gilsin.append("태극귀인")

        # 화개 판단 (예시: 화 오행이 있으면)
        if balance.get(WuXing.FIRE, 0) > 0.15:
            gilsin.append("화개")

        # 역마 판단 (예시: 수 오행이 강하면)
        if balance.get(WuXing.WATER, 0) > 0.25:
            gilsin.append("역마")

        # 도화 판단 (예시: 화 오행이 강하면)
        if balance.get(WuXing.FIRE, 0) > 0.25:
            gilsin.append("도화")

        # 양인 판단 (예시: 금 오행이 매우 강하면)
        if balance.get(WuXing.METAL, 0) > 0.3:
            hyungsin.append("양인")

        # 겁살 판단 (예시: 일간이 약하고 재성이 강하면)
        if strength in ["weak", "very_weak"]:
            day_element = self._get_day_stem_element(saju_data)
            wealth_element = get_ke_element(day_element)
            if balance.get(wealth_element, 0) > 0.25:
                hyungsin.append("겁살")

        # 백호 판단 (예시: 금/화 충돌)
        if (balance.get(WuXing.METAL, 0) > 0.2 and
            balance.get(WuXing.FIRE, 0) > 0.2):
            hyungsin.append("백호")

        # 공망 판단 (예시: 어떤 오행이 0이면)
        for elem, ratio in balance.items():
            if ratio < 0.05:
                hyungsin.append("공망")
                break

        return {
            "gilsin": gilsin[:4],
            "hyungsin": hyungsin[:3],
        }

    def determine_yong_sin(self, saju_data: Dict[str, Any]) -> WuXing:
        """
        신살중심 방식의 용신 결정
        흉신을 제어하고 길신을 강화하는 오행
        """
        day_element = self._get_day_stem_element(saju_data)
        balance = self._get_wuxing_balance(saju_data)
        shensha = self._analyze_shensha(saju_data)

        # 흉신이 많으면 제어하는 오행
        if len(shensha.get("hyungsin", [])) >= 2:
            # 가장 강한 오행을 제어
            strongest = max(balance, key=balance.get)
            return get_ke_me_element(strongest)

        # 길신을 강화하는 오행
        if "문창귀인" in shensha.get("gilsin", []):
            return WuXing.WOOD  # 목으로 학문 강화

        if "역마" in shensha.get("gilsin", []):
            return WuXing.WATER  # 수로 이동운 강화

        # 기본: 일간을 돕는 오행
        return get_sheng_me_element(day_element)

    def interpret_health(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석 - 신살중심 관점"""
        shensha = self._analyze_shensha(saju_data)
        hyungsin = shensha.get("hyungsin", [])
        gilsin = shensha.get("gilsin", [])

        health_text = "신살중심에서는 흉살의 영향으로 건강을 봅니다. "

        # 흉살 관련 건강 주의
        if "양인" in hyungsin:
            health_text += "양인이 있어 날카로운 것에 의한 부상에 주의하세요. "
        if "백호" in hyungsin:
            health_text += "백호살이 있어 수술이나 사고에 주의가 필요합니다. "

        # 길신 관련 건강
        if "천을귀인" in gilsin:
            health_text += "천을귀인이 있어 위기 시 도움을 받습니다. "
        if "화개" in gilsin:
            health_text += "화개가 있어 정신적 수양이 건강에 도움됩니다. "

        if not hyungsin:
            health_text += "특별한 흉살이 없어 건강운이 안정적입니다. "

        health_text += f"{yong_sin.value} 오행으로 균형을 맞추세요."

        return health_text

    def interpret_wealth(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석 - 신살중심 관점"""
        shensha = self._analyze_shensha(saju_data)
        hyungsin = shensha.get("hyungsin", [])
        gilsin = shensha.get("gilsin", [])

        wealth_text = "신살중심에서 재물운은 길신과 흉신의 작용입니다. "

        # 길신 관련 재물
        if "천을귀인" in gilsin:
            wealth_text += "천을귀인으로 귀인의 도움으로 재물을 얻습니다. "
        if "식신" in gilsin:
            wealth_text += "식신이 있어 재능으로 수입이 생깁니다. "

        # 흉신 관련 재물 주의
        if "겁살" in hyungsin:
            wealth_text += "겁살이 있어 재물 손실에 주의하세요. "
        if "공망" in hyungsin:
            wealth_text += "공망이 있어 투자 시 신중해야 합니다. "

        if "역마" in gilsin:
            wealth_text += "역마가 있어 이동이나 해외에서 재물 기회가 있습니다. "

        return wealth_text

    def interpret_career(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석 - 신살중심 관점"""
        shensha = self._analyze_shensha(saju_data)
        gilsin = shensha.get("gilsin", [])

        career_text = "신살중심에서 직업은 길신의 특성으로 봅니다. "

        # 길신별 직업 추천
        if "문창귀인" in gilsin:
            career_text += "문창귀인으로 교육, 문서, 시험 관련 직업이 좋습니다. "
        if "역마" in gilsin:
            career_text += "역마로 무역, 여행, 운송 관련 직업이 적합합니다. "
        if "화개" in gilsin:
            career_text += "화개로 예술, 종교, 철학 분야가 어울립니다. "
        if "도화" in gilsin:
            career_text += "도화로 연예, 미용, 서비스업이 적합합니다. "
        if "천을귀인" in gilsin:
            career_text += "천을귀인으로 상담, 중개, 사회사업이 좋습니다. "

        if not gilsin:
            career_text += "특별한 길신이 없어 성실함으로 승부하세요. "

        return career_text

    def interpret_relationship(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석 - 신살중심 관점"""
        shensha = self._analyze_shensha(saju_data)
        gilsin = shensha.get("gilsin", [])
        hyungsin = shensha.get("hyungsin", [])

        rel_text = "신살중심에서 인간관계는 귀인과 살의 작용입니다. "

        # 귀인 관련
        if "천을귀인" in gilsin:
            rel_text += "천을귀인이 있어 좋은 사람들이 주변에 모입니다. "
        if "천덕귀인" in gilsin:
            rel_text += "천덕귀인으로 덕망이 있어 존경받습니다. "

        # 도화 관련
        if "도화" in gilsin:
            rel_text += "도화가 있어 이성에게 매력적이지만, 과도함에 주의하세요. "

        # 흉신 관련
        if "양인" in hyungsin:
            rel_text += "양인이 있어 관계에서 날카로움을 조절하세요. "

        return rel_text

    def interpret_fame(self, saju_data: Dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석 - 신살중심 관점"""
        shensha = self._analyze_shensha(saju_data)
        gilsin = shensha.get("gilsin", [])

        fame_text = "신살중심에서 명예는 길신의 힘입니다. "

        if "천덕귀인" in gilsin:
            fame_text += "천덕귀인으로 사회적 존경을 받습니다. "
        if "문창귀인" in gilsin:
            fame_text += "문창귀인으로 학문이나 시험에서 명예를 얻습니다. "
        if "태극귀인" in gilsin:
            fame_text += "태극귀인으로 근본이 튼튼하여 오래가는 명성을 얻습니다. "

        if not any(g in gilsin for g in ["천덕귀인", "문창귀인", "태극귀인"]):
            fame_text += "명예 관련 길신이 약하니 실력으로 쌓아가세요. "

        return fame_text

    def calculate_confidence(self, saju_data: Dict[str, Any]) -> float:
        """신뢰도 계산 - 신살중심"""
        base = 0.65  # 신살은 해석이 다양하여 기본 신뢰도가 낮음

        # 사주 정보가 완전할수록 신뢰도 상승
        for pillar in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]:
            if saju_data.get(pillar, {}).get("stem") and saju_data.get(pillar, {}).get("branch"):
                base += 0.05

        return min(0.85, base)

    def extract_key_features(
        self,
        saju_data: Dict[str, Any],
        yong_sin: WuXing
    ) -> List[str]:
        """핵심 특징 추출"""
        shensha = self._analyze_shensha(saju_data)
        gilsin = shensha.get("gilsin", [])
        hyungsin = shensha.get("hyungsin", [])

        features = [
            f"용신: {yong_sin.value}",
            f"길신: {', '.join(gilsin) if gilsin else '없음'}",
            f"흉신: {', '.join(hyungsin) if hyungsin else '없음'}",
            "해석 기준: 신살(神煞) 중심 분석",
        ]

        return features
