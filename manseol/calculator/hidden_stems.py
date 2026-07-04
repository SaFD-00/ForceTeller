"""
지장간(支藏干) 계산 모듈
지지에 숨겨진 천간(여기, 중기, 본기) 분석
"""

from typing import Any

from config.constants import HIDDEN_STEMS_DETAILED, STEMS


class HiddenStemsCalculator:
    """지장간 계산 클래스"""

    def __init__(self, day_stem_index: int):
        """
        Args:
            day_stem_index: 일간 천간 인덱스 (십성 계산용)
        """
        self.day_stem_index = day_stem_index

    def get_hidden_stems(self, branch_index: int) -> list[dict[str, Any]]:
        """
        지지의 지장간 반환

        지지별 지장간 개수에 따라 타입 분류 (월률분야 표준표 기준):
        - 2개: 여기 + 본기 (왕지: 자, 묘, 유)
        - 3개: 여기 + 중기 + 본기 (나머지)

        Args:
            branch_index: 지지 인덱스

        Returns:
            [{stem_index, korean, chinese, type, ratio}, ...]
        """
        hidden = HIDDEN_STEMS_DETAILED.get(branch_index, [])
        result = []

        count = len(hidden)

        # 지장간 개수에 따른 타입 분류
        if count == 1:  # 표준표에는 없으나 방어적으로 유지
            type_map = {0: "본기"}
        elif count == 2:  # 왕지(자·묘·유): 여기 + 본기
            type_map = {0: "여기", 1: "본기"}
        else:  # count == 3
            type_map = {0: "여기", 1: "중기", 2: "본기"}

        for i, stem_data in enumerate(hidden):
            stem_idx = stem_data["stem"]
            stem = STEMS[stem_idx]

            result.append(
                {
                    "stem_index": stem_idx,
                    "korean": stem["korean"],
                    "chinese": stem["chinese"],
                    "element": stem["element"].value,
                    "type": type_map.get(i, "본기"),
                    "ratio": stem_data.get("ratio", 0),
                }
            )

        return result

    def get_hidden_stems_ten_gods(self, branch_index: int) -> list[dict[str, Any]]:
        """
        지장간의 십성 포함 정보 반환

        Args:
            branch_index: 지지 인덱스

        Returns:
            [{stem_info, ten_god}, ...]
        """
        from .ten_gods import TenGodsCalculator

        hidden_stems = self.get_hidden_stems(branch_index)
        ten_gods_calc = TenGodsCalculator(self.day_stem_index)

        for stem_info in hidden_stems:
            stem_idx = stem_info["stem_index"]
            stem_info["ten_god"] = ten_gods_calc.get_ten_god_for_stem(stem_idx)

        return hidden_stems

    def calculate_all_hidden_stems(self, pillars: dict[str, tuple]) -> dict[str, list[dict]]:
        """
        사주 전체의 지장간 계산

        Args:
            pillars: {"year": (stem, branch), ...}

        Returns:
            {"year": [{hidden_stem_info}, ...], ...}
        """
        result = {}

        for pillar_name, pillar_data in pillars.items():
            if pillar_data is None:
                continue
            _, branch_idx = pillar_data
            if branch_idx is not None:
                result[pillar_name] = self.get_hidden_stems_ten_gods(branch_idx)

        return result

    def get_main_qi(self, branch_index: int) -> dict[str, Any]:
        """
        지지의 본기(本氣) 반환

        본기는 해당 지지의 가장 강한 기운

        Args:
            branch_index: 지지 인덱스

        Returns:
            본기 정보
        """
        hidden = self.get_hidden_stems(branch_index)
        if hidden:
            # 마지막 항목이 본기
            return hidden[-1]
        return {}

    def analyze_hidden_stems_strength(self, pillars: dict[str, tuple]) -> dict[str, float]:
        """
        지장간 기반 오행 비율 분석

        각 지장간의 비율을 반영하여 오행 분포 계산

        Args:
            pillars: 사주 4주 데이터

        Returns:
            {오행: 비율, ...}
        """
        element_scores = {"목": 0.0, "화": 0.0, "토": 0.0, "금": 0.0, "수": 0.0}

        all_hidden = self.calculate_all_hidden_stems(pillars)

        for pillar_name, hidden_list in all_hidden.items():
            for hidden in hidden_list:
                element = hidden["element"]
                ratio = hidden.get("ratio", 10) / 100  # 비율을 0-1 범위로
                element_scores[element] += ratio

        # 정규화 (합계를 100으로)
        total = sum(element_scores.values())
        if total > 0:
            for elem in element_scores:
                element_scores[elem] = round(element_scores[elem] / total * 100, 1)

        return element_scores


def get_hidden_stems(branch_index: int) -> list[dict]:
    """편의 함수: 지장간 반환"""
    calc = HiddenStemsCalculator(0)  # day_stem 미사용
    return calc.get_hidden_stems(branch_index)
