"""
내장 음력 데이터 모듈
한국천문연구원 데이터 기반 1900-2100년 음력 데이터

manseryeok 라이브러리 참조
"""

from datetime import date, datetime
from typing import Tuple, Optional


# 1900-2100년 음력 데이터 (출처: 한국천문연구원)
# 각 16비트 값의 구조:
# - Bit 0-3: 윤달 위치 (0이면 윤달 없음)
# - Bit 4: 윤달 일수 (0=29일, 1=30일)
# - Bit 5-16: 각 월의 대소월 (0=29일, 1=30일)
LUNAR_DATA = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
    0x0d520,
]

# 기준일: 1900년 1월 31일 (양력)
BASE_DATE = date(1900, 1, 31)


def get_lunar_year_days(year: int) -> int:
    """
    음력 연도의 총 일수를 계산

    Args:
        year: 연도 (1900-2100)

    Returns:
        해당 연도의 총 일수
    """
    if year < 1900 or year > 2100:
        raise ValueError(f"지원하지 않는 연도: {year} (1900-2100만 지원)")

    total = 348  # 평년 기본 일수 (29일 * 12개월 = 348일)

    # 각 월의 대소월 여부를 비트 연산으로 확인
    # 비트 15-4 (12개월): 1이면 30일, 0이면 29일
    mask = 0x8000
    while mask > 0x8:
        if LUNAR_DATA[year - 1900] & mask:
            total += 1
        mask >>= 1

    return total + get_leap_month_days(year)


def get_leap_month(year: int) -> int:
    """
    음력 연도의 윤달 위치를 반환

    Args:
        year: 연도 (1900-2100)

    Returns:
        윤달 위치 (1-12), 없으면 0
    """
    return LUNAR_DATA[year - 1900] & 0xf


def get_leap_month_days(year: int) -> int:
    """
    음력 연도의 윤달 일수를 반환

    Args:
        year: 연도 (1900-2100)

    Returns:
        윤달 일수 (29 또는 30), 윤달 없으면 0
    """
    leap_month = get_leap_month(year)
    if leap_month:
        return 30 if LUNAR_DATA[year - 1900] & 0x10000 else 29
    return 0


def get_lunar_month_days(year: int, month: int) -> int:
    """
    음력 특정 월의 일수를 반환

    Args:
        year: 연도 (1900-2100)
        month: 월 (1-12)

    Returns:
        해당 월의 일수 (29 또는 30)
    """
    return 30 if LUNAR_DATA[year - 1900] & (0x10000 >> month) else 29


def lunar_to_solar(
    year: int,
    month: int,
    day: int,
    is_leap_month: bool = False
) -> date:
    """
    음력을 양력으로 변환

    Args:
        year: 음력 연도
        month: 음력 월
        day: 음력 일
        is_leap_month: 윤달 여부

    Returns:
        양력 날짜
    """
    if year < 1900 or year > 2100:
        raise ValueError(f"지원하지 않는 연도: {year} (1900-2100만 지원)")

    offset = 0

    # 1900년부터 해당 연도까지의 일수 계산
    for i in range(1900, year):
        offset += get_lunar_year_days(i)

    # 해당 연도의 월까지의 일수 계산
    leap_month = get_leap_month(year)
    is_leap = False

    for i in range(1, month):
        if leap_month > 0 and i == leap_month and not is_leap:
            offset += get_leap_month_days(year)
            is_leap = True
            continue

        if is_leap:
            offset += get_lunar_month_days(year, i)
        else:
            offset += get_lunar_month_days(year, i)

    # 윤달인 경우 처리
    if is_leap_month and leap_month == month:
        offset += get_lunar_month_days(year, month)

    # 일수 더하기
    offset += day - 1

    # 기준일로부터 offset일 후의 양력 날짜
    from datetime import timedelta
    solar_date = BASE_DATE + timedelta(days=offset)

    return solar_date


def solar_to_lunar(
    year: int,
    month: int,
    day: int
) -> Tuple[int, int, int, bool]:
    """
    양력을 음력으로 변환

    Args:
        year: 양력 연도
        month: 양력 월
        day: 양력 일

    Returns:
        (음력연, 음력월, 음력일, 윤달여부)
    """
    target_date = date(year, month, day)
    offset = (target_date - BASE_DATE).days

    if offset < 0:
        raise ValueError(f"지원하지 않는 날짜: {year}-{month}-{day} (1900-01-31 이후만 지원)")

    lunar_year = 1900
    remaining_days = offset

    # 음력 연도 계산
    for i in range(1900, 2101):
        year_days = get_lunar_year_days(i)
        if remaining_days < year_days:
            lunar_year = i
            break
        remaining_days -= year_days

    # 음력 월 계산
    leap_month = get_leap_month(lunar_year)
    lunar_month = 1
    is_leap_month = False

    for i in range(1, 13):
        month_days: int

        if leap_month > 0 and i == leap_month + 1 and not is_leap_month:
            month_days = get_leap_month_days(lunar_year)
            is_leap_month = True
            i -= 1
        else:
            month_days = get_lunar_month_days(lunar_year, i)
            is_leap_month = False

        if remaining_days < month_days:
            lunar_month = i
            break
        remaining_days -= month_days

    lunar_day = remaining_days + 1

    return lunar_year, lunar_month, lunar_day, is_leap_month


def is_supported_date(year: int) -> bool:
    """
    내장 음력 데이터로 지원되는 연도인지 확인

    Args:
        year: 연도

    Returns:
        지원 여부
    """
    return 1900 <= year <= 2100
