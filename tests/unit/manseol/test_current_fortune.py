"""현재 운세(연운·월운·일운) 계산 단위 테스트 — current_fortune 모듈

calculate_current_fortune / calculate_fortune_ranges / now_kst 를 검증한다.
기준 시각은 항상 now 주입으로 결정론화한다(datetime.now() 의존 테스트 금지,
default-now 는 스모크 1개로만 구조를 확인).

## 골든 기준값 규약
- 간지(干支): KASI 만세력 표준값을 리터럴로 단언. 구현이 표준과 어긋나면
  테스트를 구현에 맞추지 않고 xfail(strict)로 고정 + 보고한다.
- month 라벨: 구현은 "달력 정렬" 넘버링을 쓴다(소한=1/축월, 입춘=2/인월, …,
  대설=12/자월 — pillar_engine·solar_terms docstring에 명시된 의도적 규약).
  KASI 표준이 정의하는 건 지지(인·묘·축·오)이며 그건 간지가 이미 단언하므로,
  month 정수는 구현 규약 값으로 단언한다. (규약차: 브리프 텍스트의
  "절기월 1(인월)/2(묘월)/12(축월)"은 전통 인월=1 넘버링을 쓴 것이고, 구현은
  달력정렬을 쓴다. 같은 브리프의 7월 골든 "오월=6"은 구현 달력정렬과 일치한다.)

천간 인덱스: 0갑 1을 2병 3정 4무 5기 6경 7신 8임 9계 (양=짝수, 음=홀수)
지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

from datetime import datetime

import pytest

from manseol.calculator.current_fortune import (
    calculate_current_fortune,
    calculate_fortune_ranges,
    now_kst,
)

# 공통 필수 필드(모든 연/월/일 항목)
COMMON_FIELDS = {
    "stem",
    "branch",
    "stem_hanja",
    "branch_hanja",
    "stem_index",
    "branch_index",
    "element",
    "ganji_korean",
    "ganji_chinese",
    "ten_god",
    "branch_ten_god",
    "twelve_phase",
}
ELEMENTS_KOREAN = {"목", "화", "토", "금", "수"}

# 십성·12운성 이론값은 일간 갑(0) 기준으로 단언(test_ten_gods 골든과 정합)
DAY_STEM_GAP = 0


class TestYearlyIpchunBoundary:
    """연운: 입춘 기준 연도 경계 (절기 시각에서 ±1일↑ 여유)"""

    def test_before_ipchun_stays_previous_year(self):
        """2025-02-02(입춘 2/3 이전): 연=갑진, 입춘 기준 연=2024"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 2, 2, 12, 0))
        assert r["yearly"]["ganji_korean"] == "갑진"
        assert r["yearly"]["ganji_chinese"] == "甲辰"
        assert r["yearly"]["year"] == 2024

    def test_after_ipchun_advances_year(self):
        """2025-02-05(입춘 이후): 연=을사, 입춘 기준 연=2025"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 2, 5, 12, 0))
        assert r["yearly"]["ganji_korean"] == "을사"
        assert r["yearly"]["ganji_chinese"] == "乙巳"
        assert r["yearly"]["year"] == 2025

    @pytest.mark.parametrize(
        "year, expected_ganji",
        [
            (2024, "갑진"),
            (2025, "을사"),
            (2026, "병오"),
        ],
    )
    def test_annual_ganji(self, year, expected_ganji):
        """연간지: 입춘 이후가 확실한 6/1 기준"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(year, 6, 1, 12, 0))
        assert r["yearly"]["ganji_korean"] == expected_ganji
        assert r["yearly"]["year"] == year


class TestMonthlyGyeongchipBoundary:
    """월운: 경칩 기준 인월→묘월 경계 (경칩 3/5, ±1일↑ 여유)"""

    def test_before_gyeongchip_is_muin(self):
        """2025-03-03(경칩 이전): 월주=무인(戊寅), 인월(month=2)"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 3, 3, 12, 0))
        m = r["monthly"]
        assert m["ganji_korean"] == "무인"
        assert m["ganji_chinese"] == "戊寅"
        assert m["branch_index"] == 2  # 인(寅)
        assert m["month"] == 2  # 달력정렬: 입춘=인월=2

    def test_after_gyeongchip_is_gimyo(self):
        """2025-03-07(경칩 이후): 월주=기묘(己卯), 묘월(month=3)"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 3, 7, 12, 0))
        m = r["monthly"]
        assert m["ganji_korean"] == "기묘"
        assert m["ganji_chinese"] == "己卯"
        assert m["branch_index"] == 3  # 묘(卯)
        assert m["month"] == 3  # 달력정렬: 경칩=묘월=3

    def test_after_ipchun_month_is_muin(self):
        """2025-02-05(입춘 이후): 월주=무인(戊寅), 인월(month=2)"""
        m = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 2, 5, 12, 0))["monthly"]
        assert m["ganji_korean"] == "무인"
        assert m["month"] == 2

    @pytest.mark.parametrize(
        "now",
        [
            datetime(2024, 12, 31, 12, 0),
            datetime(2025, 1, 1, 12, 0),
        ],
    )
    def test_jawol_persists_across_gregorian_newyear(self, now):
        """2024-12-31 vs 2025-01-01: 둘 다 자월 유지 → 월주=병자(丙子), month=12"""
        m = calculate_current_fortune(DAY_STEM_GAP, now)["monthly"]
        assert m["ganji_korean"] == "병자"
        assert m["ganji_chinese"] == "丙子"
        assert m["branch_index"] == 0  # 자(子)
        assert m["month"] == 12  # 달력정렬: 대설=자월=12

    def test_today_type_case_is_gabo(self):
        """2026-07-05 12:00(소서 7/7 이전): 월주=갑오(甲午), 오월(month=6)"""
        m = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))["monthly"]
        assert m["ganji_korean"] == "갑오"
        assert m["branch_index"] == 6  # 오(午)
        assert m["month"] == 6  # 달력정렬: 망종=오월=6


