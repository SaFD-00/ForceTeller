"""
해외 출생 시간대 환산 테스트

엔진은 한국 벽시계를 전제하므로 해외 출생은 현지 시각을 한국 시각으로 환산한
뒤 계산해야 한다. 환산 후의 기존 진태양시 보정 (현지경도 − 135°)×4분은
수학적으로 현지 시태양시와 일치한다 — 뉴욕 케이스의 기대값이 그 검산이다.
(환산 누락 시절엔 뉴욕 14:30 출생이 −836분 보정으로 자시(병자)가 됐었다.)
"""

from datetime import date, time

import pytest

from manseol.data.city_coordinates import CityCoordinates
from manseol.models.input_model import CalendarType, Gender, SajuInput
from manseol.output.json_exporter import JsonExporter


def _result(**kwargs):
    defaults = dict(
        name="테스트",
        birth_date=date(1990, 5, 15),
        birth_time=time(14, 30),
        calendar=CalendarType("solar"),
        city="Seoul",
        gender=Gender("male"),
    )
    defaults.update(kwargs)
    return JsonExporter(SajuInput(**defaults)).generate_result()


def _pillars(result):
    p = result.pillars
    return {
        k: getattr(p, k).stem.korean + getattr(p, k).branch.korean
        for k in ("year", "month", "day", "hour")
        if getattr(p, k) is not None
    }


class TestForeignBirthConversion:
    def test_new_york_converts_to_korean_time(self):
        """뉴욕 1990-05-15 14:30 EDT = KST 05-16 03:30. 진태양시는 현지
        시태양시(13:30 EST + 경도 +4분 + 균시차 ≈ 13:37)와 일치해야 한다."""
        r = _result(city="New York City")
        tc = r.adjusted_time

        assert tc.birth_timezone == "America/New_York"
        assert tc.korean_time == "1990-05-16 03:30:00"
        # 진태양시 = 현지 시태양시 (동치 검산: 13:37 ± 수 분)
        assert tc.true_solar_time.startswith("1990-05-15 13:3")

        pillars = _pillars(r)
        # 일주는 현지 태양일 기준으로 5/15 경진 유지, 시주는 미시(계미)
        assert pillars["day"] == "경진"
        assert pillars["hour"] == "계미"

    def test_seoul_unchanged(self):
        """한국 출생은 환산이 일어나지 않고 기존 결과와 동일하다."""
        r = _result(city="Seoul")
        tc = r.adjusted_time

        assert tc.birth_timezone is None
        assert tc.korean_time is None
        assert _pillars(r)["hour"] == "계미"

    def test_tokyo_same_offset_no_shift(self):
        """도쿄는 UTC+9라 벽시계가 같고, 경도 보정만 동경 139.65° 기준
        +18분대로 달라진다."""
        r = _result(city="Tokyo")
        tc = r.adjusted_time

        assert tc.birth_timezone == "Asia/Tokyo"
        assert tc.korean_time == "1990-05-15 14:30:00"
        assert 17 < tc.longitude_correction_minutes < 21

    def test_hong_kong_midnight_boundary(self):
        """홍콩 23:40(UTC+8) → 한국 다음날 00:40 → 진태양시가 전날 23:20대로
        복귀해 일주는 당일(경진), 시주는 자시(병자)가 된다."""
        r = _result(city="Hong Kong", birth_time=time(23, 40))
        tc = r.adjusted_time

        assert tc.korean_time == "1990-05-16 00:40:00"
        assert tc.true_solar_time.startswith("1990-05-15 23:2")

        pillars = _pillars(r)
        assert pillars["day"] == "경진"
        assert pillars["hour"] == "병자"

    def test_explicit_timezone_overrides_city(self):
        """timezone 명시 입력은 city 조회보다 우선한다."""
        r = _result(city="Seoul", timezone="America/New_York")
        assert r.adjusted_time.birth_timezone == "America/New_York"
        assert r.adjusted_time.korean_time == "1990-05-16 03:30:00"

    def test_unknown_timezone_raises(self):
        with pytest.raises(ValueError, match="시간대"):
            _result(timezone="Mars/Olympus_Mons")

    def test_conversion_applies_without_time_correction(self):
        """진태양시 보정을 꺼도(유파 선택) 시간대 환산(타임라인 정합)은 적용된다."""
        r = _result(city="Hong Kong", birth_time=time(23, 40), apply_time_correction=False)
        # 보정 상세는 없지만 한국시각 00:40 기준이라 일주가 다음날로 넘어간다
        assert r.adjusted_time is None
        assert _pillars(r)["day"] == "신사"


class TestCityTimezoneData:
    def test_get_timezone_matches_coordinates_city(self):
        """get_timezone은 get_coordinates와 같은 도시를 가리켜야 한다."""
        assert CityCoordinates.get_timezone("Seoul") == "Asia/Seoul"
        assert CityCoordinates.get_timezone("New York City") == "America/New_York"
        assert CityCoordinates.get_timezone("존재하지않는도시명") is None

    def test_search_city_includes_timezone(self):
        results = CityCoordinates.search_city("Tokyo", limit=1)
        assert results and results[0]["timezone"] == "Asia/Tokyo"
