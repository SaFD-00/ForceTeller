"""
12운성(十二運星) 계산 모듈
일간 기준 각 지지의 12운성 산출
"""

from config.constants import STEMS, TWELVE_PHASES


class TwelvePhasesCalculator:
    """12운성 계산 클래스"""

    # 천간별 12운성 시작 지지 (장생 위치)
    # 양간: 순행, 음간: 역행
    CHANGSHENG_POSITIONS = {
        # 갑목(양) - 해(亥)에서 장생
        0: 11,  # 갑 -> 해
        # 을목(음) - 오(午)에서 장생
        1: 6,  # 을 -> 오
        # 병화(양) - 인(寅)에서 장생
        2: 2,  # 병 -> 인
        # 정화(음) - 유(酉)에서 장생
        3: 9,  # 정 -> 유
        # 무토(양) - 인(寅)에서 장생 (병화와 동일)
        4: 2,  # 무 -> 인
        # 기토(음) - 유(酉)에서 장생 (정화와 동일)
        5: 9,  # 기 -> 유
        # 경금(양) - 사(巳)에서 장생
        6: 5,  # 경 -> 사
        # 신금(음) - 자(子)에서 장생
        7: 0,  # 신 -> 자
        # 임수(양) - 신(申)에서 장생
        8: 8,  # 임 -> 신
        # 계수(음) - 묘(卯)에서 장생
        9: 3,  # 계 -> 묘
    }

    def __init__(self, day_stem_index: int):
        """
        Args:
            day_stem_index: 일간 천간 인덱스
        """
        self.day_stem_index = day_stem_index
        self.day_stem = STEMS[day_stem_index]
        self.is_yang = self.day_stem["polarity"].value == "yang"

        # 장생 시작 위치
        self.changsheng_branch = self.CHANGSHENG_POSITIONS[day_stem_index]

    def get_twelve_phase(self, branch_index: int) -> str:
        """
        지지에 대한 12운성 반환

        Args:
            branch_index: 지지 인덱스

        Returns:
            12운성명
        """
        # 장생 위치로부터의 거리 계산
        if self.is_yang:
            # 양간: 순행 (지지 인덱스 증가 방향)
            distance = (branch_index - self.changsheng_branch) % 12
        else:
            # 음간: 역행 (지지 인덱스 감소 방향)
            distance = (self.changsheng_branch - branch_index) % 12

        # 12운성 순서
        phases = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]

        return phases[distance]

    def get_twelve_phase_info(self, branch_index: int) -> dict:
        """
        12운성 상세 정보 반환

        Args:
            branch_index: 지지 인덱스

        Returns:
            12운성 정보 딕셔너리
        """
        phase_name = self.get_twelve_phase(branch_index)
        phase_data = TWELVE_PHASES.get(phase_name, {})

        return {
            "name": phase_name,
            "meaning": phase_data.get("meaning", ""),
            "energy": phase_data.get("energy", 0),
        }

    def calculate_all_phases(self, pillars: dict[str, tuple]) -> dict[str, str]:
        """
        사주 전체의 12운성 계산

        Args:
            pillars: {"year": (stem, branch), "month": ..., ...}

        Returns:
            {"year": "장생", "month": "건록", ...}
        """
        result = {}

        for pillar_name, pillar_data in pillars.items():
            if pillar_data is None:
                continue
            stem_idx, branch_idx = pillar_data
            if branch_idx is not None:
                result[pillar_name] = self.get_twelve_phase(branch_idx)

        return result

    def get_strength_score(self, pillars: dict[str, tuple]) -> int:
        """
        12운성 기반 신강/신약 점수 계산

        강한 운성: 장생, 관대, 건록, 제왕 (+점수)
        약한 운성: 쇠, 병, 사, 묘, 절 (-점수)

        Args:
            pillars: 사주 4주 데이터

        Returns:
            강도 점수
        """
        scores = {
            "장생": 8,
            "목욕": 4,
            "관대": 10,
            "건록": 12,
            "제왕": 12,
            "쇠": -4,
            "병": -8,
            "사": -10,
            "묘": -12,
            "절": -8,
            "태": 2,
            "양": 4,
        }

        total = 50  # 기본 점수

        for pillar_name, pillar_data in pillars.items():
            if pillar_data is None:
                continue
            _, branch_idx = pillar_data
            if branch_idx is not None:
                phase = self.get_twelve_phase(branch_idx)
                total += scores.get(phase, 0)

        # 0-100 범위로 정규화
        return max(0, min(100, total))


def calculate_twelve_phase(day_stem_index: int, branch_index: int) -> str:
    """편의 함수: 특정 지지의 12운성 계산"""
    calc = TwelvePhasesCalculator(day_stem_index)
    return calc.get_twelve_phase(branch_index)
