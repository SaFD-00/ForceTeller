"""
사주명리학 상수 정의
천간(天干), 지지(地支), 오행(五行), 음양(陰陽) 등
"""

from enum import Enum, IntEnum
from typing import Any


# =============================================================================
# 오행 (Five Elements)
# =============================================================================
class Element(str, Enum):
    WOOD = "wood"  # 목(木)
    FIRE = "fire"  # 화(火)
    EARTH = "earth"  # 토(土)
    METAL = "metal"  # 금(金)
    WATER = "water"  # 수(水)


ELEMENT_KOREAN = {
    Element.WOOD: "목",
    Element.FIRE: "화",
    Element.EARTH: "토",
    Element.METAL: "금",
    Element.WATER: "수",
}

ELEMENT_CHINESE = {
    Element.WOOD: "木",
    Element.FIRE: "火",
    Element.EARTH: "土",
    Element.METAL: "金",
    Element.WATER: "水",
}

# 오행 상생 관계 (생하는 관계)
ELEMENT_GENERATES = {
    Element.WOOD: Element.FIRE,  # 목생화
    Element.FIRE: Element.EARTH,  # 화생토
    Element.EARTH: Element.METAL,  # 토생금
    Element.METAL: Element.WATER,  # 금생수
    Element.WATER: Element.WOOD,  # 수생목
}

# 오행 상극 관계 (극하는 관계)
ELEMENT_CONTROLS = {
    Element.WOOD: Element.EARTH,  # 목극토
    Element.FIRE: Element.METAL,  # 화극금
    Element.EARTH: Element.WATER,  # 토극수
    Element.METAL: Element.WOOD,  # 금극목
    Element.WATER: Element.FIRE,  # 수극화
}


# =============================================================================
# 음양 (Yin-Yang)
# =============================================================================
class Polarity(str, Enum):
    YANG = "yang"  # 양(陽)
    YIN = "yin"  # 음(陰)


POLARITY_KOREAN = {
    Polarity.YANG: "양",
    Polarity.YIN: "음",
}


# =============================================================================
# 천간 오행별 색상 (띠 색깔)
# =============================================================================
STEM_ELEMENT_COLORS = {
    0: "푸른",
    1: "푸른",  # 갑, 을 (목)
    2: "붉은",
    3: "붉은",  # 병, 정 (화)
    4: "노란",
    5: "노란",  # 무, 기 (토)
    6: "하얀",
    7: "하얀",  # 경, 신 (금)
    8: "검은",
    9: "검은",  # 임, 계 (수)
}


# =============================================================================
# 천간 (Heavenly Stems) - 10개
# =============================================================================
class Stem(IntEnum):
    GAP = 0  # 갑(甲)
    EUL = 1  # 을(乙)
    BYEONG = 2  # 병(丙)
    JEONG = 3  # 정(丁)
    MU = 4  # 무(戊)
    GI = 5  # 기(己)
    GYEONG = 6  # 경(庚)
    SIN = 7  # 신(辛)
    IM = 8  # 임(壬)
    GYE = 9  # 계(癸)


STEMS: dict[int, dict] = {
    0: {"korean": "갑", "chinese": "甲", "element": Element.WOOD, "polarity": Polarity.YANG},
    1: {"korean": "을", "chinese": "乙", "element": Element.WOOD, "polarity": Polarity.YIN},
    2: {"korean": "병", "chinese": "丙", "element": Element.FIRE, "polarity": Polarity.YANG},
    3: {"korean": "정", "chinese": "丁", "element": Element.FIRE, "polarity": Polarity.YIN},
    4: {"korean": "무", "chinese": "戊", "element": Element.EARTH, "polarity": Polarity.YANG},
    5: {"korean": "기", "chinese": "己", "element": Element.EARTH, "polarity": Polarity.YIN},
    6: {"korean": "경", "chinese": "庚", "element": Element.METAL, "polarity": Polarity.YANG},
    7: {"korean": "신", "chinese": "辛", "element": Element.METAL, "polarity": Polarity.YIN},
    8: {"korean": "임", "chinese": "壬", "element": Element.WATER, "polarity": Polarity.YANG},
    9: {"korean": "계", "chinese": "癸", "element": Element.WATER, "polarity": Polarity.YIN},
}


