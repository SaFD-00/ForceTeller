"""절기 시각 절대 정합 회귀 테스트 — KASI 공표값 기준

과거 엔진은 (1) ephem이 naive datetime을 UTC로 해석하는데 KST 변환 없이
쓰고(−9h), (2) ephem.Ecliptic 기본값(J2000 분점) 황경을 써 세차만큼
어긋나(2024년 +8h·1990년 −3h) 절기 시각이 실제와 최대 ±12시간 어긋났다.
이 테스트는 수정 후 절기 시각이 공표 절입 시각과 ±2분 이내임을 고정한다.

## 기준 데이터 출처 (2026-07 수집)
- 2024년 24절기 절입시각(한국천문연구원 기반):
  https://bebeyam.com/사주-만세력-2024년-갑진년-24절기-절입시간-입춘-춘분-입/
- 역대 입춘 절입시각(1946~2023, 역서 기반):
  https://bebeyam.com/1946년-2021년-역대-입춘-시간-절입시간-모음/
- 2000년 24절기(NASA DE441 + KASI 특일정보 기반):
  https://uncle.tools/manse/solar-terms/2000
- 일진(일주 간지) 대조: https://uncle.tools/manse/calendar/{YYYY}/{MM}
- 표준시 변천·서머타임: https://ko.wikipedia.org/wiki/대한민국_표준시
  (1908 UTC+8:30 → 1912 UTC+9 → 1954.03.21 UTC+8:30 → 1961.08.10 UTC+9,
   서머타임 1948~1951·1955~1960·1987~1988)

## 시각 규약
절기 시각은 '해당 시점의 한국 표준시 벽시계'(서머타임 제외)로 반환한다.
현행은 KST(UTC+9)=KASI 공표값이고, 1954~1961(UTC+8:30) 시기는 당시 역서
공표 관례대로 30분을 뺀 당시 표준시다(1955 입춘 22:48, 1960 입춘 03:54).
"""

from datetime import datetime

import pytest

from manseol.calculator.pillar_engine import PillarEngine
from manseol.core.solar_terms import SolarTermsCalculator

# 절입 시각 판정 허용 오차(분): 공표값은 분 단위 반올림 + 탐색 정밀도 1분
TOLERANCE_MINUTES = 2.0


def _ganji(engine: PillarEngine, stem_idx: int, branch_idx: int) -> str:
    return engine.get_pillar_details(stem_idx, branch_idx)["ganji_korean"]


@pytest.fixture(scope="module")
def solar_terms() -> SolarTermsCalculator:
    return SolarTermsCalculator()


@pytest.fixture(scope="module")
def engine() -> PillarEngine:
    return PillarEngine()


class TestJeolgiAbsoluteAlignment:
    """절입 시각이 공표값(KST 또는 당시 표준시)과 ±2분 이내"""

    @pytest.mark.parametrize(
        "year, month, expected",
        [
            # 현행 KST(UTC+9) — KASI 공표값
            (1987, 2, datetime(1987, 2, 4, 17, 52)),  # 입춘
            (1988, 2, datetime(1988, 2, 4, 23, 43)),  # 입춘
            (1990, 2, datetime(1990, 2, 4, 11, 14)),  # 입춘
            (2000, 1, datetime(2000, 1, 6, 10, 0)),  # 소한
            (2000, 2, datetime(2000, 2, 4, 21, 40)),  # 입춘
            (2000, 3, datetime(2000, 3, 5, 15, 42)),  # 경칩
            (2024, 1, datetime(2024, 1, 6, 5, 49)),  # 소한
            (2024, 2, datetime(2024, 2, 4, 17, 27)),  # 입춘
            (2024, 3, datetime(2024, 3, 5, 11, 23)),  # 경칩
            (2024, 12, datetime(2024, 12, 7, 0, 17)),  # 대설
            # 1954~1961 UTC+8:30 시기 — 당시 역서 공표값(당시 표준시)
            (1955, 2, datetime(1955, 2, 4, 22, 48)),  # 입춘
            (1960, 2, datetime(1960, 2, 5, 3, 54)),  # 입춘
        ],
    )
    def test_jeolgi_matches_published_time(self, solar_terms, year, month, expected):
        got = solar_terms.get_jeolgi_for_month(year, month)
        diff_minutes = abs((got - expected).total_seconds()) / 60
        assert diff_minutes <= TOLERANCE_MINUTES, (
            f"{year}-{month:02d} 절입 {got} vs 공표 {expected} (차이 {diff_minutes:.1f}분)"
        )

    def test_era_wall_clock_is_kst_minus_30min(self, solar_terms):
        """UTC+8:30 시기 반환값 = KST 환산값 − 30분 (당시 표준시 규약)"""
        got = solar_terms.get_jeolgi_for_month(1955, 2)
        kst_equivalent = solar_terms._local_to_kst(got)
        assert (kst_equivalent - got).total_seconds() == 30 * 60


