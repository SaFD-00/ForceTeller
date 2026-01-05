"""
신살(神煞) 계산 모듈
길신/흉신 판단

12신살은 삼합(三合)을 기준으로 12운성의 특정 지지에 해당하는 신살을 판단합니다.
- 도화살(桃花煞): 목욕지(沐浴地) - 이성 매력
- 역마살(驛馬殺): 병지(病地) - 이동, 변동
- 화개살(華蓋殺): 묘지(墓地) - 학문, 예술, 종교
- 장성살(將星殺): 제왕지(帝旺地) - 왕성한 기운, 리더십
- 망신살(亡身殺): 임관지(臨官地) - 명예, 체면 관련
- 겁살(劫殺): 절지(絶地) - 경쟁, 시비
"""

from typing import Dict, List, Any, Optional
from config.constants import SHENSHA

# 삼합 그룹 정의 (년지/일지가 속한 삼합)
# 지지 번호: 0=자, 1=축, 2=인, 3=묘, 4=진, 5=사, 6=오, 7=미, 8=신, 9=유, 10=술, 11=해
SAMHAP_GROUPS = {
    # 신자진(申子辰) 삼합 - 水局
    8: '水', 0: '水', 4: '水',
    # 인오술(寅午戌) 삼합 - 火局
    2: '火', 6: '火', 10: '火',
    # 사유축(巳酉丑) 삼합 - 金局
    5: '金', 9: '金', 1: '金',
    # 해묘미(亥卯未) 삼합 - 木局
    11: '木', 3: '木', 7: '木',
}

# 삼합 그룹별 12신살 지지 매핑 (참고문서 기반)
# 기존 6개 신살
SHENSHA_BY_SAMHAP = {
    # 신자진(水) 삼합: 도화=유(9), 역마=인(2), 화개=진(4), 장성=자(0), 망신=신(8), 겁살=사(5)
    '水': {'도화': 9, '역마': 2, '화개': 4, '장성': 0, '망신': 8, '겁살': 5},
    # 인오술(火) 삼합: 도화=묘(3), 역마=신(8), 화개=술(10), 장성=오(6), 망신=인(2), 겁살=해(11)
    '火': {'도화': 3, '역마': 8, '화개': 10, '장성': 6, '망신': 2, '겁살': 11},
    # 사유축(金) 삼합: 도화=오(6), 역마=해(11), 화개=축(1), 장성=유(9), 망신=사(5), 겁살=인(2)
    '金': {'도화': 6, '역마': 11, '화개': 1, '장성': 9, '망신': 5, '겁살': 2},
    # 해묘미(木) 삼합: 도화=자(0), 역마=사(5), 화개=미(7), 장성=묘(3), 망신=해(11), 겁살=신(8)
    '木': {'도화': 0, '역마': 5, '화개': 7, '장성': 3, '망신': 11, '겁살': 8},
}

# 완전한 12신살 테이블 (삼합 그룹별)
# 순서: 겁살 → 재살 → 천살 → 지살 → 연살 → 월살 → 망신살 → 장성살 → 반안살 → 역마살 → 육해살 → 화개살
# 각 삼합의 마지막 글자 다음 지지부터 겁살 시작
FULL_12_SHENSHA_BY_SAMHAP = {
    # 신자진(水) 삼합: 마지막=진(4), 다음=사(5)부터 겁살 시작
    '水': {
        '겁살': 5, '재살': 6, '천살': 7, '지살': 8,
        '연살': 9, '월살': 10, '망신살': 11, '장성살': 0,
        '반안살': 1, '역마살': 2, '육해살': 3, '화개살': 4
    },
    # 인오술(火) 삼합: 마지막=술(10), 다음=해(11)부터 겁살 시작
    '火': {
        '겁살': 11, '재살': 0, '천살': 1, '지살': 2,
        '연살': 3, '월살': 4, '망신살': 5, '장성살': 6,
        '반안살': 7, '역마살': 8, '육해살': 9, '화개살': 10
    },
    # 사유축(金) 삼합: 마지막=축(1), 다음=인(2)부터 겁살 시작
    '金': {
        '겁살': 2, '재살': 3, '천살': 4, '지살': 5,
        '연살': 6, '월살': 7, '망신살': 8, '장성살': 9,
        '반안살': 10, '역마살': 11, '육해살': 0, '화개살': 1
    },
    # 해묘미(木) 삼합: 마지막=미(7), 다음=신(8)부터 겁살 시작
    '木': {
        '겁살': 8, '재살': 9, '천살': 10, '지살': 11,
        '연살': 0, '월살': 1, '망신살': 2, '장성살': 3,
        '반안살': 4, '역마살': 5, '육해살': 6, '화개살': 7
    },
}

# 괴강살 일주 조합 (경진, 경술, 임진, 임술, 무술)
# (천간, 지지) 형태로 저장
GOEGANG_COMBINATIONS = [
    (6, 4),   # 경진 (庚辰)
    (6, 10),  # 경술 (庚戌)
    (8, 4),   # 임진 (壬辰)
    (8, 10),  # 임술 (壬戌)
    (4, 10),  # 무술 (戊戌)
]

# 홍염살 - 일간 기준 특정 지지
# 갑->오, 을->신, 병->인, 정->미, 무->진/술, 기->진/술, 경->술, 신->유, 임->자, 계->신
HONGYEOM_TABLE = {
    0: [6],      # 갑 -> 오
    1: [8],      # 을 -> 신
    2: [2],      # 병 -> 인
    3: [7],      # 정 -> 미
    4: [4, 10],  # 무 -> 진, 술
    5: [4, 10],  # 기 -> 진, 술
    6: [10],     # 경 -> 술
    7: [9],      # 신 -> 유
    8: [0],      # 임 -> 자
    9: [8],      # 계 -> 신
}

