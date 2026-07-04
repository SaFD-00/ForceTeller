"""
신살(神煞) 계산 단위 테스트

ShenshaCalculator의 대표 신살 규칙을 명리 표준표에서 독립 도출한 기대값으로
검증한다. 구현은 12신살(역마·도화·화개 등)을 **년지 삼합** 기준으로 판단하고,
귀인·양인 등은 일간 기준으로 판단한다.

검증 규칙(표준):
- 역마살: 삼합국 생지(장생)의 충 — 신자진(水)→인, 인오술(火)→신, 사유축(金)→해, 해묘미(木)→사
- 도화살: 삼합국 왕지 다음(목욕지) 자오묘유 — 신자진→유, 인오술→묘, 사유축→오, 해묘미→자
- 화개살: 삼합국 고지(묘지) — 신자진→진, 인오술→술, 사유축→축, 해묘미→미
- 천을귀인(일간): 갑무경→축미, 을기→자신, 병정→해유, 신→인오, 임계→묘사
- 문창귀인(일간): 갑→사, 병무→신, 경→해 …
- 양인살(일간·양간): 갑→묘, 병무→오, 경→유, 임→자

신살 이름은 "역마살 (驛馬殺)" 형식이므로 " (" 앞부분(한글)으로 대조한다.

지지 인덱스: 0자 1축 2인 3묘 4진 5사 6오 7미 8신 9유 10술 11해
천간 인덱스: 0갑 1을 2병 3정 4무 5기 6경 7신 8임 9계
"""

from manseol.calculator.shensha import ShenshaCalculator


def _names(year, month, day, hour=None):
    """사주 4주 (천간, 지지) 튜플로 신살 한글명 집합 반환"""
    calc = ShenshaCalculator(year, month, day, hour)
    return {item["name"].split(" (")[0] for item in calc.calculate_all_shensha()}


class TestSamhapShensha:
    """삼합(년지) 기반 12신살 — 역마·도화·화개"""

    def test_yeokma_water_present(self):
        """수국(년지 자) + 인(寅) → 역마살"""
        # 년 갑자(水局), 시 병인 → 인이 역마
        assert "역마살" in _names((0, 0), (1, 3), (1, 3), (2, 2))

    def test_yeokma_water_absent(self):
        """수국(년지 자)이나 인(寅) 없으면 역마살 없음"""
        assert "역마살" not in _names((0, 0), (1, 3), (1, 3))

    def test_dohwa_fire_present(self):
        """화국(년지 인) + 묘(卯) → 도화살"""
        # 년 병인(火局), 일 을묘 → 묘가 도화
        assert "도화살" in _names((2, 2), (2, 2), (1, 3))

    def test_dohwa_fire_absent(self):
        """화국(년지 인)이나 묘(卯) 없으면 도화살 없음"""
        assert "도화살" not in _names((2, 2), (2, 2), (2, 2))

    def test_hwagae_wood_present(self):
        """목국(년지 묘) + 미(未) → 화개살"""
        # 년 정묘(木局), 일 정미 → 미가 화개
        assert "화개살" in _names((3, 3), (3, 3), (3, 7))

    def test_hwagae_wood_absent(self):
        """목국(년지 묘)이나 미(未) 없으면 화개살 없음"""
        assert "화개살" not in _names((3, 3), (3, 3), (3, 3))


class TestDayStemShensha:
    """일간 기준 귀인·양인"""

    def test_cheonul_guiin_present(self):
        """갑 일간 + 축(丑) → 천을귀인"""
        # 일 갑자(일간 갑), 년 정축 → 축이 천을귀인
        assert "천을귀인" in _names((3, 1), (0, 0), (0, 0))

    def test_cheonul_guiin_absent(self):
        """갑 일간이나 축·미 없으면 천을귀인 없음"""
        assert "천을귀인" not in _names((0, 0), (0, 0), (0, 0))

    def test_munchang_guiin_present(self):
        """병 일간 + 신(申) → 문창귀인"""
        # 일 병자(일간 병), 년 무신 → 신이 문창귀인
        assert "문창귀인" in _names((4, 8), (2, 0), (2, 0))

    def test_yangin_present(self):
        """병 일간 + 오(午) → 양인살 (제왕지)"""
        # 일 병자(일간 병), 월 갑오 → 오가 양인
        assert "양인살" in _names((2, 0), (0, 6), (2, 0))
