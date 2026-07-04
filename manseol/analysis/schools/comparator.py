"""
유파 비교 엔진
여러 유파의 해석 결과를 비교하고 합의점/차이점 분석
Reference: fortuneteller/src/lib/school_comparator.ts
"""

from typing import Any

from config.logging_config import get_logger

from .base_interpreter import (
    SCHOOL_NAMES,
    BaseSchoolInterpreter,
    ConsensusItem,
    DifferenceItem,
    SchoolCode,
    SchoolComparisonResult,
    SchoolInterpretation,
)
from .dts import DTSInterpreter
from .modern import ModernInterpreter
from .qtbj import QTBJInterpreter
from .shensha import ShenshaInterpreter
from .ziping import ZipingInterpreter

logger = get_logger(__name__)

# 유파별 해석기 레지스트리
INTERPRETERS: dict[SchoolCode, type[BaseSchoolInterpreter]] = {
    SchoolCode.ZIPING: ZipingInterpreter,
    SchoolCode.DTS: DTSInterpreter,
    SchoolCode.QTBJ: QTBJInterpreter,
    SchoolCode.MODERN: ModernInterpreter,
    SchoolCode.SHENSHA: ShenshaInterpreter,
}


def get_school_interpreter(school: SchoolCode) -> BaseSchoolInterpreter:
    """유파별 해석기 인스턴스 반환"""
    interpreter_class = INTERPRETERS.get(school)
    if not interpreter_class:
        raise ValueError(f"Unknown school code: {school}")
    return interpreter_class()


