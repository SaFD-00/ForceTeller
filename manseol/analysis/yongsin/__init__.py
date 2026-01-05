"""
용신(用神) 분석 모듈
사주의 불균형을 조절하고 운을 개선하는 핵심 오행 분석
"""

from .base import (
    WuXing,
    YongSinMethod,
    DayMasterStrength,
    YongSinResult,
    YongSinRecommendations,
)
from .selector import (
    select_yongsin,
    select_yongsin_auto,
    compare_yongsin_methods,
    YongSinSelector,
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