class TestChukwolMonthStemBug:
    """축월(소한~입춘, month=1) 월간 -2 오차 — pillar_engine 코어 버그.

    KASI 오호둔: 갑진년 축월=정축(丁丑). 구현은 을축(乙丑)으로 천간 -2.
    근본 원인: 축월은 절기 시퀀스상 자월(month=12) 다음(13번째)인데 달력정렬
    넘버링이 month=1로 wrap하고, 월간 공식 (month_stem_start + jeolgi_month - 2)이
    그 wrap을 보정하지 못한다. current_fortune 국소 버그가 아니라
    calculate_month_pillar(출생 사주 공통 경로) 버그이며 모든 축월 월주에 영향.
    """

    def test_chukwol_branch_is_correct(self):
        """지지(축)는 정확 — 버그는 천간에 국한"""
        m = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 2, 2, 12, 0))["monthly"]
        assert m["branch_index"] == 1  # 축(丑)
        assert m["month"] == 1  # 달력정렬: 소한=축월=1

    def test_chukwol_stem_matches_kasi(self):
        """KASI 표준: 2025-02-02(갑진년 축월) 월주=정축 (축월 월간 wrap 버그 회귀 방지)"""
        m = calculate_current_fortune(DAY_STEM_GAP, datetime(2025, 2, 2, 12, 0))["monthly"]
        assert m["ganji_korean"] == "정축"


class TestDailyAnchors:
    """일운: 60갑자 앵커(1992-10-24 계유 기준) 일진"""

    @pytest.mark.parametrize(
        "now, expected_ganji, expected_chinese",
        [
            (datetime(2000, 1, 1, 12, 0), "무오", "戊午"),
            (datetime(2026, 7, 5, 12, 0), "경진", "庚辰"),
        ],
    )
    def test_daily_ganji(self, now, expected_ganji, expected_chinese):
        """일진 앵커 검증"""
        d = calculate_current_fortune(DAY_STEM_GAP, now)["daily"]
        assert d["ganji_korean"] == expected_ganji
        assert d["ganji_chinese"] == expected_chinese
        assert d["date"] == now.date().isoformat()


class TestDecorations:
    """십성·12운성 장식 — 일간 갑(0) 이론값 (2026-07-05 기준)

    갑(甲, 양목) 일간 기준:
      - 천간 병(丙)=식신(목생화·양), 천간 갑=비견(동일)
      - 지지 오(午) 본기 정(丁·음화) → 상관(목생화·이음양)
      - 12운성: 갑 양간 장생은 해(亥). 오(午)까지 거리 7 → '사'
    """

    def test_yearly_byeongo_decorations(self):
        """연운 병오(丙午): ten_god=식신, branch_ten_god=상관, 12운성=사"""
        y = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))["yearly"]
        assert y["ganji_korean"] == "병오"
        assert y["ten_god"] == "식신"
        assert y["branch_ten_god"] == "상관"
        assert y["twelve_phase"] == "사"
        assert y["element"] == "화"  # 병(丙) 오행 = 화

    def test_monthly_gabo_decorations(self):
        """월운 갑오(甲午): ten_god=비견, branch_ten_god=상관, 12운성=사"""
        m = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))["monthly"]
        assert m["ganji_korean"] == "갑오"
        assert m["ten_god"] == "비견"
        assert m["branch_ten_god"] == "상관"
        assert m["twelve_phase"] == "사"
        assert m["element"] == "목"  # 갑(甲) 오행 = 목