class TestIpchunBoundaryPillars:
    """입춘 절입 시각 전후 년주·월주 간지 판정 (보정 없는 KST 원시각 기준)

    과거 오프셋(1990년 −12.3h, 2000년 −9.2h, 2024년 −1.2h) 창 안의 시각을
    골라, 절대 정합 후에만 옳게 판정되는 케이스를 고정한다.
    """

    def test_1990_before_ipchun(self, engine):
        """1990-02-04 11:00 (입춘 11:14 직전): 기사년 정축월"""
        p = engine.calculate_all_pillars(datetime(1990, 2, 4, 11, 0))
        assert _ganji(engine, *p["year"]) == "기사"
        assert _ganji(engine, *p["month"]) == "정축"

    def test_1990_after_ipchun(self, engine):
        """1990-02-04 11:30 (입춘 11:14 직후): 경오년 무인월"""
        p = engine.calculate_all_pillars(datetime(1990, 2, 4, 11, 30))
        assert _ganji(engine, *p["year"]) == "경오"
        assert _ganji(engine, *p["month"]) == "무인"

    def test_2000_before_ipchun(self, engine):
        """2000-02-04 21:20 (입춘 21:40 직전): 기묘년 정축월"""
        p = engine.calculate_all_pillars(datetime(2000, 2, 4, 21, 20))
        assert _ganji(engine, *p["year"]) == "기묘"
        assert _ganji(engine, *p["month"]) == "정축"

    def test_2000_after_ipchun(self, engine):
        """2000-02-04 22:00 (입춘 21:40 직후): 경진년 무인월"""
        p = engine.calculate_all_pillars(datetime(2000, 2, 4, 22, 0))
        assert _ganji(engine, *p["year"]) == "경진"
        assert _ganji(engine, *p["month"]) == "무인"

    def test_2024_before_ipchun(self, engine):
        """2024-02-04 17:00 (입춘 17:27 직전): 계묘년 을축월"""
        p = engine.calculate_all_pillars(datetime(2024, 2, 4, 17, 0))
        assert _ganji(engine, *p["year"]) == "계묘"
        assert _ganji(engine, *p["month"]) == "을축"

    def test_2024_after_ipchun(self, engine):
        """2024-02-04 18:00 (입춘 17:27 직후): 갑진년 병인월"""
        p = engine.calculate_all_pillars(datetime(2024, 2, 4, 18, 0))
        assert _ganji(engine, *p["year"]) == "갑진"
        assert _ganji(engine, *p["month"]) == "병인"


class TestDayPillarAnchors:
    """일진(일주 간지) 독립 대조 — uncle.tools 만세력 달력

    일진은 시간대 규약과 무관한 만국 공통 60갑자 순환이라 독립 검증 앵커로
    쓴다. 출처: https://uncle.tools/manse/calendar/{YYYY}/{MM}
    """

    @pytest.mark.parametrize(
        "d, expected",
        [
            (datetime(1955, 5, 15), "병자"),
            (datetime(1988, 7, 27), "계미"),
            (datetime(1990, 2, 4), "경자"),
            (datetime(1990, 5, 15), "경진"),
            (datetime(1999, 12, 31), "정사"),
            (datetime(2000, 1, 1), "무오"),
            (datetime(2024, 2, 4), "무술"),
        ],
    )
    def test_day_pillar_anchor(self, engine, d, expected):
        assert _ganji(engine, *engine.calculate_day_pillar(d)) == expected


class TestHistoricalEraCharts:
    """서머타임·UTC+8:30 시기 4주 회귀 (진태양시 보정 포함 전체 경로)

    기대값 구성 근거: 검증된 절입 시각(위 클래스) + 검증된 일진 앵커 +
    오호둔(월간)·오서둔(시간) 공식. 보정값은 time_correction 규약
    (서머타임 −60분, 경도 보정, 균시차)을 따른다.
    """

    def _corrected_pillars(self, birth: datetime) -> dict[str, str]:
        from manseol.core.time_correction import TimeCorrector

        engine = PillarEngine()
        corrected, _ = TimeCorrector(birth).calculate_true_solar_time()
        raw = engine.calculate_all_pillars(corrected)
        return {k: _ganji(engine, *v) for k, v in raw.items() if v}

    def test_1988_summer_time_chart(self):
        """1988-07-27 14:00 서울(서머타임): 무진년 기미월 계미일 무오시

        벽시계 14:00 → DST −60분 → 13:00 → 경도 −32.1분 + 균시차 ≈ 12:21
        """
        p = self._corrected_pillars(datetime(1988, 7, 27, 14, 0))
        assert p == {"year": "무진", "month": "기미", "day": "계미", "hour": "무오"}

    def test_1955_utc830_dst_chart(self):
        """1955-05-15 12:00 서울(UTC+8:30 시기 + 서머타임): 을미년 신사월 병자일 갑오시

        벽시계 12:00 → DST −60분 → 11:00 → 경도 보정(기준 자오선 127.5,
        −2.1분) + 균시차(+3.8분) ≈ 11:02 → 오시
        """
        p = self._corrected_pillars(datetime(1955, 5, 15, 12, 0))
        assert p == {"year": "을미", "month": "신사", "day": "병자", "hour": "갑오"}
