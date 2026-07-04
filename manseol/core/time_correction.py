"""
시간 보정 모듈
진태양시(真太陽時) 계산을 위한 시간 보정

T_saju = T_clock - T_DST + ΔT_long + E

- T_clock: 시계 시간
- T_DST: 일광절약시간 보정
- ΔT_long: 경도 보정 = (Longitude - StandardMeridian) × 4분
- E: 균시차 (Equation of Time)
"""

import math
from datetime import datetime, timedelta

from manseol.data.city_coordinates import CityCoordinates
from manseol.data.kst_history import KSTHistory


class TimeCorrector:
    """시간 보정 클래스"""

    def __init__(
        self, birth_datetime: datetime, longitude: float | None = None, city: str = "Seoul"
    ):
        """
        Args:
            birth_datetime: 출생 일시 (시계 시간)
            longitude: 출생지 경도 (직접 지정시)
            city: 출생 도시명 (경도 조회용)
        """
        self.birth_datetime = birth_datetime

        # 경도 결정
        if longitude is not None:
            self.longitude = longitude
        else:
            self.longitude = CityCoordinates.get_longitude(city, default=126.9780)

        # 해당 시점의 표준 자오선
        self.standard_meridian = KSTHistory.get_standard_meridian(birth_datetime)

    def calculate_true_solar_time(self) -> tuple[datetime, dict]:
        """
        진태양시 계산

        Returns:
            (진태양시, 보정 상세정보 딕셔너리)
        """
        corrections = {}

        # 1. DST 보정 (서머타임 기간이면 1시간 빼기)
        dst_minutes = KSTHistory.get_dst_offset(self.birth_datetime)
        adjusted = self.birth_datetime - timedelta(minutes=dst_minutes)
        corrections["dst_minutes"] = -dst_minutes

        # 2. 경도 보정
        # (출생지 경도 - 표준 자오선) × 4분/도
        longitude_diff = self.longitude - self.standard_meridian
        longitude_minutes = longitude_diff * 4
        adjusted = adjusted + timedelta(minutes=longitude_minutes)
        corrections["longitude_minutes"] = longitude_minutes

        # 3. 균시차 보정
        eot_minutes = self._calculate_equation_of_time(adjusted)
        adjusted = adjusted + timedelta(minutes=eot_minutes)
        corrections["eot_minutes"] = eot_minutes

        # 총 보정량
        corrections["total_minutes"] = (
            corrections["dst_minutes"]
            + corrections["longitude_minutes"]
            + corrections["eot_minutes"]
        )
        corrections["standard_meridian"] = self.standard_meridian
        corrections["birth_longitude"] = self.longitude

        return adjusted, corrections

    def _calculate_equation_of_time(self, dt: datetime) -> float:
        """
        균시차(Equation of Time) 계산

        E = 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B)
        B = 360/365 * (N - 81)

        Args:
            dt: 계산 기준 일시

        Returns:
            균시차 (분 단위)
        """
        # 연중 일수 (1월 1일 = 1)
        day_of_year = dt.timetuple().tm_yday

        # B 계산 (라디안)
        B = math.radians(360 / 365 * (day_of_year - 81))

        # 균시차 (분)
        E = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

        return E

    def get_correction_summary(self) -> dict:
        """보정 요약 정보 반환"""
        true_solar_time, corrections = self.calculate_true_solar_time()

        return {
            "original_time": self.birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "true_solar_time": true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
            "longitude_correction_minutes": round(corrections["longitude_minutes"], 2),
            "eot_correction_minutes": round(corrections["eot_minutes"], 2),
            "dst_correction_minutes": corrections["dst_minutes"],
            "total_correction_minutes": round(corrections["total_minutes"], 2),
            "standard_meridian": corrections["standard_meridian"],
            "birth_longitude": corrections["birth_longitude"],
        }


def calculate_true_solar_time(
    birth_datetime: datetime, longitude: float | None = None, city: str = "Seoul"
) -> tuple[datetime, dict]:
    """
    편의 함수: 진태양시 계산

    Args:
        birth_datetime: 출생 일시
        longitude: 출생지 경도
        city: 출생 도시

    Returns:
        (진태양시, 보정정보)
    """
    corrector = TimeCorrector(birth_datetime, longitude, city)
    return corrector.calculate_true_solar_time()
