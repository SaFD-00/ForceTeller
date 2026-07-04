"""
24절기 계산 모듈
태양 황경 기반 절기 계산
"""

from datetime import datetime

from config.constants import SOLAR_TERMS

from .astronomical import AstronomicalCalculator


class SolarTermsCalculator:
    """24절기 계산 클래스"""

    def __init__(self):
        self.astro = AstronomicalCalculator()

        # 절기 순서 (절기만, 중기 제외)
        # 월 구분에 사용되는 절기 (0=입춘, 2=경칩, ...)
        self.jeolgi_indices = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

    def get_solar_term_for_date(self, dt: datetime) -> tuple[str, int]:
        """
        특정 날짜의 절기 정보 반환

        Args:
            dt: 확인할 날짜

        Returns:
            (절기명, 절기 인덱스)
        """
        sun_lon = self.astro.get_sun_longitude(dt)

        # 황경을 절기 인덱스로 변환
        # 춘분(0도) 기준, 15도마다 절기 변경
        # 입춘 = 315도
        term_index = int((sun_lon + 45) / 15) % 24

        return SOLAR_TERMS[term_index]["korean"], term_index

    def get_jeolgi_for_month(self, year: int, month: int) -> datetime:
        """
        특정 연월의 절기(節氣) 시각 계산

        절기는 월의 시작을 결정함
        - 1월: 소한 (황경 285도)
        - 2월: 입춘 (황경 315도)
        - 3월: 경칩 (황경 345도)
        - 등등...

        Args:
            year: 연도
            month: 월 (1-12)

        Returns:
            해당 월의 절기 시각
        """
        # 월별 절기 황경
        # 2월(인월) = 입춘 315도 기준
        # month 1 = 소한(285), month 2 = 입춘(315), ...
        jeolgi_longitudes = {
            1: 285,  # 소한
            2: 315,  # 입춘
            3: 345,  # 경칩
            4: 15,  # 청명
            5: 45,  # 입하
            6: 75,  # 망종
            7: 105,  # 소서
            8: 135,  # 입추
            9: 165,  # 백로
            10: 195,  # 한로
            11: 225,  # 입동
            12: 255,  # 대설
        }

        target_lon = jeolgi_longitudes[month]

        # 해당 연월 근처에서 검색 시작
        # 절기는 보통 월 초순에 있음
        if month >= 2:
            start = datetime(year, month - 1, 20)
        else:
            start = datetime(year - 1, 12, 20)

        return self.astro.find_sun_longitude_time(target_lon, start)

    def get_all_jeolgi_for_year(self, year: int) -> list[dict]:
        """
        해당 연도의 모든 절기 시각 계산

        Args:
            year: 연도

        Returns:
            [{month, name, datetime}, ...]
        """
        result = []
        for month in range(1, 13):
            jeolgi_dt = self.get_jeolgi_for_month(year, month)
            result.append(
                {"month": month, "name": self._get_jeolgi_name(month), "datetime": jeolgi_dt}
            )
        return result

    def _get_jeolgi_name(self, month: int) -> str:
        """월에 해당하는 절기명 반환"""
        jeolgi_names = {
            1: "소한",
            2: "입춘",
            3: "경칩",
            4: "청명",
            5: "입하",
            6: "망종",
            7: "소서",
            8: "입추",
            9: "백로",
            10: "한로",
            11: "입동",
            12: "대설",
        }
        return jeolgi_names.get(month, "")

    def get_month_by_jeolgi(self, dt: datetime) -> tuple[int, int]:
        """
        절기 기준 월 계산 (사주 월주 산출용)

        절기가 지나야 해당 월로 넘어감

        Args:
            dt: 확인할 날짜

        Returns:
            (절기 기준 연도, 절기 기준 월)
        """
        year = dt.year

        # 해당 연도와 전년도의 절기 시각 가져오기
        for month in range(12, 0, -1):
            check_year = year if month >= 2 else year
            if month == 1:
                # 소한(1월 절기)은 해당 연도에 있음
                check_year = year

            jeolgi_dt = self.get_jeolgi_for_month(check_year, month)

            if dt >= jeolgi_dt:
                # 연도 조정: 입춘(2월) 이전이면 전년도
                result_year = check_year
                if month == 1:
                    result_year = year
                elif month >= 2:
                    result_year = check_year

                return result_year, month

        # 입춘 이전이면 전년도 12월 (대설 이후)
        return year - 1, 12

    def get_year_by_ipchun(self, dt: datetime) -> int:
        """
        입춘 기준 연도 계산

        입춘이 지나야 새해로 넘어감 (년주 계산용)

        Args:
            dt: 확인할 날짜

        Returns:
            입춘 기준 연도
        """
        year = dt.year
        ipchun = self.get_jeolgi_for_month(year, 2)  # 입춘

        if dt < ipchun:
            return year - 1
        return year


def get_month_by_jeolgi(dt: datetime) -> tuple[int, int]:
    """편의 함수: 절기 기준 월 계산"""
    calc = SolarTermsCalculator()
    return calc.get_month_by_jeolgi(dt)


def get_year_by_ipchun(dt: datetime) -> int:
    """편의 함수: 입춘 기준 연도"""
    calc = SolarTermsCalculator()
    return calc.get_year_by_ipchun(dt)