class SchoolComparator:
    """유파 비교기"""

    @staticmethod
    def compare_schools(
        saju_data: dict[str, Any], schools: list[SchoolCode] | None = None
    ) -> SchoolComparisonResult:
        """
        여러 유파로 해석 및 비교

        Args:
            saju_data: 사주 데이터
            schools: 비교할 유파 목록 (None이면 전체)

        Returns:
            비교 결과
        """
        if schools is None:
            schools = list(SchoolCode)

        # 각 유파별 해석 수행
        interpretations: list[SchoolInterpretation] = []

        for school in schools:
            try:
                interpreter = get_school_interpreter(school)
                interpretation = interpreter.interpret(saju_data)
                interpretations.append(interpretation)
            except Exception as e:
                logger.warning("유파 해석 실패, 건너뜀 (school=%s): %s", school, e)

        # 합의 항목 찾기
        consensus = SchoolComparator._find_consensus(interpretations)

        # 차이점 분석
        differences = SchoolComparator._find_differences(interpretations)

        # 최종 권장 사항 생성
        recommendation = SchoolComparator._generate_recommendation(
            interpretations, consensus, differences
        )

        return SchoolComparisonResult(
            schools=schools,
            interpretations=interpretations,
            consensus=consensus,
            differences=differences,
            recommendation=recommendation,
        )

    @staticmethod
    def _find_consensus(interpretations: list[SchoolInterpretation]) -> list[ConsensusItem]:
        """합의 항목 찾기"""
        consensus: list[ConsensusItem] = []

        if not interpretations:
            return consensus

        # 용신 합의
        yongsin_counts: dict[str, list[SchoolCode]] = {}
        for interp in interpretations:
            yongsin = interp.yong_sin.value
            if yongsin not in yongsin_counts:
                yongsin_counts[yongsin] = []
            yongsin_counts[yongsin].append(interp.school)

        # 2개 이상 유파가 동의하는 용신
        for yongsin, schools in yongsin_counts.items():
            if len(schools) >= 2:
                consensus.append(
                    ConsensusItem(
                        category="yongsin",
                        agreement=f"용신으로 {yongsin} 오행을 사용하는 것이 좋습니다",
                        schools=schools,
                    )
                )

        # 카테고리별 유사 키워드 검색
        categories = ["health", "wealth", "career", "relationship", "fame"]

        for category in categories:
            common_keywords = SchoolComparator._find_common_keywords(interpretations, category)
            if common_keywords:
                agreeing_schools = [
                    interp.school
                    for interp in interpretations
                    if any(keyword in getattr(interp, category, "") for keyword in common_keywords)
                ]

                if len(agreeing_schools) >= 2:
                    consensus.append(
                        ConsensusItem(
                            category=category,
                            agreement=f"{', '.join(common_keywords[:2])} 관련 조언이 공통적입니다",
                            schools=agreeing_schools,
                        )
                    )

        return consensus

    @staticmethod
    def _find_differences(interpretations: list[SchoolInterpretation]) -> list[DifferenceItem]:
        """차이점 분석"""
        differences: list[DifferenceItem] = []

        categories = ["health", "wealth", "career", "relationship", "fame"]

        for category in categories:
            unique_interps = [
                {
                    "school": interp.school.value,
                    "school_name": interp.school_name,
                    "interpretation": getattr(interp, category, ""),
                }
                for interp in interpretations
            ]

            # 고유한 해석이 2개 이상인 경우 차이점으로 기록
            unique_texts = set(ui["interpretation"] for ui in unique_interps)
            if len(unique_texts) >= 2:
                differences.append(
                    DifferenceItem(
                        category=category,
                        interpretations=unique_interps,
                    )
                )

        return differences

    @staticmethod
    def _find_common_keywords(
        interpretations: list[SchoolInterpretation], category: str
    ) -> list[str]:
        """공통 키워드 찾기"""
        keywords: dict[str, int] = {}

        # 각 해석에서 키워드 추출
        for interp in interpretations:
            text = getattr(interp, category, "")
            words = [w for w in text.replace(",", " ").replace(".", " ").split() if len(w) >= 2]

            for word in words:
                keywords[word] = keywords.get(word, 0) + 1

        # 2개 이상 유파에서 등장하는 키워드
        common = [word for word, count in keywords.items() if count >= 2]

        return common[:5]

    @staticmethod
    def _generate_recommendation(
        interpretations: list[SchoolInterpretation],
        consensus: list[ConsensusItem],
        differences: list[DifferenceItem],
    ) -> str:
        """최종 권장 사항 생성"""
        lines = []

        # 합의 사항 요약
        if consensus:
            lines.append(f"{len(consensus)}개 항목에서 여러 유파가 동의합니다:")
            for item in consensus[:3]:
                lines.append(f"  - {item.agreement} ({len(item.schools)}개 유파 동의)")

        # 신뢰도 높은 해석 우선 권장
        high_confidence = [interp for interp in interpretations if interp.confidence >= 0.8]
        if high_confidence:
            best = max(high_confidence, key=lambda x: x.confidence)
            lines.append("")
            lines.append(
                f"가장 신뢰도 높은 해석: {best.school_name} ({best.confidence * 100:.0f}%)"
            )

        # 차이점 고려 권장
        if differences:
            lines.append("")
            lines.append(
                f"{len(differences)}개 영역에서 유파별 관점이 다릅니다. "
                "자신의 상황과 가치관에 맞는 해석을 선택하세요."
            )

        if not lines:
            return "각 유파의 관점을 참고하여 종합적으로 판단하시기 바랍니다."

        return "\n".join(lines)

    @staticmethod
    def recommend_school(saju_data: dict[str, Any], priority: str = "general") -> SchoolCode:
        """
        우선순위에 따른 유파 추천

        Args:
            saju_data: 사주 데이터
            priority: 우선순위 영역 (health/wealth/career/relationship/fame/general)

        Returns:
            추천 유파 코드
        """
        # 우선순위별 추천 유파
        recommendations = {
            "health": SchoolCode.QTBJ,  # 궁통보감 - 건강/조후
            "wealth": SchoolCode.MODERN,  # 현대명리 - 재물
            "career": SchoolCode.MODERN,  # 현대명리 - 직업
            "relationship": SchoolCode.SHENSHA,  # 신살중심 - 인간관계
            "fame": SchoolCode.DTS,  # 적천수 - 명예
            "general": SchoolCode.ZIPING,  # 자평명리 - 일반
        }

        return recommendations.get(priority, SchoolCode.ZIPING)

    @staticmethod
    def get_all_school_info() -> list[dict[str, str]]:
        """모든 유파 정보 반환"""
        return [
            {
                "code": school.value,
                "name": SCHOOL_NAMES.get(school, ""),
                "description": get_school_interpreter(school).description,
            }
            for school in SchoolCode
        ]


def compare_schools(
    saju_data: dict[str, Any], schools: list[SchoolCode] | None = None
) -> SchoolComparisonResult:
    """
    유파 비교 편의 함수

    Args:
        saju_data: 사주 데이터
        schools: 비교할 유파 목록

    Returns:
        비교 결과
    """
    return SchoolComparator.compare_schools(saju_data, schools)


def interpret_single_school(saju_data: dict[str, Any], school: SchoolCode) -> SchoolInterpretation:
    """
    단일 유파 해석 편의 함수

    Args:
        saju_data: 사주 데이터
        school: 유파 코드

    Returns:
        해석 결과
    """
    interpreter = get_school_interpreter(school)
    return interpreter.interpret(saju_data)
