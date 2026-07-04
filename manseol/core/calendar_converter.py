"""
음양력 변환 모듈
내장 음력 데이터 우선 사용, korean_lunar_calendar 라이브러리를 fallback으로 활용
"""

from datetime import date

from korean_lunar_calendar import KoreanLunarCalendar

from manseol.data.lunar_data import (
    is_supported_date,
)
from manseol.data.lunar_data import (
    lunar_to_solar as builtin_lunar_to_solar,
)
from manseol.data.lunar_data import (
    solar_to_lunar as builtin_solar_to_lunar,
)


class CalendarConverter:
    """음양력 변환 클래스"""

    def __init__(self):
        self.calendar = KoreanLunarCalendar()

    def lunar_to_solar(self, year: int, month: int, day: int, is_leap_month: bool = False) -> date:
        """
        음력 → 양력 변환

        내장 음력 데이터를 우선 사용하고, 지원 범위 외의 날짜는
        korean_lunar_calendar 라이브러리를 fallback으로 사용

        Args:
            year: 음력 연도
            month: 음력 월
            day: 음력 일
            is_leap_month: 윤달 여부

        Returns:
            양력 날짜
        """
        # 내장 데이터 지원 범위 (1900-2100) 내면 내장 데이터 사용
        if is_supported_date(year):
            try:
                return builtin_lunar_to_solar(year, month, day, is_leap_month)
            except (ValueError, IndexError):
                pass  # fallback to external library

        # fallback: korean_lunar_calendar 라이브러리
        self.calendar.setLunarDate(year, month, day, is_leap_month)
        return date(self.calendar.solarYear, self.calendar.solarMonth, self.calendar.solarDay)

    def solar_to_lunar(self, year: int, month: int, day: int) -> tuple[int, int, int, bool]:
        """
        양력 → 음력 변환

        내장 음력 데이터를 우선 사용하고, 지원 범위 외의 날짜는
        korean_lunar_calendar 라이브러리를 fallback으로 사용

        Args:
            year: 양력 연도
            month: 양력 월
            day: 양력 일

        Returns:
            (음력연, 음력월, 음력일, 윤달여부)
        """
        # 내장 데이터 지원 범위 (1900-2100) 내면 내장 데이터 사용
        if is_supported_date(year):
            try:
                return builtin_solar_to_lunar(year, month, day)
            except (ValueError, IndexError):
                pass  # fallback to external library

        # fallback: korean_lunar_calendar 라이브러리
        self.calendar.setSolarDate(year, month, day)
        return (
            self.calendar.lunarYear,
            self.calendar.lunarMonth,
            self.calendar.lunarDay,
            self.calendar.isIntercalation,
        )

    def get_lunar_date_info(self, solar_date: date) -> dict:
        """
        양력 날짜의 음력 정보 상세 반환

        Args:
            solar_date: 양력 날짜

        Returns:
            음력 정보 딕셔너리
        """
        self.calendar.setSolarDate(solar_date.year, solar_date.month, solar_date.day)

        return {
            "lunar_year": self.calendar.lunarYear,
            "lunar_month": self.calendar.lunarMonth,
            "lunar_day": self.calendar.lunarDay,
            "is_leap_month": self.calendar.isIntercalation,
            "gapja_year": self.calendar.getGapJaString(),
            "chinese_gapja_year": self.calendar.getChineseGapJaString(),
        }

    def get_gapja_string(self, solar_date: date) -> tuple[str, str]:
        """
        날짜의 간지 문자열 반환

        Args:
            solar_date: 양력 날짜

        Returns:
            (한글 간지, 한자 간지)
        """
        self.calendar.setSolarDate(solar_date.year, solar_date.month, solar_date.day)
        return (self.calendar.getGapJaString(), self.calendar.getChineseGapJaString())

    def is_leap_month(self, lunar_year: int, lunar_month: int) -> bool:
        """
        해당 음력 연월에 윤달이 있는지 확인

        Args:
            lunar_year: 음력 연도
            lunar_month: 음력 월

        Returns:
            윤달 존재 여부
        """
        # 해당 월의 윤달 존재 여부 확인
        try:
            self.calendar.setLunarDate(lunar_year, lunar_month, 1, True)
            # 변환 후 같은 달인지 확인
            return True
        except Exception:
            return False


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> date:
    """편의 함수: 음력 → 양력"""
    converter = CalendarConverter()
    return converter.lunar_to_solar(year, month, day, is_leap_month)


def solar_to_lunar(year: int, month: int, day: int) -> tuple[int, int, int, bool]:
    """편의 함수: 양력 → 음력"""
    converter = CalendarConverter()
    return converter.solar_to_lunar(year, month, day)
