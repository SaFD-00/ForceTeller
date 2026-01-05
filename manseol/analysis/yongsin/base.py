"""
용신(用神) 분석 기본 인터페이스 및 오행 관계 유틸리티
Reference: fortuneteller/src/lib/yong_sin.ts, fortuneteller/src/lib/yongsin/base.ts
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod


class WuXing(str, Enum):
    """오행(五行)"""
    WOOD = "목"
    FIRE = "화"
    EARTH = "토"
    METAL = "금"
    WATER = "수"


class YongSinMethod(str, Enum):
    """용신 선정 방법론"""
    STRENGTH = "strength"      # 강약용신: 일간 강약 기준
    SEASONAL = "seasonal"      # 조후용신: 계절 한난조습 조절
    MEDIATION = "mediation"    # 통관용신: 충돌 오행 중재
    DISEASE = "disease"        # 병약용신: 사주 불균형 진단 및 치료


class DayMasterStrength(str, Enum):
    """일간 강약 레벨"""
    VERY_STRONG = "very_strong"  # 매우 강함
    STRONG = "strong"            # 강함
    MEDIUM = "medium"            # 중화 (이상적 균형)
    WEAK = "weak"                # 약함
    VERY_WEAK = "very_weak"      # 매우 약함


@dataclass
class YongSinRecommendations:
    """용신 기반 추천 정보"""
    colors: List[str] = field(default_factory=list)      # 길한 색상
    directions: List[str] = field(default_factory=list)  # 유리한 방향
    careers: List[str] = field(default_factory=list)     # 적합한 직업
    activities: List[str] = field(default_factory=list)  # 권장 활동
    cautions: List[str] = field(default_factory=list)    # 주의사항


@dataclass
class YongSinResult:
    """용신 분석 결과"""
    primary_yongsin: WuXing                          # 주 용신
    secondary_yongsin: Optional[WuXing] = None       # 보조 용신 (희신의 일부)
    xi_sin: List[WuXing] = field(default_factory=list)   # 희신(喜神) - 용신을 돕는 오행
    ji_sin: List[WuXing] = field(default_factory=list)   # 기신(忌神) - 피해야 할 오행
    chou_sin: List[WuXing] = field(default_factory=list) # 수신(仇神) - 용신을 극하는 오행
    day_master_strength: DayMasterStrength = DayMasterStrength.MEDIUM
    reasoning: str = ""                               # 용신 선정 이유
    method: YongSinMethod = YongSinMethod.STRENGTH    # 사용된 방법론
    confidence: float = 0.8                           # 신뢰도 (0.0~1.0)
    recommendations: YongSinRecommendations = field(default_factory=YongSinRecommendations)

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "primary_yongsin": self.primary_yongsin.value,
            "secondary_yongsin": self.secondary_yongsin.value if self.secondary_yongsin else None,
            "xi_sin": [x.value for x in self.xi_sin],
            "ji_sin": [x.value for x in self.ji_sin],
            "chou_sin": [x.value for x in self.chou_sin],
            "day_master_strength": self.day_master_strength.value,
            "reasoning": self.reasoning,
            "method": self.method.value,
            "confidence": self.confidence,
            "recommendations": {
                "colors": self.recommendations.colors,
                "directions": self.recommendations.directions,
                "careers": self.recommendations.careers,
                "activities": self.recommendations.activities,
                "cautions": self.recommendations.cautions,
            }
        }


# ============================================================================
# 오행 상생상극 관계 유틸리티
# ============================================================================

# 오행 상생 관계: A가 B를 생(生)함
# 목생화, 화생토, 토생금, 금생수, 수생목
SHENG_MAP: Dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.FIRE,    # 목생화
    WuXing.FIRE: WuXing.EARTH,   # 화생토
    WuXing.EARTH: WuXing.METAL,  # 토생금
    WuXing.METAL: WuXing.WATER,  # 금생수
    WuXing.WATER: WuXing.WOOD,   # 수생목
}

# 나를 생(生)하는 오행
SHENG_ME_MAP: Dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.WATER,   # 수생목
    WuXing.FIRE: WuXing.WOOD,    # 목생화
    WuXing.EARTH: WuXing.FIRE,   # 화생토
    WuXing.METAL: WuXing.EARTH,  # 토생금
    WuXing.WATER: WuXing.METAL,  # 금생수
}

# 오행 상극 관계: A가 B를 극(克)함
# 목극토, 토극수, 수극화, 화극금, 금극목
KE_MAP: Dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.EARTH,   # 목극토
    WuXing.FIRE: WuXing.METAL,   # 화극금
    WuXing.EARTH: WuXing.WATER,  # 토극수
    WuXing.METAL: WuXing.WOOD,   # 금극목
    WuXing.WATER: WuXing.FIRE,   # 수극화
}

# 나를 극(克)하는 오행
KE_ME_MAP: Dict[WuXing, WuXing] = {
    WuXing.WOOD: WuXing.METAL,   # 금극목
    WuXing.FIRE: WuXing.WATER,   # 수극화
    WuXing.EARTH: WuXing.WOOD,   # 목극토
    WuXing.METAL: WuXing.FIRE,   # 화극금
    WuXing.WATER: WuXing.EARTH,  # 토극수
}


def get_sheng_element(element: WuXing) -> WuXing:
    """내가 생(生)하는 오행 반환 (설기)"""
    return SHENG_MAP[element]


def get_sheng_me_element(element: WuXing) -> WuXing:
    """나를 생(生)하는 오행 반환 (인성)"""
    return SHENG_ME_MAP[element]


def get_ke_element(element: WuXing) -> WuXing:
    """내가 극(克)하는 오행 반환 (재성)"""
    return KE_MAP[element]


def get_ke_me_element(element: WuXing) -> WuXing:
    """나를 극(克)하는 오행 반환 (관성)"""
    return KE_ME_MAP[element]


def get_weakening_element(element: WuXing) -> WuXing:
    """나의 기운을 설(洩)하는 오행 반환 (식상)"""
    return get_sheng_element(element)


# ============================================================================
# 오행별 속성 (색상, 방위, 직업, 활동)
# ============================================================================

WUXING_ATTRIBUTES: Dict[WuXing, Dict[str, List[str]]] = {
    WuXing.WOOD: {
        "colors": ["초록색", "청록색", "연두색"],
        "directions": ["동쪽"],
        "careers": ["교육", "출판", "섬유", "목재", "종이", "인쇄", "꽃/식물 사업", "환경", "의류"],
        "activities": ["산책", "등산", "원예", "독서", "글쓰기", "학습", "요가"],
    },
    WuXing.FIRE: {
        "colors": ["빨간색", "주황색", "보라색", "분홍색"],
        "directions": ["남쪽"],
        "careers": ["요리", "전기", "광고", "방송", "예술", "연예", "IT", "교육", "에너지", "조명"],
        "activities": ["운동", "사교 활동", "공연 관람", "창작 활동", "여행", "봉사"],
    },
    WuXing.EARTH: {
        "colors": ["노란색", "갈색", "황토색", "베이지"],
        "directions": ["중앙", "남서", "북동"],
        "careers": ["건설", "부동산", "농업", "도자기", "중개", "물류", "보관", "컨설팅", "요식업"],
        "activities": ["명상", "요가", "전통 문화", "농사", "부동산 투자", "중재", "정리정돈"],
    },
    WuXing.METAL: {
        "colors": ["흰색", "금색", "은색", "회색"],
        "directions": ["서쪽"],
        "careers": ["금융", "은행", "회계", "법조", "금속", "기계", "자동차", "정밀 산업", "보석"],
        "activities": ["금융 투자", "골프", "등산", "정리 정돈", "법률 공부", "계획 수립"],
    },
    WuXing.WATER: {
        "colors": ["검은색", "남색", "파란색"],
        "directions": ["북쪽"],
        "careers": ["물류", "유통", "무역", "수산", "음료", "화학", "연구", "의료", "정보통신", "해운"],
        "activities": ["수영", "낚시", "여행", "연구", "학습", "명상", "휴식"],
    },
}


def get_wuxing_attributes(element: WuXing) -> Dict[str, List[str]]:
    """오행별 속성 반환"""
    return WUXING_ATTRIBUTES.get(element, {})


# ============================================================================
# 용신 알고리즘 추상 베이스 클래스
# ============================================================================

class YongSinAlgorithm(ABC):
    """용신 선정 알고리즘 추상 베이스 클래스"""

    @property
    @abstractmethod
    def name(self) -> str:
        """알고리즘 이름"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """알고리즘 설명"""
        pass

    @abstractmethod
    def select(self, saju_data: Dict[str, Any]) -> YongSinResult:
        """용신 선정"""
        pass

    @abstractmethod
    def calculate_applicability(self, saju_data: Dict[str, Any]) -> float:
        """
        이 알고리즘의 적용 적합도 계산 (0.0 ~ 1.0)
        사주 특성에 따라 적합한 알고리즘이 다름
        """
        pass


# ============================================================================
# 유틸리티 함수
# ============================================================================

def find_weakest_element(wuxing_count: Dict[str, int]) -> WuXing:
    """가장 약한 오행 찾기"""
    min_element = WuXing.WOOD
    min_count = float('inf')

    for element in WuXing:
        count = wuxing_count.get(element.value, 0)
        if count < min_count:
            min_count = count
            min_element = element

    return min_element


def find_strongest_element(wuxing_count: Dict[str, int]) -> WuXing:
    """가장 강한 오행 찾기"""
    max_element = WuXing.WOOD
    max_count = 0

    for element in WuXing:
        count = wuxing_count.get(element.value, 0)
        if count > max_count:
            max_count = count
            max_element = element

    return max_element


def get_day_master_strength_from_score(score: int) -> DayMasterStrength:
    """점수로부터 일간 강약 레벨 반환"""
    if score >= 80:
        return DayMasterStrength.VERY_STRONG
    elif score >= 60:
        return DayMasterStrength.STRONG
    elif score >= 40:
        return DayMasterStrength.MEDIUM
    elif score >= 20:
        return DayMasterStrength.WEAK
    else:
        return DayMasterStrength.VERY_WEAK


def str_to_wuxing(element_str: str) -> Optional[WuXing]:
    """문자열을 WuXing enum으로 변환"""
    for element in WuXing:
        if element.value == element_str:
            return element
    return None
