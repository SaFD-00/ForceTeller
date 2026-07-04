"""
십이운성(十二運星) 계산 단위 테스트

TwelvePhasesCalculator는 포태법 표준표를 따른다. 양간은 장생지에서 순행,
음간은 장생지에서 역행하며 12운성(장생·목욕·관대·건록·제왕·쇠·병·사·묘·절·태·양)이
순환한다. 기대값은 표준 포태표에서 손으로 도출한 리터럴이다.

토(무·기) 일간은 화토동궁/수토동궁 논쟁으로 표준이 하나가 아니므로 제외하고,
양간(갑·경)·음간(을·계) 대표로 12지지 전수 검증한다.

지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

import pytest

from manseol.calculator.twelve_phases import TwelvePhasesCalculator, calculate_twelve_phase

# 갑(甲, 양목): 해에서 장생, 순행
GAP_PHASES = {
    11: "장생",
    0: "목욕",
    1: "관대",
    2: "건록",
    3: "제왕",
    4: "쇠",
    5: "병",
    6: "사",
    7: "묘",
    8: "절",
    9: "태",
    10: "양",
}

# 을(乙, 음목): 오에서 장생, 역행
EUL_PHASES = {
    6: "장생",
    5: "목욕",
    4: "관대",
    3: "건록",
    2: "제왕",
    1: "쇠",
    0: "병",
    11: "사",
    10: "묘",
    9: "절",
    8: "태",
    7: "양",
}

# 경(庚, 양금): 사에서 장생, 순행
GYEONG_PHASES = {
    5: "장생",
    6: "목욕",
    7: "관대",
    8: "건록",
    9: "제왕",
    10: "쇠",
    11: "병",
    0: "사",
    1: "묘",
    2: "절",
    3: "태",
    4: "양",
}

# 계(癸, 음수): 묘에서 장생, 역행
GYE_PHASES = {
    3: "장생",
    2: "목욕",
    1: "관대",
    0: "건록",
    11: "제왕",
    10: "쇠",
    9: "병",
    8: "사",
    7: "묘",
    6: "절",
    5: "태",
    4: "양",
}

_PHASE_TABLE = {
    0: GAP_PHASES,  # 갑
    1: EUL_PHASES,  # 을
    6: GYEONG_PHASES,  # 경
    9: GYE_PHASES,  # 계
}


class TestTwelvePhases:
    """대표 일간(양간 갑·경, 음간 을·계) × 12지지 전수 검증"""

    @pytest.mark.parametrize("day_stem", [0, 1, 6, 9])
    def test_all_branches_per_day_stem(self, day_stem):
        """일간별 12지지 12운성 전수"""
        calc = TwelvePhasesCalculator(day_stem)
        expected = _PHASE_TABLE[day_stem]
        for branch in range(12):
            assert calc.get_twelve_phase(branch) == expected[branch], (
                f"일간={day_stem}, 지지={branch}"
            )

    def test_yang_forward_vs_yin_backward(self):
        """양간(갑) 장생 해, 음간(을) 장생 오 — 순행/역행 방향 확인"""
        assert TwelvePhasesCalculator(0).get_twelve_phase(11) == "장생"  # 갑 → 해
        assert TwelvePhasesCalculator(0).get_twelve_phase(6) == "사"  # 갑 → 오는 사
        assert TwelvePhasesCalculator(1).get_twelve_phase(6) == "장생"  # 을 → 오
        assert TwelvePhasesCalculator(1).get_twelve_phase(11) == "사"  # 을 → 해는 사

    def test_geonrok_at_stem_native_branch(self):
        """건록(임관)은 일간의 오행이 왕한 본기 지지 — 갑=인, 경=신"""
        assert TwelvePhasesCalculator(0).get_twelve_phase(2) == "건록"  # 갑 → 인
        assert TwelvePhasesCalculator(6).get_twelve_phase(8) == "건록"  # 경 → 신

    def test_convenience_function_matches(self):
        """calculate_twelve_phase 편의 함수가 클래스 메서드와 일치"""
        assert calculate_twelve_phase(0, 11) == "장생"  # 갑 → 해
        assert calculate_twelve_phase(9, 3) == "장생"  # 계 → 묘
