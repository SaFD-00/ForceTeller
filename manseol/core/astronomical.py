"""
천문 계산 모듈
ephem 라이브러리를 활용한 천문 계산

시각 규약: 이 모듈의 모든 datetime 입출력은 naive KST(UTC+9)다.
엔진 전체가 naive dt를 KST로 취급하는 규약(current_fortune.now_kst 참조)을
따르며, ephem은 내부적으로 UTC만 다루므로 경계에서 반드시 변환한다.
(과거 이 변환이 없어 절기 시각이 UTC로 반환되던 것이 '~9h 오프셋'의 원인 1)

황경 규약: 절기는 '그 시점(of-date) 진분점 기준 시태양 황경'으로 정의된다
(KASI·자오선 관례 동일). ephem.Ecliptic(body)는 기본적으로 J2000 분점 기준
좌표를 반환해 세차(약 50.3″/년)만큼 어긋난 황경을 주며, 이는 2024년 기준
약 8시간의 절기 시각 오차를 만든다('~9h 오프셋'의 원인 2). 따라서 겉보기
지심 적경/적위(g_ra/g_dec)를 관측 시점 분점으로 해석해 황경을 얻는다.
"""

from datetime import datetime, timedelta

import ephem

# 엔진의 naive datetime 규약(KST, UTC+9)과 ephem(UTC) 사이 변환 오프셋
KST_UTC_OFFSET = timedelta(hours=9)


class AstronomicalCalculator:
    """천문 계산 클래스 (입출력 datetime은 naive KST)"""

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

    @staticmethod
    def _kst_to_utc(dt: datetime) -> datetime:
        """naive KST → naive UTC"""
        return dt - KST_UTC_OFFSET

    @staticmethod
    def _utc_to_kst(dt: datetime) -> datetime:
        """naive UTC → naive KST"""
        return dt + KST_UTC_OFFSET

    @staticmethod
    def _apparent_ecliptic_longitude(body, when: "ephem.Date") -> float:
        """겉보기 지심 좌표(g_ra/g_dec)를 of-date 분점으로 해석한 황경(도)

        절기 정의(시태양 황경)와 일치시키기 위해 J2000이 아닌 관측 시점
        분점을 사용한다. 검증: KASI 공표 입춘 시각(1990/2000/2024)에서
        본 계산의 황경이 315.000°±0.0002° 이내.
        """
        equatorial = ephem.Equatorial(body.g_ra, body.g_dec, epoch=when)
        return float(ephem.Ecliptic(equatorial).lon) * 180 / ephem.pi

    def get_sun_longitude(self, dt: datetime) -> float:
        """
        태양 황경(黃經) 계산 — of-date 분점 기준 겉보기 황경

        Args:
            dt: 계산 시점 (naive KST)

        Returns:
            태양 황경 (도 단위, 0-360)
        """
        when = ephem.Date(self._kst_to_utc(dt))
        sun = ephem.Sun(when)
        return self._apparent_ecliptic_longitude(sun, when)

    def get_moon_longitude(self, dt: datetime) -> float:
        """
        달 황경 계산 — of-date 분점 기준 겉보기 황경

        Args:
            dt: 계산 시점 (naive KST)

        Returns:
            달 황경 (도 단위, 0-360)
        """
        when = ephem.Date(self._kst_to_utc(dt))
        moon = ephem.Moon(when)
        return self._apparent_ecliptic_longitude(moon, when)

    def find_sun_longitude_time(
        self, target_longitude: float, start_dt: datetime, precision_minutes: float = 1.0
    ) -> datetime:
        """
        태양이 특정 황경에 도달하는 시각 찾기

        Args:
            target_longitude: 목표 황경 (도)
            start_dt: 검색 시작 시점 (naive KST)
            precision_minutes: 정밀도 (분)

        Returns:
            목표 황경 도달 시각 (naive KST)
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
            dt: 기준 날짜 (naive KST)

        Returns:
            신월 시각 (naive KST)
        """
        date = ephem.Date(self._kst_to_utc(dt))
        next_new = ephem.next_new_moon(date)
        return self._utc_to_kst(ephem.Date(next_new).datetime())

    def get_previous_new_moon(self, dt: datetime) -> datetime:
        """
        주어진 날짜 이전 가장 가까운 신월 시각

        Args:
            dt: 기준 날짜 (naive KST)

        Returns:
            신월 시각 (naive KST)
        """
        date = ephem.Date(self._kst_to_utc(dt))
        prev_new = ephem.previous_new_moon(date)
        return self._utc_to_kst(ephem.Date(prev_new).datetime())

    def get_full_moon(self, dt: datetime) -> datetime:
        """
        주어진 날짜 이후 첫 번째 보름(망) 시각

        Args:
            dt: 기준 날짜 (naive KST)

        Returns:
            보름 시각 (naive KST)
        """
        date = ephem.Date(self._kst_to_utc(dt))
        next_full = ephem.next_full_moon(date)
        return self._utc_to_kst(ephem.Date(next_full).datetime())


def get_sun_longitude(dt: datetime) -> float:
    """편의 함수: 태양 황경 계산 (dt는 naive KST)"""
    calc = AstronomicalCalculator()
    return calc.get_sun_longitude(dt)
