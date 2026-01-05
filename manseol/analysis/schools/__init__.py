"""
유파별 해석 및 비교 모듈
5개 유파: 자평명리, 적천수, 궁통보감, 현대명리, 신살중심
"""

from .base_interpreter import (
    SchoolCode,
    SchoolInterpretation,
    ConsensusItem,
    DifferenceItem,
    SchoolComparisonResult,
    BaseSchoolInterpreter,
)
from .ziping import ZipingInterpreter
from .dts import DTSInterpreter
from .qtbj import QTBJInterpreter
from .modern import ModernInterpreter
from .shensha import ShenshaInterpreter
from .comparator import SchoolComparator, compare_schools, get_school_interpreter

__all__ = [
    # 기본 타입
    "SchoolCode",
    "SchoolInterpretation",
    "ConsensusItem",
    "DifferenceItem",
    "SchoolComparisonResult",
    "BaseSchoolInterpreter",
    # 유파 해석기
    "ZipingInterpreter",
    "DTSInterpreter",
    "QTBJInterpreter",
    "ModernInterpreter",
    "ShenshaInterpreter",
    # 비교 도구
    "SchoolComparator",
    "compare_schools",
    "get_school_interpreter",
]