# =============================================================================
# 지지 (Earthly Branches) - 12개
# =============================================================================
class Branch(IntEnum):
    JA = 0  # 자(子)
    CHUK = 1  # 축(丑)
    IN = 2  # 인(寅)
    MYO = 3  # 묘(卯)
    JIN = 4  # 진(辰)
    SA = 5  # 사(巳)
    O = 6  # noqa: E741  # 오(午) — 도메인 로마자 표기, 개명 시 .name 직렬화 깨짐
    MI = 7  # 미(未)
    SHIN = 8  # 신(申)
    YU = 9  # 유(酉)
    SUL = 10  # 술(戌)
    HAE = 11  # 해(亥)


BRANCHES: dict[int, dict] = {
    0: {
        "korean": "자",
        "chinese": "子",
        "element": Element.WATER,
        "polarity": Polarity.YANG,
        "animal": "쥐",
        "animal_en": "Rat",
        "month_angle": 270,
        "time_range": (23, 1),
    },
    1: {
        "korean": "축",
        "chinese": "丑",
        "element": Element.EARTH,
        "polarity": Polarity.YIN,
        "animal": "소",
        "animal_en": "Ox",
        "month_angle": 300,
        "time_range": (1, 3),
    },
    2: {
        "korean": "인",
        "chinese": "寅",
        "element": Element.WOOD,
        "polarity": Polarity.YANG,
        "animal": "호랑이",
        "animal_en": "Tiger",
        "month_angle": 315,
        "time_range": (3, 5),
    },
    3: {
        "korean": "묘",
        "chinese": "卯",
        "element": Element.WOOD,
        "polarity": Polarity.YIN,
        "animal": "토끼",
        "animal_en": "Rabbit",
        "month_angle": 345,
        "time_range": (5, 7),
    },
    4: {
        "korean": "진",
        "chinese": "辰",
        "element": Element.EARTH,
        "polarity": Polarity.YANG,
        "animal": "용",
        "animal_en": "Dragon",
        "month_angle": 15,
        "time_range": (7, 9),
    },
    5: {
        "korean": "사",
        "chinese": "巳",
        "element": Element.FIRE,
        "polarity": Polarity.YIN,
        "animal": "뱀",
        "animal_en": "Snake",
        "month_angle": 45,
        "time_range": (9, 11),
    },
    6: {
        "korean": "오",
        "chinese": "午",
        "element": Element.FIRE,
        "polarity": Polarity.YANG,
        "animal": "말",
        "animal_en": "Horse",
        "month_angle": 75,
        "time_range": (11, 13),
    },
    7: {
        "korean": "미",
        "chinese": "未",
        "element": Element.EARTH,
        "polarity": Polarity.YIN,
        "animal": "양",
        "animal_en": "Sheep",
        "month_angle": 105,
        "time_range": (13, 15),
    },
    8: {
        "korean": "신",
        "chinese": "申",
        "element": Element.METAL,
        "polarity": Polarity.YANG,
        "animal": "원숭이",
        "animal_en": "Monkey",
        "month_angle": 135,
        "time_range": (15, 17),
    },
    9: {
        "korean": "유",
        "chinese": "酉",
        "element": Element.METAL,
        "polarity": Polarity.YIN,
        "animal": "닭",
        "animal_en": "Rooster",
        "month_angle": 165,
        "time_range": (17, 19),
    },
    10: {
        "korean": "술",
        "chinese": "戌",
        "element": Element.EARTH,
        "polarity": Polarity.YANG,
        "animal": "개",
        "animal_en": "Dog",
        "month_angle": 195,
        "time_range": (19, 21),
    },
    11: {
        "korean": "해",
        "chinese": "亥",
        "element": Element.WATER,
        "polarity": Polarity.YIN,
        "animal": "돼지",
        "animal_en": "Pig",
        "month_angle": 225,
        "time_range": (21, 23),
    },
}


