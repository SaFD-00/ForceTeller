"""
십성(十星/十神) 계산 단위 테스트

TenGodsCalculator는 일간 오행·음양 대비 대상 천간의 오행·음양 관계로
십성을 결정하는 순수 결정론 함수다. 기대값은 구현 테이블을 베끼지 않고
명리 표준 이론에서 손으로 도출한 리터럴을 사용한다.

천간 인덱스: 0갑 1을 2병 3정 4무 5기 6경 7신 8임 9계 (양=짝수, 음=홀수)
지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

import pytest

from manseol.calculator.ten_gods import TenGodsCalculator, calculate_ten_god

# 갑(甲, 양목) 일간 기준 10천간 십성
# 갑=비견, 을=겁재, 병(목생화·양)=식신, 정(목생화·음)=상관,
# 무(목극토·양)=편재, 기(목극토·음)=정재, 경(금극목·양)=편관, 신(금극목·음)=정관,
# 임(수생목·양)=편인, 계(수생목·음)=정인
GAP_STEM_TEN_GODS = ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"]

# 경(庚, 양금) 일간 기준 10천간 십성
# 갑(금극목·양)=편재, 을=정재, 병(화극금·양)=편관, 정=정관, 무(토생금·양)=편인, 기=정인,
# 경=비견, 신=겁재, 임(금생수·양)=식신, 계=상관
GYEONG_STEM_TEN_GODS = [
    "편재",
    "정재",
    "편관",
    "정관",
    "편인",
    "정인",
    "비견",
    "겁재",
    "식신",
    "상관",
]

# 계(癸, 음수) 일간 기준 10천간 십성
# 갑(수생목·양)=상관, 을(음)=식신, 병(수극화·양)=정재, 정(음)=편재,
# 무(토극수·양)=정관, 기(음)=편관, 경(금생수·양)=정인, 신(음)=편인, 임(양)=겁재, 계=비견
GYE_STEM_TEN_GODS = ["상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인", "겁재", "비견"]

_DAY_MASTER_TABLE = {
    0: GAP_STEM_TEN_GODS,
    6: GYEONG_STEM_TEN_GODS,
    9: GYE_STEM_TEN_GODS,
}


class TestTenGodsForStem:
    """천간 대상 십성 전수 검증 (대표 일간 갑·경·계 × 10천간)"""

    @pytest.mark.parametrize("day_master", [0, 6, 9])
    def test_all_stems_per_day_master(self, day_master):
        """대표 일간 3개에 대해 10천간 십성 전수 확인"""
        calc = TenGodsCalculator(day_master)
        expected = _DAY_MASTER_TABLE[day_master]
        for target in range(10):
            assert calc.get_ten_god_for_stem(target) == expected[target], (
                f"일간={day_master}, 대상천간={target}"
            )

    def test_self_is_bigyeon(self):
        """일간과 동일 천간은 비견(같은 오행·같은 음양)"""
        for day_master in range(10):
            assert TenGodsCalculator(day_master).get_ten_god_for_stem(day_master) == "비견"

    def test_convenience_function_matches(self):
        """calculate_ten_god 편의 함수가 클래스 메서드와 일치"""
        assert calculate_ten_god(0, 2) == "식신"  # 갑 일간 → 병
        assert calculate_ten_god(6, 0) == "편재"  # 경 일간 → 갑


# 갑(甲, 양목) 일간 기준 지지 본기(정기) 십성 — 표준 정기 기준, 오(午)는 별도
# 자:계(정인) 축:기(정재) 인:갑(비견) 묘:을(겁재) 진:무(편재) 사:병(식신)
# 미:기(정재) 신:경(편관) 유:신(정관) 술:무(편재) 해:임(편인)
GAP_BRANCH_TEN_GODS = {
    0: "정인",
    1: "정재",
    2: "비견",
    3: "겁재",
    4: "편재",
    5: "식신",
    7: "정재",
    8: "편관",
    9: "정관",
    10: "편재",
    11: "편인",
}

# 경(庚, 양금) 일간 기준 지지 본기(정기) 십성 — 오(午) 제외
# 자:계(상관) 축:기(정인) 인:갑(편재) 묘:을(정재) 진:무(편인) 사:병(편관)
# 미:기(정인) 신:경(비견) 유:신(겁재) 술:무(편인) 해:임(식신)
GYEONG_BRANCH_TEN_GODS = {
    0: "상관",
    1: "정인",
    2: "편재",
    3: "정재",
    4: "편인",
    5: "편관",
    7: "정인",
    8: "비견",
    9: "겁재",
    10: "편인",
    11: "식신",
}


class TestTenGodsForBranch:
    """지지 본기 기준 십성 검증 (오 제외 — 오는 별도 xfail)"""

    @pytest.mark.parametrize("branch, expected", sorted(GAP_BRANCH_TEN_GODS.items()))
    def test_gap_branch(self, branch, expected):
        """갑 일간 기준 지지 본기 십성"""
        assert TenGodsCalculator(0).get_ten_god_for_branch(branch) == expected

    @pytest.mark.parametrize("branch, expected", sorted(GYEONG_BRANCH_TEN_GODS.items()))
    def test_gyeong_branch(self, branch, expected):
        """경 일간 기준 지지 본기 십성"""
        assert TenGodsCalculator(6).get_ten_god_for_branch(branch) == expected

    @pytest.mark.xfail(
        reason="구현이 오(午)의 지장간 본기를 기(己·토)로 잡음. 표준 정기는 정(丁·화)이라 "
        "갑 일간 기준 표준=상관이나 구현=정재. hidden_stems 오 본기 이슈와 동일 원인.",
        strict=True,
    )
    def test_gap_branch_o_standard(self):
        """갑 일간 기준 오(午) 십성 표준값(상관) — 구현 본기 오류로 실패 예상"""
        assert TenGodsCalculator(0).get_ten_god_for_branch(6) == "상관"
