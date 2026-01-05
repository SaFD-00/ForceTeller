"""
천간/지지 작용(合/沖/刑/破/害) 계산 모듈

사주 내 천간과 지지 간의 상호작용을 분석합니다.
- 천간합(天干合): 5합 - 갑기, 을경, 병신, 정임, 무계
- 지지육합(地支六合): 자축, 인해, 묘술, 진유, 사신, 오미
- 지지삼합(地支三合): 신자진(水), 인오술(火), 사유축(金), 해묘미(木)
- 지지방합(地支方合): 인묘진(東), 사오미(南), 신유술(西), 해자축(北)
- 지지충(地支沖): 6충 - 자오, 축미, 인신, 묘유, 진술, 사해
- 지지형(地支刑): 삼형 등
- 지지파(地支破): 6파
- 지지해(地支害): 6해
- 공망(空亡): 순갑법 기반
"""

from typing import Dict, List, Any, Optional, Tuple

# 천간합 (5합) 정의
# 합화 결과: (천간1, 천간2): 합화오행
STEM_COMBINATIONS = {
    (0, 5): "토",   # 갑기합토
    (5, 0): "토",   # 기갑합토
    (1, 6): "금",   # 을경합금
    (6, 1): "금",   # 경을합금
    (2, 7): "수",   # 병신합수
    (7, 2): "수",   # 신병합수
    (3, 8): "목",   # 정임합목
    (8, 3): "목",   # 임정합목
    (4, 9): "화",   # 무계합화
    (9, 4): "화",   # 계무합화
}

# 천간충·극 (충돌하는 천간 쌍)
# 갑경, 을신, 병임, 정계, 무(충 없음), 기(충 없음)
STEM_CLASH = {
    0: 6,   # 갑 vs 경 (목극금이 아닌 금극목)
    6: 0,   # 경 vs 갑
    1: 7,   # 을 vs 신
    7: 1,   # 신 vs 을
    2: 8,   # 병 vs 임 (화수상충)
    8: 2,   # 임 vs 병
    3: 9,   # 정 vs 계
    9: 3,   # 계 vs 정
}

# 지지육합 (6합) 정의
# (지지1, 지지2): 합화오행
BRANCH_SIX_COMBINATIONS = {
    (0, 1): "토",    # 자축합토
    (1, 0): "토",
    (2, 11): "목",   # 인해합목
    (11, 2): "목",
    (3, 10): "화",   # 묘술합화
    (10, 3): "화",
    (4, 9): "금",    # 진유합금
    (9, 4): "금",
    (5, 8): "수",    # 사신합수
    (8, 5): "수",
    (6, 7): "화",    # 오미합화 (혹은 토)
    (7, 6): "화",
}

# 지지삼합 정의
# 삼합국: 세 지지가 모두 있어야 완성
BRANCH_THREE_COMBINATIONS = {
    "水局": [8, 0, 4],    # 신자진 삼합 (水)
    "火局": [2, 6, 10],   # 인오술 삼합 (火)
    "金局": [5, 9, 1],    # 사유축 삼합 (金)
    "木局": [11, 3, 7],   # 해묘미 삼합 (木)
}

# 지지방합 정의
# 방합: 계절(방위)을 이루는 세 지지
BRANCH_DIRECTIONAL_COMBINATIONS = {
    "東方木局": [2, 3, 4],     # 인묘진 (봄, 동쪽)
    "南方火局": [5, 6, 7],     # 사오미 (여름, 남쪽)
    "西方金局": [8, 9, 10],    # 신유술 (가을, 서쪽)
    "北方水局": [11, 0, 1],    # 해자축 (겨울, 북쪽)
}

