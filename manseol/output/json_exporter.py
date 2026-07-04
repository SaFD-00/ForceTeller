"""
JSON 출력 모듈
사주 계산 결과를 JSON 형식으로 변환
"""

from datetime import datetime

from config.constants import BRANCHES, STEM_ELEMENT_COLORS, STEMS
from manseol.calculator.fortune_cycle import FortuneCycleCalculator
from manseol.calculator.hidden_stems import HiddenStemsCalculator
from manseol.calculator.interactions import InteractionsCalculator
from manseol.calculator.pillar_engine import PillarEngine
from manseol.calculator.shensha import ShenshaCalculator
from manseol.calculator.ten_gods import TenGodsCalculator
from manseol.calculator.twelve_phases import TwelvePhasesCalculator
from manseol.core.calendar_converter import CalendarConverter
from manseol.core.time_correction import TimeCorrector
from manseol.models.input_model import SajuInput
from manseol.models.saju_result import (
    BranchData,
    DayMasterAnalysis,
    FiveElementsAnalysis,
    FortuneCycle,
    FortuneCycleData,
    FourPillars,
    InputSummary,
    MetaInfo,
    PillarData,
    SajuAnalysis,
    SajuResult,
    ShenshaData,
    StemData,
    StrengthAnalysis,
    TenGodsDistribution,
    TimeCorrection,
    UsefulGodAnalysis,
)


