"""
분석 API 라우트
용신, 운세, 유파 비교 분석 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Dict, List, Optional

from api.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisTypesResponse,
    AnalysisType,
    YongSinMethodType,
    SchoolCodeType,
    FortuneResult,
    YongSinResultSchema,
    SchoolInterpretationSchema,
    SchoolComparisonSchema,
    ErrorResponse,
)
from conversation.session_manager import SessionManager
from manseol.analysis import (
    # 운세 분석
    FortuneAnalyzer,
    FortuneType,
    analyze_fortune,
    # 용신 분석
    select_yongsin,
    select_yongsin_auto,
    YongSinMethod,
    # 유파 비교
    compare_schools,
    SchoolCode,
    SchoolComparator,
)


router = APIRouter(prefix="/api/analysis", tags=["analysis"])

# 전역 세션 매니저 (chat.py와 공유)
session_manager = SessionManager()


def _convert_display_to_analysis_format(saju_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    프론트엔드 display 형식을 분석 함수용 형식으로 변환

    Display format (frontend):
    - four_pillars.day.heavenly_stem.element
    - five_elements.distribution
    - strength.is_strong / strength.type

    Analysis format (expected by analyzers):
    - day_pillar.stem_element
    - wuxing_count
    - day_master_strength.level
    """
    # 이미 분석 형식이면 그대로 반환
    if "day_pillar" in saju_data and "stem_element" in saju_data.get("day_pillar", {}):
        return saju_data

    # 백엔드 원본 형식이면 변환
    if "pillars" in saju_data and "analysis" in saju_data:
        return _convert_original_to_analysis_format(saju_data)

    # 프론트엔드 display 형식 변환
    if "four_pillars" not in saju_data:
        return saju_data  # 알 수 없는 형식은 그대로 반환

    four_pillars = saju_data.get("four_pillars", {})
    five_elements = saju_data.get("five_elements", {})
    strength = saju_data.get("strength", {})

    # day_pillar 변환
    day_pillar_data = four_pillars.get("day", {})
    day_stem = day_pillar_data.get("heavenly_stem", {}) if isinstance(day_pillar_data, dict) else {}
    stem_element = day_stem.get("element", "목") if isinstance(day_stem, dict) else "목"

    # wuxing_count 변환 (distribution을 그대로 사용)
    distribution = five_elements.get("distribution", {}) if isinstance(five_elements, dict) else {}
    wuxing_count = distribution if distribution else {"목": 2, "화": 2, "토": 2, "금": 1, "수": 1}

    # strength 변환
    if isinstance(strength, dict):
        is_strong = strength.get("is_strong", True)
        strength_type = strength.get("type", "")
        if strength_type:
            level = strength_type  # 신강, 신약, 중화
        else:
            level = "strong" if is_strong else "weak"
    else:
        level = "medium"

    return {
        "day_pillar": {
            "stem_element": stem_element,
        },
        "wuxing_count": wuxing_count,
        "day_master_strength": {
            "level": level,
        },
        # 원본 데이터도 유지 (다른 분석에서 필요할 수 있음)
        "original": saju_data,
    }


