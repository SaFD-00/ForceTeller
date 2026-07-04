"""
대운(大運)·세운(歲運) 계산 단위 테스트

FortuneCycleCalculator의 결정론 규칙을 검증한다:
- 대운 방향: 양남음녀 순행, 음남양녀 역행
- 대운 간지: 월주에서 순행/역행으로 연속
- 세운: 해당 연도의 연간지(갑자년 1984 기준)

대운 시작 나이는 SolarTermsCalculator(절기) 의존이라 값 자체는 단언하지 않고,
방향과 간지 시퀀스만 검증한다.

천간 인덱스: 0갑 1을 2병 3정 4무 5기 6경 7신 8임 9계 (양=짝수, 음=홀수)
지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

from datetime import datetime

import pytest

from manseol.calculator.fortune_cycle import FortuneCycleCalculator

_BIRTH = datetime(1990, 5, 15, 14, 30)  # 방향·간지엔 무관, 절기 조회용


def _calc(year_stem, gender, month_stem=7, month_branch=5):
    """월주 기본값 신사(7,5)로 계산기 생성"""
    return FortuneCycleCalculator(_BIRTH, gender, year_stem, month_stem, month_branch)


class TestDaewunDirection:
    """대운 방향: 양남음녀 순행 / 음남양녀 역행"""

    @pytest.mark.parametrize(
        "year_stem, gender, expected_forward",
        [
            (0, "male", True),  # 갑(양) 남 → 순행
            (0, "female", False),  # 갑(양) 여 → 역행
            (1, "male", False),  # 을(음) 남 → 역행
            (1, "female", True),  # 을(음) 여 → 순행
            (6, "male", True),  # 경(양) 남 → 순행
            (8, "female", False),  # 임(양) 여 → 역행
            (9, "male", False),  # 계(음) 남 → 역행
            (9, "female", True),  # 계(음) 여 → 순행
        ],
    )
    def test_direction(self, year_stem, gender, expected_forward):
        """양간/음간 × 남/녀 순행·역행"""
        assert _calc(year_stem, gender).is_forward is expected_forward


class TestDaewunSequence:
    """대운 간지가 월주에서 순행/역행으로 연속하는지"""

    def test_forward_sequence(self):
        """순행: 월주 신사(7,5) 다음부터 간지 +1씩 (임오·계미·갑신…)"""
        cycles = _calc(6, "male").calculate_daewun_cycles(10)  # 경(양) 남 → 순행
        assert [c["stem_index"] for c in cycles] == [8, 9, 0, 1, 2, 3, 4, 5, 6, 7]
        assert [c["branch_index"] for c in cycles] == [6, 7, 8, 9, 10, 11, 0, 1, 2, 3]
        assert cycles[0]["ganji_korean"] == "임오"

    def test_backward_sequence(self):
        """역행: 월주 신사(7,5) 이전부터 간지 -1씩 (경진·기묘·무인…)"""
        cycles = _calc(9, "male").calculate_daewun_cycles(10)  # 계(음) 남 → 역행
        assert [c["stem_index"] for c in cycles] == [6, 5, 4, 3, 2, 1, 0, 9, 8, 7]
        assert [c["branch_index"] for c in cycles] == [4, 3, 2, 1, 0, 11, 10, 9, 8, 7]
        assert cycles[0]["ganji_korean"] == "경진"

    def test_cycles_are_consecutive(self):
        """대운 간지는 인접 대운끼리 60갑자상 연속"""
        cycles = _calc(6, "male").calculate_daewun_cycles(10)
        for prev, cur in zip(cycles, cycles[1:]):
            assert cur["stem_index"] == (prev["stem_index"] + 1) % 10
            assert cur["branch_index"] == (prev["branch_index"] + 1) % 12


class TestSewun:
    """세운: 해당 연도의 연간지 (입춘 무관, 갑자년 1984 기준)"""

    @pytest.mark.parametrize(
        "year, expected",
        [
            (1984, "갑자"),  # 60갑자 기준점
            (2000, "경진"),
            (2020, "경자"),
            (2024, "갑진"),
            (2025, "을사"),
        ],
    )
    def test_year_ganji(self, year, expected):
        """연도별 연간지"""
        calc = _calc(0, "male")
        assert calc.calculate_sewun(year)["ganji_korean"] == expected
