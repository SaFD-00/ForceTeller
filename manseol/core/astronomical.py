"""
천문 계산 모듈
ephem 라이브러리를 활용한 천문 계산
"""

from datetime import datetime, timedelta

import ephem


class AstronomicalCalculator:
    """천문 계산 클래스"""

    def __init__(self, latitude: float = 37.5665, longitude: float = 126.9780):
        """
        Args:
            latitude: 관측 위도 (기본: 서울)
            longitude: 관측 경도 (기본: 서울)
        """
        self.observer = ephem.Observer()
        self.observer.lat = str(latitude)
        self.observer.lon = str(longitude)
        self.observer.elevation = 0

    def get_sun_longitude(self, dt: datetime) -> float:
        """
        태양 황경(黃經) 계산

        Args:
            dt: 계산 시점

        Returns:
            태양 황경 (도 단위, 0-360)
        """
        self.observer.date = ephem.Date(dt)
        sun = ephem.Sun(self.observer)
        # ecliptic longitude in radians -> degrees
        ecl = ephem.Ecliptic(sun)
        return float(ecl.lon) * 180 / ephem.pi

    def get_moon_longitude(self, dt: datetime) -> float:
        """
        달 황경 계산

        Args:
            dt: 계산 시점

        Returns:
            달 황경 (도 단위, 0-360)
        """
        self.observer.date = ephem.Date(dt)
        moon = ephem.Moon(self.observer)
        ecl = ephem.Ecliptic(moon)
        return float(ecl.lon) * 180 / ephem.pi

    def find_sun_longitude_time(
        self, target_longitude: float, start_dt: datetime, precision_minutes: float = 1.0
    ) -> datetime:
        """
        태양이 특정 황경에 도달하는 시각 찾기

        Args:
            target_longitude: 목표 황경 (도)
            start_dt: 검색 시작 시점
            precision_minutes: 정밀도 (분)

        Returns:
            목표 황경 도달 시각
        """
        # 이진 탐색으로 시각 찾기
        dt = start_dt
        step = timedelta(days=1)

        # 대략적인 위치 찾기
        while True:
            current_lon = self.get_sun_longitude(dt)
            next_lon = self.get_sun_longitude(dt + step)

            # 목표 황경이 현재와 다음 사이에 있는지 확인
            # 360도 경계 처리
            if current_lon > 270 and next_lon < 90:
                # 360도 경계를 넘는 경우
                if target_longitude > 270 or target_longitude < 90:
                    if current_lon <= target_longitude or target_longitude <= next_lon:
                        break
            elif current_lon <= target_longitude <= next_lon:
                break
            elif current_lon >= target_longitude >= next_lon:
                break

            dt += step
            if dt > start_dt + timedelta(days=400):
                raise ValueError(f"Cannot find sun longitude {target_longitude}")

        # 정밀 탐색
        low, high = dt, dt + step
        precision = timedelta(minutes=precision_minutes)

        while high - low > precision:
            mid = low + (high - low) / 2
            mid_lon = self.get_sun_longitude(mid)

            # 360도 경계 처리
            if target_longitude > 270 and mid_lon < 90:
                mid_lon += 360
            if target_longitude < 90 and mid_lon > 270:
                target_longitude_adj = target_longitude + 360
            else:
                target_longitude_adj = target_longitude

            if mid_lon < target_longitude_adj:
                low = mid
            else:
                high = mid

        return low + (high - low) / 2

    def get_new_moon(self, dt: datetime) -> datetime:
        """
        주어진 날짜 이후 첫 번째 신월(합삭) 시각

        Args:
            dt: 기준 날짜

        Returns:
            신월 시각
        """
        date = ephem.Date(dt)
        next_new = ephem.next_new_moon(date)
        return ephem.Date(next_new).datetime()

    def get_previous_new_moon(self, dt: datetime) -> datetime:
        """
        주어진 날짜 이전 가장 가까운 신월 시각

        Args:
            dt: 기준 날짜

        Returns:
            신월 시각
        """
        date = ephem.Date(dt)
        prev_new = ephem.previous_new_moon(date)
        return ephem.Date(prev_new).datetime()

    def get_full_moon(self, dt: datetime) -> datetime:
        """
        주어진 날짜 이후 첫 번째 보름(망) 시각

        Args:
            dt: 기준 날짜

        Returns:
            보름 시각
        """
        date = ephem.Date(dt)
        next_full = ephem.next_full_moon(date)
        return ephem.Date(next_full).datetime()


def get_sun_longitude(dt: datetime) -> float:
    """편의 함수: 태양 황경 계산"""
    calc = AstronomicalCalculator()
    return calc.get_sun_longitude(dt)
