"""
사주 4주(四柱) 계산 엔진
년주, 월주, 일주, 시주 산출
"""

from datetime import date, datetime, timedelta
from typing import Any

from config.constants import BRANCHES, STEMS
from manseol.core.calendar_converter import CalendarConverter
from manseol.core.solar_terms import SolarTermsCalculator
from manseol.data.stems_branches import StemBranchData


class PillarEngine:
    """사주 4주 계산 엔진"""

    def __init__(self):
        self.solar_terms = SolarTermsCalculator()
        self.calendar = CalendarConverter()

    def calculate_year_pillar(self, dt: datetime) -> tuple[int, int]:
        """
        년주(年柱) 계산

        입춘 기준으로 년주 결정
        - 입춘 이전: 전년도 간지
        - 입춘 이후: 해당 연도 간지

        Args:
            dt: 출생 일시

        Returns:
            (천간 인덱스, 지지 인덱스)
        """
        # 입춘 기준 연도
        year = self.solar_terms.get_year_by_ipchun(dt)

        # 갑자(甲子)년 기준점: 1984년
        # 1984년 = 갑자년 (천간 0, 지지 0)
        year_offset = year - 1984

        stem_index = year_offset % 10
        branch_index = year_offset % 12

        return stem_index, branch_index

    def calculate_month_pillar(self, dt: datetime) -> tuple[int, int]:
        """
        월주(月柱) 계산

        절기 기준으로 월주 결정
        년간(年干)에 따른 월간 계산 공식 적용

        Args:
            dt: 출생 일시

        Returns:
            (천간 인덱스, 지지 인덱스)
        """
        # 절기 기준 연월
        _, jeolgi_month = self.solar_terms.get_month_by_jeolgi(dt)

        # 년주 천간
        year_stem, _ = self.calculate_year_pillar(dt)

        # 월지: 절기월과 지지 인덱스 직접 매핑
        # jeolgi_month 1 = 소한 = 축월(1)
        # jeolgi_month 2 = 입춘 = 인월(2)
        # ...
        # jeolgi_month 11 = 입동 = 해월(11)
        # jeolgi_month 12 = 대설 = 자월(0)
        branch_index = jeolgi_month % 12

        # 월간 계산: 년간에 따른 월간 공식
        # 갑/기년: 병인월 시작 (병=2)
        # 을/경년: 무인월 시작 (무=4)
        # 병/신년: 경인월 시작 (경=6)
        # 정/임년: 임인월 시작 (임=8)
        # 무/계년: 갑인월 시작 (갑=0)
        year_stem_base = year_stem % 5
        month_stem_start = (year_stem_base * 2 + 2) % 10

        # 월간 = 시작 천간 + (월 - 2)
        # 참조: manseryeok의 월 번호 체계(1=인월)와 현재 체계(2=인월) 차이 보정
        stem_index = (month_stem_start + jeolgi_month - 2) % 10

        return stem_index, branch_index

    def calculate_day_pillar(self, dt: datetime) -> tuple[int, int]:
        """
        일주(日柱) 계산

        기준일로부터의 일수 계산

        Args:
            dt: 출생 일시

        Returns:
            (천간 인덱스, 지지 인덱스)
        """
        # 기준일: 1992년 10월 24일 = 계유일(癸酉日)
        # 천간 계(癸) = 9, 지지 유(酉) = 9
        # (manseryeok 라이브러리 검증 기준일)
        base_date = date(1992, 10, 24)
        base_stem = 9  # 계
        base_branch = 9  # 유

        target_date = dt.date() if isinstance(dt, datetime) else dt
        days_diff = (target_date - base_date).days

        stem_index = (base_stem + days_diff) % 10
        branch_index = (base_branch + days_diff) % 12

        return stem_index, branch_index

    def calculate_hour_pillar(self, dt: datetime, jajasi: bool = False) -> tuple[int, int]:
        """
        시주(時柱) 계산

        시간에 따른 지지 결정 후, 일간에 따른 천간 계산

        Args:
            dt: 출생 일시
            jajasi: 야자시/조자시 구분 (True면 23:00~24:00을 다음날로)

        Returns:
            (천간 인덱스, 지지 인덱스)
        """
        hour = dt.hour
        minute = dt.minute

        # 야자시/조자시 처리
        # jajasi=True: 23:00~24:00은 다음날 자시
        # jajasi=False: 23:00~24:00은 당일 자시
        day_stem, _ = self.calculate_day_pillar(dt)

        if jajasi and hour == 23:
            # 야자시: 23:00~24:00은 다음날로 취급
            next_day = dt + timedelta(days=1)
            day_stem, _ = self.calculate_day_pillar(next_day)

        # 시지 계산
        branch_index = StemBranchData.get_time_branch(hour, minute)

        # 시간 계산: 일간에 따른 시간 공식
        # 갑/기일: 갑자시 시작 (갑=0)
        # 을/경일: 병자시 시작 (병=2)
        # 병/신일: 무자시 시작 (무=4)
        # 정/임일: 경자시 시작 (경=6)
        # 무/계일: 임자시 시작 (임=8)
        day_stem_base = day_stem % 5
        hour_stem_start = (day_stem_base * 2) % 10

        stem_index = (hour_stem_start + branch_index) % 10

        return stem_index, branch_index

    def calculate_all_pillars(
        self, dt: datetime, jajasi: bool = False, include_hour: bool = True
    ) -> dict[str, tuple[int, int]]:
        """
        사주 4주 전체 계산

        Args:
            dt: 출생 일시
            jajasi: 야자시/조자시 옵션
            include_hour: 시주 포함 여부

        Returns:
            {
                "year": (천간, 지지),
                "month": (천간, 지지),
                "day": (천간, 지지),
                "hour": (천간, 지지) or None
            }
        """
        result = {
            "year": self.calculate_year_pillar(dt),
            "month": self.calculate_month_pillar(dt),
            "day": self.calculate_day_pillar(dt),
        }

        if include_hour:
            result["hour"] = self.calculate_hour_pillar(dt, jajasi)
        else:
            result["hour"] = None

        return result

    def get_pillar_details(self, stem_index: int, branch_index: int) -> dict[str, Any]:
        """
        주(柱) 상세 정보 반환

        Args:
            stem_index: 천간 인덱스
            branch_index: 지지 인덱스

        Returns:
            상세 정보 딕셔너리
        """
        stem = STEMS[stem_index]
        branch = BRANCHES[branch_index]

        return {
            "stem": {
                "index": stem_index,
                "korean": stem["korean"],
                "chinese": stem["chinese"],
                "element": stem["element"].value,
                "polarity": stem["polarity"].value,
            },
            "branch": {
                "index": branch_index,
                "korean": branch["korean"],
                "chinese": branch["chinese"],
                "element": branch["element"].value,
                "polarity": branch["polarity"].value,
                "animal": branch["animal"],
            },
            "ganji_korean": f"{stem['korean']}{branch['korean']}",
            "ganji_chinese": f"{stem['chinese']}{branch['chinese']}",
        }