# 천덕귀인 (天德貴人) - 월지 기준 천간
# 월지에 따라 해당하는 천간이 사주 어디에 있으면 천덕귀인
CHUNDEOK_TABLE = {
    # 월지 -> 천덕 천간 인덱스
    2: 3,   # 인월 -> 정(丁)
    3: 8,   # 묘월 -> 신(申) -> 이건 지지라 천간으로 변환 필요, 실제로는 임(壬)
    4: 8,   # 진월 -> 임(壬)
    5: 7,   # 사월 -> 신(辛)
    6: 0,   # 오월 -> 갑(甲)
    7: 9,   # 미월 -> 계(癸)
    8: 2,   # 신월 -> 병(丙)
    9: 1,   # 유월 -> 을(乙)
    10: 4,  # 술월 -> 무(戊)
    11: 3,  # 해월 -> 정(丁)
    0: 6,   # 자월 -> 경(庚)
    1: 5,   # 축월 -> 기(己)
}

# 월덕귀인 (月德貴人) - 월지 기준 천간
# 월지가 속한 삼합의 오행에 따라 천간 결정
WOLDEOK_TABLE = {
    # 인오술(火) -> 병(丙)
    2: 2, 6: 2, 10: 2,
    # 사유축(金) -> 경(庚)
    5: 6, 9: 6, 1: 6,
    # 신자진(水) -> 임(壬)
    8: 8, 0: 8, 4: 8,
    # 해묘미(木) -> 갑(甲)
    11: 0, 3: 0, 7: 0,
}

# 양인살 (羊刃殺) - 일간 기준 (건록 다음 지지 = 제왕지)
# 일간의 제왕지에 해당하는 지지
YANGIN_TABLE = {
    0: 3,   # 갑 -> 묘(卯) - 건록 인 다음
    1: 2,   # 을 -> 인(寅) - 음간은 역행, 건록 묘 이전
    2: 6,   # 병 -> 오(午)
    3: 5,   # 정 -> 사(巳)
    4: 6,   # 무 -> 오(午)
    5: 5,   # 기 -> 사(巳)
    6: 9,   # 경 -> 유(酉)
    7: 8,   # 신 -> 신(申)
    8: 0,   # 임 -> 자(子)
    9: 11,  # 계 -> 해(亥)
}

# 학당귀인 (學堂貴人) - 일간 기준 지지
# 장생지가 학당귀인이 되는 오행
HAKDANG_TABLE = {
    0: 11,  # 갑 -> 해(亥) - 목의 장생
    1: 6,   # 을 -> 오(午) - 음목 장생
    2: 2,   # 병 -> 인(寅) - 화의 장생
    3: 9,   # 정 -> 유(酉) - 음화 장생
    4: 2,   # 무 -> 인(寅) - 토는 화를 따름
    5: 9,   # 기 -> 유(酉)
    6: 5,   # 경 -> 사(巳) - 금의 장생
    7: 0,   # 신 -> 자(子) - 음금 장생
    8: 8,   # 임 -> 신(申) - 수의 장생
    9: 3,   # 계 -> 묘(卯) - 음수 장생
}

# 금여록 (金輿祿) - 일간 기준 지지
# 천간의 녹(祿)이 있는 지지의 전 지지
GEUMYEO_TABLE = {
    0: 4,   # 갑 -> 진(辰) - 건록 인 이전의 이전
    1: 5,   # 을 -> 사(巳)
    2: 7,   # 병 -> 미(未)
    3: 8,   # 정 -> 신(申)
    4: 7,   # 무 -> 미(未)
    5: 8,   # 기 -> 신(申)
    6: 10,  # 경 -> 술(戌)
    7: 11,  # 신 -> 해(亥)
    8: 1,   # 임 -> 축(丑)
    9: 2,   # 계 -> 인(寅)
}

# 백호살 (白虎殺) - 일지 기준 특정 지지 조합
# 일지가 특정 지지일 때 다른 위치에 특정 지지가 있으면
BAEKHO_TABLE = {
    0: 6,   # 자 -> 오
    1: 7,   # 축 -> 미
    2: 8,   # 인 -> 신
    3: 9,   # 묘 -> 유
    4: 10,  # 진 -> 술
    5: 11,  # 사 -> 해
    6: 0,   # 오 -> 자
    7: 1,   # 미 -> 축
    8: 2,   # 신 -> 인
    9: 3,   # 유 -> 묘
    10: 4,  # 술 -> 진
    11: 5,  # 해 -> 사
}

# 건록 (建祿) - 일간 기준 지지 (일간의 록지)
GEONROK_TABLE = {
    0: 2,   # 갑 -> 인
    1: 3,   # 을 -> 묘
    2: 5,   # 병 -> 사
    3: 6,   # 정 -> 오
    4: 5,   # 무 -> 사
    5: 6,   # 기 -> 오
    6: 8,   # 경 -> 신
    7: 9,   # 신 -> 유
    8: 11,  # 임 -> 해
    9: 0,   # 계 -> 자
}

# 천의귀인 (天醫貴人) - 일간 기준 지지 (의료/치유 재능)
CHUNUI_TABLE = {
    0: 1,   # 갑 -> 축
    1: 0,   # 을 -> 자
    2: 11,  # 병 -> 해
    3: 10,  # 정 -> 술
    4: 9,   # 무 -> 유
    5: 8,   # 기 -> 신
    6: 7,   # 경 -> 미
    7: 6,   # 신 -> 오
    8: 5,   # 임 -> 사
    9: 4,   # 계 -> 진
}

# 태극귀인 (太極貴人) - 일간 기준 지지
TAEGEUK_TABLE = {
    0: [0, 1],    # 갑 -> 자, 축
    1: [0, 1],    # 을 -> 자, 축
    2: [3, 6],    # 병 -> 묘, 오
    3: [3, 6],    # 정 -> 묘, 오
    4: [4, 10, 1, 7],  # 무 -> 진, 술, 축, 미
    5: [4, 10, 1, 7],  # 기 -> 진, 술, 축, 미
    6: [2, 11],   # 경 -> 인, 해
    7: [2, 11],   # 신 -> 인, 해
    8: [5, 8],    # 임 -> 사, 신
    9: [5, 8],    # 계 -> 사, 신
}

# 복성귀인 (福星貴人) - 일간 기준 지지
BOKSUNG_TABLE = {
    0: 2,   # 갑 -> 인
    1: 1,   # 을 -> 축
    2: 5,   # 병 -> 사
    3: 8,   # 정 -> 신
    4: 5,   # 무 -> 사
    5: 8,   # 기 -> 신
    6: 11,  # 경 -> 해
    7: 2,   # 신 -> 인
    8: 11,  # 임 -> 해
    9: 2,   # 계 -> 인
}