class TestContract:
    """구조 계약: 필수 필드·element 한글·ganji_korean 합성"""

    def test_top_level_keys(self):
        """최상위: reference_datetime / yearly / monthly / daily"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))
        assert set(r) == {"reference_datetime", "yearly", "monthly", "daily"}

    def test_required_fields_present(self):
        """각 항목에 공통 필수 필드 + 고유 라벨 존재"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))
        assert COMMON_FIELDS <= set(r["yearly"])
        assert COMMON_FIELDS <= set(r["monthly"])
        assert COMMON_FIELDS <= set(r["daily"])
        assert "year" in r["yearly"]
        assert {"year", "month"} <= set(r["monthly"])
        assert "date" in r["daily"]

    def test_element_is_korean(self):
        """element 는 한글 오행(목/화/토/금/수)"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))
        for key in ("yearly", "monthly", "daily"):
            assert r[key]["element"] in ELEMENTS_KOREAN

    def test_ganji_korean_is_stem_plus_branch(self):
        """ganji_korean = stem + branch, ganji_chinese = stem_hanja + branch_hanja"""
        r = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 5, 12, 0))
        for key in ("yearly", "monthly", "daily"):
            entry = r[key]
            assert entry["ganji_korean"] == entry["stem"] + entry["branch"]
            assert entry["ganji_chinese"] == entry["stem_hanja"] + entry["branch_hanja"]

    def test_reference_datetime_matches_injected_now(self):
        """reference_datetime 은 주입 now 의 ISO 표기와 일치"""
        now = datetime(2026, 7, 5, 12, 0)
        r = calculate_current_fortune(DAY_STEM_GAP, now)
        assert r["reference_datetime"] == now.isoformat()


class TestFortuneRanges:
    """calculate_fortune_ranges: 슬라이더용 연/월/일 범위 계약"""

    NOW = datetime(2026, 7, 5, 12, 0)

    def test_counts(self):
        """개수: yearly 11 / monthly 12 / daily 15"""
        ranges = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)
        assert len(ranges["yearly"]) == 11
        assert len(ranges["monthly"]) == 12
        assert len(ranges["daily"]) == 15

    def test_yearly_center_matches_current(self):
        """yearly 중앙(index 5)이 current_fortune.yearly 와 동일"""
        current = calculate_current_fortune(DAY_STEM_GAP, self.NOW)
        ranges = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)
        assert ranges["yearly"][5] == current["yearly"]

    def test_daily_center_matches_current(self):
        """daily 중앙(index 7, ±7일)이 current_fortune.daily 와 동일"""
        current = calculate_current_fortune(DAY_STEM_GAP, self.NOW)
        ranges = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)
        assert ranges["daily"][7] == current["daily"]

    def test_monthly_entry_matches_midmonth_reference(self):
        """monthly 는 매월 15일 기준 샘플. 7월 항목은 datetime(연,7,15) 월운과 일치.

        now(7/5, 소서 이전)의 monthly(갑오)와는 다를 수 있다 — ranges 는 각 달
        15일을 기준으로 잡기 때문(7/15는 소서 이후 → 을미). 브리프는 monthly 중앙=
        current 를 요구하지 않으므로(yearly·daily 만), 실제 계약인 15일 기준
        참조와의 일치를 검증한다. calendar_month 필드가 추가돼 dict 통째 비교는 불가.
        """
        midmonth = calculate_current_fortune(DAY_STEM_GAP, datetime(2026, 7, 15))["monthly"]
        july = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)["monthly"][6]  # 7월
        assert july["ganji_korean"] == midmonth["ganji_korean"]
        assert july["month"] == midmonth["month"]
        assert july["calendar_month"] == 7

    def test_calendar_month_covers_1_to_12(self):
        """monthly.calendar_month 가 1~12 전수"""
        ranges = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)
        assert [m["calendar_month"] for m in ranges["monthly"]] == list(range(1, 13))

    def test_entry_field_contract(self):
        """범위 항목도 동일 필드 계약(yearly/daily 공통 필드, monthly 는 calendar_month 추가)"""
        ranges = calculate_fortune_ranges(DAY_STEM_GAP, self.NOW)
        for y in ranges["yearly"]:
            assert COMMON_FIELDS <= set(y)
            assert "year" in y
            assert y["element"] in ELEMENTS_KOREAN
            assert y["ganji_korean"] == y["stem"] + y["branch"]
        for m in ranges["monthly"]:
            assert COMMON_FIELDS <= set(m)
            assert {"year", "month", "calendar_month"} <= set(m)
        for d in ranges["daily"]:
            assert COMMON_FIELDS <= set(d)
            assert "date" in d


class TestDefaultNow:
    """default-now 스모크: 예외 없이 구조만 반환(값 단언 금지 — 벽시계 의존)"""

    def test_now_kst_is_naive(self):
        """now_kst() 는 naive(tzinfo 없음) datetime"""
        assert now_kst().tzinfo is None

    def test_current_fortune_default_now_returns_structure(self):
        """now 미주입 시 예외 없이 계약 dict 반환"""
        r = calculate_current_fortune(DAY_STEM_GAP)
        assert set(r) == {"reference_datetime", "yearly", "monthly", "daily"}
        assert COMMON_FIELDS <= set(r["yearly"])
        # reference_datetime 은 파싱 가능한 ISO 문자열
        assert datetime.fromisoformat(r["reference_datetime"]) is not None

    def test_fortune_ranges_default_now_returns_structure(self):
        """now 미주입 시 범위도 예외 없이 개수 계약 유지"""
        ranges = calculate_fortune_ranges(DAY_STEM_GAP)
        assert len(ranges["yearly"]) == 11
        assert len(ranges["monthly"]) == 12
        assert len(ranges["daily"]) == 15
