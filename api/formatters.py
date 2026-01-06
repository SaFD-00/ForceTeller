"""
메시지 포맷터

분석 결과를 사용자에게 보여줄 메시지로 변환합니다.
"""

from typing import Any, List

from api.schemas import AnalysisType


class FortuneFormatter:
    """운세 분석 결과 포맷터"""

    @staticmethod
    def format(fortune_result: Any, fortune_type_name: str) -> str:
        """운세 분석 결과를 메시지로 변환"""
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


class YongsinFormatter:
    """용신 분석 결과 포맷터"""

    @staticmethod
    def format(yongsin_result: Any) -> str:
        """용신 분석 결과를 메시지로 변환"""
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


class SchoolComparisonFormatter:
    """유파 비교 결과 포맷터"""

    @staticmethod
    def format(comparison_result: Any) -> str:
        """유파 비교 결과를 메시지로 변환"""
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


class SuggestedQuestionsGenerator:
    """추천 질문 생성기"""

    # 분석 유형별 추천 질문
    _QUESTIONS_BY_TYPE = {
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

    # 키워드별 추천 질문
    _QUESTIONS_BY_KEYWORD = {
        "성격": [
            "제 성격의 장점을 극대화하려면 어떻게 해야 할까요?",
            "대인관계에서 주의할 점은 무엇인가요?",
            "성격적으로 맞는 직업은 무엇인가요?",
        ],
        "기질": [
            "제 성격의 장점을 극대화하려면 어떻게 해야 할까요?",
            "대인관계에서 주의할 점은 무엇인가요?",
            "성격적으로 맞는 직업은 무엇인가요?",
        ],
        "직업": [
            "올해 재물운은 어떤가요?",
            "사업을 시작하기 좋은 시기는 언제인가요?",
            "투자에 유리한 방향은 무엇인가요?",
        ],
        "재물": [
            "올해 재물운은 어떤가요?",
            "사업을 시작하기 좋은 시기는 언제인가요?",
            "투자에 유리한 방향은 무엇인가요?",
        ],
        "사업": [
            "올해 재물운은 어떤가요?",
            "사업을 시작하기 좋은 시기는 언제인가요?",
            "투자에 유리한 방향은 무엇인가요?",
        ],
        "연애": [
            "좋은 인연을 만나는 시기는 언제인가요?",
            "어떤 스타일의 사람과 잘 맞나요?",
            "연애운을 높이려면 어떻게 해야 할까요?",
        ],
        "결혼": [
            "좋은 인연을 만나는 시기는 언제인가요?",
            "어떤 스타일의 사람과 잘 맞나요?",
            "연애운을 높이려면 어떻게 해야 할까요?",
        ],
        "인연": [
            "좋은 인연을 만나는 시기는 언제인가요?",
            "어떤 스타일의 사람과 잘 맞나요?",
            "연애운을 높이려면 어떻게 해야 할까요?",
        ],
        "건강": [
            "건강을 위해 특별히 주의해야 할 점은요?",
            "저에게 맞는 운동이나 식이요법이 있나요?",
            "건강운이 좋아지는 시기는 언제인가요?",
        ],
        "체질": [
            "건강을 위해 특별히 주의해야 할 점은요?",
            "저에게 맞는 운동이나 식이요법이 있나요?",
            "건강운이 좋아지는 시기는 언제인가요?",
        ],
        "운세": [
            "이번 달 특별히 주의할 점은 무엇인가요?",
            "행운을 높이기 위한 방법이 있을까요?",
            "중요한 결정을 하기 좋은 시기는 언제인가요?",
        ],
        "올해": [
            "이번 달 특별히 주의할 점은 무엇인가요?",
            "행운을 높이기 위한 방법이 있을까요?",
            "중요한 결정을 하기 좋은 시기는 언제인가요?",
        ],
        "내년": [
            "이번 달 특별히 주의할 점은 무엇인가요?",
            "행운을 높이기 위한 방법이 있을까요?",
            "중요한 결정을 하기 좋은 시기는 언제인가요?",
        ],
        "용신": [
            "용신을 강화하는 방법은 무엇인가요?",
            "일상에서 용신을 활용하는 법을 알려주세요.",
            "기신을 피하는 방법이 있나요?",
        ],
        "기신": [
            "용신을 강화하는 방법은 무엇인가요?",
            "일상에서 용신을 활용하는 법을 알려주세요.",
            "기신을 피하는 방법이 있나요?",
        ],
    }

    _DEFAULT_QUESTIONS = [
        "이 내용에 대해 더 자세히 설명해주세요.",
        "다른 관점에서도 분석해주실 수 있나요?",
        "실생활에서 어떻게 활용할 수 있을까요?",
    ]

    @classmethod
    def for_analysis_type(cls, analysis_type: AnalysisType) -> List[str]:
        """분석 유형에 따른 추천 질문 반환"""
        return cls._QUESTIONS_BY_TYPE.get(analysis_type, cls._DEFAULT_QUESTIONS)

    @classmethod
    def from_context(cls, user_question: str, ai_response: str) -> List[str]:
        """질문/응답 컨텍스트 기반 추천 질문 생성"""
        # 키워드 매칭
        for keyword, questions in cls._QUESTIONS_BY_KEYWORD.items():
            if keyword in user_question:
                return questions[:3]

        return cls._DEFAULT_QUESTIONS[:3]