# 문곡귀인 (文曲貴人) - 일간 기준 지지 (문장력, 예술)
MUNGOK_TABLE = {
    0: 5,   # 갑 -> 사
    1: 6,   # 을 -> 오
    2: 7,   # 병 -> 미
    3: 8,   # 정 -> 신
    4: 9,   # 무 -> 유
    5: 10,  # 기 -> 술
    6: 11,  # 경 -> 해
    7: 0,   # 신 -> 자
    8: 1,   # 임 -> 축
    9: 2,   # 계 -> 인
}

# 황은대사 (皇恩大赦) - 일간 기준 지지 (황제의 은혜)
HWANGEUN_TABLE = {
    0: 6,   # 갑 -> 오
    1: 6,   # 을 -> 오
    2: 8,   # 병 -> 신
    3: 8,   # 정 -> 신
    4: 8,   # 무 -> 신
    5: 9,   # 기 -> 유
    6: 10,  # 경 -> 술
    7: 11,  # 신 -> 해
    8: 11,  # 임 -> 해
    9: 0,   # 계 -> 자
}

# 현침살 (懸針殺) - 일간 기준 (의료/기술직)
HYUNCHIM_TABLE = {
    0: 8,   # 갑 -> 신
    1: 9,   # 을 -> 유
    2: 8,   # 병 -> 신
    3: 9,   # 정 -> 유
    4: 8,   # 무 -> 신
    5: 9,   # 기 -> 유
    6: 2,   # 경 -> 인
    7: 3,   # 신 -> 묘
    8: 2,   # 임 -> 인
    9: 3,   # 계 -> 묘
}

# 급각살 (急脚殺) - 일간 기준 (다리 부상)
GEUPGAK_TABLE = {
    0: 11,  # 갑 -> 해
    1: 8,   # 을 -> 신
    2: 2,   # 병 -> 인
    3: 9,   # 정 -> 유
    4: 2,   # 무 -> 인
    5: 9,   # 기 -> 유
    6: 5,   # 경 -> 사
    7: 0,   # 신 -> 자
    8: 5,   # 임 -> 사
    9: 6,   # 계 -> 오
}

# 탕화살 (湯火殺) - 일지 기준 (뜨거운 물/불 사고)
TANGHWA_TABLE = {
    0: 6,   # 자 -> 오
    1: 5,   # 축 -> 사
    2: 6,   # 인 -> 오
    3: 5,   # 묘 -> 사
    4: 6,   # 진 -> 오
    5: 6,   # 사 -> 오
    6: 0,   # 오 -> 자
    7: 11,  # 미 -> 해
    8: 0,   # 신 -> 자
    9: 11,  # 유 -> 해
    10: 0,  # 술 -> 자
    11: 0,  # 해 -> 자
}

# 낙정관살 (落井關殺) - 일지 기준 (물 관련 사고)
NAKJEONG_TABLE = {
    2: 11,  # 인 -> 해
    3: 0,   # 묘 -> 자
    5: 1,   # 사 -> 축
    8: 5,   # 신 -> 사
    9: 6,   # 유 -> 오
    11: 7,  # 해 -> 미
}

# 고신살 (孤辰殺) - 년지/일지 기준 (남자 고독)
GOSHIN_TABLE = {
    2: 5, 3: 5, 4: 5,     # 인묘진 -> 사
    5: 8, 6: 8, 7: 8,     # 사오미 -> 신
    8: 11, 9: 11, 10: 11, # 신유술 -> 해
    11: 2, 0: 2, 1: 2,    # 해자축 -> 인
}

# 과숙살 (寡宿殺) - 년지/일지 기준 (여자 고독)
GWASUK_TABLE = {
    2: 1, 3: 1, 4: 1,     # 인묘진 -> 축
    5: 4, 6: 4, 7: 4,     # 사오미 -> 진
    8: 7, 9: 7, 10: 7,    # 신유술 -> 미
    11: 10, 0: 10, 1: 10, # 해자축 -> 술
}

# 상문 (喪門) - 년지 기준 (상복, 장례)
SANGMUN_TABLE = {
    0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7,
    6: 8, 7: 9, 8: 10, 9: 11, 10: 0, 11: 1,
}

# 조객 (吊客) - 년지 기준 (조문객)
JOGAEK_TABLE = {
    0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11,
    6: 0, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5,
}

# 십악대패살 (十惡大敗殺) - 특정 일주 조합
SIBAK_DAEPAE_COMBINATIONS = [
    (0, 4),   # 갑진
    (1, 5),   # 을사
    (2, 8),   # 병신
    (3, 11),  # 정해
    (4, 2),   # 무인
    (5, 11),  # 기해
    (6, 4),   # 경진
    (7, 5),   # 신사
    (8, 8),   # 임신
    (9, 11),  # 계해
]

# 천라지망살 (天羅地網殺) - 특정 지지 조합
# 사술(巳戌) = 천라, 해진(亥辰) = 지망
CHUNRA_JIMANG = {
    '천라': [(5, 10), (10, 5)],  # 사-술 조합
    '지망': [(11, 4), (4, 11)],  # 해-진 조합
}

# 월공귀인 (月空貴人) - 월지 기준 천간
# 월지에 따라 해당 천간이 있으면 월공귀인
WOLGONG_TABLE = {
    2: 5,   # 인월 -> 기
    3: 0,   # 묘월 -> 갑
    4: 9,   # 진월 -> 계
    5: 2,   # 사월 -> 병
    6: 7,   # 오월 -> 신
    7: 4,   # 미월 -> 무
    8: 3,   # 신월 -> 정
    9: 8,   # 유월 -> 임
    10: 1,  # 술월 -> 을
    11: 6,  # 해월 -> 경
    0: 5,   # 자월 -> 기
    1: 0,   # 축월 -> 갑
}

# 암록귀인 (暗祿貴人) - 일간의 건록 충 위치
# 건록의 충이 되는 지지가 사주에 있으면 암록귀인
AMROK_TABLE = {
    0: 8,   # 갑(건록 인) -> 신(인의 충)
    1: 9,   # 을(건록 묘) -> 유(묘의 충)
    2: 11,  # 병(건록 사) -> 해(사의 충)
    3: 0,   # 정(건록 오) -> 자(오의 충)
    4: 11,  # 무(건록 사) -> 해
    5: 0,   # 기(건록 오) -> 자
    6: 2,   # 경(건록 신) -> 인(신의 충)
    7: 3,   # 신(건록 유) -> 묘(유의 충)
    8: 5,   # 임(건록 해) -> 사(해의 충)
    9: 6,   # 계(건록 자) -> 오(자의 충)
}

