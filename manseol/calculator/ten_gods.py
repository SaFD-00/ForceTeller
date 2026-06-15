"""
십성(十星/十神) 계산 모듈
일간 기준 각 천간/지지의 십성 관계 산출
"""

from typing import Dict, List, Optional
from config.constants import (
    Element, Polarity, STEMS, BRANCHES,
    TEN_GODS_BY_RELATION, HIDDEN_STEMS_DETAILED
)


class TenGodsCalculator:
    """십성 계산 클래스"""

    # 오행 상생상극 관계
    # 생: 木→火→土→金→水→木
    # 극: 木→土→水→火→金→木
    GENERATION = {
        Element.WOOD: Element.FIRE,
        Element.FIRE: Element.EARTH,
        Element.EARTH: Element.METAL,
        Element.METAL: Element.WATER,
        Element.WATER: Element.WOOD,
    }

    CONTROL = {
        Element.WOOD: Element.EARTH,
        Element.FIRE: Element.METAL,
        Element.EARTH: Element.WATER,
        Element.METAL: Element.WOOD,
        Element.WATER: Element.FIRE,
    }

    def __init__(self, day_stem_index: int):
        """
        Args:
            day_stem_index: 일간 천간 인덱스
        """
        self.day_stem_index = day_stem_index
        self.day_stem = STEMS[day_stem_index]
        self.day_element = self.day_stem["element"]
        self.day_polarity = self.day_stem["polarity"]

    def get_ten_god_for_stem(self, stem_index: int) -> str:
        """
        천간에 대한 십성 반환

        Args:
            stem_index: 대상 천간 인덱스

        Returns:
            십성명
        """
        if stem_index == self.day_stem_index:
            return "비견"  # 자기 자신

        target_stem = STEMS[stem_index]
        target_element = target_stem["element"]
        target_polarity = target_stem["polarity"]

        relation = self._get_relation(target_element)
        same_polarity = (target_polarity == self.day_polarity)

        return TEN_GODS_BY_RELATION[(relation, same_polarity)]

    def get_ten_god_for_branch(self, branch_index: int) -> str:
        """
        지지에 대한 십성 반환 (지지의 본기 기준)

        Args:
            branch_index: 지지 인덱스

        Returns:
            십성명
        """
        # 지장간에서 본기(마지막 항목, 가장 높은 비율) 추출
        hidden_stems = HIDDEN_STEMS_DETAILED.get(branch_index, [])
        if not hidden_stems:
            # fallback: 지지 표면 오행 사용
            branch = BRANCHES[branch_index]
            branch_element = branch["element"]
            branch_polarity = branch["polarity"]
        else:
            # 본기 (마지막 항목) 사용
            main_qi = hidden_stems[-1]
            main_stem_idx = main_qi["stem"]
            main_stem = STEMS[main_stem_idx]
            branch_element = main_stem["element"]
            branch_polarity = main_stem["polarity"]

        relation = self._get_relation(branch_element)
        same_polarity = (branch_polarity == self.day_polarity)

        return TEN_GODS_BY_RELATION[(relation, same_polarity)]

    def _get_relation(self, target_element: Element) -> str:
        """
        일간 오행과 대상 오행의 관계 반환

        Returns:
            "same" | "generate" | "generated_by" | "control" | "controlled_by"
        """
        if target_element == self.day_element:
            return "same"  # 비견/겁재

        # 내가 생하는 오행
        if self.GENERATION[self.day_element] == target_element:
            return "generate"  # 식신/상관

        # 나를 생하는 오행
        for elem, gen in self.GENERATION.items():
            if gen == self.day_element and elem == target_element:
                return "generated_by"  # 편인/정인

        # 내가 극하는 오행
        if self.CONTROL[self.day_element] == target_element:
            return "control"  # 편재/정재

        # 나를 극하는 오행
        for elem, ctrl in self.CONTROL.items():
            if ctrl == self.day_element and elem == target_element:
                return "controlled_by"  # 편관/정관

        return "same"  # fallback

    def calculate_all_ten_gods(
        self,
        pillars: Dict[str, tuple]
    ) -> Dict[str, Dict[str, str]]:
        """
        사주 전체의 십성 계산

        Args:
            pillars: {"year": (stem, branch), "month": ..., "day": ..., "hour": ...}

        Returns:
            {
                "year": {"stem": "편인", "branch": "정관"},
                "month": {...},
                ...
            }
        """
        result = {}

        for pillar_name, pillar in pillars.items():
            # 시간 미상 등으로 비어 있는 주는 건너뛴다
            if pillar is None:
                continue
            stem_idx, branch_idx = pillar
            if pillar_name == "day":
                # 일간은 십성 계산 안 함 (기준점)
                result[pillar_name] = {
                    "stem": "일간",
                    "branch": self.get_ten_god_for_branch(branch_idx)
                }
            elif stem_idx is not None and branch_idx is not None:
                result[pillar_name] = {
                    "stem": self.get_ten_god_for_stem(stem_idx),
                    "branch": self.get_ten_god_for_branch(branch_idx)
                }

        return result

    def get_ten_gods_distribution(
        self,
        pillars: Dict[str, tuple]
    ) -> Dict[str, int]:
        """
        십성 분포 계산

        Args:
            pillars: 사주 4주 데이터

        Returns:
            {십성명: 개수, ...}
        """
        distribution = {
            "비견": 0, "겁재": 0,
            "식신": 0, "상관": 0,
            "편재": 0, "정재": 0,
            "편관": 0, "정관": 0,
            "편인": 0, "정인": 0,
        }

        ten_gods = self.calculate_all_ten_gods(pillars)

        for pillar_name, gods in ten_gods.items():
            stem_god = gods.get("stem")
            branch_god = gods.get("branch")

            if stem_god and stem_god in distribution:
                distribution[stem_god] += 1
            if branch_god and branch_god in distribution:
                distribution[branch_god] += 1

        return distribution


def calculate_ten_god(
    day_stem_index: int,
    target_stem_index: int
) -> str:
    """편의 함수: 특정 천간의 십성 계산"""
    calc = TenGodsCalculator(day_stem_index)
    return calc.get_ten_god_for_stem(target_stem_index)
