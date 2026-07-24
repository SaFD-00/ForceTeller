"""
사주 계산 입력 데이터 모델
"""

from datetime import date, datetime, time
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CalendarType(str, Enum):
    """달력 유형"""

    SOLAR = "solar"  # 양력
    LUNAR = "lunar"  # 음력 (평달)
    LEAP_LUNAR = "leap_lunar"  # 음력 (윤달)


class Gender(str, Enum):
    """성별"""

    MALE = "male"
    FEMALE = "female"


class SajuInput(BaseModel):
    """사주 계산 입력 데이터"""

    name: str = Field(..., min_length=1, max_length=50, description="이름")

    birth_date: date = Field(..., description="생년월일 (YYYY-MM-DD)")

    birth_time: time | None = Field(default=None, description="출생 시간 (HH:MM). 미상시 None")

    calendar: CalendarType = Field(
        default=CalendarType.SOLAR, description="달력 유형 (solar/lunar/leap_lunar)"
    )

    city: str = Field(default="Seoul", description="출생 도시 (경도 보정용)")

    gender: Gender = Field(..., description="성별 (male/female)")

    jajasi: bool = Field(default=False, description="야자시/조자시 적용 여부")

    longitude: float | None = Field(
        default=None, ge=-180.0, le=180.0, description="직접 입력 경도 (city 대신 사용)"
    )

    timezone: str | None = Field(
        default=None,
        max_length=64,
        description="출생지 IANA 시간대 (예: America/New_York). 해외 출생 시 현지 시각을 "
        "한국 벽시계로 환산하는 데 쓴다. 미지정이면 city로 조회하고, 한국이면 변환 없음",
    )

    apply_time_correction: bool = Field(default=True, description="시간 보정 적용 여부")

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        """생년월일 유효성 검증"""
        # 1800년 이후만 지원
        if v.year < 1800:
            raise ValueError("1800년 이전 날짜는 지원하지 않습니다")
        # 미래 날짜 불가
        if v > date.today():
            raise ValueError("미래 날짜는 입력할 수 없습니다")
        return v

    @property
    def birth_datetime(self) -> datetime | None:
        """출생 일시 반환"""
        if self.birth_time:
            return datetime.combine(self.birth_date, self.birth_time)
        return None

    @property
    def has_time(self) -> bool:
        """시간 정보 유무"""
        return self.birth_time is not None

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "name": self.name,
            "birth_date": self.birth_date.isoformat(),
            "birth_time": self.birth_time.isoformat() if self.birth_time else None,
            "calendar": self.calendar.value,
            "city": self.city,
            "gender": self.gender.value,
            "jajasi": self.jajasi,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "apply_time_correction": self.apply_time_correction,
        }

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "홍길동",
                "birth_date": "1990-05-15",
                "birth_time": "14:30",
                "calendar": "solar",
                "city": "Seoul",
                "gender": "male",
                "jajasi": False,
            }
        }
    )