# 재고귀인 (財庫貴人) - 일지가 진술축미(토고)일 때
# 진술축미는 재물 창고
JAEGO_BRANCHES = [1, 4, 7, 10]  # 축, 진, 미, 술

# 효신살 (梟神殺) - 년지 기준
# 년지에 따라 특정 지지가 효신살
HYOSHIN_TABLE = {
    0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11,
    6: 0, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5,
}

# 고란살 (孤鸞殺) - 특정 일주 조합
# 을사, 정사, 신해, 무신, 갑인, 임자, 병오
GORAN_COMBINATIONS = [
    (1, 5),   # 을사
    (3, 5),   # 정사
    (7, 11),  # 신해
    (4, 8),   # 무신
    (0, 2),   # 갑인
    (8, 0),   # 임자
    (2, 6),   # 병오
]

# 삼기귀인 (三奇貴人) - 세 천간이 연속으로 있을 때
# 천상삼기: 을병정 (1, 2, 3)
# 지상삼기: 갑무경 (0, 4, 6)
# 인중삼기: 임계기 (8, 9, 5)
SAMGI_PATTERNS = {
    '천상삼기': [1, 2, 3],   # 을, 병, 정
    '지상삼기': [0, 4, 6],   # 갑, 무, 경
    '인중삼기': [8, 9, 5],   # 임, 계, 기
}


