"""
내장 음력 데이터 모듈
한국천문연구원 데이터 기반 1900-2100년 음력 데이터

manseryeok 라이브러리 참조
"""

from datetime import date

# 1900-2100년 음력 데이터 (출처: 한국천문연구원)
# 각 16비트 값의 구조:
# - Bit 0-3: 윤달 위치 (0이면 윤달 없음)
# - Bit 4: 윤달 일수 (0=29일, 1=30일)
# - Bit 5-16: 각 월의 대소월 (0=29일, 1=30일)
LUNAR_DATA = [
    0x04BD8,
    0x04AE0,
    0x0A570,
    0x054D5,
    0x0D260,
    0x0D950,
    0x16554,
    0x056A0,
    0x09AD0,
    0x055D2,
    0x04AE0,
    0x0A5B6,
    0x0A4D0,
    0x0D250,
    0x1D255,
    0x0B540,
    0x0D6A0,
    0x0ADA2,
    0x095B0,
    0x14977,
    0x04970,
    0x0A4B0,
    0x0B4B5,
    0x06A50,
    0x06D40,
    0x1AB54,
    0x02B60,
    0x09570,
    0x052F2,
    0x04970,
    0x06566,
    0x0D4A0,
    0x0EA50,
    0x06E95,
    0x05AD0,
    0x02B60,
    0x186E3,
    0x092E0,
    0x1C8D7,
    0x0C950,
    0x0D4A0,
    0x1D8A6,
    0x0B550,
    0x056A0,
    0x1A5B4,
    0x025D0,
    0x092D0,
    0x0D2B2,
    0x0A950,
    0x0B557,
    0x06CA0,
    0x0B550,
    0x15355,
    0x04DA0,
    0x0A5B0,
    0x14573,
    0x052B0,
    0x0A9A8,
    0x0E950,
    0x06AA0,
    0x0AEA6,
    0x0AB50,
    0x04B60,
    0x0AAE4,
    0x0A570,
    0x05260,
    0x0F263,
    0x0D950,
    0x05B57,
    0x056A0,
    0x096D0,
    0x04DD5,
    0x04AD0,
    0x0A4D0,
    0x0D4D4,
    0x0D250,
    0x0D558,
    0x0B540,
    0x0B6A0,
    0x195A6,
    0x095B0,
    0x049B0,
    0x0A974,
    0x0A4B0,
    0x0B27A,
    0x06A50,
    0x06D40,
    0x0AF46,
    0x0AB60,
    0x09570,
    0x04AF5,
    0x04970,
    0x064B0,
    0x074A3,
    0x0EA50,
    0x06B58,
    0x055C0,
    0x0AB60,
    0x096D5,
    0x092E0,
    0x0C960,
    0x0D954,
    0x0D4A0,
    0x0DA50,
    0x07552,
    0x056A0,
    0x0ABB7,
    0x025D0,
    0x092D0,
    0x0CAB5,
    0x0A950,
    0x0B4A0,
    0x0BAA4,
    0x0AD50,
    0x055D9,
    0x04BA0,
    0x0A5B0,
    0x15176,
    0x052B0,
    0x0A930,
    0x07954,
    0x06AA0,
    0x0AD50,
    0x05B52,
    0x04B60,
    0x0A6E6,
    0x0A4E0,
    0x0D260,
    0x0EA65,
    0x0D530,
    0x05AA0,
    0x076A3,
    0x096D0,
    0x04AFB,
    0x04AD0,
    0x0A4D0,
    0x1D0B6,
    0x0D250,
    0x0D520,
    0x0DD45,
    0x0B5A0,
    0x056D0,
    0x055B2,
    0x049B0,
    0x0A577,
    0x0A4B0,
    0x0AA50,
    0x1B255,
    0x06D20,
    0x0ADA0,
    0x14B63,
    0x09370,
    0x049F8,
    0x04970,
    0x064B0,
    0x168A6,
    0x0EA50,
    0x06B20,
    0x1A6C4,
    0x0AAE0,
    0x0A2E0,
    0x0D2E3,
    0x0C960,
    0x0D557,
    0x0D4A0,
    0x0DA50,
    0x05D55,
    0x056A0,
    0x0A6D0,
    0x055D4,
    0x052D0,
    0x0A9B8,
    0x0A950,
    0x0B4A0,
    0x0B6A6,
    0x0AD50,
    0x055A0,
    0x0ABA4,
    0x0A5B0,
    0x052B0,
    0x0B273,
    0x06930,
    0x07337,
    0x06AA0,
    0x0AD50,
    0x14B55,
    0x04B60,
    0x0A570,
    0x054E4,
    0x0D160,
    0x0E968,
    0x0D520,
    0x0DAA0,
    0x16AA6,
    0x056D0,
    0x04AE0,
    0x0A9D4,
    0x0A2D0,
    0x0D150,
    0x0F252,
    0x0D520,
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
    return LUNAR_DATA[year - 1900] & 0xF


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


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> date:
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


def solar_to_lunar(year: int, month: int, day: int) -> tuple[int, int, int, bool]:
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
