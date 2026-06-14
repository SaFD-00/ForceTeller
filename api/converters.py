"""
데이터 변환 유틸리티

프론트엔드/백엔드 데이터 형식 변환 및 Enum 변환을 담당합니다.
"""

from typing import Dict, Any, Optional

from api.schemas import AnalysisType, SchoolCodeType, YongSinMethodType
from manseol.analysis import FortuneType, SchoolCode


class SajuDataConverter:
    """사주 데이터 형식 변환기"""

    @staticmethod
    def to_analysis_format(saju_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        다양한 형식의 사주 데이터를 분석 함수용 형식으로 변환

        Args:
            saju_data: 사주 데이터 (display, original, analysis 형식 중 하나)

        Returns:
            분석 함수용 형식의 사주 데이터
        """
        # 이미 분석 형식이면 그대로 반환
        if "day_pillar" in saju_data and "stem_element" in saju_data.get("day_pillar", {}):
            return saju_data

        # 백엔드 원본 형식이면 변환
        if "pillars" in saju_data and "analysis" in saju_data:
            return SajuDataConverter._convert_original_format(saju_data)

        # 프론트엔드 display 형식 변환
        if "four_pillars" in saju_data:
            return SajuDataConverter._convert_display_format(saju_data)

        # 알 수 없는 형식은 그대로 반환
        return saju_data

    @staticmethod
    def _convert_display_format(saju_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        프론트엔드 display 형식을 분석 형식으로 변환

        Display format (frontend):
        - four_pillars.day.heavenly_stem.element
        - five_elements.distribution
        - strength.is_strong / strength.type
        """
        four_pillars = saju_data.get("four_pillars", {})
        five_elements = saju_data.get("five_elements", {})
        strength = saju_data.get("strength", {})

        # day_pillar 변환
        day_pillar_data = four_pillars.get("day", {})
        day_stem = day_pillar_data.get("heavenly_stem", {}) if isinstance(day_pillar_data, dict) else {}
        stem_element = day_stem.get("element", "목") if isinstance(day_stem, dict) else "목"

        # wuxing_count 변환 (distribution을 그대로 사용)
        distribution = five_elements.get("distribution", {}) if isinstance(five_elements, dict) else {}
        wuxing_count = distribution if distribution else {"목": 2, "화": 2, "토": 2, "금": 1, "수": 1}

        # strength 변환
        if isinstance(strength, dict):
            is_strong = strength.get("is_strong", True)
            strength_type = strength.get("type", "")
            if strength_type:
                level = strength_type  # 신강, 신약, 중화
            else:
                level = "strong" if is_strong else "weak"
        else:
            level = "medium"

        return {
            "day_pillar": {
                "stem_element": stem_element,
            },
            "wuxing_count": wuxing_count,
            "day_master_strength": {
                "level": level,
            },
            # 원본 데이터도 유지 (다른 분석에서 필요할 수 있음)
            "original": saju_data,
        }

    @staticmethod
    def _convert_original_format(saju_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        백엔드 원본 형식을 분석 형식으로 변환
        """
        pillars = saju_data.get("pillars", {})
        analysis = saju_data.get("analysis", {})

        # day pillar 정보
        day_pillar = pillars.get("day", {})
        day_stem = day_pillar.get("stem", {}) if isinstance(day_pillar, dict) else {}
        stem_element = day_stem.get("element", "목") if isinstance(day_stem, dict) else "목"

        # 오행 분포
        five_elements = analysis.get("five_elements", {}) if isinstance(analysis, dict) else {}
        wuxing_count = {
            "목": five_elements.get("wood", 2),
            "화": five_elements.get("fire", 2),
            "토": five_elements.get("earth", 2),
            "금": five_elements.get("metal", 1),
            "수": five_elements.get("water", 1),
        }

        # 신강/신약
        strength_info = analysis.get("strength", {}) if isinstance(analysis, dict) else {}
        level = strength_info.get("level", "medium") if isinstance(strength_info, dict) else "medium"

        return {
            "day_pillar": {
                "stem_element": stem_element,
            },
            "wuxing_count": wuxing_count,
            "day_master_strength": {
                "level": level,
            },
            "original": saju_data,
        }


def enrich_with_analysis(result_dict: Dict[str, Any]) -> Dict[str, Any]:
    """만세력 결과(dict)에 이미 구현된 분석 라이브러리 결과를 덧붙인다.

    json_exporter는 결정론 계산만 담당하고, 용신 4방법·개운법·유파 비교·
    운세 점수처럼 analysis 패키지가 책임지는 항목은 여기서 한 번에 조립한다.
    개별 분석이 실패해도 기본 만세력 결과는 보존되도록 방어적으로 처리한다.

    Args:
        result_dict: SajuResult.to_dict() 결과

    Returns:
        결과 dict에 병합할 추가 키들 (yongsin_comparison, yongsin_recommendations 등)
    """
    enriched: Dict[str, Any] = {}

    try:
        analysis_data = SajuDataConverter.to_analysis_format(result_dict)
    except Exception:
        return enriched

    # 용신 4방법 비교 + 개운법 추천 (강약/조후/통관/병약)
    try:
        from manseol.analysis import compare_yongsin_methods, select_yongsin_auto
        from manseol.analysis.yongsin.recommendations import (
            generate_detailed_recommendations,
        )

        enriched["yongsin_comparison"] = compare_yongsin_methods(analysis_data)
        yongsin_result = select_yongsin_auto(analysis_data)
        enriched["yongsin_recommendations"] = generate_detailed_recommendations(
            yongsin_result
        )
    except Exception:
        pass

    return enriched


class EnumConverter:
    """Enum 타입 변환기"""

    @staticmethod
    def to_fortune_type(analysis_type: AnalysisType) -> Optional[FortuneType]:
        """AnalysisType을 FortuneType으로 변환"""
        mapping = {
            AnalysisType.FORTUNE_GENERAL: FortuneType.GENERAL,
            AnalysisType.FORTUNE_CAREER: FortuneType.CAREER,
            AnalysisType.FORTUNE_WEALTH: FortuneType.WEALTH,
            AnalysisType.FORTUNE_HEALTH: FortuneType.HEALTH,
            AnalysisType.FORTUNE_LOVE: FortuneType.LOVE,
        }
        return mapping.get(analysis_type)

    @staticmethod
    def to_school_code(code: SchoolCodeType) -> Optional[SchoolCode]:
        """SchoolCodeType을 SchoolCode로 변환"""
        mapping = {
            SchoolCodeType.ZIPING: SchoolCode.ZIPING,
            SchoolCodeType.DTS: SchoolCode.DTS,
            SchoolCodeType.QTBJ: SchoolCode.QTBJ,
            SchoolCodeType.MODERN: SchoolCode.MODERN,
            SchoolCodeType.SHENSHA: SchoolCode.SHENSHA,
        }
        return mapping.get(code)

    @staticmethod
    def yongsin_method_to_string(method: YongSinMethodType) -> str:
        """YongSinMethodType을 문자열로 변환"""
        return method.value
