"""
용신 기반 추천 생성 모듈
색상, 방향, 직업, 활동 추천
"""

from .base import (
    WuXing,
    YongSinResult,
    get_wuxing_attributes,
)


def generate_detailed_recommendations(yongsin_result: YongSinResult) -> dict[str, any]:
    """
    용신 결과를 바탕으로 상세 추천 정보 생성

    Args:
        yongsin_result: 용신 분석 결과

    Returns:
        상세 추천 정보 딕셔너리
    """
    primary = yongsin_result.primary_yongsin
    secondary = yongsin_result.secondary_yongsin

    # 기본 추천 (recommendations 필드에서)
    recs = yongsin_result.recommendations

    # 상세 정보 추가
    detailed = {
        "summary": _generate_summary(yongsin_result),
        "primary_element": {
            "element": primary.value,
            "colors": recs.colors[:3],
            "directions": recs.directions[:2],
            "main_careers": recs.careers[:5],
            "recommended_activities": recs.activities[:4],
        },
        "lucky_items": _generate_lucky_items(primary),
        "lifestyle_tips": _generate_lifestyle_tips(primary, secondary),
        "cautions": recs.cautions,
        "seasonal_advice": _generate_seasonal_advice(primary),
    }

    if secondary:
        detailed["secondary_element"] = {
            "element": secondary.value,
            "colors": get_wuxing_attributes(secondary).get("colors", [])[:2],
            "directions": get_wuxing_attributes(secondary).get("directions", [])[:1],
        }

    return detailed


def _generate_summary(yongsin_result: YongSinResult) -> str:
    """추천 요약 생성"""
    primary = yongsin_result.primary_yongsin
    method_names = {
        "strength": "강약용신",
        "seasonal": "조후용신",
        "mediation": "통관용신",
        "disease": "병약용신",
    }
    method_name = method_names.get(yongsin_result.method.value, "용신")

    return (
        f"{method_name} 분석 결과, 당신에게 가장 필요한 오행은 {primary.value}입니다. "
        f"일상생활에서 {primary.value} 기운을 활용하면 운세 개선에 도움이 됩니다."
    )


def _generate_lucky_items(element: WuXing) -> dict[str, list[str]]:
    """행운 아이템 생성"""
    lucky_items = {
        WuXing.WOOD: {
            "accessories": ["목걸이 (나무 소재)", "녹색 팔찌", "식물 문양 액세서리"],
            "home_decor": ["화분", "나무 가구", "녹색 커튼"],
            "food": ["녹색 채소", "신맛 나는 과일", "콩나물"],
        },
        WuXing.FIRE: {
            "accessories": ["붉은색 스카프", "삼각형 모양 액세서리", "루비 장신구"],
            "home_decor": ["캔들", "남향 창문", "붉은 인테리어 소품"],
            "food": ["쓴맛 식품", "커피", "씀바귀"],
        },
        WuXing.EARTH: {
            "accessories": ["황금색 반지", "사각형 시계", "크리스탈"],
            "home_decor": ["도자기", "황토색 러그", "돌 장식"],
            "food": ["단맛 나는 음식", "고구마", "꿀"],
        },
        WuXing.METAL: {
            "accessories": ["금속 팔찌", "은 목걸이", "원형 장신구"],
            "home_decor": ["금속 조명", "흰색 소품", "유리 장식"],
            "food": ["매운 음식", "마늘", "생강"],
        },
        WuXing.WATER: {
            "accessories": ["검정색 가방", "물결 무늬 스카프", "진주"],
            "home_decor": ["어항", "분수", "파란색 그림"],
            "food": ["짠맛 음식", "해조류", "검은콩"],
        },
    }

    return lucky_items.get(element, {})


