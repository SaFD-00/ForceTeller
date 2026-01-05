"""
사주 분석 모듈
- yongsin: 용신 분석 (4가지 방법론: 강약/조후/통관/병약)
- fortune: 운세 분석 (5가지 유형: general/career/wealth/health/love)
- schools: 유파별 해석 (5개 유파: 자평명리/적천수/궁통보감/현대명리/신살중심)
"""

from .yongsin import (
    WuXing,
    YongSinResult,
    YongSinMethod,
    YongSinRecommendations,
    DayMasterStrength,
    select_yongsin,
    select_yongsin_auto,
    compare_yongsin_methods,
)
from .fortune import (
    FortuneAnalyzer,
    FortuneType,
    FortuneAnalysis,
    FortuneDetails,
    LuckyElements,
    analyze_fortune,
    analyze_all_fortunes,
)
from .schools import (
    SchoolComparator,
    SchoolCode,
    SchoolComparisonResult,
    SchoolInterpretation,
    compare_schools,
    get_school_interpreter,
)

__all__ = [
    # 오행
    "WuXing",
    # 용신
    "YongSinResult",
    "YongSinMethod",
    "YongSinRecommendations",
    "DayMasterStrength",
    "select_yongsin",
    "select_yongsin_auto",
    "compare_yongsin_methods",
    # 운세
    "FortuneAnalyzer",
    "FortuneType",
    "FortuneAnalysis",
    "FortuneDetails",
    "LuckyElements",
    "analyze_fortune",
    "analyze_all_fortunes",
    # 유파
    "SchoolComparator",
    "SchoolCode",
    "SchoolComparisonResult",
    "SchoolInterpretation",
    "compare_schools",
    "get_school_interpreter",
]