# 지지반합 (삼합의 2개만 있는 경우)
# (지지1, 지지2): (반합명, 주합오행)
BRANCH_HALF_COMBINATIONS = {
    # 수국 반합
    (8, 0): ("신자반합", "수"),   # 신자
    (0, 4): ("자진반합", "수"),   # 자진
    (8, 4): ("신진반합", "수"),   # 신진 (반합 아닌 경우도 있음)
    # 화국 반합
    (2, 6): ("인오반합", "화"),   # 인오
    (6, 10): ("오술반합", "화"),  # 오술
    (2, 10): ("인술반합", "화"),  # 인술
    # 금국 반합
    (5, 9): ("사유반합", "금"),   # 사유
    (9, 1): ("유축반합", "금"),   # 유축
    (5, 1): ("사축반합", "금"),   # 사축
    # 목국 반합
    (11, 3): ("해묘반합", "목"),  # 해묘
    (3, 7): ("묘미반합", "목"),   # 묘미
    (11, 7): ("해미반합", "목"),  # 해미
}

# 지지충 (6충)
BRANCH_CLASH = {
    0: 6,    # 자오충
    6: 0,
    1: 7,    # 축미충
    7: 1,
    2: 8,    # 인신충
    8: 2,
    3: 9,    # 묘유충
    9: 3,
    4: 10,   # 진술충
    10: 4,
    5: 11,   # 사해충
    11: 5,
}

# 지지형 (刑)
# 삼형살: 인사신, 축술미
# 자형: 자묘, 진진, 오오, 유유, 해해
BRANCH_PUNISHMENT = {
    # 무은지형 (인사신 삼형)
    2: [5, 8],   # 인 -> 사, 신
    5: [8, 2],   # 사 -> 신, 인
    8: [2, 5],   # 신 -> 인, 사
    # 무례지형 (축술미 삼형)
    1: [10, 7],  # 축 -> 술, 미
    10: [7, 1],  # 술 -> 미, 축
    7: [1, 10],  # 미 -> 축, 술
    # 무례지형 (자묘형)
    0: [3],      # 자 -> 묘
    3: [0],      # 묘 -> 자
    # 자형 (같은 지지끼리)
    4: [4],      # 진진 자형
    6: [6],      # 오오 자형
    9: [9],      # 유유 자형
    11: [11],    # 해해 자형
}

# 지지파 (破)
BRANCH_BREAK = {
    0: 9,    # 자유파
    9: 0,
    1: 4,    # 축진파
    4: 1,
    2: 11,   # 인해파
    11: 2,
    3: 6,    # 묘오파
    6: 3,
    5: 8,    # 사신파
    8: 5,
    7: 10,   # 미술파
    10: 7,
}

# 지지해 (害) - 육해
BRANCH_HARM = {
    0: 7,    # 자미해
    7: 0,
    1: 6,    # 축오해
    6: 1,
    2: 5,    # 인사해
    5: 2,
    3: 4,    # 묘진해
    4: 3,
    8: 11,   # 신해해
    11: 8,
    9: 10,   # 유술해
    10: 9,
}

# 공망 테이블 (갑자순~계해순)
# 각 순(旬)에서 빠진 두 지지가 공망
# 천간 0-9가 갑~계, 지지 0-11이 자~해
# 갑자순(갑자~계유): 술해 공망
# 갑술순(갑술~계미): 신유 공망
# ...
GONGMANG_TABLE = {
    # (일간, 일지)의 순 시작점 기준
    # 일간 + 일지로 60갑자 번호 계산 후 10으로 나눈 몫이 순 번호
    0: [10, 11],  # 갑자순 -> 술, 해 공망
    1: [8, 9],    # 갑술순 -> 신, 유 공망
    2: [6, 7],    # 갑신순 -> 오, 미 공망
    3: [4, 5],    # 갑오순 -> 진, 사 공망
    4: [2, 3],    # 갑진순 -> 인, 묘 공망
    5: [0, 1],    # 갑인순 -> 자, 축 공망
}