class ShenshaCalculator:
    """신살 계산 클래스"""

    def __init__(
        self,
        year_pillar: tuple,
        month_pillar: tuple,
        day_pillar: tuple,
        hour_pillar: tuple = None
    ):
        """
        Args:
            year_pillar: (천간, 지지) 년주
            month_pillar: (천간, 지지) 월주
            day_pillar: (천간, 지지) 일주
            hour_pillar: (천간, 지지) 시주
        """
        self.year = year_pillar
        self.month = month_pillar
        self.day = day_pillar
        self.hour = hour_pillar

        self.year_branch = year_pillar[1] if year_pillar else None
        self.month_branch = month_pillar[1] if month_pillar else None
        self.day_stem = day_pillar[0] if day_pillar else None
        self.day_branch = day_pillar[1] if day_pillar else None

        # 삼합 그룹 결정 (년지 기준)
        self.samhap_group = SAMHAP_GROUPS.get(self.year_branch) if self.year_branch is not None else None

        # 공망 계산 (일주 기준)
        self.gongmang_branches = self._calculate_gongmang() if self.day else []

    def _calculate_gongmang(self) -> List[int]:
        """
        공망(空亡) 지지 계산
        일주가 속한 순(旬)에서 빠진 두 지지를 반환
        """
        if not self.day:
            return []

        stem = self.day[0]
        branch = self.day[1]

        # 60갑자 인덱스 계산: (6 * stem - 5 * branch) % 60
        ganji_index = (6 * stem - 5 * branch) % 60

        # 순(旬) 인덱스: 0~5 (갑자순, 갑술순, 갑신순, 갑오순, 갑진순, 갑인순)
        xun_index = ganji_index // 10

        # 공망 지지: 순에 따라 결정
        # 순0(갑자): 술(10),해(11), 순1(갑술): 신(8),유(9), 순2(갑신): 오(6),미(7)
        # 순3(갑오): 진(4),사(5), 순4(갑진): 인(2),묘(3), 순5(갑인): 자(0),축(1)
        first_gongmang = (10 - 2 * xun_index) % 12
        second_gongmang = (11 - 2 * xun_index) % 12

        return [first_gongmang, second_gongmang]

    def calculate_all_shensha(self) -> List[Dict[str, Any]]:
        """
        모든 신살 계산

        Returns:
            [{name, type, position, description}, ...]
        """
        result = []

        # 년지 기준 신살 (삼합 기반 12신살)
        if self.year_branch is not None:
            result.extend(self._check_samhap_based_shensha())

        # 월지 기준 신살 (천덕귀인, 월덕귀인)
        if self.month is not None:
            result.extend(self._check_month_branch_shensha())

        # 일간 기준 신살
        if self.day_stem is not None:
            result.extend(self._check_day_stem_shensha())

        # 일지 기준 신살
        if self.day_branch is not None:
            result.extend(self._check_day_branch_shensha())

        # 일주 조합 기준 신살 (괴강살, 십악대패살)
        result.extend(self._check_day_pillar_shensha())

        # 공망살
        result.extend(self._check_gongmang_shensha())

        # 천라지망살
        result.extend(self._check_chunra_jimang_shensha())

        # 년지 기준 신살 (상문, 조객)
        result.extend(self._check_year_based_shensha())

        # 삼기귀인
        result.extend(self._check_samgi_shensha())

        return result

    def _check_samhap_based_shensha(self) -> List[Dict]:
        """
        삼합(三合) 기반 12신살 확인
        년지가 속한 삼합 그룹을 기준으로 12신살을 판단합니다.
        """
        result = []

        if self.samhap_group is None:
            return result

        # 완전한 12신살 테이블 사용
        shensha_map = FULL_12_SHENSHA_BY_SAMHAP.get(self.samhap_group, {})

        # 12신살 정보 정의 (전체) - "한글 (한문)" 형식
        shensha_info = {
            '겁살': {
                'name': '겁살 (劫殺)',
                'type': '흉신',
                'hanja': '劫殺',
                'description': SHENSHA.get("겁살", {}).get("description", "경쟁과 시비, 재물 손실 우려, 절지(絶地)에 해당")
            },
            '재살': {
                'name': '재살 (災殺)',
                'type': '흉신',
                'hanja': '災殺',
                'description': SHENSHA.get("재살", {}).get("description", "재앙과 질병의 별, 태지(胎地)에 해당")
            },
            '천살': {
                'name': '천살 (天殺)',
                'type': '흉신',
                'hanja': '天殺',
                'description': SHENSHA.get("천살", {}).get("description", "하늘의 재앙, 양지(養地)에 해당, 예기치 못한 사고")
            },
            '지살': {
                'name': '지살 (地殺)',
                'type': '흉신',
                'hanja': '地殺',
                'description': SHENSHA.get("지살", {}).get("description", "땅의 재앙, 장생지(長生地)에 해당, 부동산/토지 관련 흉")
            },
            '연살': {
                'name': '연살 (年殺)',
                'type': '흉신',
                'hanja': '年殺',
                'description': SHENSHA.get("연살", {}).get("description", "해당 년의 액운, 목욕지에 해당")
            },
            '월살': {
                'name': '월살 (月殺)',
                'type': '흉신',
                'hanja': '月殺',
                'description': SHENSHA.get("월살", {}).get("description", "해당 월의 액운, 관대지에 해당")
            },
            '망신살': {
                'name': '망신살 (亡身殺)',
                'type': '흉신',
                'hanja': '亡身殺',
                'description': SHENSHA.get("망신", {}).get("description", "체면과 명예 관련 구설수, 자신을 드러냄, 임관지에 해당")
            },
            '장성살': {
                'name': '장성살 (將星殺)',
                'type': '길신',
                'hanja': '將星殺',
                'description': SHENSHA.get("장성", {}).get("description", "왕성한 기운, 리더십과 권력의 별, 제왕지에 해당")
            },
            '반안살': {
                'name': '반안살 (攀鞍殺)',
                'type': '길신',
                'hanja': '攀鞍殺',
                'description': SHENSHA.get("반안살", {}).get("description", "안장에 오름, 승진과 발전의 별, 쇠지(衰地)에 해당")
            },
            '역마살': {
                'name': '역마살 (驛馬殺)',
                'type': '중성',
                'hanja': '驛馬殺',
                'description': SHENSHA.get("역마", {}).get("description", "이동과 변동이 많은 별, 잦은 이동수, 병지(病地)에 해당")
            },
            '육해살': {
                'name': '육해살 (六害殺)',
                'type': '흉신',
                'hanja': '六害殺',
                'description': SHENSHA.get("육해살", {}).get("description", "육친과의 갈등, 해로운 관계, 사지(死地)에 해당")
            },
            '화개살': {
                'name': '화개살 (華蓋殺)',
                'type': '길신',
                'hanja': '華蓋殺',
                'description': SHENSHA.get("화개", {}).get("description", "학문, 예술, 종교적 심성의 별, 묘지(墓地)에 해당")
            },
            # 도화살은 별도 (목욕지 = 연살과 같은 위치지만 다른 의미)
            '도화': {
                'name': '도화살 (桃花殺)',
                'type': '중성',
                'hanja': '桃花殺',
                'description': SHENSHA.get("도화", {}).get("description", "이성에게 매력을 끼치는 별, 색정과 연애 운")
            },
        }

        # 각 신살별로 사주 내 지지 확인
        for shensha_name, target_branch in shensha_map.items():
            info = shensha_info.get(shensha_name, {})
            for pillar, branch in self._get_all_branches():
                if branch == target_branch:
                    result.append({
                        "name": info.get('name', shensha_name),
                        "hanja": info.get('hanja', ''),
                        "type": info.get('type', '중성'),
                        "position": pillar,
                        "description": info.get('description', '')
                    })

        # 도화살 추가 검사 (기존 SHENSHA_BY_SAMHAP의 도화 사용)
        dohua_branch = SHENSHA_BY_SAMHAP.get(self.samhap_group, {}).get('도화')
        if dohua_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == dohua_branch:
                    info = shensha_info.get('도화', {})
                    result.append({
                        "name": info.get('name', '도화살'),
                        "hanja": info.get('hanja', ''),
                        "type": info.get('type', '중성'),
                        "position": pillar,
                        "description": info.get('description', '')
                    })

        return result

    def _check_year_branch_shensha(self) -> List[Dict]:
        """년지 기준 신살 확인 (하위 호환용)"""
        return self._check_samhap_based_shensha()

    def _check_day_stem_shensha(self) -> List[Dict]:
        """일간 기준 신살 확인"""
        result = []

        # 천을귀인 (天乙貴人)
        # 일간 기준 천을귀인 지지
        chuneul_table = {
            0: [1, 7],   # 갑 -> 축, 미
            1: [0, 8],   # 을 -> 자, 신
            2: [11, 9],  # 병 -> 해, 유
            3: [11, 9],  # 정 -> 해, 유
            4: [1, 7],   # 무 -> 축, 미
            5: [0, 8],   # 기 -> 자, 신
            6: [1, 7],   # 경 -> 축, 미 (또는 인, 오)
            7: [2, 6],   # 신 -> 인, 오
            8: [3, 5],   # 임 -> 묘, 사
            9: [3, 5],   # 계 -> 묘, 사
        }

        chuneul_branches = chuneul_table.get(self.day_stem, [])
        for pillar, branch in self._get_all_branches():
            if branch in chuneul_branches:
                result.append({
                    "name": "천을귀인 (天乙貴人)",
                    "hanja": "天乙貴人",
                    "type": "길신",
                    "position": pillar,
                    "description": SHENSHA.get("천을귀인", {}).get("description", "귀인의 도움을 받음, 위기에서 구원받음")
                })

        # 문창귀인 (文昌貴人)
        munchang_table = {
            0: [5],  # 갑 -> 사
            1: [6],  # 을 -> 오
            2: [8],  # 병 -> 신
            3: [9],  # 정 -> 유
            4: [8],  # 무 -> 신
            5: [9],  # 기 -> 유
            6: [11], # 경 -> 해
            7: [0],  # 신 -> 자
            8: [2],  # 임 -> 인
            9: [3],  # 계 -> 묘
        }

        munchang_branches = munchang_table.get(self.day_stem, [])
        for pillar, branch in self._get_all_branches():
            if branch in munchang_branches:
                result.append({
                    "name": "문창귀인 (文昌貴人)",
                    "hanja": "文昌貴人",
                    "type": "길신",
                    "position": pillar,
                    "description": SHENSHA.get("문창귀인", {}).get("description", "학문, 시험 운이 좋음, 글재주")
                })

        # 홍염살 (紅艶殺) - 일간 기준
        hongyeom_branches = HONGYEOM_TABLE.get(self.day_stem, [])
        for pillar, branch in self._get_all_branches():
            if branch in hongyeom_branches:
                result.append({
                    "name": "홍염살 (紅艶殺)",
                    "hanja": "紅艶殺",
                    "type": "중성",
                    "position": pillar,
                    "description": SHENSHA.get("홍염살", {}).get("description", "능동적 매력, 타겟에게 의도적 매력 발산")
                })

        # 양인살 (羊刃殺) - 일간 기준
        yangin_branch = YANGIN_TABLE.get(self.day_stem)
        if yangin_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == yangin_branch:
                    result.append({
                        "name": "양인살 (羊刃殺)",
                        "hanja": "羊刃殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": SHENSHA.get("양인살", {}).get("description", "날카로운 칼날의 별, 강한 기운이나 재앙 우려, 제왕지에 해당")
                    })

        # 학당귀인 (學堂貴人) - 일간 기준
        hakdang_branch = HAKDANG_TABLE.get(self.day_stem)
        if hakdang_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == hakdang_branch:
                    result.append({
                        "name": "학당귀인 (學堂貴人)",
                        "hanja": "學堂貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": SHENSHA.get("학당귀인", {}).get("description", "학문에 뛰어난 재능, 총명함, 장생지에 해당")
                    })

        # 금여록 (金輿祿) - 일간 기준
        geumyeo_branch = GEUMYEO_TABLE.get(self.day_stem)
        if geumyeo_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == geumyeo_branch:
                    result.append({
                        "name": "금여록 (金輿祿)",
                        "hanja": "金輿祿",
                        "type": "길신",
                        "position": pillar,
                        "description": SHENSHA.get("금여록", {}).get("description", "금수레의 별, 명예와 부귀를 누림, 귀한 배우자")
                    })

        # 건록 (建祿) - 일간 기준
        geonrok_branch = GEONROK_TABLE.get(self.day_stem)
        if geonrok_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == geonrok_branch:
                    result.append({
                        "name": "건록 (建祿)",
                        "hanja": "建祿",
                        "type": "길신",
                        "position": pillar,
                        "description": "녹(祿)을 세움, 안정적 직업과 재물 기반, 건강하고 활동적"
                    })

        # 협록 (挾祿) - 건록 양옆 지지
        if geonrok_branch is not None:
            hyeoprok_branches = [(geonrok_branch - 1) % 12, (geonrok_branch + 1) % 12]
            for pillar, branch in self._get_all_branches():
                if branch in hyeoprok_branches:
                    result.append({
                        "name": "협록 (挾祿)",
                        "hanja": "挾祿",
                        "type": "길신",
                        "position": pillar,
                        "description": "녹을 끼고 있음, 재물과 도움이 곁에 있음"
                    })

        # 천의귀인 (天醫貴人) - 일간 기준
        chunui_branch = CHUNUI_TABLE.get(self.day_stem)
        if chunui_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == chunui_branch:
                    result.append({
                        "name": "천의귀인 (天醫貴人)",
                        "hanja": "天醫貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": "하늘의 의사, 의료/치유 재능, 건강 회복 운"
                    })

        # 태극귀인 (太極貴人) - 일간 기준
        taegeuk_branches = TAEGEUK_TABLE.get(self.day_stem, [])
        for pillar, branch in self._get_all_branches():
            if branch in taegeuk_branches:
                result.append({
                    "name": "태극귀인 (太極貴人)",
                    "hanja": "太極貴人",
                    "type": "길신",
                    "position": pillar,
                    "description": "시작과 끝의 별, 리더십, 높은 지위 도달"
                })

        # 복성귀인 (福星貴人) - 일간 기준
        boksung_branch = BOKSUNG_TABLE.get(self.day_stem)
        if boksung_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == boksung_branch:
                    result.append({
                        "name": "복성귀인 (福星貴人)",
                        "hanja": "福星貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": "복과 행운을 가져오는 별"
                    })

        # 문곡귀인 (文曲貴人) - 일간 기준
        mungok_branch = MUNGOK_TABLE.get(self.day_stem)
        if mungok_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == mungok_branch:
                    result.append({
                        "name": "문곡귀인 (文曲貴人)",
                        "hanja": "文曲貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": "문장력과 예술적 감각이 뛰어남"
                    })

        # 황은대사 (皇恩大赦) - 일간 기준
        hwangeun_branch = HWANGEUN_TABLE.get(self.day_stem)
        if hwangeun_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == hwangeun_branch:
                    result.append({
                        "name": "황은대사 (皇恩大赦)",
                        "hanja": "皇恩大赦",
                        "type": "길신",
                        "position": pillar,
                        "description": "황제의 은혜, 높은 지위와 명예, 사면 받음"
                    })

        # 현침살 (懸針殺) - 일간 기준
        hyunchim_branch = HYUNCHIM_TABLE.get(self.day_stem)
        if hyunchim_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == hyunchim_branch:
                    result.append({
                        "name": "현침살 (懸針殺)",
                        "hanja": "懸針殺",
                        "type": "중성",
                        "position": pillar,
                        "description": "바늘에 걸림, 의료/기술직에 유리, 날카로운 재능"
                    })

        # 급각살 (急脚殺) - 일간 기준
        geupgak_branch = GEUPGAK_TABLE.get(self.day_stem)
        if geupgak_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == geupgak_branch:
                    result.append({
                        "name": "급각살 (急脚殺)",
                        "hanja": "急脚殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "다리 부상, 이동 장애, 급하게 움직이다 사고"
                    })

        # 암록귀인 (暗祿貴人) - 일간 기준 (건록의 충 위치)
        amrok_branch = AMROK_TABLE.get(self.day_stem)
        if amrok_branch is not None:
            for pillar, branch in self._get_all_branches():
                if branch == amrok_branch:
                    result.append({
                        "name": "암록귀인 (暗祿貴人)",
                        "hanja": "暗祿貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": "숨겨진 재물, 은밀한 도움, 예상치 못한 복"
                    })

        # 재고귀인 (財庫貴人) - 일지가 진술축미일 때
        if self.day_branch in JAEGO_BRANCHES:
            result.append({
                "name": "재고귀인 (財庫貴人)",
                "hanja": "財庫貴人",
                "type": "길신",
                "position": "day",
                "description": "재물 창고, 부의 축적 능력, 저축 운이 좋음"
            })

        return result

    def _check_day_branch_shensha(self) -> List[Dict]:
        """일지 기준 신살 확인"""
        result = []

        # 원진살 (怨嗔殺) 검사
        # 자-미, 축-오, 인-사, 묘-진, 진-묘, 사-인, 오-축, 미-자
        # 신-해, 유-술, 술-유, 해-신
        wonjin_pairs = {
            0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2,
            6: 1, 7: 0, 8: 11, 9: 10, 10: 9, 11: 8
        }

        wonjin_target = wonjin_pairs.get(self.day_branch)
        for pillar, branch in self._get_all_branches():
            if pillar != "day" and branch == wonjin_target:
                result.append({
                    "name": "원진살 (怨嗔殺)",
                    "hanja": "怨嗔殺",
                    "type": "흉신",
                    "position": pillar,
                    "description": SHENSHA.get("원진", {}).get("description", "인연의 괴로움, 서로 불편한 관계")
                })

        # 귀문관살 (鬼門關殺) 검사
        # 자-유, 축-술, 인-미, 묘-오, 진-사, 사-진
        gwimun_pairs = {
            0: 9, 1: 10, 2: 7, 3: 6, 4: 5, 5: 4,
            6: 3, 7: 2, 8: 1, 9: 0, 10: 11, 11: 8
        }

        gwimun_target = gwimun_pairs.get(self.day_branch)
        for pillar, branch in self._get_all_branches():
            if pillar != "day" and branch == gwimun_target:
                result.append({
                    "name": "귀문관살 (鬼門關殺)",
                    "hanja": "鬼門關殺",
                    "type": "흉신",
                    "position": pillar,
                    "description": SHENSHA.get("귀문관살", {}).get("description", "정신적 고민, 신비 체험, 예민한 감각")
                })

        # 백호살 (白虎殺) 검사 - 일지 기준 충
        baekho_target = BAEKHO_TABLE.get(self.day_branch)
        if baekho_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "day" and branch == baekho_target:
                    result.append({
                        "name": "백호살 (白虎殺)",
                        "hanja": "白虎殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": SHENSHA.get("백호살", {}).get("description", "흰 호랑이의 별, 혈광지사 우려, 외과적 수술 암시")
                    })

        # 탕화살 (湯火殺) - 일지 기준
        tanghwa_target = TANGHWA_TABLE.get(self.day_branch)
        if tanghwa_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "day" and branch == tanghwa_target:
                    result.append({
                        "name": "탕화살 (湯火殺)",
                        "hanja": "湯火殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "뜨거운 물/불 관련 사고 주의, 화상 위험"
                    })

        # 낙정관살 (落井關殺) - 일지 기준
        nakjeong_target = NAKJEONG_TABLE.get(self.day_branch)
        if nakjeong_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "day" and branch == nakjeong_target:
                    result.append({
                        "name": "낙정관살 (落井關殺)",
                        "hanja": "落井關殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "우물에 빠짐, 물 관련 사고 주의"
                    })

        # 고신살 (孤辰殺) - 일지 기준 (남자)
        goshin_target = GOSHIN_TABLE.get(self.day_branch)
        if goshin_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "day" and branch == goshin_target:
                    result.append({
                        "name": "고신살 (孤辰殺)",
                        "hanja": "孤辰殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "남자에게 고독, 배우자와 이별 또는 독신 가능성"
                    })

        # 과숙살 (寡宿殺) - 일지 기준 (여자)
        gwasuk_target = GWASUK_TABLE.get(self.day_branch)
        if gwasuk_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "day" and branch == gwasuk_target:
                    result.append({
                        "name": "과숙살 (寡宿殺)",
                        "hanja": "寡宿殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "여자에게 고독, 배우자와 이별 또는 독신 가능성"
                    })

        return result

    def _check_day_pillar_shensha(self) -> List[Dict]:
        """일주 조합 기준 신살 확인 (괴강살, 십악대패살 등)"""
        result = []

        if self.day is None:
            return result

        day_stem = self.day[0]
        day_branch = self.day[1]

        # 괴강살 (魁罡殺) 검사
        # 경진(庚辰), 경술(庚戌), 임진(壬辰), 임술(壬戌), 무술(戊戌)
        if (day_stem, day_branch) in GOEGANG_COMBINATIONS:
            result.append({
                "name": "괴강살 (魁罡殺)",
                "hanja": "魁罡殺",
                "type": "중성",
                "position": "day",
                "description": SHENSHA.get("괴강살", {}).get(
                    "description",
                    "북두칠성의 우두머리 별, 총명하고 카리스마가 강함, 대발 또는 대흉의 극단적 운명"
                )
            })

        # 십악대패살 (十惡大敗殺) 검사
        if (day_stem, day_branch) in SIBAK_DAEPAE_COMBINATIONS:
            result.append({
                "name": "십악대패살 (十惡大敗殺)",
                "hanja": "十惡大敗殺",
                "type": "흉신",
                "position": "day",
                "description": "10개의 흉일주, 큰 재앙과 패망의 위험, 신중함 필요"
            })

        # 고란살 (孤鸞殺) 검사 - 을사, 정사, 신해, 무신, 갑인, 임자, 병오
        if (day_stem, day_branch) in GORAN_COMBINATIONS:
            result.append({
                "name": "고란살 (孤鸞殺)",
                "hanja": "孤鸞殺",
                "type": "흉신",
                "position": "day",
                "description": "외로운 난새, 배우자 복이 약함, 혼인 지연 또는 이별"
            })

        return result

    def _check_gongmang_shensha(self) -> List[Dict]:
        """공망살 (空亡殺) 확인"""
        result = []

        if not self.gongmang_branches:
            return result

        for pillar, branch in self._get_all_branches():
            if branch in self.gongmang_branches:
                result.append({
                    "name": "공망살 (空亡殺)",
                    "hanja": "空亡殺",
                    "type": "흉신",
                    "position": pillar,
                    "description": "빈 것, 허무, 해당 주의 기운이 약해짐, 노력이 헛됨"
                })

        return result

    def _check_chunra_jimang_shensha(self) -> List[Dict]:
        """천라지망살 (天羅地網殺) 확인"""
        result = []

        all_branches = [b for _, b in self._get_all_branches()]

        # 천라 (巳-戌)
        if 5 in all_branches and 10 in all_branches:
            result.append({
                "name": "천라살 (天羅殺)",
                "hanja": "天羅殺",
                "type": "흉신",
                "position": "사주",
                "description": "하늘의 그물, 구속과 제약, 관재/소송 주의"
            })

        # 지망 (亥-辰)
        if 11 in all_branches and 4 in all_branches:
            result.append({
                "name": "지망살 (地網殺)",
                "hanja": "地網殺",
                "type": "흉신",
                "position": "사주",
                "description": "땅의 그물, 구속과 제약, 곤란한 상황"
            })

        return result

    def _check_year_based_shensha(self) -> List[Dict]:
        """년지 기준 신살 확인 (상문, 조객, 효신살)"""
        result = []

        if self.year_branch is None:
            return result

        # 상문 (喪門) - 년지 기준
        sangmun_target = SANGMUN_TABLE.get(self.year_branch)
        if sangmun_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "year" and branch == sangmun_target:
                    result.append({
                        "name": "상문 (喪門)",
                        "hanja": "喪門",
                        "type": "흉신",
                        "position": pillar,
                        "description": "상복, 장례 관련, 가족 건강 주의"
                    })

        # 조객 (吊客) - 년지 기준
        jogaek_target = JOGAEK_TABLE.get(self.year_branch)
        if jogaek_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "year" and branch == jogaek_target:
                    result.append({
                        "name": "조객 (吊客)",
                        "hanja": "吊客",
                        "type": "흉신",
                        "position": pillar,
                        "description": "조문객, 조의금, 타인의 상 소식"
                    })

        # 효신살 (梟神殺) - 년지 기준
        hyoshin_target = HYOSHIN_TABLE.get(self.year_branch)
        if hyoshin_target is not None:
            for pillar, branch in self._get_all_branches():
                if pillar != "year" and branch == hyoshin_target:
                    result.append({
                        "name": "효신살 (梟神殺)",
                        "hanja": "梟神殺",
                        "type": "흉신",
                        "position": pillar,
                        "description": "효조(올빼미)의 별, 부모 상 또는 효도 문제, 은혜를 갚지 못함"
                    })

        return result

    def _check_samgi_shensha(self) -> List[Dict]:
        """삼기귀인 (三奇貴人) 확인 - 세 천간이 모두 있을 때"""
        result = []

        # 모든 천간 수집
        all_stems = [s for _, s in self._get_all_stems()]

        # 삼기 패턴 검사
        samgi_descriptions = {
            '천상삼기': "을병정(乙丙丁), 하늘의 세 기이한 별, 큰 복과 귀함",
            '지상삼기': "갑무경(甲戊庚), 땅의 세 기이한 별, 안정과 재물",
            '인중삼기': "임계기(壬癸己), 인간의 세 기이한 별, 지혜와 융통성",
        }

        for samgi_name, stems in SAMGI_PATTERNS.items():
            if all(stem in all_stems for stem in stems):
                result.append({
                    "name": f"삼기귀인 (三奇貴人) - {samgi_name}",
                    "hanja": "三奇貴人",
                    "type": "길신",
                    "position": "사주",
                    "description": samgi_descriptions.get(samgi_name, "세 가지 기이한 별, 특별한 재능과 복")
                })

        return result

    def _check_month_branch_shensha(self) -> List[Dict]:
        """월지 기준 신살 확인 (천덕귀인, 월덕귀인, 월공귀인)"""
        result = []

        if self.month is None:
            return result

        month_branch = self.month[1]

        # 천덕귀인 (天德貴人) - 월지 기준 천간 검사
        chundeok_stem = CHUNDEOK_TABLE.get(month_branch)
        if chundeok_stem is not None:
            for pillar, stem in self._get_all_stems():
                if stem == chundeok_stem:
                    result.append({
                        "name": "천덕귀인 (天德貴人)",
                        "hanja": "天德貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": SHENSHA.get("천덕귀인", {}).get("description", "하늘의 덕을 받는 귀인, 재난을 피하고 복을 받음")
                    })

        # 월덕귀인 (月德貴人) - 월지 기준 천간 검사
        woldeok_stem = WOLDEOK_TABLE.get(month_branch)
        if woldeok_stem is not None:
            for pillar, stem in self._get_all_stems():
                if stem == woldeok_stem:
                    result.append({
                        "name": "월덕귀인 (月德貴人)",
                        "hanja": "月德貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": SHENSHA.get("월덕귀인", {}).get("description", "달의 덕을 받는 귀인, 평화롭고 화합함")
                    })

        # 월공귀인 (月空貴人) - 월지 기준 천간 검사
        wolgong_stem = WOLGONG_TABLE.get(month_branch)
        if wolgong_stem is not None:
            for pillar, stem in self._get_all_stems():
                if stem == wolgong_stem:
                    result.append({
                        "name": "월공귀인 (月空貴人)",
                        "hanja": "月空貴人",
                        "type": "길신",
                        "position": pillar,
                        "description": "월의 공덕, 험난함을 피하고 도움받음"
                    })

        return result

    def _get_all_branches(self) -> List[tuple]:
        """모든 지지 반환"""
        result = []
        if self.year:
            result.append(("year", self.year[1]))
        if self.month:
            result.append(("month", self.month[1]))
        if self.day:
            result.append(("day", self.day[1]))
        if self.hour:
            result.append(("hour", self.hour[1]))
        return result

    def _get_all_stems(self) -> List[tuple]:
        """모든 천간 반환"""
        result = []
        if self.year:
            result.append(("year", self.year[0]))
        if self.month:
            result.append(("month", self.month[0]))
        if self.day:
            result.append(("day", self.day[0]))
        if self.hour:
            result.append(("hour", self.hour[0]))
        return result

    def get_gilsin_list(self) -> List[Dict]:
        """길신 목록만 반환"""
        all_shensha = self.calculate_all_shensha()
        return [s for s in all_shensha if s["type"] == "길신"]

    def get_hyungsin_list(self) -> List[Dict]:
        """흉신 목록만 반환"""
        all_shensha = self.calculate_all_shensha()
        return [s for s in all_shensha if s["type"] == "흉신"]
