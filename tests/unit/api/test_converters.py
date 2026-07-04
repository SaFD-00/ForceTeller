"""
데이터 변환 유틸리티 테스트
"""


class TestSajuDataConverter:
    """사주 데이터 변환기 테스트"""

    def test_convert_display_format_to_analysis_format(self):
        """프론트엔드 display 형식을 분석 형식으로 변환"""
        from api.converters import SajuDataConverter

        display_data = {
            "four_pillars": {"day": {"heavenly_stem": {"element": "목"}}},
            "five_elements": {"distribution": {"목": 3, "화": 2, "토": 1, "금": 1, "수": 1}},
            "strength": {"is_strong": True, "type": "신강"},
        }

        result = SajuDataConverter.to_analysis_format(display_data)

        assert "day_pillar" in result
        assert result["day_pillar"]["stem_element"] == "목"
        assert result["wuxing_count"]["목"] == 3
        assert result["day_master_strength"]["level"] == "신강"

    def test_convert_original_format_to_analysis_format(self):
        """백엔드 원본 형식을 분석 형식으로 변환"""
        from api.converters import SajuDataConverter

        original_data = {
            "pillars": {"day": {"stem": {"element": "화"}}},
            "analysis": {
                "five_elements": {"wood": 2, "fire": 3, "earth": 2, "metal": 1, "water": 0},
                "strength": {"level": "medium"},
            },
        }

        result = SajuDataConverter.to_analysis_format(original_data)

        assert result["day_pillar"]["stem_element"] == "화"
        assert result["wuxing_count"]["화"] == 3
        assert result["wuxing_count"]["수"] == 0
        assert result["day_master_strength"]["level"] == "medium"

    def test_already_analysis_format_returns_unchanged(self):
        """이미 분석 형식이면 그대로 반환"""
        from api.converters import SajuDataConverter

        analysis_data = {
            "day_pillar": {"stem_element": "금"},
            "wuxing_count": {"목": 2, "화": 2, "토": 2, "금": 1, "수": 1},
            "day_master_strength": {"level": "strong"},
        }

        result = SajuDataConverter.to_analysis_format(analysis_data)

        assert result == analysis_data

    def test_unknown_format_returns_unchanged(self):
        """알 수 없는 형식은 그대로 반환"""
        from api.converters import SajuDataConverter

        unknown_data = {"random": "data", "unknown": "format"}

        result = SajuDataConverter.to_analysis_format(unknown_data)

        assert result == unknown_data

    def test_display_format_without_strength_type(self):
        """strength.type이 없는 display 형식 처리"""
        from api.converters import SajuDataConverter

        display_data = {
            "four_pillars": {"day": {"heavenly_stem": {"element": "토"}}},
            "five_elements": {"distribution": {"목": 1, "화": 2, "토": 3, "금": 1, "수": 1}},
            "strength": {"is_strong": False},
        }

        result = SajuDataConverter.to_analysis_format(display_data)

        assert result["day_master_strength"]["level"] == "weak"

    def test_preserves_original_data(self):
        """원본 데이터가 보존되는지 확인"""
        from api.converters import SajuDataConverter

        display_data = {
            "four_pillars": {"day": {"heavenly_stem": {"element": "수"}}},
            "five_elements": {"distribution": {"목": 2, "화": 2, "토": 2, "금": 1, "수": 1}},
            "strength": {"is_strong": True, "type": "신강"},
        }

        result = SajuDataConverter.to_analysis_format(display_data)

        assert "original" in result
        assert result["original"] == display_data


class TestEnumConverter:
    """Enum 변환기 테스트"""

    def test_fortune_type_conversion(self):
        """AnalysisType을 FortuneType으로 변환"""
        from api.converters import EnumConverter
        from api.schemas import AnalysisType
        from manseol.analysis import FortuneType

        mapping = {
            AnalysisType.FORTUNE_GENERAL: FortuneType.GENERAL,
            AnalysisType.FORTUNE_CAREER: FortuneType.CAREER,
            AnalysisType.FORTUNE_WEALTH: FortuneType.WEALTH,
            AnalysisType.FORTUNE_HEALTH: FortuneType.HEALTH,
            AnalysisType.FORTUNE_LOVE: FortuneType.LOVE,
        }

        for analysis_type, expected_fortune_type in mapping.items():
            result = EnumConverter.to_fortune_type(analysis_type)
            assert result == expected_fortune_type

    def test_fortune_type_invalid_returns_none(self):
        """유효하지 않은 타입은 None 반환"""
        from api.converters import EnumConverter
        from api.schemas import AnalysisType

        result = EnumConverter.to_fortune_type(AnalysisType.YONGSIN)
        assert result is None

    def test_school_code_conversion(self):
        """SchoolCodeType을 SchoolCode로 변환"""
        from api.converters import EnumConverter
        from api.schemas import SchoolCodeType
        from manseol.analysis import SchoolCode

        mapping = {
            SchoolCodeType.ZIPING: SchoolCode.ZIPING,
            SchoolCodeType.DTS: SchoolCode.DTS,
            SchoolCodeType.QTBJ: SchoolCode.QTBJ,
            SchoolCodeType.MODERN: SchoolCode.MODERN,
            SchoolCodeType.SHENSHA: SchoolCode.SHENSHA,
        }

        for schema_code, expected_code in mapping.items():
            result = EnumConverter.to_school_code(schema_code)
            assert result == expected_code

    def test_yongsin_method_to_string(self):
        """YongSinMethodType을 문자열로 변환"""
        from api.converters import EnumConverter
        from api.schemas import YongSinMethodType

        result = EnumConverter.yongsin_method_to_string(YongSinMethodType.STRENGTH)
        assert result == "strength"

        result = EnumConverter.yongsin_method_to_string(YongSinMethodType.SEASONAL)
        assert result == "seasonal"
