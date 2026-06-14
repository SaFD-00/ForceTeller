"""
사주 계산 결과 데이터 모델
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from config.constants import Element, Polarity


class StemData(BaseModel):
    """천간 데이터"""
    index: int = Field(..., ge=0, le=9, description="천간 인덱스 (0-9)")
    korean: str = Field(..., description="한글 (갑, 을, ...)")
    chinese: str = Field(..., description="한자 (甲, 乙, ...)")
    element: str = Field(..., description="오행 (木, 火, ...)")
    polarity: str = Field(..., description="음양 (양, 음)")


class BranchData(BaseModel):
    """지지 데이터"""
    index: int = Field(..., ge=0, le=11, description="지지 인덱스 (0-11)")
    korean: str = Field(..., description="한글 (자, 축, ...)")
    chinese: str = Field(..., description="한자 (子, 丑, ...)")
    element: str = Field(..., description="오행")
    polarity: str = Field(..., description="음양")
    animal: str = Field(..., description="띠 동물")
    hidden_stems: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="지장간 정보"
    )


class PillarData(BaseModel):
    """사주 1주(柱) 데이터"""
    stem: StemData = Field(..., description="천간")
    branch: BranchData = Field(..., description="지지")
    ganji_korean: str = Field(..., description="간지 한글 (예: 갑자)")
    ganji_chinese: str = Field(..., description="간지 한자 (예: 甲子)")
    ten_god: Optional[str] = Field(None, description="십성 (일주 제외)")
    twelve_phase: Optional[str] = Field(None, description="12운성")


class FourPillars(BaseModel):
    """사주 4주"""
    year: PillarData = Field(..., description="년주")
    month: PillarData = Field(..., description="월주")
    day: PillarData = Field(..., description="일주")
    hour: Optional[PillarData] = Field(None, description="시주 (시간 미상시 None)")


class TimeCorrection(BaseModel):
    """시간 보정 정보"""
    original_time: str = Field(..., description="원본 시계 시간")
    true_solar_time: str = Field(..., description="진태양시")
    longitude_correction_minutes: float = Field(..., description="경도 보정 (분)")
    eot_correction_minutes: float = Field(..., description="균시차 보정 (분)")
    dst_correction_minutes: float = Field(default=0, description="DST 보정 (분)")
    total_correction_minutes: float = Field(..., description="총 보정 (분)")
    standard_meridian: float = Field(..., description="기준 자오선 경도")
    birth_longitude: float = Field(..., description="출생지 경도")


class DayMasterAnalysis(BaseModel):
    """일간(日干) 분석"""
    element: str = Field(..., description="오행")
    polarity: str = Field(..., description="음양")
    korean: str = Field(..., description="한글명")
    chinese: str = Field(..., description="한자명")
    metaphor: str = Field(..., description="물상 은유")
    characteristics: List[str] = Field(
        default_factory=list,
        description="특성 키워드"
    )


class FiveElementsAnalysis(BaseModel):
    """오행 분포 분석"""
    wood: int = Field(default=0, description="목(木) 점수")
    fire: int = Field(default=0, description="화(火) 점수")
    earth: int = Field(default=0, description="토(土) 점수")
    metal: int = Field(default=0, description="금(金) 점수")
    water: int = Field(default=0, description="수(水) 점수")
    dominant: List[str] = Field(default_factory=list, description="과다 오행")
    lacking: List[str] = Field(default_factory=list, description="부족 오행")
    distribution: Dict[str, float] = Field(
        default_factory=dict,
        description="오행 비율 (%)"
    )


class TenGodsDistribution(BaseModel):
    """십성 분포"""
    비견: int = Field(default=0)
    겁재: int = Field(default=0)
    식신: int = Field(default=0)
    상관: int = Field(default=0)
    편재: int = Field(default=0)
    정재: int = Field(default=0)
    편관: int = Field(default=0)
    정관: int = Field(default=0)
    편인: int = Field(default=0)
    정인: int = Field(default=0)

    def to_dict(self) -> Dict[str, int]:
        """딕셔너리 변환"""
        return {
            "비견": self.비견, "겁재": self.겁재,
            "식신": self.식신, "상관": self.상관,
            "편재": self.편재, "정재": self.정재,
            "편관": self.편관, "정관": self.정관,
            "편인": self.편인, "정인": self.정인,
        }


class StrengthAnalysis(BaseModel):
    """신강/신약 분석"""
    level: str = Field(..., description="신강/신약/중화")
    score: int = Field(..., ge=0, le=100, description="강도 점수 (0-100)")
    supporting_count: int = Field(default=0, description="생조 개수")
    weakening_count: int = Field(default=0, description="극설 개수")
    analysis: str = Field(default="", description="분석 설명")


class UsefulGodAnalysis(BaseModel):
    """용신 분석"""
    type: str = Field(..., description="용신 선정 방식 (억부/조후/통관/병약)")
    primary: str = Field(..., description="용신 오행")
    secondary: Optional[str] = Field(None, description="희신 오행")
    avoid: Optional[str] = Field(None, description="기신 오행")
    reasoning: str = Field(default="", description="선정 이유")


class FortuneCycle(BaseModel):
    """대운/세운 1개 주기"""
    start_age: int = Field(..., description="시작 나이")
    end_age: int = Field(..., description="종료 나이")
    stem_index: int = Field(..., description="천간 인덱스")
    branch_index: int = Field(..., description="지지 인덱스")
    ganji_korean: str = Field(..., description="간지 한글")
    ganji_chinese: str = Field(..., description="간지 한자")
    ten_god: str = Field(..., description="십성")
    twelve_phase: str = Field(..., description="12운성")


class FortuneCycleData(BaseModel):
    """대운/세운 전체 데이터"""
    start_age: int = Field(..., description="대운 시작 나이")
    direction: str = Field(..., description="순행/역행")
    cycles: List[FortuneCycle] = Field(
        default_factory=list,
        description="대운 목록 (10개)"
    )
    current_cycle_index: Optional[int] = Field(
        None,
        description="현재 대운 인덱스"
    )


class ShenshaData(BaseModel):
    """신살 데이터"""
    name: str = Field(..., description="신살명")
    type: str = Field(..., description="길신/흉신")
    position: str = Field(..., description="위치 (년/월/일/시)")
    description: str = Field(default="", description="설명")


class SajuAnalysis(BaseModel):
    """사주 종합 분석"""
    day_master: DayMasterAnalysis = Field(..., description="일간 분석")
    five_elements: FiveElementsAnalysis = Field(..., description="오행 분석")
    ten_gods_dist: TenGodsDistribution = Field(..., description="십성 분포")
    strength: StrengthAnalysis = Field(..., description="신강/신약")
    useful_god: UsefulGodAnalysis = Field(..., description="용신")
    shensha: List[ShenshaData] = Field(
        default_factory=list,
        description="신살 목록"
    )


class MetaInfo(BaseModel):
    """메타 정보"""
    version: str = Field(default="1.0.0", description="버전")
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="생성 시각"
    )
    engine: str = Field(default="ForceTeller", description="엔진명")


class InputSummary(BaseModel):
    """입력 요약"""
    name: str
    birth_date: str
    birth_time: Optional[str]
    calendar: str
    city: str
    gender: str
    jajasi: bool
    # 음력 정보
    lunar_year: Optional[int] = Field(None, description="음력 연도")
    lunar_month: Optional[int] = Field(None, description="음력 월")
    lunar_day: Optional[int] = Field(None, description="음력 일")
    is_leap_month: Optional[bool] = Field(None, description="윤달 여부")
    # 일주 정보
    day_ganji_korean: Optional[str] = Field(None, description="일주 한글 (예: 경진)")
    day_ganji_chinese: Optional[str] = Field(None, description="일주 한자 (예: 庚辰)")
    day_metaphor: Optional[str] = Field(None, description="일주 물상 (예: 하얀 용)")
    day_animal: Optional[str] = Field(None, description="일지 동물 (예: 용)")


class SajuResult(BaseModel):
    """사주 계산 최종 결과"""

    meta: MetaInfo = Field(
        default_factory=MetaInfo,
        description="메타 정보"
    )

    input: InputSummary = Field(..., description="입력 요약")

    adjusted_time: Optional[TimeCorrection] = Field(
        None,
        description="시간 보정 정보"
    )

    pillars: FourPillars = Field(..., description="사주 4주")

    analysis: SajuAnalysis = Field(..., description="사주 분석")

    fortune_cycles: Optional[FortuneCycleData] = Field(
        None,
        description="대운 데이터"
    )

    interactions: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        None,
        description="천간/지지 상호작용 (합·충·형·파·해·공망)"
    )

    sewun: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="세운(歲運) - 올해부터 향후 수년간 연운"
    )

    def to_json(self, indent: int = 2) -> str:
        """JSON 문자열 변환"""
        return self.model_dump_json(indent=indent, exclude_none=True)

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return self.model_dump(exclude_none=True)

    def to_hanja_string(self) -> str:
        """
        한자 사주 문자열 반환

        Returns:
            "庚辰年柱, 丁亥月柱, 庚辰日柱, 丁亥時柱" 형식
        """
        parts = [
            f"{self.pillars.year.ganji_chinese}年柱",
            f"{self.pillars.month.ganji_chinese}月柱",
            f"{self.pillars.day.ganji_chinese}日柱",
        ]
        if self.pillars.hour:
            parts.append(f"{self.pillars.hour.ganji_chinese}時柱")
        return ", ".join(parts)

    def to_korean_string(self) -> str:
        """
        한글 사주 문자열 반환

        Returns:
            "경진년주, 정해월주, 경진일주, 정해시주" 형식
        """
        parts = [
            f"{self.pillars.year.ganji_korean}년주",
            f"{self.pillars.month.ganji_korean}월주",
            f"{self.pillars.day.ganji_korean}일주",
        ]
        if self.pillars.hour:
            parts.append(f"{self.pillars.hour.ganji_korean}시주")
        return ", ".join(parts)

    def to_hanja_object(self) -> Dict[str, Dict[str, str]]:
        """
        한글/한자 사주 객체 반환

        Returns:
            {
                "year": {"korean": "경진", "hanja": "庚辰"},
                "month": {"korean": "정해", "hanja": "丁亥"},
                ...
            }
        """
        result = {
            "year": {
                "korean": self.pillars.year.ganji_korean,
                "hanja": self.pillars.year.ganji_chinese,
            },
            "month": {
                "korean": self.pillars.month.ganji_korean,
                "hanja": self.pillars.month.ganji_chinese,
            },
            "day": {
                "korean": self.pillars.day.ganji_korean,
                "hanja": self.pillars.day.ganji_chinese,
            },
        }
        if self.pillars.hour:
            result["hour"] = {
                "korean": self.pillars.hour.ganji_korean,
                "hanja": self.pillars.hour.ganji_chinese,
            }
        return result

    class Config:
        json_schema_extra = {
            "example": {
                "meta": {
                    "version": "1.0.0",
                    "generated_at": "2024-01-15T10:30:00",
                    "engine": "ForceTeller"
                },
                "input": {
                    "name": "홍길동",
                    "birth_date": "1990-05-15",
                    "birth_time": "14:30",
                    "calendar": "solar",
                    "city": "Seoul",
                    "gender": "male",
                    "jajasi": False
                },
                "pillars": {
                    "year": {"ganji_korean": "경오", "ganji_chinese": "庚午"},
                    "month": {"ganji_korean": "신사", "ganji_chinese": "辛巳"},
                    "day": {"ganji_korean": "갑술", "ganji_chinese": "甲戌"},
                    "hour": {"ganji_korean": "임신", "ganji_chinese": "壬申"}
                }
            }
        }