# =============================================================================
# 지장간 (Hidden Stems in Branches)
# =============================================================================
HIDDEN_STEMS: dict[int, list[tuple[int, float]]] = {
    # (천간 인덱스, 비율) - 순서: 여기(餘氣), 중기(中氣), 정기(正氣)
    0: [(9, 1.0)],  # 자: 계
    1: [(9, 0.3), (7, 0.3), (5, 0.4)],  # 축: 계, 신, 기
    2: [(4, 0.3), (2, 0.3), (0, 0.4)],  # 인: 무, 병, 갑
    3: [(1, 1.0)],  # 묘: 을
    4: [(1, 0.3), (9, 0.3), (4, 0.4)],  # 진: 을, 계, 무
    5: [(4, 0.3), (6, 0.3), (2, 0.4)],  # 사: 무, 경, 병
    6: [(3, 0.3), (5, 0.7)],  # 오: 정, 기
    7: [(3, 0.3), (1, 0.3), (5, 0.4)],  # 미: 정, 을, 기
    8: [(5, 0.3), (8, 0.3), (6, 0.4)],  # 신: 기, 임, 경
    9: [(7, 1.0)],  # 유: 신
    10: [(7, 0.3), (3, 0.3), (4, 0.4)],  # 술: 신, 정, 무
    11: [(4, 0.2), (0, 0.2), (8, 0.6)],  # 해: 무, 갑, 임
}

# 정확한 지장간 (한국 전통 기준) - {stem: 천간인덱스, ratio: 비율}
# 월률분야 표준표 기준 (여기·중기·정기 순, 마지막이 본기)
HIDDEN_STEMS_DETAILED: dict[int, list[dict[str, Any]]] = {
    0: [{"stem": 8, "ratio": 30}, {"stem": 9, "ratio": 70}],  # 자: 임, 계
    1: [
        {"stem": 9, "ratio": 30},
        {"stem": 7, "ratio": 30},
        {"stem": 5, "ratio": 40},
    ],  # 축: 계, 신, 기
    2: [
        {"stem": 4, "ratio": 20},
        {"stem": 2, "ratio": 30},
        {"stem": 0, "ratio": 50},
    ],  # 인: 무, 병, 갑
    3: [{"stem": 0, "ratio": 30}, {"stem": 1, "ratio": 70}],  # 묘: 갑, 을
    4: [
        {"stem": 1, "ratio": 30},
        {"stem": 9, "ratio": 30},
        {"stem": 4, "ratio": 40},
    ],  # 진: 을, 계, 무
    5: [
        {"stem": 4, "ratio": 20},
        {"stem": 6, "ratio": 30},
        {"stem": 2, "ratio": 50},
    ],  # 사: 무, 경, 병
    6: [
        {"stem": 2, "ratio": 30},
        {"stem": 5, "ratio": 30},
        {"stem": 3, "ratio": 40},
    ],  # 오: 병, 기, 정
    7: [
        {"stem": 3, "ratio": 30},
        {"stem": 1, "ratio": 30},
        {"stem": 5, "ratio": 40},
    ],  # 미: 정, 을, 기
    8: [
        {"stem": 4, "ratio": 20},
        {"stem": 8, "ratio": 30},
        {"stem": 6, "ratio": 50},
    ],  # 신: 무, 임, 경
    9: [{"stem": 6, "ratio": 30}, {"stem": 7, "ratio": 70}],  # 유: 경, 신
    10: [
        {"stem": 7, "ratio": 30},
        {"stem": 3, "ratio": 30},
        {"stem": 4, "ratio": 40},
    ],  # 술: 신, 정, 무
    11: [
        {"stem": 4, "ratio": 20},
        {"stem": 0, "ratio": 20},
        {"stem": 8, "ratio": 60},
    ],  # 해: 무, 갑, 임
}


