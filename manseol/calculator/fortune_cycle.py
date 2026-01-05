"""
대운(大運) 및 세운(歲運) 계산 모듈
"""

from datetime import datetime, date
from typing import Dict, List, Tuple, Optional
from config.constants import STEMS, BRANCHES, Polarity


class FortuneCycleCalculator:
    """대운/세운 계산 클래스"""

    def __init__(
        self,
        birth_datetime: datetime,
        gender: str,
        year_stem: int,
        month_stem: int,
        month_branch: int
    ):
        """
        Args:
            birth_datetime: 출생 일시
            gender: 성별 ("male" | "female")
            year_stem: 년간 인덱스
            month_stem: 월간 인덱스
            month_branch: 월지 인덱스
        """
        self.birth_datetime = birth_datetime
        self.gender = gender
        self.year_stem = year_stem
        self.month_stem = month_stem
        self.month_branch = month_branch

        # 대운 진행 방향 결정
        # 양년 남자, 음년 여자 = 순행
        # 양년 여자, 음년 남자 = 역행
        year_is_yang = STEMS[year_stem]["polarity"] == Polarity.YANG
        is_male = (gender == "male")

        self.is_forward = (year_is_yang and is_male) or (not year_is_yang and not is_male)

    def calculate_daewun_start_age(self) -> Tuple[int, int, int]:
        """
        대운 시작 나이 계산

        출생일로부터 가장 가까운 절기까지의 일수를 3으로 나눔

        Returns:
            (대운 시작 나이, 대운 시작까지 남은 개월, 남은 일수)
        """
        from manseol.core.solar_terms import SolarTermsCalculator

        solar_terms = SolarTermsCalculator()

        birth_date = self.birth_datetime.date() if isinstance(
            self.birth_datetime, datetime
        ) else self.birth_datetime

        # 해당 월의 절기와 다음 월의 절기
        year = self.birth_datetime.year
        month = self.birth_datetime.month

        current_jeolgi = solar_terms.get_jeolgi_for_month(year, month)
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        next_jeolgi = solar_terms.get_jeolgi_for_month(next_year, next_month)

        # 순행: 다음 절기까지 일수
        # 역행: 이전 절기까지 일수
        if self.is_forward:
            target_jeolgi = next_jeolgi
        else:
            target_jeolgi = current_jeolgi

        # 일수 차이 계산
        birth_dt = datetime.combine(birth_date, self.birth_datetime.time()) \
            if isinstance(self.birth_datetime, datetime) else datetime.combine(birth_date, datetime.min.time())

        if self.is_forward:
            days_diff = (target_jeolgi - birth_dt).days
        else:
            days_diff = (birth_dt - target_jeolgi).days

        days_diff = abs(days_diff)

        # 3일 = 1년으로 환산
        years = days_diff // 3
        remaining_days = days_diff % 3
        remaining_months = remaining_days * 4  # 1일 = 4개월

        return years, remaining_months, remaining_days

    def calculate_daewun_cycles(self, count: int = 10) -> List[Dict]:
        """
        대운 목록 계산

        Args:
            count: 대운 개수 (기본 10개)

        Returns:
            [{start_age, end_age, stem_index, branch_index, ...}, ...]
        """
        start_age, _, _ = self.calculate_daewun_start_age()

        cycles = []
        current_stem = self.month_stem
        current_branch = self.month_branch

        for i in range(count):
            # 순행/역행에 따라 간지 이동
            if self.is_forward:
                current_stem = (current_stem + 1) % 10
                current_branch = (current_branch + 1) % 12
            else:
                current_stem = (current_stem - 1) % 10
                current_branch = (current_branch - 1) % 12

            stem = STEMS[current_stem]
            branch = BRANCHES[current_branch]

            cycles.append({
                "order": i + 1,
                "start_age": start_age + (i * 10),
                "end_age": start_age + ((i + 1) * 10) - 1,
                "stem_index": current_stem,
                "branch_index": current_branch,
                "ganji_korean": f"{stem['korean']}{branch['korean']}",
                "ganji_chinese": f"{stem['chinese']}{branch['chinese']}",
            })

        return cycles

    def get_current_daewun(
        self,
        current_age: int = None
    ) -> Optional[Dict]:
        """
        현재 대운 반환

        Args:
            current_age: 현재 나이 (없으면 오늘 기준 계산)

        Returns:
            현재 대운 정보 또는 None
        """
        if current_age is None:
            today = date.today()
            birth_year = self.birth_datetime.year
            current_age = today.year - birth_year

        cycles = self.calculate_daewun_cycles()

        for cycle in cycles:
            if cycle["start_age"] <= current_age <= cycle["end_age"]:
                return cycle

        return None

    def calculate_sewun(self, year: int) -> Dict:
        """
        세운(歲運) 계산

        해당 연도의 년주가 세운

        Args:
            year: 연도

        Returns:
            세운 정보
        """
        # 갑자년 기준: 1984년
        year_offset = year - 1984

        stem_index = year_offset % 10
        branch_index = year_offset % 12

        stem = STEMS[stem_index]
        branch = BRANCHES[branch_index]

        return {
            "year": year,
            "stem_index": stem_index,
            "branch_index": branch_index,
            "ganji_korean": f"{stem['korean']}{branch['korean']}",
            "ganji_chinese": f"{stem['chinese']}{branch['chinese']}",
        }

    def get_fortune_summary(self) -> Dict:
        """
        대운 요약 정보 반환

        Returns:
            대운 요약 딕셔너리
        """
        start_age, months, days = self.calculate_daewun_start_age()
        cycles = self.calculate_daewun_cycles()

        return {
            "start_age": start_age,
            "direction": "순행" if self.is_forward else "역행",
            "cycles": cycles,
            "current_cycle_index": None,  # 나이 정보 필요시 계산
        }
