"""
운세 분석 모듈
5가지 운세 타입: general, career, wealth, health, love
Reference: fortuneteller/src/lib/fortune.ts
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..yongsin.base import WuXing, get_ke_element, get_sheng_element


class FortuneType(str, Enum):
    """운세 분석 유형"""

    GENERAL = "general"  # 종합운
    CAREER = "career"  # 직업운
    WEALTH = "wealth"  # 재물운
    HEALTH = "health"  # 건강운
    LOVE = "love"  # 애정운


@dataclass
class FortuneDetails:
    """운세 상세 정보"""

    positive: list[str] = field(default_factory=list)  # 긍정적 요소
    negative: list[str] = field(default_factory=list)  # 부정적 요소
    advice: list[str] = field(default_factory=list)  # 조언


@dataclass
class LuckyElements:
    """행운 요소"""

    colors: list[str] = field(default_factory=list)
    numbers: list[int] = field(default_factory=list)
    directions: list[str] = field(default_factory=list)
    times: list[str] = field(default_factory=list)


@dataclass
class FortuneAnalysis:
    """운세 분석 결과"""

    fortune_type: FortuneType
    score: int  # 0-100
    summary: str
    details: FortuneDetails
    lucky_elements: LuckyElements
    period_analysis: dict[str, Any] | None = None


# 오행별 건강 관련 장기
WUXING_ORGANS: dict[WuXing, dict[str, list[str]]] = {
    WuXing.WOOD: {
        "organs": ["간", "담"],
        "weak_symptoms": ["눈 피로", "근육 경련", "화병"],
        "advice": ["녹색 채소 섭취", "산책", "스트레칭"],
    },
    WuXing.FIRE: {
        "organs": ["심장", "소장"],
        "weak_symptoms": ["불면증", "가슴 두근거림", "혀 염증"],
        "advice": ["심호흡", "명상", "쓴맛 음식"],
    },
    WuXing.EARTH: {
        "organs": ["비장", "위"],
        "weak_symptoms": ["소화불량", "식욕 부진", "사지 무력"],
        "advice": ["규칙적 식사", "단맛 적절히", "복부 마사지"],
    },
    WuXing.METAL: {
        "organs": ["폐", "대장"],
        "weak_symptoms": ["호흡기 질환", "피부 트러블", "변비"],
        "advice": ["심호흡 운동", "매운맛 적당히", "보습 관리"],
    },
    WuXing.WATER: {
        "organs": ["신장", "방광"],
        "weak_symptoms": ["허리 통증", "귀 문제", "생식기 문제"],
        "advice": ["충분한 수분", "검은콩", "허리 보호"],
    },
}

# 오행별 직업 적성
WUXING_CAREERS: dict[WuXing, dict[str, Any]] = {
    WuXing.WOOD: {
        "fields": ["교육", "출판", "의류", "목재", "환경", "의료"],
        "traits": ["창의성", "성장 지향", "인내심"],
        "favorable": "새로운 시작과 성장이 필요한 분야",
    },
    WuXing.FIRE: {
        "fields": ["IT", "광고", "방송", "예술", "요리", "에너지"],
        "traits": ["열정", "표현력", "리더십"],
        "favorable": "창의적 표현과 활동적인 분야",
    },
    WuXing.EARTH: {
        "fields": ["부동산", "건설", "농업", "컨설팅", "중개", "물류"],
        "traits": ["안정성", "신뢰성", "중재력"],
        "favorable": "신뢰와 안정이 중요한 분야",
    },
    WuXing.METAL: {
        "fields": ["금융", "법률", "회계", "기계", "자동차", "정밀산업"],
        "traits": ["분석력", "결단력", "정확성"],
        "favorable": "정밀함과 판단력이 요구되는 분야",
    },
    WuXing.WATER: {
        "fields": ["무역", "유통", "연구", "IT", "의료", "서비스"],
        "traits": ["유연성", "지혜", "소통능력"],
        "favorable": "변화와 소통이 중요한 분야",
    },
}

# 오행별 애정운 특성
WUXING_LOVE: dict[WuXing, dict[str, Any]] = {
    WuXing.WOOD: {
        "style": "성장하는 사랑",
        "traits": ["함께 발전", "지적 교감", "자유로운 관계"],
        "compatible": [WuXing.WATER, WuXing.FIRE],
        "challenges": [WuXing.METAL],
    },
    WuXing.FIRE: {
        "style": "열정적인 사랑",
        "traits": ["적극적 표현", "로맨틱", "드라마틱"],
        "compatible": [WuXing.WOOD, WuXing.EARTH],
        "challenges": [WuXing.WATER],
    },
    WuXing.EARTH: {
        "style": "안정적인 사랑",
        "traits": ["헌신적", "가정적", "믿음직한"],
        "compatible": [WuXing.FIRE, WuXing.METAL],
        "challenges": [WuXing.WOOD],
    },
    WuXing.METAL: {
        "style": "의리있는 사랑",
        "traits": ["책임감", "보호 본능", "일관성"],
        "compatible": [WuXing.EARTH, WuXing.WATER],
        "challenges": [WuXing.FIRE],
    },
    WuXing.WATER: {
        "style": "유연한 사랑",
        "traits": ["포용력", "감성적", "적응력"],
        "compatible": [WuXing.METAL, WuXing.WOOD],
        "challenges": [WuXing.EARTH],
    },
}

# 오행별 재물운 특성
WUXING_WEALTH: dict[WuXing, dict[str, Any]] = {
    WuXing.WOOD: {
        "style": "성장형 재물",
        "traits": ["장기 투자", "교육 투자", "점진적 축적"],
        "favorable_times": ["봄", "아침"],
        "advice": ["급하게 굴지 말 것", "씨앗을 뿌리는 마음으로"],
    },
    WuXing.FIRE: {
        "style": "활동형 재물",
        "traits": ["적극적 투자", "사업 확장", "인맥 활용"],
        "favorable_times": ["여름", "낮"],
        "advice": ["충동 투자 주의", "열정을 수익으로"],
    },
    WuXing.EARTH: {
        "style": "축적형 재물",
        "traits": ["부동산", "안정 자산", "꾸준한 저축"],
        "favorable_times": ["환절기", "토요일"],
        "advice": ["욕심 부리지 말 것", "땅과 관련된 것에 행운"],
    },
    WuXing.METAL: {
        "style": "관리형 재물",
        "traits": ["금융 투자", "체계적 관리", "절약"],
        "favorable_times": ["가을", "저녁"],
        "advice": ["분석 후 투자", "금속/귀금속에 인연"],
    },
    WuXing.WATER: {
        "style": "유동형 재물",
        "traits": ["무역", "유통", "다양한 수입원"],
        "favorable_times": ["겨울", "밤"],
        "advice": ["흐름을 타라", "물과 관련된 사업 유리"],
    },
}

# 오행별 색상
WUXING_COLORS: dict[WuXing, list[str]] = {
    WuXing.WOOD: ["초록", "청록", "연두"],
    WuXing.FIRE: ["빨강", "주황", "보라"],
    WuXing.EARTH: ["노랑", "갈색", "베이지"],
    WuXing.METAL: ["흰색", "금색", "은색"],
    WuXing.WATER: ["검정", "남색", "파랑"],
}

# 오행별 방향
WUXING_DIRECTIONS: dict[WuXing, list[str]] = {
    WuXing.WOOD: ["동쪽"],
    WuXing.FIRE: ["남쪽"],
    WuXing.EARTH: ["중앙", "남서", "북동"],
    WuXing.METAL: ["서쪽"],
    WuXing.WATER: ["북쪽"],
}

# 오행별 숫자
WUXING_NUMBERS: dict[WuXing, list[int]] = {
    WuXing.WOOD: [3, 8],
    WuXing.FIRE: [2, 7],
    WuXing.EARTH: [5, 10],
    WuXing.METAL: [4, 9],
    WuXing.WATER: [1, 6],
}

# 오행별 시간
WUXING_TIMES: dict[WuXing, list[str]] = {
    WuXing.WOOD: ["05:00-09:00", "인시", "묘시"],
    WuXing.FIRE: ["09:00-13:00", "사시", "오시"],
    WuXing.EARTH: ["07:00-09:00", "13:00-15:00", "19:00-21:00", "01:00-03:00"],
    WuXing.METAL: ["15:00-19:00", "신시", "유시"],
    WuXing.WATER: ["21:00-01:00", "해시", "자시"],
}


class FortuneAnalyzer:
    """운세 분석기"""

    def __init__(self, saju_data: dict[str, Any]):
        """
        Args:
            saju_data: 사주 데이터 (만세력 계산 결과)
        """
        self.saju_data = saju_data
        self.day_stem_element = self._get_day_stem_element()
        self.wuxing_balance = self._analyze_wuxing_balance()

    def _get_day_stem_element(self) -> WuXing:
        """일간의 오행 추출"""
        day_pillar = self.saju_data.get("day_pillar", {})
        stem_element = day_pillar.get("stem_element", "목")
        return WuXing(stem_element)

    def _analyze_wuxing_balance(self) -> dict[WuXing, float]:
        """오행 균형 분석"""
        wuxing_count = self.saju_data.get("wuxing_count", {})
        total = sum(wuxing_count.values()) or 1

        balance = {}
        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            balance[element] = count / total

        return balance

    def _get_strength_level(self) -> str:
        """일간 강약 수준"""
        strength_info = self.saju_data.get("day_master_strength", {})
        return strength_info.get("level", "medium")

    def analyze(self, fortune_type: FortuneType) -> FortuneAnalysis:
        """
        지정된 유형의 운세 분석

        Args:
            fortune_type: 분석할 운세 유형

        Returns:
            운세 분석 결과
        """
        if fortune_type == FortuneType.GENERAL:
            return self._analyze_general()
        elif fortune_type == FortuneType.CAREER:
            return self._analyze_career()
        elif fortune_type == FortuneType.WEALTH:
            return self._analyze_wealth()
        elif fortune_type == FortuneType.HEALTH:
            return self._analyze_health()
        elif fortune_type == FortuneType.LOVE:
            return self._analyze_love()
        else:
            raise ValueError(f"Unknown fortune type: {fortune_type}")

    def _calculate_base_score(self) -> int:
        """기본 점수 계산 (오행 균형 기반)"""
        # 균형이 잡힐수록 높은 점수
        balance_values = list(self.wuxing_balance.values())
        ideal = 0.2  # 5개 오행이 균등하면 각 0.2

        variance = sum((v - ideal) ** 2 for v in balance_values)
        # 분산이 0이면 100점, 분산이 클수록 낮은 점수
        score = max(50, int(100 - variance * 500))
        return min(100, score)

    def _get_lucky_elements(self, primary_element: WuXing) -> LuckyElements:
        """행운 요소 생성"""
        supporting_element = get_sheng_element(primary_element)

        colors = WUXING_COLORS.get(primary_element, [])[:2]
        colors.extend(WUXING_COLORS.get(supporting_element, [])[:1])

        numbers = WUXING_NUMBERS.get(primary_element, [])
        directions = WUXING_DIRECTIONS.get(primary_element, [])
        times = WUXING_TIMES.get(primary_element, [])[:2]

        return LuckyElements(
            colors=colors,
            numbers=numbers,
            directions=directions,
            times=times,
        )

    def _analyze_general(self) -> FortuneAnalysis:
        """종합운 분석"""
        strength = self._get_strength_level()
        base_score = self._calculate_base_score()

        positive = []
        negative = []
        advice = []

        # 오행 균형 분석
        strong_elements = [e for e, v in self.wuxing_balance.items() if v > 0.25]
        weak_elements = [e for e, v in self.wuxing_balance.items() if v < 0.15]

        for elem in strong_elements:
            positive.append(
                f"{elem.value} 기운이 강하여 {WUXING_CAREERS[elem]['traits'][0]}이 돋보입니다"
            )

        for elem in weak_elements:
            negative.append(f"{elem.value} 기운이 약하여 보완이 필요합니다")
            advice.append(f"{elem.value} 관련 활동으로 균형을 맞추세요")

        # 일간 강약 기반 조언
        if strength in ["very_strong", "strong"]:
            positive.append("일간이 강하여 추진력과 자신감이 있습니다")
            advice.append("에너지를 적절히 분산시키세요")
        elif strength in ["weak", "very_weak"]:
            negative.append("일간이 약하여 외부 도움이 필요할 수 있습니다")
            advice.append("자신을 돕는 사람들과 함께하세요")
        else:
            positive.append("일간이 중화되어 균형 잡힌 성향입니다")

        summary = self._generate_general_summary(strength, base_score)

        return FortuneAnalysis(
            fortune_type=FortuneType.GENERAL,
            score=base_score,
            summary=summary,
            details=FortuneDetails(
                positive=positive[:4],
                negative=negative[:3],
                advice=advice[:4],
            ),
            lucky_elements=self._get_lucky_elements(self.day_stem_element),
        )

    def _generate_general_summary(self, strength: str, score: int) -> str:
        """종합운 요약 생성"""
        if score >= 80:
            quality = "매우 좋은"
        elif score >= 60:
            quality = "양호한"
        elif score >= 40:
            quality = "보통의"
        else:
            quality = "주의가 필요한"

        return (
            f"{quality} 기운을 가진 사주입니다. "
            f"일간({self.day_stem_element.value})이 {self._strength_text(strength)} "
            f"오행의 균형을 고려하여 생활하면 운세 개선에 도움이 됩니다."
        )

    def _strength_text(self, strength: str) -> str:
        """강약 텍스트"""
        texts = {
            "very_strong": "매우 강하여",
            "strong": "강하여",
            "medium": "중화되어",
            "weak": "약하여",
            "very_weak": "매우 약하여",
        }
        return texts.get(strength, "")

    def _analyze_career(self) -> FortuneAnalysis:
        """직업운 분석"""
        career_info = WUXING_CAREERS.get(self.day_stem_element, {})
        base_score = self._calculate_base_score()

        # 직업 적성 조정
        strength = self._get_strength_level()
        if strength in ["strong", "very_strong"]:
            base_score = min(100, base_score + 10)
        elif strength in ["weak", "very_weak"]:
            base_score = max(0, base_score - 5)

        fields = career_info.get("fields", [])
        traits = career_info.get("traits", [])

        positive = [
            f"적합한 분야: {', '.join(fields[:4])}",
            f"강점: {', '.join(traits)}",
            career_info.get("favorable", ""),
        ]

        # 상생 오행의 직업도 추천
        supporting_element = get_sheng_element(self.day_stem_element)
        supporting_careers = WUXING_CAREERS.get(supporting_element, {})
        if supporting_careers:
            positive.append(f"보조 적성: {', '.join(supporting_careers.get('fields', [])[:2])}")

        negative = []
        advice = []

        # 상극 오행 주의
        conflicting_element = get_ke_element(self.day_stem_element)
        conflicting_careers = WUXING_CAREERS.get(conflicting_element, {})
        if conflicting_careers:
            negative.append(f"주의 분야: {', '.join(conflicting_careers.get('fields', [])[:2])}")
            advice.append("해당 분야 진출 시 충분한 준비가 필요합니다")

        advice.extend(
            [
                "자신의 강점을 살리는 분야에서 성공 가능성이 높습니다",
                "협력자의 오행도 고려하면 시너지를 낼 수 있습니다",
            ]
        )

        summary = (
            f"일간 {self.day_stem_element.value}의 특성상 "
            f"{', '.join(fields[:2])} 분야에서 능력을 발휘할 수 있습니다. "
            f"{', '.join(traits[:2])}을 활용하세요."
        )

        return FortuneAnalysis(
            fortune_type=FortuneType.CAREER,
            score=base_score,
            summary=summary,
            details=FortuneDetails(
                positive=[p for p in positive if p][:4],
                negative=negative[:3],
                advice=advice[:4],
            ),
            lucky_elements=self._get_lucky_elements(self.day_stem_element),
        )

    def _analyze_wealth(self) -> FortuneAnalysis:
        """재물운 분석"""
        wealth_info = WUXING_WEALTH.get(self.day_stem_element, {})
        base_score = self._calculate_base_score()

        # 재성(일간이 극하는 오행) 분석
        wealth_element = get_ke_element(self.day_stem_element)
        wealth_balance = self.wuxing_balance.get(wealth_element, 0)

        if wealth_balance > 0.2:
            base_score = min(100, base_score + 15)
        elif wealth_balance < 0.1:
            base_score = max(0, base_score - 10)

        style = wealth_info.get("style", "")
        traits = wealth_info.get("traits", [])
        favorable_times = wealth_info.get("favorable_times", [])
        wealth_advice = wealth_info.get("advice", [])

        positive = [
            f"재물 성향: {style}",
            f"유리한 방식: {', '.join(traits[:2])}",
        ]

        if wealth_balance > 0.2:
            positive.append("재성이 강하여 재물 운이 좋습니다")

        negative = []
        if wealth_balance < 0.1:
            negative.append("재성이 약하여 재물 축적에 노력이 필요합니다")

        advice = list(wealth_advice[:2])
        if favorable_times:
            advice.append(f"유리한 시기: {', '.join(favorable_times)}")

        summary = (
            f"{style}의 특성을 가지고 있습니다. "
            f"{', '.join(traits[:2])}이 재물 축적에 도움이 됩니다."
        )

        return FortuneAnalysis(
            fortune_type=FortuneType.WEALTH,
            score=base_score,
            summary=summary,
            details=FortuneDetails(
                positive=positive[:4],
                negative=negative[:3],
                advice=advice[:4],
            ),
            lucky_elements=self._get_lucky_elements(wealth_element),
        )

    def _analyze_health(self) -> FortuneAnalysis:
        """건강운 분석"""
        base_score = self._calculate_base_score()

        positive = []
        negative = []
        advice = []

        # 각 오행별 건강 분석
        for element, balance in self.wuxing_balance.items():
            organ_info = WUXING_ORGANS.get(element, {})
            organs = organ_info.get("organs", [])

            if balance > 0.3:
                # 과다 - 주의 필요
                negative.append(f"{element.value} 과다: {', '.join(organs)} 관련 주의")
            elif balance < 0.1:
                # 부족 - 보강 필요
                symptoms = organ_info.get("weak_symptoms", [])
                negative.append(f"{element.value} 부족: {', '.join(symptoms[:2])} 주의")
                organ_advice = organ_info.get("advice", [])
                advice.extend(organ_advice[:1])
            else:
                if organs:
                    positive.append(f"{element.value} 균형: {', '.join(organs)} 건강")

        # 일간 기준 주요 건강 조언
        main_organ_info = WUXING_ORGANS.get(self.day_stem_element, {})
        main_organs = main_organ_info.get("organs", [])
        main_advice = main_organ_info.get("advice", [])

        if main_organs:
            positive.insert(0, f"주요 관리 장기: {', '.join(main_organs)}")
        advice.extend(main_advice[:2])

        summary = (
            f"일간 {self.day_stem_element.value} 기준으로 "
            f"{', '.join(main_organs)}의 관리가 중요합니다. "
            f"오행 균형을 통해 전반적인 건강을 유지하세요."
        )

        return FortuneAnalysis(
            fortune_type=FortuneType.HEALTH,
            score=base_score,
            summary=summary,
            details=FortuneDetails(
                positive=positive[:4],
                negative=negative[:4],
                advice=advice[:5],
            ),
            lucky_elements=self._get_lucky_elements(self.day_stem_element),
        )

    def _analyze_love(self) -> FortuneAnalysis:
        """애정운 분석"""
        love_info = WUXING_LOVE.get(self.day_stem_element, {})
        base_score = self._calculate_base_score()

        style = love_info.get("style", "")
        traits = love_info.get("traits", [])
        compatible = love_info.get("compatible", [])
        challenges = love_info.get("challenges", [])

        positive = [
            f"연애 스타일: {style}",
            f"매력 포인트: {', '.join(traits[:2])}",
        ]

        if compatible:
            compatible_names = [e.value for e in compatible]
            positive.append(f"궁합이 좋은 오행: {', '.join(compatible_names)}")

        negative = []
        if challenges:
            challenge_names = [e.value for e in challenges]
            negative.append(f"주의할 오행: {', '.join(challenge_names)}")
            negative.append("해당 오행의 상대와는 서로 이해하려는 노력이 필요합니다")

        advice = [
            f"당신의 {style} 특성을 이해해주는 사람이 좋은 인연입니다",
            f"{', '.join(traits[:2])}을 장점으로 어필하세요",
        ]

        if compatible:
            advice.append(f"{compatible_names[0]} 오행의 상대와 좋은 케미를 기대할 수 있습니다")

        summary = (
            f"당신은 {style}을 추구합니다. "
            f"{', '.join(traits[:2])}이 연애에서 강점입니다. "
            f"상대방의 오행을 고려하면 더 좋은 관계를 만들 수 있습니다."
        )

        return FortuneAnalysis(
            fortune_type=FortuneType.LOVE,
            score=base_score,
            summary=summary,
            details=FortuneDetails(
                positive=positive[:4],
                negative=negative[:3],
                advice=advice[:4],
            ),
            lucky_elements=self._get_lucky_elements(self.day_stem_element),
        )

    def analyze_all(self) -> dict[FortuneType, FortuneAnalysis]:
        """모든 유형의 운세 분석"""
        return {fortune_type: self.analyze(fortune_type) for fortune_type in FortuneType}


def analyze_fortune(saju_data: dict[str, Any], fortune_type: str = "general") -> FortuneAnalysis:
    """
    운세 분석 편의 함수

    Args:
        saju_data: 사주 데이터
        fortune_type: 운세 유형 (general/career/wealth/health/love)

    Returns:
        운세 분석 결과
    """
    analyzer = FortuneAnalyzer(saju_data)
    ft = FortuneType(fortune_type)
    return analyzer.analyze(ft)


def analyze_all_fortunes(saju_data: dict[str, Any]) -> dict[str, FortuneAnalysis]:
    """
    모든 운세 분석 편의 함수

    Args:
        saju_data: 사주 데이터

    Returns:
        모든 운세 분석 결과
    """
    analyzer = FortuneAnalyzer(saju_data)
    results = analyzer.analyze_all()
    return {ft.value: analysis for ft, analysis in results.items()}
