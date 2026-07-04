"""
용신(用神) 분석 모듈
사주의 불균형을 조절하고 운을 개선하는 핵심 오행 분석
"""

from .base import (
    DayMasterStrength,
    WuXing,
    YongSinMethod,
    YongSinRecommendations,
    YongSinResult,
)
from .selector import (
    YongSinSelector,
    compare_yongsin_methods,
    select_yongsin,
    select_yongsin_auto,
)

__all__ = [
    "WuXing",
    "YongSinMethod",
    "DayMasterStrength",
    "YongSinResult",
    "YongSinRecommendations",
    "select_yongsin",
    "select_yongsin_auto",
    "compare_yongsin_methods",
    "YongSinSelector",
]
