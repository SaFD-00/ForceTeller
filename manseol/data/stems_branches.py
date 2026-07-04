"""
천간(天干)과 지지(地支) 데이터 클래스
"""

from config.constants import BRANCHES, HIDDEN_STEMS_DETAILED, STEMS, Element, Polarity


class StemBranchData:
    """천간/지지 데이터 접근 클래스"""

    @staticmethod
    def get_stem(index: int) -> dict:
        """천간 정보 반환"""
        return STEMS[index % 10]

    @staticmethod
    def get_branch(index: int) -> dict:
        """지지 정보 반환"""
        return BRANCHES[index % 12]

    @staticmethod
    def get_stem_element(index: int) -> Element:
        """천간의 오행 반환"""
        return STEMS[index % 10]["element"]

    @staticmethod
    def get_stem_polarity(index: int) -> Polarity:
        """천간의 음양 반환"""
        return STEMS[index % 10]["polarity"]

    @staticmethod
    def get_branch_element(index: int) -> Element:
        """지지의 오행 반환"""
        return BRANCHES[index % 12]["element"]

    @staticmethod
    def get_branch_polarity(index: int) -> Polarity:
        """지지의 음양 반환"""
        return BRANCHES[index % 12]["polarity"]

    @staticmethod
    def get_hidden_stems(branch_index: int) -> list[int]:
        """지지의 지장간 반환"""
        return HIDDEN_STEMS_DETAILED.get(branch_index % 12, [])

    @staticmethod
    def get_stem_korean(index: int) -> str:
        """천간 한글명 반환"""
        return STEMS[index % 10]["korean"]

    @staticmethod
    def get_stem_chinese(index: int) -> str:
        """천간 한자명 반환"""
        return STEMS[index % 10]["chinese"]

    @staticmethod
    def get_branch_korean(index: int) -> str:
        """지지 한글명 반환"""
        return BRANCHES[index % 12]["korean"]

    @staticmethod
    def get_branch_chinese(index: int) -> str:
        """지지 한자명 반환"""
        return BRANCHES[index % 12]["chinese"]

    @staticmethod
    def get_branch_animal(index: int) -> str:
        """지지의 띠 동물 반환"""
        return BRANCHES[index % 12]["animal"]

    @staticmethod
    def get_ganji_korean(stem_index: int, branch_index: int) -> str:
        """간지 한글명 반환 (예: 갑자)"""
        stem = STEMS[stem_index % 10]["korean"]
        branch = BRANCHES[branch_index % 12]["korean"]
        return f"{stem}{branch}"

    @staticmethod
    def get_ganji_chinese(stem_index: int, branch_index: int) -> str:
        """간지 한자명 반환 (예: 甲子)"""
        stem = STEMS[stem_index % 10]["chinese"]
        branch = BRANCHES[branch_index % 12]["chinese"]
        return f"{stem}{branch}"

    @staticmethod
    def stem_index_by_korean(korean: str) -> int | None:
        """한글 천간명으로 인덱스 반환"""
        for idx, data in STEMS.items():
            if data["korean"] == korean:
                return idx
        return None

    @staticmethod
    def branch_index_by_korean(korean: str) -> int | None:
        """한글 지지명으로 인덱스 반환"""
        for idx, data in BRANCHES.items():
            if data["korean"] == korean:
                return idx
        return None

    @staticmethod
    def get_time_branch(hour: int, minute: int = 0) -> int:
        """
        시간으로 지지 인덱스 반환 (분 단위 정밀도)

        각 시진(時辰)은 2시간 단위:
        자시(子時): 23:00 ~ 01:00 (0)
        축시(丑時): 01:00 ~ 03:00 (1)
        인시(寅時): 03:00 ~ 05:00 (2)
        묘시(卯時): 05:00 ~ 07:00 (3)
        진시(辰時): 07:00 ~ 09:00 (4)
        사시(巳時): 09:00 ~ 11:00 (5)
        오시(午時): 11:00 ~ 13:00 (6)
        미시(未時): 13:00 ~ 15:00 (7)
        신시(申時): 15:00 ~ 17:00 (8)
        유시(酉時): 17:00 ~ 19:00 (9)
        술시(戌時): 19:00 ~ 21:00 (10)
        해시(亥時): 21:00 ~ 23:00 (11)

        manseryeok 참조: 분 단위 정밀도로 시진 경계 계산
        """
        # 23시는 자시(0)로 처리
        adjusted_hour = 0 if hour == 23 else hour

        # 정확한 시진 계산 (분을 고려하여 보정)
        # 각 시진은 2시간(120분)이므로, +60분 오프셋으로 23:00 기준 조정
        total_minutes = adjusted_hour * 60 + minute
        shichen = ((total_minutes + 60) // 120) % 12

        return shichen

    @staticmethod
    def get_time_range_for_branch(branch_index: int) -> tuple[int, int]:
        """지지에 해당하는 시간 범위 반환"""
        return BRANCHES[branch_index % 12]["time_range"]
