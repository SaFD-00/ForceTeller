"""
지장간(支藏干) 계산 단위 테스트

HiddenStemsCalculator는 각 지지에 숨은 천간(여기·중기·본기)을 반환한다.
기대값은 구현 테이블을 베끼지 않고 월률분야 표준 지장간표에서 손으로 도출한다.

C5 표준표 정합 이후 모든 지지의 지장간 구성·본기가 월률분야 표준과 일치한다:
- 사맹지·사고지(축·인·진·사·미·술·해)·오·신: 여기·중기·본기 3지장간
- 왕지(자·묘·유): 여기·본기 2지장간 (자=임계, 묘=갑을, 유=경신)

주의(표시 계층, 범위 밖): HiddenStemsCalculator는 지장간 개수로 type을 매겨
2지장간 왕지의 여기(임·갑·경)를 "중기"로 라벨링한다. 간지·비율·본기는 표준이나
type 라벨만 비표준이므로, 왕지 검증은 type 시퀀스가 아닌 구성·본기로 단언한다.

지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

import pytest

from manseol.calculator.hidden_stems import HiddenStemsCalculator, get_hidden_stems

# 월률분야 표준 지장간 구성 (korean 집합) — 3지장간 지지
STANDARD_COMPOSITION = {
    1: {"계", "신", "기"},  # 축: 계신기
    2: {"무", "병", "갑"},  # 인: 무병갑
    4: {"을", "계", "무"},  # 진: 을계무
    5: {"무", "경", "병"},  # 사: 무경병
    6: {"병", "기", "정"},  # 오: 병기정
    7: {"정", "을", "기"},  # 미: 정을기
    8: {"무", "임", "경"},  # 신: 무임경
    10: {"신", "정", "무"},  # 술: 신정무
    11: {"무", "갑", "임"},  # 해: 무갑임
}

# 왕지 표준 지장간 구성 — ({여기·본기 집합}, 본기)
WANGJI_COMPOSITION = {
    0: ({"임", "계"}, "계"),  # 자: 여기 임, 본기 계
    3: ({"갑", "을"}, "을"),  # 묘: 여기 갑, 본기 을
    9: ({"경", "신"}, "신"),  # 유: 여기 경, 본기 신
}

# 표준 정기(본기) — 오(午)는 별도 명시 테스트(test_o_main_qi_standard)
STANDARD_MAIN_QI = {
    0: "계",  # 자
    1: "기",  # 축
    2: "갑",  # 인
    3: "을",  # 묘
    4: "무",  # 진
    5: "병",  # 사
    7: "기",  # 미
    8: "경",  # 신
    9: "신",  # 유
    10: "무",  # 술
    11: "임",  # 해
}


class TestHiddenStemsComposition:
    """지장간 구성 검증 (월률분야 표준)"""

    @pytest.mark.parametrize("branch, expected", sorted(STANDARD_COMPOSITION.items()))
    def test_standard_composition(self, branch, expected):
        """3지장간 지지의 여기·중기·본기 집합"""
        stems = {d["korean"] for d in get_hidden_stems(branch)}
        assert stems == expected

    @pytest.mark.parametrize("branch, expected", sorted(WANGJI_COMPOSITION.items()))
    def test_wangji_composition(self, branch, expected):
        """왕지(자·묘·유)는 여기 포함 2지장간, 본기는 마지막 요소"""
        expected_set, expected_main = expected
        stems = get_hidden_stems(branch)
        assert {d["korean"] for d in stems} == expected_set
        assert stems[-1]["korean"] == expected_main

    @pytest.mark.parametrize("branch, expected", sorted(STANDARD_MAIN_QI.items()))
    def test_main_qi(self, branch, expected):
        """지지 정기(본기) — 표준 정기와 일치 (오는 별도)"""
        assert HiddenStemsCalculator(0).get_main_qi(branch)["korean"] == expected

    def test_shin_main_and_middle_qi(self):
        """신(申)은 본기 경·중기 임 검증"""
        stems = get_hidden_stems(8)
        assert stems[-1]["korean"] == "경"  # 본기 경
        middle = next(d for d in stems if d["type"] == "중기")
        assert middle["korean"] == "임"


class TestHiddenStemsStructure:
    """지장간 구조·비율 합리성 검증 (지지 무관 순수 구조)"""

    def test_ratio_sums_to_100(self):
        """모든 지지의 지장간 비율 합은 100"""
        for branch in range(12):
            total = sum(d["ratio"] for d in get_hidden_stems(branch))
            assert total == 100, f"지지={branch}, 합={total}"

    @pytest.mark.parametrize("branch", [0, 3, 9])
    def test_wangji_has_two_stems(self, branch):
        """왕지(자·묘·유)는 여기·본기 2지장간"""
        assert len(get_hidden_stems(branch)) == 2

    @pytest.mark.parametrize("branch", [1, 2, 4, 5, 6, 7, 8, 10, 11])
    def test_triple_type(self, branch):
        """3지장간 지지는 여기·중기·본기 순"""
        types = [d["type"] for d in get_hidden_stems(branch)]
        assert types == ["여기", "중기", "본기"]


class TestHiddenStemsStandardConformance:
    """C5 표준표 정합 — 이전 구현 불일치 회귀 가드"""

    def test_o_main_qi_standard(self):
        """오(午) 본기 표준값(정) — 이전 구현은 기(己·토)로 오류"""
        assert HiddenStemsCalculator(0).get_main_qi(6)["korean"] == "정"

    def test_shin_yeogi_standard(self):
        """신(申) 여기 표준값(무) — 이전 구현은 기(己)"""
        yeogi = next(d for d in get_hidden_stems(8) if d["type"] == "여기")
        assert yeogi["korean"] == "무"
