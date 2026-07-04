"""
_build_current_fortune_from_saju 단위 테스트

세션 saju_data(display 형식)의 일간에서 현재 연·월·일운을 서버 재계산하는
헬퍼의 4개 경로를 검증한다. 정상 경로는 실시간(now_kst) 계산이라 값이 아니라
계약 구조만 단언하고, 나머지 3경로는 복원 실패 → None 폴백을 단언한다.
"""

from api.routes.chat import _build_current_fortune_from_saju


class TestBuildCurrentFortuneFromSaju:
    """display 형식 일간 복원 → 현재 운세 재계산"""

    def test_valid_day_stem_returns_fortune_contract(self):
        """정상 경로: 유효한 한글 천간 → yearly/monthly/daily 계약 dict 반환"""
        saju = {"four_pillars": {"day": {"heavenly_stem": {"korean": "갑"}}}}

        result = _build_current_fortune_from_saju(saju)

        assert result is not None
        # 계약 최상위 키
        assert "reference_datetime" in result
        for section in ("yearly", "monthly", "daily"):
            assert section in result
            entry = result[section]
            # 간지 필드가 채워졌는지 (값은 실행 시각 의존이라 존재만 확인)
            for field in ("stem", "branch", "ganji_korean", "ten_god"):
                assert field in entry
                assert entry[field]

    def test_missing_four_pillars_returns_none(self):
        """four_pillars 자체가 없으면 복원 불가 → None"""
        saju = {"birth_info": {"name": "테스트"}}

        assert _build_current_fortune_from_saju(saju) is None

    def test_non_dict_heavenly_stem_returns_none(self):
        """heavenly_stem이 dict가 아니면(구조 불일치) → None"""
        saju = {"four_pillars": {"day": {"heavenly_stem": "갑"}}}

        assert _build_current_fortune_from_saju(saju) is None

    def test_unregistered_korean_stem_returns_none(self):
        """등록되지 않은 한글 천간명이면 인덱스 복원 실패 → None"""
        saju = {"four_pillars": {"day": {"heavenly_stem": {"korean": "봄"}}}}

        assert _build_current_fortune_from_saju(saju) is None
