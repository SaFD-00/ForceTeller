"""
만세력 엔진 회귀 테스트

알려진 입력의 결정론적 출력(골든 스냅샷)을 고정해 계산 로직 변경으로 인한
회귀를 감지한다. 또한 새로 배선된 자산(상호작용·세운)과 분석 보강(enrich)을
구조적으로 검증하고, 시간 미상 입력이 끝까지 동작하는지 확인한다.
"""

from datetime import date, time

import pytest

from api.converters import enrich_with_analysis
from manseol.models.input_model import CalendarType, Gender, SajuInput
from manseol.output.json_exporter import JsonExporter


def _result(**kwargs):
    defaults = dict(
        name="홍길동",
        birth_date=date(1990, 5, 15),
        birth_time=time(14, 30),
        calendar=CalendarType("solar"),
        city="Seoul",
        gender=Gender("male"),
    )
    defaults.update(kwargs)
    return JsonExporter(SajuInput(**defaults)).generate_result().to_dict()


class TestManseolGolden:
    """고정 입력의 결정론 출력 회귀(골든) 검증"""

    def test_pillars_golden(self):
        """1990-05-15 14:30 서울 남성의 사주팔자 고정값"""
        d = _result()
        p = d["pillars"]
        assert p["year"]["ganji_korean"] == "경오"
        assert p["month"]["ganji_korean"] == "신사"
        assert p["day"]["ganji_korean"] == "경진"
        assert p["hour"]["ganji_korean"] == "계미"

    def test_day_master_and_strength_golden(self):
        d = _result()
        assert d["analysis"]["day_master"]["korean"] == "경"
        assert d["analysis"]["strength"]["level"] == "신강"


class TestInteractionsWiring:
    """합·충·형·파·해·공망 상호작용 노출 검증"""

    EXPECTED_KEYS = {
        "천간합",
        "천간충극",
        "지지육합",
        "지지삼합",
        "지지방합",
        "지지반합",
        "지지충",
        "지지형",
        "지지파",
        "지지해",
        "공망",
    }

    def test_interactions_present_with_all_categories(self):
        d = _result()
        assert "interactions" in d
        assert set(d["interactions"].keys()) == self.EXPECTED_KEYS

    def test_interaction_items_are_lists(self):
        d = _result()
        for key, items in d["interactions"].items():
            assert isinstance(items, list)


class TestSewunWiring:
    """세운(연운) 노출 검증"""

    def test_sewun_has_six_years(self):
        d = _result()
        assert "sewun" in d
        assert len(d["sewun"]) == 6

    def test_sewun_item_fields(self):
        d = _result()
        item = d["sewun"][0]
        for field in ("year", "ganji_korean", "ten_god", "twelve_phase"):
            assert field in item


class TestNoTimeRobustness:
    """시간 미상 입력이 크래시 없이 끝까지 계산되는지"""

    def test_no_time_calculation_succeeds(self):
        d = _result(birth_time=None)
        assert d["pillars"].get("hour") is None
        assert len(d["sewun"]) == 6
        assert len(d["interactions"]) == 11

    def test_no_time_enrich_succeeds(self):
        d = _result(birth_time=None)
        enr = enrich_with_analysis(d)
        assert "yongsin_recommendations" in enr


class TestEnrichWithAnalysis:
    """용신·유파·운세 분석 보강 검증"""

    def test_enrich_keys(self):
        enr = enrich_with_analysis(_result())
        for key in (
            "yongsin_comparison",
            "yongsin_recommendations",
            "school_comparison",
            "fortune_scores",
        ):
            assert key in enr

    def test_school_comparison_structure(self):
        sc = enrich_with_analysis(_result())["school_comparison"]
        assert len(sc["schools"]) == 5
        assert len(sc["interpretations"]) == 5
        assert 0.0 <= sc["confidence"] <= 1.0

    def test_fortune_scores_types(self):
        fs = enrich_with_analysis(_result())["fortune_scores"]
        assert set(fs.keys()) == {"general", "career", "wealth", "health", "love"}
        for item in fs.values():
            assert 0 <= item["score"] <= 100

    def test_yongsin_recommendations_shape(self):
        rec = enrich_with_analysis(_result())["yongsin_recommendations"]
        assert "primary_element" in rec
        assert "colors" in rec["primary_element"]


@pytest.mark.parametrize(
    "birth, gender, expected_day",
    [
        (date(2000, 1, 1), "male", "무오"),
        (date(1985, 8, 20), "female", "신묘"),
    ],
)
def test_additional_golden_day_pillars(birth, gender, expected_day):
    """추가 레퍼런스 일주 회귀(현재 엔진 출력 고정)"""
    d = _result(birth_date=birth, birth_time=time(12, 0), gender=Gender(gender))
    assert d["pillars"]["day"]["ganji_korean"] == expected_day
