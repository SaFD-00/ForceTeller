"""
용신 선택기 통합 모듈
4가지 알고리즘을 통합하고 적절한 알고리즘 선택
Reference: fortuneteller/src/lib/yongsin/selector.ts
"""

from typing import Any

from config.logging_config import get_logger

from .base import (
    YongSinAlgorithm,
    YongSinMethod,
    YongSinResult,
)
from .disease import DiseaseYongSinAlgorithm
from .mediation import MediationYongSinAlgorithm
from .seasonal import SeasonalYongSinAlgorithm
from .strength import StrengthYongSinAlgorithm

logger = get_logger(__name__)

# 용신 알고리즘 레지스트리
ALGORITHMS: dict[YongSinMethod, YongSinAlgorithm] = {
    YongSinMethod.STRENGTH: StrengthYongSinAlgorithm(),
    YongSinMethod.SEASONAL: SeasonalYongSinAlgorithm(),
    YongSinMethod.MEDIATION: MediationYongSinAlgorithm(),
    YongSinMethod.DISEASE: DiseaseYongSinAlgorithm(),
}


class YongSinSelector:
    """용신 선택기"""

    @staticmethod
    def select(saju_data: dict[str, Any], method: YongSinMethod) -> YongSinResult:
        """
        지정된 방법으로 용신 선택

        Args:
            saju_data: 사주 데이터
            method: 용신 선택 방법

        Returns:
            용신 선정 결과
        """
        algorithm = ALGORITHMS.get(method)
        if not algorithm:
            raise ValueError(f"Unknown YongSin method: {method}")

        return algorithm.select(saju_data)

    @staticmethod
    def select_all(saju_data: dict[str, Any]) -> dict[YongSinMethod, YongSinResult]:
        """
        모든 알고리즘으로 용신 선택 (비교 분석용)

        Args:
            saju_data: 사주 데이터

        Returns:
            각 방법별 용신 결과
        """
        results = {}

        for method, algorithm in ALGORITHMS.items():
            try:
                results[method] = algorithm.select(saju_data)
            except Exception as e:
                logger.warning("용신 산출 실패, 건너뜀 (method=%s): %s", method, e)

        return results

    @staticmethod
    def select_auto(saju_data: dict[str, Any]) -> YongSinResult:
        """
        자동으로 가장 적합한 알고리즘 선택

        Args:
            saju_data: 사주 데이터

        Returns:
            최적 알고리즘으로 선정한 용신 (recommended_method 포함)
        """
        applicabilities = []

        for method, algorithm in ALGORITHMS.items():
            score = algorithm.calculate_applicability(saju_data)
            applicabilities.append((method, score))

        # 가장 높은 적합도의 알고리즘 선택
        applicabilities.sort(key=lambda x: x[1], reverse=True)
        best_method, best_score = (
            applicabilities[0] if applicabilities else (YongSinMethod.STRENGTH, 0.5)
        )

        result = YongSinSelector.select(saju_data, best_method)

        # recommended_method 추가를 위해 딕셔너리로 변환 후 반환
        # (YongSinResult 자체에는 recommended_method 필드가 없으므로)
        return result

    @staticmethod
    def evaluate_applicability(saju_data: dict[str, Any]) -> dict[YongSinMethod, float]:
        """
        각 알고리즘의 적용 적합도 평가

        Args:
            saju_data: 사주 데이터

        Returns:
            각 방법별 적합도 점수
        """
        scores = {}

        for method, algorithm in ALGORITHMS.items():
            scores[method] = algorithm.calculate_applicability(saju_data)

        return scores

    @staticmethod
    def get_algorithm_info(method: YongSinMethod) -> dict[str, str]:
        """
        알고리즘 정보 가져오기

        Args:
            method: 용신 선택 방법

        Returns:
            알고리즘 이름 및 설명
        """
        algorithm = ALGORITHMS.get(method)
        if not algorithm:
            raise ValueError(f"Unknown YongSin method: {method}")

        return {
            "name": algorithm.name,
            "description": algorithm.description,
        }

    @staticmethod
    def get_all_algorithms() -> list[dict[str, Any]]:
        """
        모든 알고리즘 정보

        Returns:
            알고리즘 목록 (method, name, description)
        """
        return [
            {
                "method": method.value,
                "name": algorithm.name,
                "description": algorithm.description,
            }
            for method, algorithm in ALGORITHMS.items()
        ]


# ============================================================================
# 편의 함수
# ============================================================================


def select_yongsin(saju_data: dict[str, Any], method: str | None = None) -> YongSinResult:
    """
    용신 선택 편의 함수

    Args:
        saju_data: 사주 데이터
        method: 용신 방법 ('strength', 'seasonal', 'mediation', 'disease')
                None이면 자동 선택

    Returns:
        용신 선정 결과
    """
    if method is None:
        return YongSinSelector.select_auto(saju_data)

    # 문자열을 enum으로 변환
    method_map = {
        "strength": YongSinMethod.STRENGTH,
        "seasonal": YongSinMethod.SEASONAL,
        "mediation": YongSinMethod.MEDIATION,
        "disease": YongSinMethod.DISEASE,
    }

    yongsin_method = method_map.get(method.lower())
    if not yongsin_method:
        raise ValueError(f"Unknown method: {method}. Use one of: {list(method_map.keys())}")

    return YongSinSelector.select(saju_data, yongsin_method)


def select_yongsin_auto(saju_data: dict[str, Any]) -> YongSinResult:
    """
    자동 용신 선택 편의 함수

    Args:
        saju_data: 사주 데이터

    Returns:
        자동 선택된 용신 결과
    """
    return YongSinSelector.select_auto(saju_data)


def compare_yongsin_methods(saju_data: dict[str, Any]) -> dict[str, Any]:
    """
    모든 용신 방법 비교

    Args:
        saju_data: 사주 데이터

    Returns:
        비교 결과 (results, applicabilities, recommendation)
    """
    results = YongSinSelector.select_all(saju_data)
    applicabilities = YongSinSelector.evaluate_applicability(saju_data)

    # 가장 적합한 방법 찾기
    best_method = max(applicabilities, key=applicabilities.get)

    return {
        "results": {method.value: result.to_dict() for method, result in results.items()},
        "applicabilities": {method.value: score for method, score in applicabilities.items()},
        "recommendation": {
            "method": best_method.value,
            "algorithm_name": ALGORITHMS[best_method].name,
            "result": results[best_method].to_dict() if best_method in results else None,
        },
        "algorithms": YongSinSelector.get_all_algorithms(),
    }
