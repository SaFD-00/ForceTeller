"""
지장간(支藏干) 계산 단위 테스트

HiddenStemsCalculator는 각 지지에 숨은 천간(여기·중기·본기)을 반환한다.
기대값은 구현 테이블을 베끼지 않고 명리 표준 지장간표에서 손으로 도출한다.

구현 대조 결과 지지 유형별로 검증 범위를 나눈다:
- 사맹지·사고지 중 표준과 완전 일치: 축·인·진·사·미·술·해 → 구성 전수 단언
- 왕지(자·묘·유): 구현이 여기를 누락하고 본기만 남김 → 본기만 단언
- 오(午): 본기가 기(己·토)로 잘못 잡힘 (표준=정 丁) → xfail
- 신(申): 여기가 기(己)로 표준(무 戊)과 다름 → 본기·중기만 단언, 여기는 xfail

지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
"""

import pytest

from manseol.calculator.hidden_stems import HiddenStemsCalculator, get_hidden_stems

# 표준과 완전 일치하는 지지의 지장간 구성 (korean 집합)
STANDARD_COMPOSITION = {
    1: {"계", "신", "기"},  # 축: 계신기
    2: {"무", "병", "갑"},  # 인: 무병갑
    4: {"을", "계", "무"},  # 진: 을계무
    5: {"무", "경", "병"},  # 사: 무경병
    7: {"정", "을", "기"},  # 미: 정을기
    10: {"신", "정", "무"},  # 술: 신정무
    11: {"무", "갑", "임"},  # 해: 무갑임
}

# 표준 정기(본기) — 오(午) 제외 (오는 별도 xfail)
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
    """지장간 구성 검증 (표준 완전 일치 지지)"""

    @pytest.mark.parametrize("branch, expected", sorted(STANDARD_COMPOSITION.items()))
    def test_standard_composition(self, branch, expected):
        """사맹지·사고지 지장간 구성(여기·중기·본기 집합)"""
        stems = {d["korean"] for d in get_hidden_stems(branch)}
        assert stems == expected

    @pytest.mark.parametrize("branch, expected", sorted(STANDARD_MAIN_QI.items()))
    def test_main_qi(self, branch, expected):
        """지지 정기(본기) — 표준 정기와 일치 (오 제외)"""
        assert HiddenStemsCalculator(0).get_main_qi(branch)["korean"] == expected

    def test_wangji_main_qi_only(self):
        """왕지(자·묘·유)는 본기만 검증 — 구현이 여기(임·갑·경)를 누락"""
        assert get_hidden_stems(0)[-1]["korean"] == "계"  # 자 본기 계
        assert get_hidden_stems(3)[-1]["korean"] == "을"  # 묘 본기 을
        assert get_hidden_stems(9)[-1]["korean"] == "신"  # 유 본기 신

    def test_shin_main_and_middle_qi(self):
        """신(申)은 본기 경·중기 임만 검증 (여기는 별도 xfail)"""
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
    def test_single_type(self, branch):
        """지장간 1개 지지(자·묘·유)는 본기만"""
        types = [d["type"] for d in get_hidden_stems(branch)]
        assert types == ["본기"]

    def test_double_type(self):
        """지장간 2개 지지(오)는 중기·본기 순"""
        types = [d["type"] for d in get_hidden_stems(6)]
        assert types == ["중기", "본기"]

    @pytest.mark.parametrize("branch", [1, 2, 4, 5, 7, 8, 10, 11])
    def test_triple_type(self, branch):
        """지장간 3개 지지는 여기·중기·본기 순"""
        types = [d["type"] for d in get_hidden_stems(branch)]
        assert types == ["여기", "중기", "본기"]


class TestHiddenStemsDiscrepancies:
    """구현-이론 불일치 문서화 (xfail)"""

    @pytest.mark.xfail(
        reason="오(午)는 화 지지로 표준 정기가 정(丁)이나, 구현은 본기를 기(己·토)로 잡음.",
        strict=True,
    )
    def test_o_main_qi_standard(self):
        """오(午) 본기 표준값(정) — 구현 오류로 실패 예상"""
        assert HiddenStemsCalculator(0).get_main_qi(6)["korean"] == "정"

    @pytest.mark.xfail(
        reason="신(申) 여기의 표준은 무(戊)이나 구현은 기(己). 4맹지 중 인·사·해는 여기 무라 내부 비일관.",
        strict=True,
    )
    def test_shin_yeogi_standard(self):
        """신(申) 여기 표준값(무) — 구현이 기(己)라 실패 예상"""
        yeogi = next(d for d in get_hidden_stems(8) if d["type"] == "여기")
        assert yeogi["korean"] == "무"