# =============================================================================
# 십성 (Ten Gods)
# =============================================================================
class TenGod(str, Enum):
    BIGYEON = "비견"  # 比肩 - 나와 같은 오행, 같은 음양
    GEOPJAE = "겁재"  # 劫財 - 나와 같은 오행, 다른 음양
    SIKSHIN = "식신"  # 食神 - 내가 생하는 오행, 같은 음양
    SANGGWAN = "상관"  # 傷官 - 내가 생하는 오행, 다른 음양
    PYEONJAE = "편재"  # 偏財 - 내가 극하는 오행, 같은 음양
    JEONGJAE = "정재"  # 正財 - 내가 극하는 오행, 다른 음양
    PYEONGWAN = "편관"  # 偏官 (七殺) - 나를 극하는 오행, 같은 음양
    JEONGGWAN = "정관"  # 正官 - 나를 극하는 오행, 다른 음양
    PYEONIN = "편인"  # 偏印 - 나를 생하는 오행, 같은 음양
    JEONGIN = "정인"  # 正印 - 나를 생하는 오행, 다른 음양


TEN_GOD_CATEGORIES = {
    "비겁": ["비견", "겁재"],
    "식상": ["식신", "상관"],
    "재성": ["편재", "정재"],
    "관성": ["편관", "정관"],
    "인성": ["편인", "정인"],
}

# 십성 관계표 - (관계유형, 음양동일여부) -> 십성
# 관계유형: "same" (비화), "generate" (내가 생), "control" (내가 극),
#          "generated_by" (나를 생), "controlled_by" (나를 극)
TEN_GODS_BY_RELATION = {
    ("same", True): "비견",  # 같은 오행, 같은 음양
    ("same", False): "겁재",  # 같은 오행, 다른 음양
    ("generate", True): "식신",  # 내가 생하는 오행, 같은 음양
    ("generate", False): "상관",  # 내가 생하는 오행, 다른 음양
    ("control", True): "편재",  # 내가 극하는 오행, 같은 음양
    ("control", False): "정재",  # 내가 극하는 오행, 다른 음양
    ("controlled_by", True): "편관",  # 나를 극하는 오행, 같은 음양
    ("controlled_by", False): "정관",  # 나를 극하는 오행, 다른 음양
    ("generated_by", True): "편인",  # 나를 생하는 오행, 같은 음양
    ("generated_by", False): "정인",  # 나를 생하는 오행, 다른 음양
}


# =============================================================================
# 12운성 (Twelve Life Stages)
# =============================================================================
class TwelvePhase(str, Enum):
    JANGSEONG = "장생"  # 長生 - 탄생
    MOKYOK = "목욕"  # 沐浴 - 목욕
    GWANDAE = "관대"  # 冠帶 - 성인
    GEONROK = "건록"  # 建祿 - 관직
    JEWANG = "제왕"  # 帝旺 - 전성기
    SOE = "쇠"  # 衰 - 쇠퇴
    BYEONG = "병"  # 病 - 병듦
    SA = "사"  # 死 - 죽음
    MYO = "묘"  # 墓 - 무덤
    JEOL = "절"  # 絶 - 단절
    TAE = "태"  # 胎 - 잉태
    YANG = "양"  # 養 - 양육


TWELVE_PHASES = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]

# 양간(陽干)의 12운성 시작 지지 (장생 위치)
# 갑(木양): 해에서 장생, 순행
# 병(火양): 인에서 장생, 순행
# 무(土양): 인에서 장생, 순행
# 경(金양): 사에서 장생, 순행
# 임(水양): 신에서 장생, 순행
YANG_STEM_JANGSEONG_BRANCH = {
    0: 11,  # 갑 -> 해
    2: 2,  # 병 -> 인
    4: 2,  # 무 -> 인
    6: 5,  # 경 -> 사
    8: 8,  # 임 -> 신
}

# 음간(陰干)의 12운성 시작 지지 (장생 위치)
# 을(木음): 오에서 장생, 역행
# 정(火음): 유에서 장생, 역행
# 기(土음): 유에서 장생, 역행
# 신(金음): 자에서 장생, 역행
# 계(水음): 묘에서 장생, 역행
YIN_STEM_JANGSEONG_BRANCH = {
    1: 6,  # 을 -> 오
    3: 9,  # 정 -> 유
    5: 9,  # 기 -> 유
    7: 0,  # 신 -> 자
    9: 3,  # 계 -> 묘
}


