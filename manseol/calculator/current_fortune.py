"""
현재 운세(연운·월운·일운) 계산 모듈

프론트엔드가 절기를 무시한 근사로 재계산하던 연운/월운/일운을 백엔드가
단일 진실 공급원으로서 산출한다. 기준 시각은 항상 naive KST(Asia/Seoul)로,
출생 사주 계산과 동일한 규약(엔진이 naive dt를 KST로 취급)을 유지한다.
"""

from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from config.constants import BRANCHES, ELEMENT_KOREAN, STEMS
from manseol.calculator.pillar_engine import PillarEngine
from manseol.calculator.ten_gods import TenGodsCalculator
from manseol.calculator.twelve_phases import TwelvePhasesCalculator
from manseol.core.solar_terms import get_month_by_jeolgi, get_year_by_ipchun

KST = ZoneInfo("Asia/Seoul")


def now_kst() -> datetime:
    """현재 시각을 naive KST(Asia/Seoul)로 반환.

    엔진 전체가 naive dt를 KST로 취급하는 규약을 따른다. datetime.now()를
    단독으로 쓰면 서버 TZ에 의존하므로 사용하지 않는다.
    """
    return datetime.now(KST).replace(tzinfo=None)


def _build_entry(
    stem_index: int,
    branch_index: int,
    ten_gods: TenGodsCalculator,
    twelve_phases: TwelvePhasesCalculator,
    labels: dict[str, Any],
) -> dict[str, Any]:
    """간지 1개(연/월/일)를 십성·12운성으로 장식한 계약 dict로 구성.

    labels(year/month/date 등)를 앞에 두어 계약의 키 순서를 유지한다. element는
    천간 오행을 한글로, ten_god은 천간·지지(본기) 각각에 대해 일간 기준으로 낸다.
    """
    stem = STEMS[stem_index]
    branch = BRANCHES[branch_index]

    entry: dict[str, Any] = dict(labels)
    entry.update(
        {
            "stem": stem["korean"],
            "branch": branch["korean"],
            "stem_hanja": stem["chinese"],
            "branch_hanja": branch["chinese"],
            "stem_index": stem_index,
            "branch_index": branch_index,
            "element": ELEMENT_KOREAN[stem["element"]],
            "ganji_korean": f"{stem['korean']}{branch['korean']}",
            "ganji_chinese": f"{stem['chinese']}{branch['chinese']}",
            "ten_god": ten_gods.get_ten_god_for_stem(stem_index),
            "branch_ten_god": ten_gods.get_ten_god_for_branch(branch_index),
            "twelve_phase": twelve_phases.get_twelve_phase(branch_index),
        }
    )
    return entry


def calculate_current_fortune(day_stem_index: int, now: datetime | None = None) -> dict[str, Any]:
    """기준 시각의 연운·월운·일운을 산출.

    Args:
        day_stem_index: 일간 천간 인덱스(십성·12운성 기준점)
        now: 기준 시각(naive KST). None이면 now_kst() 사용.

    Returns:
        reference_datetime / yearly / monthly / daily 계약 dict
    """
    if now is None:
        now = now_kst()

    engine = PillarEngine()
    ten_gods = TenGodsCalculator(day_stem_index)
    twelve_phases = TwelvePhasesCalculator(day_stem_index)

    year_stem, year_branch = engine.calculate_year_pillar(now)
    month_stem, month_branch = engine.calculate_month_pillar(now)
    day_stem, day_branch = engine.calculate_day_pillar(now)

    jeolgi_year, jeolgi_month = get_month_by_jeolgi(now)

    yearly = _build_entry(
        year_stem, year_branch, ten_gods, twelve_phases, {"year": get_year_by_ipchun(now)}
    )
    monthly = _build_entry(
        month_stem,
        month_branch,
        ten_gods,
        twelve_phases,
        {"year": jeolgi_year, "month": jeolgi_month},
    )
    daily = _build_entry(
        day_stem, day_branch, ten_gods, twelve_phases, {"date": now.date().isoformat()}
    )

    return {
        "reference_datetime": now.isoformat(),
        "yearly": yearly,
        "monthly": monthly,
        "daily": daily,
    }


def calculate_fortune_ranges(
    day_stem_index: int, now: datetime | None = None
) -> dict[str, list[dict[str, Any]]]:
    """웹 슬라이더용 연/월/일 운세 범위(C3b 계약).

    각 항목 구조는 calculate_current_fortune의 yearly/monthly/daily와 동일하며,
    monthly에는 달력월(calendar_month) 라벨이 추가된다.

    - yearly: 현재±5년(입춘 기준 연) 11개 — 중앙 항목이 current_fortune.yearly와 일치
    - monthly: 해당 연도 1~12월(절기월) 12개, 매월 15일 기준(항상 해당 절기월 내)
    - daily: 현재±7일 15개

    연운은 calculate_sewun 대신 calculate_year_pillar로 통일한다(둘 다 (Y-1984)
    오프셋으로 수치 동일하고, 6월 1일은 항상 입춘 이후라 입춘 기준 연 = year).
    """
    if now is None:
        now = now_kst()

    engine = PillarEngine()
    ten_gods = TenGodsCalculator(day_stem_index)
    twelve_phases = TwelvePhasesCalculator(day_stem_index)

    # 연운: 입춘 기준 연을 중심으로 ±5년
    center_year = get_year_by_ipchun(now)
    yearly: list[dict[str, Any]] = []
    for year in range(center_year - 5, center_year + 6):
        stem_index, branch_index = engine.calculate_year_pillar(datetime(year, 6, 1))
        yearly.append(
            _build_entry(stem_index, branch_index, ten_gods, twelve_phases, {"year": year})
        )

    # 월운: 해당 연도 12개월, 매월 15일은 항상 해당 절기월 내
    monthly: list[dict[str, Any]] = []
    for month in range(1, 13):
        ref = datetime(now.year, month, 15)
        stem_index, branch_index = engine.calculate_month_pillar(ref)
        jeolgi_year, jeolgi_month = get_month_by_jeolgi(ref)
        monthly.append(
            _build_entry(
                stem_index,
                branch_index,
                ten_gods,
                twelve_phases,
                {"year": jeolgi_year, "month": jeolgi_month, "calendar_month": month},
            )
        )

    # 일운: 현재±7일 15개
    daily: list[dict[str, Any]] = []
    for offset in range(-7, 8):
        ref = now + timedelta(days=offset)
        stem_index, branch_index = engine.calculate_day_pillar(ref)
        daily.append(
            _build_entry(
                stem_index, branch_index, ten_gods, twelve_phases, {"date": ref.date().isoformat()}
            )
        )

    return {"yearly": yearly, "monthly": monthly, "daily": daily}
