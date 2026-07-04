"""
분석 API 라우트
용신, 운세, 유파 비교 분석 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException

from api.converters import EnumConverter, SajuDataConverter
from api.dependencies import get_session_manager
from api.errors import http_500
from api.formatters import (
    FortuneFormatter,
    SchoolComparisonFormatter,
    SuggestedQuestionsGenerator,
    YongsinFormatter,
)
from api.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisType,
    AnalysisTypesResponse,
    ErrorResponse,
    FortuneResult,
    SchoolCodeType,
    SchoolComparisonSchema,
    SchoolInterpretationSchema,
    YongSinMethodType,
    YongSinResultSchema,
)
from config.logging_config import get_logger
from manseol.analysis import (
    # 운세 분석
    analyze_fortune,
    # 유파 비교
    compare_schools,
    # 용신 분석
    select_yongsin,
    select_yongsin_auto,
)
from utils.protocols import SessionManagerProtocol

logger = get_logger(__name__)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


# 분석 유형별 설명
FORTUNE_TYPE_INFO = {
    AnalysisType.FORTUNE_GENERAL: {"name": "종합운", "description": "전반적인 운세 분석"},
    AnalysisType.FORTUNE_CAREER: {"name": "직업운", "description": "직업과 커리어 관련 운세"},
    AnalysisType.FORTUNE_WEALTH: {"name": "재물운", "description": "재물과 금전 관련 운세"},
    AnalysisType.FORTUNE_HEALTH: {"name": "건강운", "description": "건강과 체력 관련 운세"},
    AnalysisType.FORTUNE_LOVE: {"name": "애정운", "description": "연애와 결혼 관련 운세"},
}

YONGSIN_METHOD_INFO = {
    YongSinMethodType.STRENGTH: {
        "name": "강약용신",
        "description": "일간의 강약을 기준으로 용신 선정",
    },
    YongSinMethodType.SEASONAL: {
        "name": "조후용신",
        "description": "계절(월령)을 기준으로 용신 선정",
    },
    YongSinMethodType.MEDIATION: {
        "name": "통관용신",
        "description": "오행 충돌을 중재하는 용신 선정",
    },
    YongSinMethodType.DISEASE: {
        "name": "병약용신",
        "description": "사주의 병(病)을 치료하는 용신 선정",
    },
}

SCHOOL_CODE_INFO = {
    SchoolCodeType.ZIPING: {"name": "자평명리", "description": "일간 중심의 강약 분석과 격국론"},
    SchoolCodeType.DTS: {"name": "적천수", "description": "오행의 생극제화와 통변성정"},
    SchoolCodeType.QTBJ: {"name": "궁통보감", "description": "월령과 조후 중심 해석"},
    SchoolCodeType.MODERN: {"name": "현대명리", "description": "심리학적 관점과 실용적 조언"},
    SchoolCodeType.SHENSHA: {"name": "신살중심", "description": "신살로 길흉 판단"},
}


@router.get(
    "/types",
    response_model=AnalysisTypesResponse,
    summary="분석 유형 목록",
    description="사용 가능한 분석 유형들을 반환합니다.",
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

    yongsin_methods = [{"code": ym.value, **YONGSIN_METHOD_INFO[ym]} for ym in YongSinMethodType]

    school_codes = [{"code": sc.value, **SCHOOL_CODE_INFO[sc]} for sc in SchoolCodeType]

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
        500: {"model": ErrorResponse},
    },
    summary="분석 요청",
    description="사주 분석을 수행합니다.",
)
async def analyze(
    request: AnalysisRequest, sm: SessionManagerProtocol = Depends(get_session_manager)
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
            session = await sm.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail=f"세션 '{request.session_id}'을 찾을 수 없습니다."
                )
        else:
            # 새 세션 생성
            if not request.saju_data:
                raise HTTPException(
                    status_code=400, detail="새 세션 생성시 saju_data가 필요합니다."
                )
            session = await sm.create_session(request.saju_data)

        # 분석 함수용 형식으로 변환
        saju_data = SajuDataConverter.to_analysis_format(session.saju_data)
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
            fortune_type = EnumConverter.to_fortune_type(analysis_type)
            if fortune_type is None:
                raise HTTPException(
                    status_code=400, detail=f"지원하지 않는 운세 유형: {analysis_type}"
                )
            fortune_type_name = FORTUNE_TYPE_INFO[analysis_type]["name"]

            fortune_analysis = analyze_fortune(saju_data, fortune_type.value)

            fortune_result = FortuneResult(
                fortune_type=fortune_analysis.fortune_type.value,
                score=fortune_analysis.score,
                summary=fortune_analysis.summary,
                positive=fortune_analysis.details.positive,
                negative=fortune_analysis.details.negative,
                advice=fortune_analysis.details.advice,
                lucky_colors=fortune_analysis.lucky_elements.colors,
                lucky_numbers=fortune_analysis.lucky_elements.numbers,
                lucky_directions=fortune_analysis.lucky_elements.directions,
            )

            message = FortuneFormatter.format(fortune_analysis, fortune_type_name)

        # 용신 분석
        elif analysis_type == AnalysisType.YONGSIN:
            yongsin_analysis = select_yongsin_auto(saju_data)

            yongsin_result_schema = YongSinResultSchema(
                primary_yongsin=yongsin_analysis.primary_yongsin.value,
                secondary_yongsin=yongsin_analysis.secondary_yongsin.value
                if yongsin_analysis.secondary_yongsin
                else None,
                xi_sin=[e.value for e in yongsin_analysis.xi_sin],
                ji_sin=[e.value for e in yongsin_analysis.ji_sin],
                chou_sin=[e.value for e in yongsin_analysis.chou_sin],
                day_master_strength=yongsin_analysis.day_master_strength.value,
                reasoning=yongsin_analysis.reasoning,
                method=yongsin_analysis.method.value,
                confidence=yongsin_analysis.confidence,
                recommendations={
                    "colors": yongsin_analysis.recommendations.colors,
                    "directions": yongsin_analysis.recommendations.directions,
                    "careers": yongsin_analysis.recommendations.careers,
                    "activities": yongsin_analysis.recommendations.activities,
                    "cautions": yongsin_analysis.recommendations.cautions,
                },
            )

            message = YongsinFormatter.format(yongsin_analysis)

        # 특정 용신 방법론
        elif analysis_type == AnalysisType.YONGSIN_METHOD:
            if not request.yongsin_method:
                raise HTTPException(
                    status_code=400, detail="용신 방법론(yongsin_method)을 지정해주세요."
                )

            method = EnumConverter.yongsin_method_to_string(request.yongsin_method)
            yongsin_method_analysis = select_yongsin(saju_data, method)

            yongsin_result_schema = YongSinResultSchema(
                primary_yongsin=yongsin_method_analysis.primary_yongsin.value,
                secondary_yongsin=yongsin_method_analysis.secondary_yongsin.value
                if yongsin_method_analysis.secondary_yongsin
                else None,
                xi_sin=[e.value for e in yongsin_method_analysis.xi_sin],
                ji_sin=[e.value for e in yongsin_method_analysis.ji_sin],
                chou_sin=[e.value for e in yongsin_method_analysis.chou_sin],
                day_master_strength=yongsin_method_analysis.day_master_strength.value,
                reasoning=yongsin_method_analysis.reasoning,
                method=yongsin_method_analysis.method.value,
                confidence=yongsin_method_analysis.confidence,
                recommendations={
                    "colors": yongsin_method_analysis.recommendations.colors,
                    "directions": yongsin_method_analysis.recommendations.directions,
                    "careers": yongsin_method_analysis.recommendations.careers,
                    "activities": yongsin_method_analysis.recommendations.activities,
                    "cautions": yongsin_method_analysis.recommendations.cautions,
                },
            )

            method_name = YONGSIN_METHOD_INFO[request.yongsin_method]["name"]
            message = f"## {method_name} 분석 결과\n\n" + YongsinFormatter.format(
                yongsin_method_analysis
            )

        # 유파 비교
        elif analysis_type == AnalysisType.SCHOOL_COMPARE:
            # 선택된 유파 또는 전체
            school_codes = None
            if request.schools:
                converted = [EnumConverter.to_school_code(s) for s in request.schools]
                school_codes = [s for s in converted if s is not None]

            school_analysis = compare_schools(saju_data, school_codes)

            school_comparison = SchoolComparisonSchema(
                schools=[s.value for s in school_analysis.schools],
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
                    for interp in school_analysis.interpretations
                ],
                consensus=[
                    {
                        "category": c.category,
                        "agreement": c.agreement,
                        "schools": [s.value for s in c.schools],
                    }
                    for c in school_analysis.consensus
                ],
                differences=[
                    {
                        "category": d.category,
                        "interpretations": d.interpretations,
                    }
                    for d in school_analysis.differences
                ],
                recommendation=school_analysis.recommendation,
            )

            message = SchoolComparisonFormatter.format(school_analysis)

        else:
            raise HTTPException(status_code=400, detail=f"지원하지 않는 분석 유형: {analysis_type}")

        # 추천 질문
        suggested_questions = SuggestedQuestionsGenerator.for_analysis_type(analysis_type)

        # 사용자 메시지가 있으면 기록
        if request.message:
            session.add_user_message(request.message)
            session.add_assistant_message(message)
            # 변형된 세션 영속 (명시적 flush)
            await sm.save_session(session)

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
        raise http_500(logger, "분석 처리 중 오류가 발생했습니다", e) from e