def _convert_original_to_analysis_format(saju_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    백엔드 원본 형식을 분석 함수용 형식으로 변환
    """
    pillars = saju_data.get("pillars", {})
    analysis = saju_data.get("analysis", {})

    # day pillar 정보
    day_pillar = pillars.get("day", {})
    day_stem = day_pillar.get("stem", {}) if isinstance(day_pillar, dict) else {}
    stem_element = day_stem.get("element", "목") if isinstance(day_stem, dict) else "목"

    # 오행 분포
    five_elements = analysis.get("five_elements", {}) if isinstance(analysis, dict) else {}
    wuxing_count = {
        "목": five_elements.get("wood", 2),
        "화": five_elements.get("fire", 2),
        "토": five_elements.get("earth", 2),
        "금": five_elements.get("metal", 1),
        "수": five_elements.get("water", 1),
    }

    # 신강/신약
    strength_info = analysis.get("strength", {}) if isinstance(analysis, dict) else {}
    level = strength_info.get("level", "medium") if isinstance(strength_info, dict) else "medium"

    return {
        "day_pillar": {
            "stem_element": stem_element,
        },
        "wuxing_count": wuxing_count,
        "day_master_strength": {
            "level": level,
        },
        "original": saju_data,
    }


def get_session_manager() -> SessionManager:
    """세션 매니저 의존성"""
    return session_manager


# 분석 유형별 설명
FORTUNE_TYPE_INFO = {
    AnalysisType.FORTUNE_GENERAL: {"name": "종합운", "description": "전반적인 운세 분석"},
    AnalysisType.FORTUNE_CAREER: {"name": "직업운", "description": "직업과 커리어 관련 운세"},
    AnalysisType.FORTUNE_WEALTH: {"name": "재물운", "description": "재물과 금전 관련 운세"},
    AnalysisType.FORTUNE_HEALTH: {"name": "건강운", "description": "건강과 체력 관련 운세"},
    AnalysisType.FORTUNE_LOVE: {"name": "애정운", "description": "연애와 결혼 관련 운세"},
}

YONGSIN_METHOD_INFO = {
    YongSinMethodType.STRENGTH: {"name": "강약용신", "description": "일간의 강약을 기준으로 용신 선정"},
    YongSinMethodType.SEASONAL: {"name": "조후용신", "description": "계절(월령)을 기준으로 용신 선정"},
    YongSinMethodType.MEDIATION: {"name": "통관용신", "description": "오행 충돌을 중재하는 용신 선정"},
    YongSinMethodType.DISEASE: {"name": "병약용신", "description": "사주의 병(病)을 치료하는 용신 선정"},
}

SCHOOL_CODE_INFO = {
    SchoolCodeType.ZIPING: {"name": "자평명리", "description": "일간 중심의 강약 분석과 격국론"},
    SchoolCodeType.DTS: {"name": "적천수", "description": "오행의 생극제화와 통변성정"},
    SchoolCodeType.QTBJ: {"name": "궁통보감", "description": "월령과 조후 중심 해석"},
    SchoolCodeType.MODERN: {"name": "현대명리", "description": "심리학적 관점과 실용적 조언"},
    SchoolCodeType.SHENSHA: {"name": "신살중심", "description": "신살로 길흉 판단"},
}


def _fortune_type_to_enum(analysis_type: AnalysisType) -> FortuneType:
    """AnalysisType을 FortuneType으로 변환"""
    mapping = {
        AnalysisType.FORTUNE_GENERAL: FortuneType.GENERAL,
        AnalysisType.FORTUNE_CAREER: FortuneType.CAREER,
        AnalysisType.FORTUNE_WEALTH: FortuneType.WEALTH,
        AnalysisType.FORTUNE_HEALTH: FortuneType.HEALTH,
        AnalysisType.FORTUNE_LOVE: FortuneType.LOVE,
    }
    return mapping.get(analysis_type)


def _yongsin_method_to_enum(method: YongSinMethodType) -> str:
    """YongSinMethodType을 문자열로 변환"""
    return method.value


def _school_code_to_enum(code: SchoolCodeType) -> SchoolCode:
    """SchoolCodeType을 SchoolCode로 변환"""
    mapping = {
        SchoolCodeType.ZIPING: SchoolCode.ZIPING,
        SchoolCodeType.DTS: SchoolCode.DTS,
        SchoolCodeType.QTBJ: SchoolCode.QTBJ,
        SchoolCodeType.MODERN: SchoolCode.MODERN,
        SchoolCodeType.SHENSHA: SchoolCode.SHENSHA,
    }
    return mapping.get(code)


def _generate_fortune_message(fortune_result, fortune_type_name: str) -> str:
    """운세 분석 결과 메시지 생성"""
    lines = [
        f"## {fortune_type_name} 분석 결과",
        "",
        f"**점수**: {fortune_result.score}/100",
        "",
        f"**요약**: {fortune_result.summary}",
        "",
    ]

    if fortune_result.details.positive:
        lines.append("### 긍정적 요소")
        for item in fortune_result.details.positive:
            lines.append(f"- {item}")
        lines.append("")

    if fortune_result.details.negative:
        lines.append("### 주의할 점")
        for item in fortune_result.details.negative:
            lines.append(f"- {item}")
        lines.append("")

    if fortune_result.details.advice:
        lines.append("### 조언")
        for item in fortune_result.details.advice:
            lines.append(f"- {item}")
        lines.append("")

    if fortune_result.lucky_elements.colors:
        lines.append(f"**행운의 색상**: {', '.join(fortune_result.lucky_elements.colors)}")
    if fortune_result.lucky_elements.numbers:
        lines.append(f"**행운의 숫자**: {', '.join(map(str, fortune_result.lucky_elements.numbers))}")
    if fortune_result.lucky_elements.directions:
        lines.append(f"**유리한 방향**: {', '.join(fortune_result.lucky_elements.directions)}")

    return "\n".join(lines)


def _generate_yongsin_message(yongsin_result) -> str:
    """용신 분석 결과 메시지 생성"""
    lines = [
        "## 용신 분석 결과",
        "",
        f"**주 용신**: {yongsin_result.primary_yongsin.value}",
    ]

    if yongsin_result.secondary_yongsin:
        lines.append(f"**보조 용신**: {yongsin_result.secondary_yongsin.value}")

    lines.extend([
        "",
        f"**분석 방법**: {yongsin_result.method.value}",
        f"**일간 강약**: {yongsin_result.day_master_strength.value}",
        f"**신뢰도**: {yongsin_result.confidence * 100:.0f}%",
        "",
        f"**선정 이유**: {yongsin_result.reasoning}",
        "",
    ])

    if yongsin_result.xi_sin:
        lines.append(f"**희신 (도움)**: {', '.join(e.value for e in yongsin_result.xi_sin)}")
    if yongsin_result.ji_sin:
        lines.append(f"**기신 (피해야 할)**: {', '.join(e.value for e in yongsin_result.ji_sin)}")

    lines.append("")
    lines.append("### 추천")

    recs = yongsin_result.recommendations
    if recs.colors:
        lines.append(f"- **색상**: {', '.join(recs.colors[:4])}")
    if recs.directions:
        lines.append(f"- **방향**: {', '.join(recs.directions)}")
    if recs.careers:
        lines.append(f"- **직업**: {', '.join(recs.careers[:5])}")
    if recs.activities:
        lines.append(f"- **활동**: {', '.join(recs.activities[:4])}")

    return "\n".join(lines)


def _generate_school_comparison_message(comparison_result) -> str:
    """유파 비교 결과 메시지 생성"""
    lines = [
        "## 유파별 해석 비교",
        "",
    ]

    for interp in comparison_result.interpretations:
        lines.extend([
            f"### {interp.school_name}",
            f"**용신**: {interp.yong_sin.value}",
        ])
        if interp.geok_guk:
            lines.append(f"**격국**: {interp.geok_guk}")
        lines.extend([
            f"**신뢰도**: {interp.confidence * 100:.0f}%",
            "",
            interp.overall,
            "",
        ])

    if comparison_result.consensus:
        lines.append("### 합의점")
        for item in comparison_result.consensus[:3]:
            lines.append(f"- {item.agreement}")
        lines.append("")

    lines.append("### 종합 권장")
    lines.append(comparison_result.recommendation)

    return "\n".join(lines)


def _get_suggested_questions(analysis_type: AnalysisType) -> List[str]:
    """분석 유형에 따른 추천 질문"""
    questions = {
        AnalysisType.FORTUNE_GENERAL: [
            "이번 달 특별히 주의해야 할 점이 있을까요?",
            "운세를 좋게 만들기 위해 어떤 노력을 해야 할까요?",
            "다른 운세 분석도 보고 싶어요",
        ],
        AnalysisType.FORTUNE_CAREER: [
            "지금 이직을 하면 좋을까요?",
            "어떤 분야의 일이 저에게 맞을까요?",
            "직장에서 성공하려면 어떻게 해야 할까요?",
        ],
        AnalysisType.FORTUNE_WEALTH: [
            "투자를 하기에 좋은 시기인가요?",
            "재물을 모으기 위한 조언을 해주세요",
            "부업이나 추가 수입을 고려해도 될까요?",
        ],
        AnalysisType.FORTUNE_HEALTH: [
            "어떤 건강 문제에 주의해야 할까요?",
            "건강을 위해 어떤 활동을 추천하시나요?",
            "스트레스 관리는 어떻게 해야 할까요?",
        ],
        AnalysisType.FORTUNE_LOVE: [
            "인연을 만나기에 좋은 시기인가요?",
            "현재 연인과의 관계는 어떻게 될까요?",
            "이상적인 파트너의 특징은 무엇인가요?",
        ],
        AnalysisType.YONGSIN: [
            "용신을 활용하는 구체적인 방법이 있을까요?",
            "다른 용신 분석 방법도 비교해보고 싶어요",
            "기신을 피하려면 어떻게 해야 하나요?",
        ],
        AnalysisType.YONGSIN_METHOD: [
            "이 방법론이 저에게 가장 적합한가요?",
            "다른 용신 방법론과 비교하면 어떤가요?",
            "용신을 일상에서 어떻게 활용할 수 있나요?",
        ],
        AnalysisType.SCHOOL_COMPARE: [
            "어떤 유파의 해석이 저에게 맞을까요?",
            "유파 간 차이가 나는 이유가 무엇인가요?",
            "특정 유파로 더 자세히 분석해주세요",
        ],
    }
    return questions.get(analysis_type, [])


@router.get(
    "/types",
    response_model=AnalysisTypesResponse,
    summary="분석 유형 목록",
    description="사용 가능한 분석 유형들을 반환합니다."
)
async def get_analysis_types() -> AnalysisTypesResponse:
    """분석 유형 목록 조회"""
    fortune_types = [
        {"code": at.value, **FORTUNE_TYPE_INFO[at]}
        for at in [
            AnalysisType.FORTUNE_GENERAL,
            AnalysisType.FORTUNE_CAREER,
            AnalysisType.FORTUNE_WEALTH,
            AnalysisType.FORTUNE_HEALTH,
            AnalysisType.FORTUNE_LOVE,
        ]
    ]

    yongsin_methods = [
        {"code": ym.value, **YONGSIN_METHOD_INFO[ym]}
        for ym in YongSinMethodType
    ]

    school_codes = [
        {"code": sc.value, **SCHOOL_CODE_INFO[sc]}
        for sc in SchoolCodeType
    ]

    return AnalysisTypesResponse(
        success=True,
        fortune_types=fortune_types,
        yongsin_methods=yongsin_methods,
        school_codes=school_codes,
    )


@router.post(
    "",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="분석 요청",
    description="사주 분석을 수행합니다."
)
async def analyze(
    request: AnalysisRequest,
    sm: SessionManager = Depends(get_session_manager)
) -> AnalysisResponse:
    """
    분석 엔드포인트

    - 운세 분석 (general/career/wealth/health/love)
    - 용신 분석 (자동 또는 특정 방법론)
    - 유파 비교 분석
    """
    try:
        # 세션 처리
        if request.session_id:
            # 기존 세션 사용
            session = sm.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404,
                    detail=f"세션 '{request.session_id}'을 찾을 수 없습니다."
                )
        else:
            # 새 세션 생성
            if not request.saju_data:
                raise HTTPException(
                    status_code=400,
                    detail="새 세션 생성시 saju_data가 필요합니다."
                )
            session = sm.create_session(request.saju_data)

        # 분석 함수용 형식으로 변환
        saju_data = _convert_display_to_analysis_format(session.saju_data)
        analysis_type = request.analysis_type

        fortune_result = None
        yongsin_result_schema = None
        school_comparison = None
        message = ""

        # 운세 분석
        if analysis_type in [
            AnalysisType.FORTUNE_GENERAL,
            AnalysisType.FORTUNE_CAREER,
            AnalysisType.FORTUNE_WEALTH,
            AnalysisType.FORTUNE_HEALTH,
            AnalysisType.FORTUNE_LOVE,
        ]:
            fortune_type = _fortune_type_to_enum(analysis_type)
            fortune_type_name = FORTUNE_TYPE_INFO[analysis_type]["name"]

            result = analyze_fortune(saju_data, fortune_type.value)

            fortune_result = FortuneResult(
                fortune_type=result.fortune_type.value,
                score=result.score,
                summary=result.summary,
                positive=result.details.positive,
                negative=result.details.negative,
                advice=result.details.advice,
                lucky_colors=result.lucky_elements.colors,
                lucky_numbers=result.lucky_elements.numbers,
                lucky_directions=result.lucky_elements.directions,
            )

            message = _generate_fortune_message(result, fortune_type_name)

        # 용신 분석
        elif analysis_type == AnalysisType.YONGSIN:
            result = select_yongsin_auto(saju_data)

            yongsin_result_schema = YongSinResultSchema(
                primary_yongsin=result.primary_yongsin.value,
                secondary_yongsin=result.secondary_yongsin.value if result.secondary_yongsin else None,
                xi_sin=[e.value for e in result.xi_sin],
                ji_sin=[e.value for e in result.ji_sin],
                chou_sin=[e.value for e in result.chou_sin],
                day_master_strength=result.day_master_strength.value,
                reasoning=result.reasoning,
                method=result.method.value,
                confidence=result.confidence,
                recommendations={
                    "colors": result.recommendations.colors,
                    "directions": result.recommendations.directions,
                    "careers": result.recommendations.careers,
                    "activities": result.recommendations.activities,
                    "cautions": result.recommendations.cautions,
                },
            )

            message = _generate_yongsin_message(result)

        # 특정 용신 방법론
        elif analysis_type == AnalysisType.YONGSIN_METHOD:
            if not request.yongsin_method:
                raise HTTPException(
                    status_code=400,
                    detail="용신 방법론(yongsin_method)을 지정해주세요."
                )

            method = _yongsin_method_to_enum(request.yongsin_method)
            result = select_yongsin(saju_data, method)

            yongsin_result_schema = YongSinResultSchema(
                primary_yongsin=result.primary_yongsin.value,
                secondary_yongsin=result.secondary_yongsin.value if result.secondary_yongsin else None,
                xi_sin=[e.value for e in result.xi_sin],
                ji_sin=[e.value for e in result.ji_sin],
                chou_sin=[e.value for e in result.chou_sin],
                day_master_strength=result.day_master_strength.value,
                reasoning=result.reasoning,
                method=result.method.value,
                confidence=result.confidence,
                recommendations={
                    "colors": result.recommendations.colors,
                    "directions": result.recommendations.directions,
                    "careers": result.recommendations.careers,
                    "activities": result.recommendations.activities,
                    "cautions": result.recommendations.cautions,
                },
            )

            method_name = YONGSIN_METHOD_INFO[request.yongsin_method]["name"]
            message = f"## {method_name} 분석 결과\n\n" + _generate_yongsin_message(result)

        # 유파 비교
        elif analysis_type == AnalysisType.SCHOOL_COMPARE:
            # 선택된 유파 또는 전체
            if request.schools:
                schools = [_school_code_to_enum(s) for s in request.schools]
            else:
                schools = None  # 전체

            result = compare_schools(saju_data, schools)

            school_comparison = SchoolComparisonSchema(
                schools=[s.value for s in result.schools],
                interpretations=[
                    SchoolInterpretationSchema(
                        school=interp.school.value,
                        school_name=interp.school_name,
                        yong_sin=interp.yong_sin.value,
                        geok_guk=interp.geok_guk,
                        overall=interp.overall,
                        health=interp.health,
                        wealth=interp.wealth,
                        career=interp.career,
                        relationship=interp.relationship,
                        fame=interp.fame,
                        confidence=interp.confidence,
                        key_features=interp.key_features,
                    )
                    for interp in result.interpretations
                ],
                consensus=[
                    {
                        "category": c.category,
                        "agreement": c.agreement,
                        "schools": [s.value for s in c.schools],
                    }
                    for c in result.consensus
                ],
                differences=[
                    {
                        "category": d.category,
                        "interpretations": d.interpretations,
                    }
                    for d in result.differences
                ],
                recommendation=result.recommendation,
            )

            message = _generate_school_comparison_message(result)

        else:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 분석 유형: {analysis_type}"
            )

        # 추천 질문
        suggested_questions = _get_suggested_questions(analysis_type)

        # 사용자 메시지가 있으면 기록
        if request.message:
            session.add_user_message(request.message)
            session.add_assistant_message(message)

        return AnalysisResponse(
            success=True,
            session_id=session.session_id,
            analysis_type=analysis_type.value,
            message=message,
            fortune_result=fortune_result,
            yongsin_result=yongsin_result_schema,
            school_comparison=school_comparison,
            suggested_questions=suggested_questions,
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"분석 처리 중 오류: {str(e)}")
