"""
한국 표준시(KST) 변천사 데이터
역사적 시간대 변경 및 일광절약시간(DST) 정보
"""

from datetime import date, datetime, timedelta

# KST 표준시 변천 역사
# (시작일, 종료일, 표준 자오선 경도, UTC 오프셋)
KST_HISTORY = [
    # 대한제국 시대 (1908.04.01 ~ 1911.12.31)
    (date(1908, 4, 1), date(1911, 12, 31), 127.5, 8.5),
    # 일제강점기 및 초기 대한민국 (1912.01.01 ~ 1954.03.20)
    (date(1912, 1, 1), date(1954, 3, 20), 135.0, 9.0),
    # 이승만 정부 변경 (1954.03.21 ~ 1961.08.09)
    (date(1954, 3, 21), date(1961, 8, 9), 127.5, 8.5),
    # 현재 표준시 (1961.08.10 ~ 현재)
    (date(1961, 8, 10), date(9999, 12, 31), 135.0, 9.0),
]

# 일광절약시간(서머타임) 시행 기간
# (시작일, 종료일) - 1시간 추가
DST_PERIODS = [
    # 1948년
    (datetime(1948, 6, 1, 0, 0), datetime(1948, 9, 12, 23, 59)),
    # 1949년
    (datetime(1949, 4, 3, 0, 0), datetime(1949, 9, 10, 23, 59)),
    # 1950년
    (datetime(1950, 4, 1, 0, 0), datetime(1950, 9, 9, 23, 59)),
    # 1951년
    (datetime(1951, 5, 6, 0, 0), datetime(1951, 9, 8, 23, 59)),
    # 1955년
    (datetime(1955, 5, 5, 0, 0), datetime(1955, 9, 8, 23, 59)),
    # 1956년
    (datetime(1956, 5, 20, 0, 0), datetime(1956, 9, 29, 23, 59)),
    # 1957년
    (datetime(1957, 5, 5, 0, 0), datetime(1957, 9, 21, 23, 59)),
    # 1958년
    (datetime(1958, 5, 4, 0, 0), datetime(1958, 9, 20, 23, 59)),
    # 1959년
    (datetime(1959, 5, 3, 0, 0), datetime(1959, 9, 19, 23, 59)),
    # 1960년
    (datetime(1960, 5, 1, 0, 0), datetime(1960, 9, 17, 23, 59)),
    # 1987년
    (datetime(1987, 5, 10, 2, 0), datetime(1987, 10, 11, 2, 59)),
    # 1988년 (서울 올림픽)
    (datetime(1988, 5, 8, 2, 0), datetime(1988, 10, 9, 2, 59)),
]


class KSTHistory:
    """한국 표준시 역사 데이터 접근 클래스"""

    @staticmethod
    def get_standard_meridian(dt: datetime) -> float:
        """
        특정 시점의 표준시 자오선 경도 반환

        Args:
            dt: 확인할 날짜/시간

        Returns:
            표준시 자오선 경도 (127.5 또는 135.0)
        """
        d = dt.date() if isinstance(dt, datetime) else dt

        for start, end, meridian, _ in KST_HISTORY:
            if start <= d <= end:
                return meridian

        # 기본값: 현재 표준시
        return 135.0

    @staticmethod
    def get_utc_offset(dt: datetime) -> float:
        """
        특정 시점의 UTC 오프셋 반환 (시간 단위)

        Args:
            dt: 확인할 날짜/시간

        Returns:
            UTC 오프셋 (8.5 또는 9.0)
        """
        d = dt.date() if isinstance(dt, datetime) else dt

        for start, end, _, offset in KST_HISTORY:
            if start <= d <= end:
                return offset

        return 9.0

    @staticmethod
    def is_dst_period(dt: datetime) -> bool:
        """
        일광절약시간 적용 기간인지 확인

        Args:
            dt: 확인할 날짜/시간

        Returns:
            DST 적용 여부
        """
        for start, end in DST_PERIODS:
            if start <= dt <= end:
                return True
        return False

    @staticmethod
    def get_dst_offset(dt: datetime) -> int:
        """
        일광절약시간 오프셋 반환 (분 단위)

        Args:
            dt: 확인할 날짜/시간

        Returns:
            DST 오프셋 (60분 또는 0분)
        """
        if KSTHistory.is_dst_period(dt):
            return 60  # 1시간 = 60분
        return 0

    @staticmethod
    def adjust_for_dst(dt: datetime) -> datetime:
        """
        일광절약시간 보정 적용

        DST 기간 중 시계 시간에서 1시간을 빼서 실제 표준시로 변환

        Args:
            dt: 시계 시간 (DST 적용된 시간)

        Returns:
            표준시 기준 시간
        """
        if KSTHistory.is_dst_period(dt):
            return dt - timedelta(hours=1)
        return dt


def get_standard_meridian(dt: datetime) -> float:
    """편의 함수: 표준시 자오선 경도 반환"""
    return KSTHistory.get_standard_meridian(dt)