def _generate_lifestyle_tips(primary: WuXing, secondary: WuXing | None) -> list[str]:
    """생활 습관 팁 생성"""
    tips = {
        WuXing.WOOD: [
            "아침 산책이나 등산으로 하루를 시작하세요",
            "식물을 키우며 생명력을 느껴보세요",
            "독서나 글쓰기로 창의력을 키우세요",
            "동쪽을 향해 중요한 일을 시작하세요",
        ],
        WuXing.FIRE: [
            "활동적인 운동으로 에너지를 발산하세요",
            "사람들과 어울리는 사교 활동을 즐기세요",
            "밝은 조명의 환경에서 일하세요",
            "남쪽 방향의 햇살을 많이 받으세요",
        ],
        WuXing.EARTH: [
            "규칙적인 생활 리듬을 유지하세요",
            "요리나 베이킹으로 안정감을 찾으세요",
            "정리정돈으로 마음을 다스리세요",
            "부동산이나 토지 관련 투자를 고려하세요",
        ],
        WuXing.METAL: [
            "매일 같은 시간에 일어나는 규칙을 세우세요",
            "악기 연주나 음악 감상을 즐기세요",
            "계획을 세우고 체계적으로 실행하세요",
            "서쪽 방향으로 중요한 미팅을 잡으세요",
        ],
        WuXing.WATER: [
            "수영이나 수상 스포츠를 즐기세요",
            "명상으로 마음의 평화를 찾으세요",
            "충분한 휴식과 수면을 취하세요",
            "북쪽 방향에서 영감을 얻으세요",
        ],
    }

    result = tips.get(primary, [])

    if secondary and secondary in tips:
        result.extend(tips[secondary][:2])

    return result[:6]


def _generate_seasonal_advice(element: WuXing) -> dict[str, str]:
    """계절별 조언 생성"""
    advice = {
        WuXing.WOOD: {
            "spring": "봄은 목의 계절로 가장 활력이 넘칩니다. 새로운 시작에 적합합니다.",
            "summer": "화기가 강한 여름에는 과로를 피하고 적절히 쉬세요.",
            "autumn": "금기가 강한 가을에는 무리한 결정을 피하세요.",
            "winter": "겨울에는 내면의 성장에 집중하세요.",
        },
        WuXing.FIRE: {
            "spring": "봄의 목기가 화를 생하니 에너지가 상승합니다.",
            "summer": "여름은 화의 계절로 활동하기 좋습니다. 단, 과열에 주의하세요.",
            "autumn": "가을에는 열정을 조절하며 차분히 행동하세요.",
            "winter": "겨울 수기가 화를 극하니 건강 관리에 신경 쓰세요.",
        },
        WuXing.EARTH: {
            "spring": "환절기마다 토의 기운이 작용하니 건강에 유의하세요.",
            "summer": "여름의 화기가 토를 생하니 안정적인 시기입니다.",
            "autumn": "가을 환절기에도 토의 기운이 있어 중심을 잡기 좋습니다.",
            "winter": "겨울에는 따뜻하게 지내며 기운을 보충하세요.",
        },
        WuXing.METAL: {
            "spring": "봄의 목기가 금을 극하니 무리하지 마세요.",
            "summer": "여름의 화기가 금을 극하니 휴식을 충분히 취하세요.",
            "autumn": "가을은 금의 계절로 결단과 실행의 좋은 시기입니다.",
            "winter": "겨울에 금생수로 에너지가 흘러가니 저축에 좋습니다.",
        },
        WuXing.WATER: {
            "spring": "봄에 수생목으로 에너지가 빠져나가니 보충이 필요합니다.",
            "summer": "여름의 화기를 억제하는 역할을 하니 시원하게 지내세요.",
            "autumn": "가을의 금기가 수를 생하니 좋은 기회가 옵니다.",
            "winter": "겨울은 수의 계절로 내면 성찰에 좋습니다.",
        },
    }

    return advice.get(element, {})


def format_recommendations_text(yongsin_result: YongSinResult) -> str:
    """
    추천 정보를 텍스트로 포맷팅

    Args:
        yongsin_result: 용신 분석 결과

    Returns:
        포맷팅된 추천 텍스트
    """
    primary = yongsin_result.primary_yongsin
    recs = yongsin_result.recommendations

    lines = [
        f"🔮 용신 분석 결과: {primary.value} 오행",
        "",
        f"📋 선정 이유: {yongsin_result.reasoning}",
        "",
        "🎨 추천 색상:",
        f"  {', '.join(recs.colors[:4])}",
        "",
        "🧭 유리한 방향:",
        f"  {', '.join(recs.directions)}",
        "",
        "💼 적합한 직업:",
        f"  {', '.join(recs.careers[:6])}",
        "",
        "🎯 권장 활동:",
        f"  {', '.join(recs.activities[:4])}",
        "",
    ]

    if recs.cautions:
        lines.extend(
            [
                "⚠️ 주의사항:",
                *[f"  • {c}" for c in recs.cautions[:3]],
            ]
        )

    return "\n".join(lines)