# =============================================================================
# 12신살 (Twelve Divine Generals / Shensha)
# =============================================================================
class Shensha(str, Enum):
    YEOKMA = "역마살"  # 易馬殺 - 이동, 변화
    DOHWA = "도화살"  # 桃花殺 - 이성, 인기
    HWAGAE = "화개살"  # 華蓋殺 - 예술, 종교
    JANGSEONG = "장성살"  # 將星殺 - 리더십
    BANAN = "반안살"  # 攀鞍殺 - 상승
    YEOKSAL = "역살"  # 驛殺 - 역마와 유사
    JASAL = "재살"  # 災殺 - 재난
    CHEONSAL = "천살"  # 天殺 - 하늘의 재앙
    JISAL = "지살"  # 地殺 - 땅의 재앙
    NYEONSAL = "년살"  # 年殺 - 연의 재앙
    WOLSAL = "월살"  # 月殺 - 월의 재앙
    MANGSIN = "망신살"  # 亡身殺 - 구설


# 월지 기준 12신살 배치 (신자진/인오술/사유축/해묘미 삼합 기준)
SHENSHA_BY_MONTH_BRANCH = {
    # 신자진(申子辰) 수국
    8: {"역마살": 2, "도화살": 9, "화개살": 4},  # 신월
    0: {"역마살": 2, "도화살": 9, "화개살": 4},  # 자월
    4: {"역마살": 2, "도화살": 9, "화개살": 4},  # 진월
    # 인오술(寅午戌) 화국
    2: {"역마살": 8, "도화살": 3, "화개살": 10},  # 인월
    6: {"역마살": 8, "도화살": 3, "화개살": 10},  # 오월
    10: {"역마살": 8, "도화살": 3, "화개살": 10},  # 술월
    # 사유축(巳酉丑) 금국
    5: {"역마살": 11, "도화살": 6, "화개살": 1},  # 사월
    9: {"역마살": 11, "도화살": 6, "화개살": 1},  # 유월
    1: {"역마살": 11, "도화살": 6, "화개살": 1},  # 축월
    # 해묘미(亥卯未) 목국
    11: {"역마살": 5, "도화살": 0, "화개살": 7},  # 해월
    3: {"역마살": 5, "도화살": 0, "화개살": 7},  # 묘월
    7: {"역마살": 5, "도화살": 0, "화개살": 7},  # 미월
}

# 신살 설명 사전
SHENSHA = {
    "역마": {
        "type": "중성",
        "description": "이동, 변동이 많음. 여행, 이사, 직업 변동이 잦을 수 있음",
    },
    "도화": {"type": "중성", "description": "매력, 이성 인연이 많음. 예술적 재능, 인기운"},
    "화개": {"type": "길신", "description": "예술, 학문 재능. 종교, 철학적 성향"},
    "천을귀인": {"type": "길신", "description": "귀인의 도움을 받음. 위기시 조력자 출현"},
    "문창귀인": {"type": "길신", "description": "학문, 시험운 좋음. 문서 관련 길함"},
    "천덕귀인": {"type": "길신", "description": "하늘의 덕을 받음. 재난 회피, 복록"},
    "월덕귀인": {"type": "길신", "description": "월의 덕을 받음. 건강, 평안"},
    "장성": {"type": "길신", "description": "리더십, 장군의 별. 명예, 권위"},
    "겁살": {"type": "흉신", "description": "강탈, 도난 주의. 급격한 변화"},
    "재살": {"type": "흉신", "description": "재난, 사고 주의. 안전에 유의"},
    "천살": {"type": "흉신", "description": "하늘의 재앙. 예측 불가한 사건"},
    "지살": {"type": "흉신", "description": "땅의 재앙. 부동산, 이동 관련 주의"},
    "년살": {"type": "흉신", "description": "연의 재앙. 해당 년도 주의"},
    "월살": {"type": "흉신", "description": "월의 재앙. 해당 월 주의"},
    "망신살": {"type": "흉신", "description": "구설, 명예 손상 주의"},
    "백호살": {"type": "흉신", "description": "피, 수술 관련 주의. 사고 주의"},
    "양인살": {"type": "흉신", "description": "날카로움, 칼날. 결단력 있으나 다툼 주의"},
    "공망": {"type": "중성", "description": "공허함, 헛됨. 해당 기운이 약함"},
}