class JsonExporter:
    """JSON 출력 변환 클래스"""

    def __init__(self, saju_input: SajuInput):
        """
        Args:
            saju_input: 사주 입력 데이터
        """
        self.input = saju_input
        self.pillar_engine = PillarEngine()

    def generate_result(self) -> SajuResult:
        """
        전체 사주 결과 생성

        Returns:
            SajuResult 객체
        """
        # 1. 시간 보정
        time_correction = None
        calc_datetime = None

        if self.input.birth_datetime:
            calc_datetime = self.input.birth_datetime

            if self.input.apply_time_correction:
                corrector = TimeCorrector(
                    calc_datetime, longitude=self.input.longitude, city=self.input.city
                )
                true_solar_time, corrections = corrector.calculate_true_solar_time()
                calc_datetime = true_solar_time

                time_correction = TimeCorrection(
                    original_time=self.input.birth_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    true_solar_time=true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
                    longitude_correction_minutes=round(corrections["longitude_minutes"], 2),
                    eot_correction_minutes=round(corrections["eot_minutes"], 2),
                    dst_correction_minutes=corrections["dst_minutes"],
                    total_correction_minutes=round(corrections["total_minutes"], 2),
                    standard_meridian=corrections["standard_meridian"],
                    birth_longitude=corrections["birth_longitude"],
                )
        else:
            # 시간 미상 - 날짜만 사용
            calc_datetime = datetime.combine(self.input.birth_date, datetime.min.time())

        # 2. 사주 4주 계산
        pillars_raw = self.pillar_engine.calculate_all_pillars(
            calc_datetime, jajasi=self.input.jajasi, include_hour=self.input.has_time
        )

        # 3. 일간 정보
        day_stem_idx = pillars_raw["day"][0]
        day_branch_idx = pillars_raw["day"][1]

        # 3.5 음력 변환
        calendar_converter = CalendarConverter()
        solar_date = self.input.birth_date
        lunar_year, lunar_month, lunar_day, is_leap_month = calendar_converter.solar_to_lunar(
            solar_date.year, solar_date.month, solar_date.day
        )

        # 3.6 일주 정보 (metaphor, animal)
        day_stem = STEMS[day_stem_idx]
        day_branch = BRANCHES[day_branch_idx]
        day_ganji_korean = f"{day_stem['korean']}{day_branch['korean']}"
        day_ganji_chinese = f"{day_stem['chinese']}{day_branch['chinese']}"
        day_animal = day_branch["animal"]

        # 색상 + 동물 조합 (예: "하얀 용")
        stem_color = STEM_ELEMENT_COLORS.get(day_stem_idx, "")
        day_metaphor = f"{stem_color} {day_animal}"

        # 4. 십성/12운성 계산기 초기화
        ten_gods_calc = TenGodsCalculator(day_stem_idx)
        twelve_phases_calc = TwelvePhasesCalculator(day_stem_idx)
        hidden_stems_calc = HiddenStemsCalculator(day_stem_idx)

        # 5. 4주 상세 정보 생성
        pillars = self._build_pillars(
            pillars_raw, ten_gods_calc, twelve_phases_calc, hidden_stems_calc
        )

        # 6. 분석 정보 생성
        analysis = self._build_analysis(
            pillars_raw,
            day_stem_idx,
            day_branch_idx,
            ten_gods_calc,
            twelve_phases_calc,
            hidden_stems_calc,
        )

        # 7. 대운 계산
        fortune_cycles = None
        if self.input.has_time:
            fortune_cycles = self._build_fortune_cycles(calc_datetime, pillars_raw)

        # 7.5 천간/지지 상호작용 (합·충·형·파·해·공망)
        interactions = self._build_interactions(pillars_raw)

        # 7.6 세운(歲運) - 올해부터 향후 수년간 연운 (시간 미상과 무관)
        sewun = self._build_sewun(calc_datetime, pillars_raw, ten_gods_calc, twelve_phases_calc)

        # 8. 최종 결과 조립
        return SajuResult(
            meta=MetaInfo(version="1.0.0", generated_at=datetime.now(), engine="ForceTeller"),
            input=InputSummary(
                name=self.input.name,
                birth_date=self.input.birth_date.isoformat(),
                birth_time=self.input.birth_time.isoformat() if self.input.birth_time else None,
                calendar=self.input.calendar.value,
                city=self.input.city,
                gender=self.input.gender.value,
                jajasi=self.input.jajasi,
                # 음력 정보
                lunar_year=lunar_year,
                lunar_month=lunar_month,
                lunar_day=lunar_day,
                is_leap_month=is_leap_month,
                # 일주 정보
                day_ganji_korean=day_ganji_korean,
                day_ganji_chinese=day_ganji_chinese,
                day_metaphor=day_metaphor,
                day_animal=day_animal,
            ),
            adjusted_time=time_correction,
            pillars=pillars,
            analysis=analysis,
            fortune_cycles=fortune_cycles,
            interactions=interactions,
            sewun=sewun,
        )

    def _build_sewun(
        self,
        calc_datetime: datetime,
        pillars_raw: dict,
        ten_gods_calc: TenGodsCalculator,
        twelve_phases_calc: TwelvePhasesCalculator,
        years: int = 6,
    ) -> list:
        """세운(歲運) 구성 - 올해부터 향후 N년간 연운(간지·십성·12운성)"""
        fortune_calc = FortuneCycleCalculator(
            birth_datetime=calc_datetime,
            gender=self.input.gender.value,
            year_stem=pillars_raw["year"][0],
            month_stem=pillars_raw["month"][0],
            month_branch=pillars_raw["month"][1],
        )
        current_year = datetime.now().year
        result = []
        for year in range(current_year, current_year + years):
            sewun = fortune_calc.calculate_sewun(year)
            sewun["ten_god"] = ten_gods_calc.get_ten_god_for_stem(sewun["stem_index"])
            sewun["twelve_phase"] = twelve_phases_calc.get_twelve_phase(sewun["branch_index"])
            result.append(sewun)
        return result

    def _build_interactions(self, pillars_raw: dict) -> dict[str, list]:
        """천간/지지 상호작용 계산 (합·충·형·파·해·공망)"""
        calc = InteractionsCalculator(
            year_pillar=pillars_raw["year"],
            month_pillar=pillars_raw["month"],
            day_pillar=pillars_raw["day"],
            hour_pillar=pillars_raw.get("hour"),
        )
        return calc.calculate_all_interactions()

    def _build_pillars(
        self,
        pillars_raw: dict,
        ten_gods_calc: TenGodsCalculator,
        twelve_phases_calc: TwelvePhasesCalculator,
        hidden_stems_calc: HiddenStemsCalculator,
    ) -> FourPillars:
        """4주 상세 정보 구성"""

        def build_pillar(name: str, stem_idx: int, branch_idx: int) -> PillarData:
            stem = STEMS[stem_idx]
            branch = BRANCHES[branch_idx]

            # 지장간
            hidden_stems = hidden_stems_calc.get_hidden_stems_ten_gods(branch_idx)

            stem_data = StemData(
                index=stem_idx,
                korean=stem["korean"],
                chinese=stem["chinese"],
                element=stem["element"].value,
                polarity=stem["polarity"].value,
            )

            branch_data = BranchData(
                index=branch_idx,
                korean=branch["korean"],
                chinese=branch["chinese"],
                element=branch["element"].value,
                polarity=branch["polarity"].value,
                animal=branch["animal"],
                hidden_stems=hidden_stems,
            )

            # 십성 (일주 제외)
            ten_god = None
            if name != "day":
                ten_god = ten_gods_calc.get_ten_god_for_stem(stem_idx)

            # 12운성
            twelve_phase = twelve_phases_calc.get_twelve_phase(branch_idx)

            return PillarData(
                stem=stem_data,
                branch=branch_data,
                ganji_korean=f"{stem['korean']}{branch['korean']}",
                ganji_chinese=f"{stem['chinese']}{branch['chinese']}",
                ten_god=ten_god,
                twelve_phase=twelve_phase,
            )

        year = build_pillar("year", *pillars_raw["year"])
        month = build_pillar("month", *pillars_raw["month"])
        day = build_pillar("day", *pillars_raw["day"])

        hour = None
        if pillars_raw["hour"]:
            hour = build_pillar("hour", *pillars_raw["hour"])

        return FourPillars(year=year, month=month, day=day, hour=hour)

    def _build_analysis(
        self,
        pillars_raw: dict,
        day_stem_idx: int,
        day_branch_idx: int,
        ten_gods_calc: TenGodsCalculator,
        twelve_phases_calc: TwelvePhasesCalculator,
        hidden_stems_calc: HiddenStemsCalculator,
    ) -> SajuAnalysis:
        """분석 정보 구성"""

        # 일간 분석
        day_stem = STEMS[day_stem_idx]
        day_branch = BRANCHES[day_branch_idx]

        # 색상 + 동물 조합 (예: "하얀 용")
        stem_color = STEM_ELEMENT_COLORS.get(day_stem_idx, "")
        day_animal = day_branch["animal"]
        metaphor_text = f"{stem_color} {day_animal}"
        characteristics = []

        day_master = DayMasterAnalysis(
            element=day_stem["element"].value,
            polarity=day_stem["polarity"].value,
            korean=day_stem["korean"],
            chinese=day_stem["chinese"],
            metaphor=metaphor_text,
            characteristics=characteristics,
        )

        # 오행 분석
        five_elements = self._calculate_five_elements(pillars_raw)

        # 십성 분포
        ten_gods_dist_dict = ten_gods_calc.get_ten_gods_distribution(pillars_raw)
        ten_gods_dist = TenGodsDistribution(**ten_gods_dist_dict)

        # 신강/신약
        strength_score = twelve_phases_calc.get_strength_score(pillars_raw)
        strength_level = (
            "신강" if strength_score >= 55 else ("신약" if strength_score <= 45 else "중화")
        )

        strength = StrengthAnalysis(
            level=strength_level,
            score=strength_score,
            supporting_count=sum(
                1 for g in ["비견", "겁재", "편인", "정인"] if ten_gods_dist_dict.get(g, 0) > 0
            ),
            weakening_count=sum(
                1
                for g in ["식신", "상관", "편재", "정재", "편관", "정관"]
                if ten_gods_dist_dict.get(g, 0) > 0
            ),
            analysis=f"일간 {day_stem['korean']}({day_stem['element'].value}) 강도: {strength_score}점",
        )

        # 용신 분석 (간단 버전)
        useful_god = self._calculate_useful_god(
            day_stem["element"].value, strength_level, five_elements
        )

        # 신살
        shensha_calc = ShenshaCalculator(
            pillars_raw["year"], pillars_raw["month"], pillars_raw["day"], pillars_raw.get("hour")
        )
        shensha_list = shensha_calc.calculate_all_shensha()
        shensha = [
            ShenshaData(
                name=s["name"], type=s["type"], position=s["position"], description=s["description"]
            )
            for s in shensha_list
        ]

        return SajuAnalysis(
            day_master=day_master,
            five_elements=five_elements,
            ten_gods_dist=ten_gods_dist,
            strength=strength,
            useful_god=useful_god,
            shensha=shensha,
        )

    def _calculate_five_elements(self, pillars_raw: dict) -> FiveElementsAnalysis:
        """오행 분포 계산"""
        # 영어 -> 한글 변환
        element_to_korean = {
            "wood": "목",
            "fire": "화",
            "earth": "토",
            "metal": "금",
            "water": "수",
        }
        counts = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}

        for pillar_name, pillar_data in pillars_raw.items():
            if pillar_data is None:
                continue
            stem_idx, branch_idx = pillar_data

            # 천간 오행
            stem = STEMS[stem_idx]
            stem_element_korean = element_to_korean.get(
                stem["element"].value, stem["element"].value
            )
            counts[stem_element_korean] += 1

            # 지지 오행
            branch = BRANCHES[branch_idx]
            branch_element_korean = element_to_korean.get(
                branch["element"].value, branch["element"].value
            )
            counts[branch_element_korean] += 1

        total = sum(counts.values())
        distribution = {k: round(v / total * 100, 1) if total > 0 else 0 for k, v in counts.items()}

        # 과다/부족 판단 (평균 20% 기준)
        # 가장 높은 비율의 오행을 dominant로 설정
        max_element = max(distribution.items(), key=lambda x: x[1])
        dominant = [max_element[0]] if max_element[1] > 0 else []
        lacking = [k for k, v in distribution.items() if v <= 10]

        return FiveElementsAnalysis(
            wood=counts["목"],
            fire=counts["화"],
            earth=counts["토"],
            metal=counts["금"],
            water=counts["수"],
            dominant=dominant,
            lacking=lacking,
            distribution=distribution,
        )

    def _calculate_useful_god(
        self, day_element: str, strength_level: str, five_elements: FiveElementsAnalysis
    ) -> UsefulGodAnalysis:
        """용신 계산 (억부용신 방식)"""

        # 영어 -> 한글 변환
        element_to_korean = {
            "wood": "목",
            "fire": "화",
            "earth": "토",
            "metal": "금",
            "water": "수",
        }
        day_element_korean = element_to_korean.get(day_element, day_element)

        # 오행 상생상극 (한글 키)
        generates = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
        generated_by = {"목": "수", "화": "목", "토": "화", "금": "토", "수": "금"}
        controls = {"목": "토", "화": "금", "토": "수", "금": "목", "수": "화"}
        controlled_by = {"목": "금", "화": "수", "토": "목", "금": "화", "수": "토"}

        if strength_level == "신강":
            # 신강: 설기(식상), 극제(재성, 관성) 필요
            primary = generates[day_element_korean]  # 식상
            secondary = controls[day_element_korean]  # 재성
            avoid = generated_by[day_element_korean]  # 인성
            reasoning = (
                f"일간이 신강하므로 {primary}(식상)으로 설기하거나 {secondary}(재성)으로 소모시킴"
            )
        elif strength_level == "신약":
            # 신약: 생조(인성, 비겁) 필요
            primary = generated_by[day_element_korean]  # 인성
            secondary = day_element_korean  # 비겁
            avoid = controlled_by[day_element_korean]  # 관성
            reasoning = f"일간이 신약하므로 {primary}(인성)으로 생조하거나 비겁으로 도움받음"
        else:
            # 중화: 부족한 오행 보충
            if five_elements.lacking:
                primary = five_elements.lacking[0]
            else:
                primary = day_element_korean
            secondary = None
            avoid = None
            reasoning = "일간이 중화하므로 균형 유지"

        return UsefulGodAnalysis(
            type="억부", primary=primary, secondary=secondary, avoid=avoid, reasoning=reasoning
        )

    def _build_fortune_cycles(self, calc_datetime: datetime, pillars_raw: dict) -> FortuneCycleData:
        """대운 정보 구성"""
        fortune_calc = FortuneCycleCalculator(
            birth_datetime=calc_datetime,
            gender=self.input.gender.value,
            year_stem=pillars_raw["year"][0],
            month_stem=pillars_raw["month"][0],
            month_branch=pillars_raw["month"][1],
        )

        summary = fortune_calc.get_fortune_summary()

        # TenGodsCalculator for fortune cycles
        day_stem_idx = pillars_raw["day"][0]
        ten_gods_calc = TenGodsCalculator(day_stem_idx)
        twelve_phases_calc = TwelvePhasesCalculator(day_stem_idx)

        cycles = []
        for cycle in summary["cycles"]:
            ten_god = ten_gods_calc.get_ten_god_for_stem(cycle["stem_index"])
            twelve_phase = twelve_phases_calc.get_twelve_phase(cycle["branch_index"])

            cycles.append(
                FortuneCycle(
                    start_age=cycle["start_age"],
                    end_age=cycle["end_age"],
                    stem_index=cycle["stem_index"],
                    branch_index=cycle["branch_index"],
                    ganji_korean=cycle["ganji_korean"],
                    ganji_chinese=cycle["ganji_chinese"],
                    ten_god=ten_god,
                    twelve_phase=twelve_phase,
                )
            )

        return FortuneCycleData(
            start_age=summary["start_age"],
            direction=summary["direction"],
            cycles=cycles,
            current_cycle_index=summary.get("current_cycle_index"),
        )

    def export_to_json(self, filepath: str = None, indent: int = 2) -> str:
        """
        JSON 파일로 내보내기

        Args:
            filepath: 출력 파일 경로 (없으면 문자열만 반환)
            indent: JSON 들여쓰기

        Returns:
            JSON 문자열
        """
        result = self.generate_result()
        json_str = result.to_json(indent=indent)

        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json_str)

        return json_str