class InteractionsCalculator:
    """천간/지지 상호작용 계산기"""

    def __init__(
        self,
        year_pillar: Tuple[int, int],
        month_pillar: Tuple[int, int],
        day_pillar: Tuple[int, int],
        hour_pillar: Optional[Tuple[int, int]] = None
    ):
        """
        Args:
            year_pillar: (천간, 지지) 년주
            month_pillar: (천간, 지지) 월주
            day_pillar: (천간, 지지) 일주
            hour_pillar: (천간, 지지) 시주 (optional)
        """
        self.pillars = {
            "year": year_pillar,
            "month": month_pillar,
            "day": day_pillar,
        }
        if hour_pillar:
            self.pillars["hour"] = hour_pillar

        # 모든 천간과 지지 추출
        self.all_stems = [(name, p[0]) for name, p in self.pillars.items()]
        self.all_branches = [(name, p[1]) for name, p in self.pillars.items()]

    def calculate_all_interactions(self) -> Dict[str, List[Dict]]:
        """모든 상호작용 계산"""
        return {
            "천간합": self._find_stem_combinations(),
            "천간충극": self._find_stem_clashes(),
            "지지육합": self._find_branch_six_combinations(),
            "지지삼합": self._find_branch_three_combinations(),
            "지지방합": self._find_branch_directional_combinations(),
            "지지반합": self._find_branch_half_combinations(),
            "지지충": self._find_branch_clashes(),
            "지지형": self._find_branch_punishments(),
            "지지파": self._find_branch_breaks(),
            "지지해": self._find_branch_harms(),
            "공망": self._find_gongmang(),
        }

    def _find_stem_combinations(self) -> List[Dict]:
        """천간합 찾기"""
        result = []
        stems = self.all_stems

        for i, (name1, stem1) in enumerate(stems):
            for name2, stem2 in stems[i+1:]:
                key = (stem1, stem2)
                if key in STEM_COMBINATIONS:
                    result.append({
                        "type": "천간합",
                        "positions": [name1, name2],
                        "stems": [stem1, stem2],
                        "result": STEM_COMBINATIONS[key],
                        "description": f"{self._stem_name(stem1)}{self._stem_name(stem2)}합{STEM_COMBINATIONS[key]}"
                    })
        return result

    def _find_stem_clashes(self) -> List[Dict]:
        """천간충·극 찾기"""
        result = []
        stems = self.all_stems

        for i, (name1, stem1) in enumerate(stems):
            for name2, stem2 in stems[i+1:]:
                if STEM_CLASH.get(stem1) == stem2:
                    result.append({
                        "type": "천간충극",
                        "positions": [name1, name2],
                        "stems": [stem1, stem2],
                        "description": f"{self._stem_name(stem1)}{self._stem_name(stem2)}충극"
                    })
        return result

    def _find_branch_six_combinations(self) -> List[Dict]:
        """지지육합 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                key = (branch1, branch2)
                if key in BRANCH_SIX_COMBINATIONS:
                    result.append({
                        "type": "지지육합",
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "result": BRANCH_SIX_COMBINATIONS[key],
                        "description": f"{self._branch_name(branch1)}{self._branch_name(branch2)}합{BRANCH_SIX_COMBINATIONS[key]}"
                    })
        return result

    def _find_branch_three_combinations(self) -> List[Dict]:
        """지지삼합 찾기"""
        result = []
        branch_values = [b[1] for b in self.all_branches]
        branch_names = {b[1]: b[0] for b in self.all_branches}

        for combo_name, combo_branches in BRANCH_THREE_COMBINATIONS.items():
            # 세 지지가 모두 있는지 확인
            present = [b for b in combo_branches if b in branch_values]
            if len(present) == 3:
                positions = [branch_names[b] for b in present]
                result.append({
                    "type": "지지삼합",
                    "name": combo_name,
                    "positions": positions,
                    "branches": present,
                    "description": f"{self._branch_name(combo_branches[0])}{self._branch_name(combo_branches[1])}{self._branch_name(combo_branches[2])} 삼합{combo_name[0]}"
                })
        return result

    def _find_branch_directional_combinations(self) -> List[Dict]:
        """지지방합 찾기"""
        result = []
        branch_values = [b[1] for b in self.all_branches]
        branch_names = {b[1]: b[0] for b in self.all_branches}

        for combo_name, combo_branches in BRANCH_DIRECTIONAL_COMBINATIONS.items():
            present = [b for b in combo_branches if b in branch_values]
            if len(present) == 3:
                positions = [branch_names[b] for b in present]
                result.append({
                    "type": "지지방합",
                    "name": combo_name,
                    "positions": positions,
                    "branches": present,
                    "description": f"{combo_name}"
                })
        return result

    def _find_branch_half_combinations(self) -> List[Dict]:
        """지지반합 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                key = (branch1, branch2)
                rev_key = (branch2, branch1)
                combo = BRANCH_HALF_COMBINATIONS.get(key) or BRANCH_HALF_COMBINATIONS.get(rev_key)
                if combo:
                    combo_name, element = combo
                    result.append({
                        "type": "지지반합",
                        "name": combo_name,
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "result": element,
                        "description": combo_name
                    })
        return result

    def _find_branch_clashes(self) -> List[Dict]:
        """지지충 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                if BRANCH_CLASH.get(branch1) == branch2:
                    result.append({
                        "type": "지지충",
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "description": f"{self._branch_name(branch1)}{self._branch_name(branch2)}충"
                    })
        return result

    def _find_branch_punishments(self) -> List[Dict]:
        """지지형 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                punish_list = BRANCH_PUNISHMENT.get(branch1, [])
                if branch2 in punish_list:
                    # 자형인지 삼형인지 구분
                    if branch1 == branch2:
                        desc = f"{self._branch_name(branch1)}자형"
                    else:
                        desc = f"{self._branch_name(branch1)}{self._branch_name(branch2)}형"
                    result.append({
                        "type": "지지형",
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "description": desc
                    })
        return result

    def _find_branch_breaks(self) -> List[Dict]:
        """지지파 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                if BRANCH_BREAK.get(branch1) == branch2:
                    result.append({
                        "type": "지지파",
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "description": f"{self._branch_name(branch1)}{self._branch_name(branch2)}파"
                    })
        return result

    def _find_branch_harms(self) -> List[Dict]:
        """지지해 찾기"""
        result = []
        branches = self.all_branches

        for i, (name1, branch1) in enumerate(branches):
            for name2, branch2 in branches[i+1:]:
                if BRANCH_HARM.get(branch1) == branch2:
                    result.append({
                        "type": "지지해",
                        "positions": [name1, name2],
                        "branches": [branch1, branch2],
                        "description": f"{self._branch_name(branch1)}{self._branch_name(branch2)}해"
                    })
        return result

    def _find_gongmang(self) -> List[Dict]:
        """공망 찾기"""
        result = []

        # 일주 기준으로 공망 계산
        day_stem = self.pillars["day"][0]
        day_branch = self.pillars["day"][1]

        # 60갑자 번호 계산
        ganji_num = (day_stem * 6 + day_branch) % 60
        # 순(旬) 번호 (0-5)
        xun_num = ganji_num // 10

        # 해당 순의 공망 지지
        gongmang_branches = GONGMANG_TABLE.get(xun_num, [])

        # 사주 내 공망 지지 확인
        for pillar_name, pillar_data in self.pillars.items():
            branch = pillar_data[1]
            if branch in gongmang_branches:
                result.append({
                    "type": "공망",
                    "position": pillar_name,
                    "branch": branch,
                    "description": f"{pillar_name} {self._branch_name(branch)} 공망"
                })

        return result

    def _stem_name(self, idx: int) -> str:
        """천간 이름 반환"""
        names = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        return names[idx] if 0 <= idx < 10 else ""

    def _branch_name(self, idx: int) -> str:
        """지지 이름 반환"""
        names = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
        return names[idx] if 0 <= idx < 12 else ""


def calculate_interactions(
    year_pillar: Tuple[int, int],
    month_pillar: Tuple[int, int],
    day_pillar: Tuple[int, int],
    hour_pillar: Optional[Tuple[int, int]] = None
) -> Dict[str, List[Dict]]:
    """편의 함수: 사주의 모든 상호작용 계산"""
    calc = InteractionsCalculator(year_pillar, month_pillar, day_pillar, hour_pillar)
    return calc.calculate_all_interactions()