# =============================================================================
# 귀인 (Noble Stars)
# =============================================================================
# 천을귀인 (天乙貴人) - 일간 기준
CHEONUL_GUIIN = {
    0: [1, 7],  # 갑 -> 축, 미
    1: [0, 8],  # 을 -> 자, 신
    2: [11, 9],  # 병 -> 해, 유
    3: [11, 9],  # 정 -> 해, 유
    4: [1, 7],  # 무 -> 축, 미
    5: [0, 8],  # 기 -> 자, 신
    6: [1, 7],  # 경 -> 축, 미 -> 수정: 축, 인
    7: [2, 6],  # 신 -> 인, 오
    8: [3, 5],  # 임 -> 묘, 사
    9: [3, 5],  # 계 -> 묘, 사
}

# 문창귀인 (文昌貴人) - 일간 기준
MUNCHANG_GUIIN = {
    0: 5,  # 갑 -> 사
    1: 6,  # 을 -> 오
    2: 8,  # 병 -> 신
    3: 9,  # 정 -> 유
    4: 8,  # 무 -> 신
    5: 9,  # 기 -> 유
    6: 11,  # 경 -> 해
    7: 0,  # 신 -> 자
    8: 2,  # 임 -> 인
    9: 3,  # 계 -> 묘
}


# =============================================================================
# 60갑자 (Sixty Jiazi / Sexagenary Cycle)
# =============================================================================
def get_ganji_index(stem_idx: int, branch_idx: int) -> int:
    """천간과 지지로 60갑자 인덱스 계산"""
    # 음양이 맞아야 유효한 조합
    if (stem_idx % 2) != (branch_idx % 2):
        raise ValueError(f"Invalid stem-branch combination: {stem_idx}, {branch_idx}")
    return (stem_idx * 6 + branch_idx // 2) % 60


def get_stem_branch_from_ganji(ganji_idx: int) -> tuple[int, int]:
    """60갑자 인덱스로 천간/지지 인덱스 반환"""
    stem_idx = ganji_idx % 10
    branch_idx = ganji_idx % 12
    return stem_idx, branch_idx


# 60갑자 물상 (Metaphors for 60 Jiazi)
SIXTY_JIAZI_METAPHORS = {
    0: "바다 위의 금",  # 갑자 - 해중금
    1: "바다 위의 금",  # 을축 - 해중금
    2: "화로 속의 불",  # 병인 - 노중화
    3: "화로 속의 불",  # 정묘 - 노중화
    4: "큰 숲의 나무",  # 무진 - 대림목
    5: "큰 숲의 나무",  # 기사 - 대림목
    6: "길가의 흙",  # 경오 - 노방토
    7: "길가의 흙",  # 신미 - 노방토
    8: "칼날의 금",  # 임신 - 검봉금
    9: "칼날의 금",  # 계유 - 검봉금
    10: "산 위의 불",  # 갑술 - 산두화
    11: "산 위의 불",  # 을해 - 산두화
    12: "시냇물",  # 병자 - 간하수
    13: "시냇물",  # 정축 - 간하수
    14: "성벽의 흙",  # 무인 - 성두토
    15: "성벽의 흙",  # 기묘 - 성두토
    16: "흰 납",  # 경진 - 백납금
    17: "흰 납",  # 신사 - 백납금
    18: "버드나무",  # 임오 - 양류목
    19: "버드나무",  # 계미 - 양류목
    20: "샘물",  # 갑신 - 천천수 -> 수정: 정정수(井泉水)
    21: "샘물",  # 을유 - 천천수 -> 수정: 정정수(井泉水)
    22: "지붕 위의 흙",  # 병술 - 옥상토
    23: "지붕 위의 흙",  # 정해 - 옥상토
    24: "벼락의 불",  # 무자 - 벽력화
    25: "벼락의 불",  # 기축 - 벽력화
    26: "소나무/잣나무",  # 경인 - 송백목
    27: "소나무/잣나무",  # 신묘 - 송백목
    28: "흐르는 물",  # 임진 - 장류수
    29: "흐르는 물",  # 계사 - 장류수
    30: "모래 속의 금",  # 갑오 - 사중금
    31: "모래 속의 금",  # 을미 - 사중금
    32: "산 아래의 불",  # 병신 - 산하화
    33: "산 아래의 불",  # 정유 - 산하화
    34: "평지의 나무",  # 무술 - 평지목
    35: "평지의 나무",  # 기해 - 평지목
    36: "벽 위의 흙",  # 경자 - 벽상토
    37: "벽 위의 흙",  # 신축 - 벽상토
    38: "금박",  # 임인 - 금박금
    39: "금박",  # 계묘 - 금박금
    40: "등불의 불",  # 갑진 - 복등화
    41: "등불의 불",  # 을사 - 복등화
    42: "큰 물",  # 병오 - 천하수
    43: "큰 물",  # 정미 - 천하수
    44: "비녀의 금",  # 무신 - 대역토 -> 수정: 대역토
    45: "비녀의 금",  # 기유 - 대역토 -> 수정: 대역토
    46: "큰 바다의 물",  # 경술 - 차천금 -> 수정: 석류목
    47: "큰 바다의 물",  # 신해 - 차천금 -> 수정: 석류목
    48: "뽕나무",  # 임자 - 상자목 -> 수정: 상자목
    49: "뽕나무",  # 계축 - 상자목 -> 수정: 상자목
    50: "큰 시내의 물",  # 갑인 - 대계수 -> 수정: 대계수
    51: "큰 시내의 물",  # 을묘 - 대계수 -> 수정: 대계수
    52: "모래의 흙",  # 병진 - 사중토
    53: "모래의 흙",  # 정사 - 사중토
    54: "하늘 위의 불",  # 무오 - 천상화
    55: "하늘 위의 불",  # 기미 - 천상화
    56: "석류나무",  # 경신 - 석류목
    57: "석류나무",  # 신유 - 석류목
    58: "큰 바다의 물",  # 임술 - 대해수
    59: "큰 바다의 물",  # 계해 - 대해수
}


# =============================================================================
# 오호둔월법 (Month Stem from Year Stem)
# =============================================================================
# 연간(年干)에 따른 인월(寅月, 1월) 천간 결정
MONTH_STEM_START = {
    0: 2,  # 갑년, 기년 -> 병인월부터
    1: 4,  # 을년, 경년 -> 무인월부터
    2: 6,  # 병년, 신년 -> 경인월부터
    3: 8,  # 정년, 임년 -> 임인월부터
    4: 0,  # 무년, 계년 -> 갑인월부터
    5: 2,  # 기년 -> 병인월부터
    6: 4,  # 경년 -> 무인월부터
    7: 6,  # 신년 -> 경인월부터
    8: 8,  # 임년 -> 임인월부터
    9: 0,  # 계년 -> 갑인월부터
}


# =============================================================================
# 오서둔시법 (Hour Stem from Day Stem)
# =============================================================================
# 일간(日干)에 따른 자시(子時) 천간 결정
HOUR_STEM_START = {
    0: 0,  # 갑일, 기일 -> 갑자시부터
    1: 2,  # 을일, 경일 -> 병자시부터
    2: 4,  # 병일, 신일 -> 무자시부터
    3: 6,  # 정일, 임일 -> 경자시부터
    4: 8,  # 무일, 계일 -> 임자시부터
    5: 0,  # 기일 -> 갑자시부터
    6: 2,  # 경일 -> 병자시부터
    7: 4,  # 신일 -> 무자시부터
    8: 6,  # 임일 -> 경자시부터
    9: 8,  # 계일 -> 임자시부터
}


# =============================================================================
# 24절기 (24 Solar Terms)
# =============================================================================
SOLAR_TERMS = [
    {"name": "소한", "name_en": "Minor Cold", "angle": 285, "month": 1},
    {"name": "대한", "name_en": "Major Cold", "angle": 300, "month": 1},
    {"name": "입춘", "name_en": "Start of Spring", "angle": 315, "month": 2},  # 인월 시작
    {"name": "우수", "name_en": "Rain Water", "angle": 330, "month": 2},
    {"name": "경칩", "name_en": "Awakening of Insects", "angle": 345, "month": 3},  # 묘월 시작
    {"name": "춘분", "name_en": "Spring Equinox", "angle": 0, "month": 3},
    {"name": "청명", "name_en": "Clear and Bright", "angle": 15, "month": 4},  # 진월 시작
    {"name": "곡우", "name_en": "Grain Rain", "angle": 30, "month": 4},
    {"name": "입하", "name_en": "Start of Summer", "angle": 45, "month": 5},  # 사월 시작
    {"name": "소만", "name_en": "Grain Buds", "angle": 60, "month": 5},
    {"name": "망종", "name_en": "Grain in Ear", "angle": 75, "month": 6},  # 오월 시작
    {"name": "하지", "name_en": "Summer Solstice", "angle": 90, "month": 6},
    {"name": "소서", "name_en": "Minor Heat", "angle": 105, "month": 7},  # 미월 시작
    {"name": "대서", "name_en": "Major Heat", "angle": 120, "month": 7},
    {"name": "입추", "name_en": "Start of Autumn", "angle": 135, "month": 8},  # 신월 시작
    {"name": "처서", "name_en": "End of Heat", "angle": 150, "month": 8},
    {"name": "백로", "name_en": "White Dew", "angle": 165, "month": 9},  # 유월 시작
    {"name": "추분", "name_en": "Autumn Equinox", "angle": 180, "month": 9},
    {"name": "한로", "name_en": "Cold Dew", "angle": 195, "month": 10},  # 술월 시작
    {"name": "상강", "name_en": "Frost's Descent", "angle": 210, "month": 10},
    {"name": "입동", "name_en": "Start of Winter", "angle": 225, "month": 11},  # 해월 시작
    {"name": "소설", "name_en": "Minor Snow", "angle": 240, "month": 11},
    {"name": "대설", "name_en": "Major Snow", "angle": 255, "month": 12},  # 자월 시작
    {"name": "동지", "name_en": "Winter Solstice", "angle": 270, "month": 12},
]

# 절기(節氣) - 월 변경 기준점 (짝수 인덱스)
JEOL_TERMS = [SOLAR_TERMS[i] for i in range(0, 24, 2)]

# 중기(中氣) - 홀수 인덱스
JUNG_TERMS = [SOLAR_TERMS[i] for i in range(1, 24, 2)]


# =============================================================================
# 형충회합 (Clashes and Combinations)
# =============================================================================
# 육합 (Six Harmonies)
BRANCH_COMBINATIONS = {
    (0, 1): Element.EARTH,  # 자축합토
    (2, 11): Element.WOOD,  # 인해합목
    (3, 10): Element.FIRE,  # 묘술합화
    (4, 9): Element.METAL,  # 진유합금
    (5, 8): Element.WATER,  # 사신합수
    (6, 7): None,  # 오미합 (합토 또는 합화)
}

# 삼합 (Three Harmonies)
BRANCH_THREE_HARMONIES = {
    (8, 0, 4): Element.WATER,  # 신자진 수국
    (2, 6, 10): Element.FIRE,  # 인오술 화국
    (5, 9, 1): Element.METAL,  # 사유축 금국
    (11, 3, 7): Element.WOOD,  # 해묘미 목국
}

# 육충 (Six Clashes)
BRANCH_CLASHES = [
    (0, 6),  # 자오충
    (1, 7),  # 축미충
    (2, 8),  # 인신충
    (3, 9),  # 묘유충
    (4, 10),  # 진술충
    (5, 11),  # 사해충
]

# 원진 (Enmity)
BRANCH_ENMITY = [
    (0, 7),  # 자미원진
    (1, 6),  # 축오원진
    (2, 5),  # 인사원진
    (3, 4),  # 묘진원진
    (8, 11),  # 신해원진
    (9, 10),  # 유술원진
]
