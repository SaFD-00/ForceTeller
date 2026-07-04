"""
유파별 해석기 기본 인터페이스 및 추상 클래스
Reference: fortuneteller/src/lib/school_interpreter.ts
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..yongsin.base import WuXing


class SchoolCode(str, Enum):
    """유파 코드"""

    ZIPING = "ziping"  # 자평명리
    DTS = "dts"  # 적천수
    QTBJ = "qtbj"  # 궁통보감
    MODERN = "modern"  # 현대명리
    SHENSHA = "shensha"  # 신살중심


SCHOOL_NAMES: dict[SchoolCode, str] = {
    SchoolCode.ZIPING: "자평명리",
    SchoolCode.DTS: "적천수",
    SchoolCode.QTBJ: "궁통보감",
    SchoolCode.MODERN: "현대명리",
    SchoolCode.SHENSHA: "신살중심",
}

SCHOOL_DESCRIPTIONS: dict[SchoolCode, str] = {
    SchoolCode.ZIPING: "송나라 서자평이 정립한 전통 명리학의 기초. 일간 중심의 강약 분석과 격국론을 중시합니다.",
    SchoolCode.DTS: "청나라 임철초의 저서로, 오행의 생극제화와 통변성정을 깊이 다룹니다.",
    SchoolCode.QTBJ: "명나라 여춘태의 저서로, 월령과 조후(調候)를 중시하는 계절 중심 해석입니다.",
    SchoolCode.MODERN: "현대 사회에 맞게 재해석한 명리학. 심리학적 관점과 실용적 조언을 결합합니다.",
    SchoolCode.SHENSHA: "신살(神煞)을 중심으로 길흉을 판단하는 전통적 접근법입니다.",
}


@dataclass
class SchoolInterpretation:
    """유파별 해석 결과"""

    school: SchoolCode
    school_name: str
    yong_sin: WuXing  # 용신
    geok_guk: str | None  # 격국 (해당되는 유파만)
    overall: str  # 종합 해석
    health: str  # 건강 해석
    wealth: str  # 재물 해석
    career: str  # 직업 해석
    relationship: str  # 인간관계 해석
    fame: str  # 명예 해석
    daeun_analysis: str  # 대운 분석
    seyun_analysis: str  # 세운 분석
    confidence: float  # 신뢰도 (0.0 ~ 1.0)
    key_features: list[str] = field(default_factory=list)  # 핵심 특징


@dataclass
class ConsensusItem:
    """합의 항목"""

    category: str  # 카테고리 (health, wealth, career, etc.)
    agreement: str  # 합의 내용
    schools: list[SchoolCode]  # 동의하는 유파들


@dataclass
class DifferenceItem:
    """차이점 항목"""

    category: str  # 카테고리
    interpretations: list[dict[str, Any]]  # 각 유파별 해석


@dataclass
class SchoolComparisonResult:
    """유파 비교 결과"""

    schools: list[SchoolCode]
    interpretations: list[SchoolInterpretation]
    consensus: list[ConsensusItem]  # 합의점
    differences: list[DifferenceItem]  # 차이점
    recommendation: str  # 종합 권장


class BaseSchoolInterpreter(ABC):
    """
    유파별 해석기 추상 클래스
    모든 해석 유파는 이 클래스를 상속해야 함
    """

    @property
    @abstractmethod
    def school_code(self) -> SchoolCode:
        """유파 코드"""
        pass

    @property
    def school_name(self) -> str:
        """유파 이름 (한글)"""
        return SCHOOL_NAMES.get(self.school_code, "")

    @property
    def description(self) -> str:
        """유파 설명"""
        return SCHOOL_DESCRIPTIONS.get(self.school_code, "")

    def interpret(self, saju_data: dict[str, Any]) -> SchoolInterpretation:
        """
        사주 해석 수행 (템플릿 메서드)

        Args:
            saju_data: 사주 데이터

        Returns:
            해석 결과
        """
        # 용신 결정
        yong_sin = self.determine_yong_sin(saju_data)

        # 격국 판단 (선택적)
        geok_guk = self.determine_geok_guk(saju_data)

        # 각 영역별 해석
        health = self.interpret_health(saju_data, yong_sin)
        wealth = self.interpret_wealth(saju_data, yong_sin)
        career = self.interpret_career(saju_data, yong_sin)
        relationship = self.interpret_relationship(saju_data, yong_sin)
        fame = self.interpret_fame(saju_data, yong_sin)

        # 종합 해석 생성
        overall = self.generate_overall(saju_data, yong_sin, geok_guk)

        # 대운/세운 해석
        daeun_analysis = self.interpret_daeun(saju_data, yong_sin)
        seyun_analysis = self.interpret_seyun(saju_data, yong_sin)

        # 신뢰도 계산
        confidence = self.calculate_confidence(saju_data)

        # 핵심 특징 추출
        key_features = self.extract_key_features(saju_data, yong_sin)

        return SchoolInterpretation(
            school=self.school_code,
            school_name=self.school_name,
            yong_sin=yong_sin,
            geok_guk=geok_guk,
            overall=overall,
            health=health,
            wealth=wealth,
            career=career,
            relationship=relationship,
            fame=fame,
            daeun_analysis=daeun_analysis,
            seyun_analysis=seyun_analysis,
            confidence=confidence,
            key_features=key_features,
        )

    @abstractmethod
    def determine_yong_sin(self, saju_data: dict[str, Any]) -> WuXing:
        """용신 결정"""
        pass

    def determine_geok_guk(self, saju_data: dict[str, Any]) -> str | None:
        """격국 판단 (선택적, 하위 클래스에서 구현)"""
        return None

    @abstractmethod
    def interpret_health(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """건강 해석"""
        pass

    @abstractmethod
    def interpret_wealth(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """재물 해석"""
        pass

    @abstractmethod
    def interpret_career(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """직업 해석"""
        pass

    @abstractmethod
    def interpret_relationship(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """인간관계 해석"""
        pass

    @abstractmethod
    def interpret_fame(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """명예 해석"""
        pass

    def generate_overall(
        self, saju_data: dict[str, Any], yong_sin: WuXing, geok_guk: str | None
    ) -> str:
        """종합 해석 생성"""
        overall = f"{self.school_name} 관점에서 용신은 {yong_sin.value}입니다."

        if geok_guk:
            overall += f" 격국은 {geok_guk}입니다."

        return overall

    def interpret_daeun(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """대운 해석 (기본 구현)"""
        return f"대운 분석: {yong_sin.value} 용신을 기준으로 대운의 길흉을 판단합니다."

    def interpret_seyun(self, saju_data: dict[str, Any], yong_sin: WuXing) -> str:
        """세운 해석 (기본 구현)"""
        return f"세운 분석: 올해의 운세는 {yong_sin.value}과의 관계에서 판단됩니다."

    def calculate_confidence(self, saju_data: dict[str, Any]) -> float:
        """신뢰도 계산 (기본 구현)"""
        # 기본값: 0.7 (중간 신뢰도)
        return 0.7

    def extract_key_features(self, saju_data: dict[str, Any], yong_sin: WuXing) -> list[str]:
        """핵심 특징 추출"""
        return [
            f"용신: {yong_sin.value}",
            f"해석 유파: {self.school_name}",
        ]

    def _get_day_stem_element(self, saju_data: dict[str, Any]) -> WuXing:
        """일간의 오행 추출"""
        day_pillar = saju_data.get("day_pillar", {})
        stem_element = day_pillar.get("stem_element", "목")
        return WuXing(stem_element)

    def _get_wuxing_balance(self, saju_data: dict[str, Any]) -> dict[WuXing, float]:
        """오행 균형 분석"""
        wuxing_count = saju_data.get("wuxing_count", {})
        total = sum(wuxing_count.values()) or 1

        balance = {}
        for element in WuXing:
            count = wuxing_count.get(element.value, 0)
            balance[element] = count / total

        return balance

    def _get_strength_level(self, saju_data: dict[str, Any]) -> str:
        """일간 강약 수준"""
        strength_info = saju_data.get("day_master_strength", {})
        return strength_info.get("level", "medium")
