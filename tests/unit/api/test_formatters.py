"""
메시지 포맷터 테스트
"""

import pytest
from dataclasses import dataclass, field
from typing import List, Optional
from unittest.mock import MagicMock


class TestFortuneFormatter:
    """운세 메시지 포맷터 테스트"""

    def create_mock_fortune_result(
        self,
        score: int = 75,
        summary: str = "좋은 운세입니다",
        positive: List[str] = None,
        negative: List[str] = None,
        advice: List[str] = None,
        colors: List[str] = None,
        numbers: List[int] = None,
        directions: List[str] = None,
    ):
        """테스트용 운세 결과 생성"""
        result = MagicMock()
        result.score = score
        result.summary = summary

        result.details = MagicMock()
        result.details.positive = ["긍정적 요소1", "긍정적 요소2"] if positive is None else positive
        result.details.negative = ["주의점1"] if negative is None else negative
        result.details.advice = ["조언1"] if advice is None else advice

        result.lucky_elements = MagicMock()
        result.lucky_elements.colors = ["빨강", "노랑"] if colors is None else colors
        result.lucky_elements.numbers = [3, 7] if numbers is None else numbers
        result.lucky_elements.directions = ["동", "남"] if directions is None else directions

        return result

    def test_format_fortune_message_basic(self):
        """기본 운세 메시지 포맷팅"""
        from api.formatters import FortuneFormatter

        result = self.create_mock_fortune_result()
        message = FortuneFormatter.format(result, "종합운")

        assert "## 종합운 분석 결과" in message
        assert "**점수**: 75/100" in message
        assert "**요약**: 좋은 운세입니다" in message
        assert "### 긍정적 요소" in message
        assert "- 긍정적 요소1" in message
        assert "### 주의할 점" in message
        assert "### 조언" in message
        assert "**행운의 색상**: 빨강, 노랑" in message
        assert "**행운의 숫자**: 3, 7" in message
        assert "**유리한 방향**: 동, 남" in message

    def test_format_fortune_message_empty_sections(self):
        """빈 섹션이 있는 운세 메시지"""
        from api.formatters import FortuneFormatter

        result = self.create_mock_fortune_result(
            positive=[],
            negative=[],
            advice=[],
            colors=[],
            numbers=[],
            directions=[]
        )
        message = FortuneFormatter.format(result, "직업운")

        assert "## 직업운 분석 결과" in message
        assert "### 긍정적 요소" not in message
        assert "### 주의할 점" not in message
        assert "### 조언" not in message
        assert "**행운의 색상**" not in message


class TestYongsinFormatter:
    """용신 메시지 포맷터 테스트"""

    def create_mock_yongsin_result(
        self,
        primary_yongsin_value: str = "목",
        secondary_yongsin_value: str = "화",
        method_value: str = "강약용신",
        day_master_strength_value: str = "신약",
        confidence: float = 0.85,
        reasoning: str = "일간이 약하여 목으로 보강",
        xi_sin: List[str] = None,
        ji_sin: List[str] = None,
    ):
        """테스트용 용신 결과 생성"""
        result = MagicMock()

        result.primary_yongsin = MagicMock()
        result.primary_yongsin.value = primary_yongsin_value

        if secondary_yongsin_value:
            result.secondary_yongsin = MagicMock()
            result.secondary_yongsin.value = secondary_yongsin_value
        else:
            result.secondary_yongsin = None

        result.method = MagicMock()
        result.method.value = method_value

        result.day_master_strength = MagicMock()
        result.day_master_strength.value = day_master_strength_value

        result.confidence = confidence
        result.reasoning = reasoning

        # 희신/기신
        result.xi_sin = [MagicMock(value=v) for v in (xi_sin or ["화", "토"])]
        result.ji_sin = [MagicMock(value=v) for v in (ji_sin or ["금", "수"])]

        # 추천
        result.recommendations = MagicMock()
        result.recommendations.colors = ["초록", "파랑"]
        result.recommendations.directions = ["동", "남"]
        result.recommendations.careers = ["교육", "상담", "의료"]
        result.recommendations.activities = ["산책", "독서"]

        return result

    def test_format_yongsin_message_basic(self):
        """기본 용신 메시지 포맷팅"""
        from api.formatters import YongsinFormatter

        result = self.create_mock_yongsin_result()
        message = YongsinFormatter.format(result)

        assert "## 용신 분석 결과" in message
        assert "**주 용신**: 목" in message
        assert "**보조 용신**: 화" in message
        assert "**분석 방법**: 강약용신" in message
        assert "**일간 강약**: 신약" in message
        assert "**신뢰도**: 85%" in message
        assert "**선정 이유**: 일간이 약하여 목으로 보강" in message
        assert "**희신 (도움)**: 화, 토" in message
        assert "**기신 (피해야 할)**: 금, 수" in message
        assert "### 추천" in message
        assert "- **색상**: 초록, 파랑" in message

    def test_format_yongsin_without_secondary(self):
        """보조 용신이 없는 경우"""
        from api.formatters import YongsinFormatter

        result = self.create_mock_yongsin_result(secondary_yongsin_value=None)
        message = YongsinFormatter.format(result)

        assert "**주 용신**: 목" in message
        assert "**보조 용신**" not in message


class TestSchoolComparisonFormatter:
    """유파 비교 메시지 포맷터 테스트"""

    def create_mock_school_comparison_result(self):
        """테스트용 유파 비교 결과 생성"""
        result = MagicMock()

        interp1 = MagicMock()
        interp1.school_name = "자평명리"
        interp1.yong_sin = MagicMock(value="목")
        interp1.geok_guk = "정인격"
        interp1.confidence = 0.9
        interp1.overall = "자평명리에서는 일간 중심으로 분석합니다."

        interp2 = MagicMock()
        interp2.school_name = "적천수"
        interp2.yong_sin = MagicMock(value="화")
        interp2.geok_guk = None
        interp2.confidence = 0.85
        interp2.overall = "적천수에서는 오행의 흐름을 중시합니다."

        result.interpretations = [interp1, interp2]

        consensus1 = MagicMock()
        consensus1.agreement = "일간이 약함에 동의"
        result.consensus = [consensus1]

        result.recommendation = "종합적으로 목 오행을 강화하는 것이 좋습니다."

        return result

    def test_format_school_comparison_message(self):
        """유파 비교 메시지 포맷팅"""
        from api.formatters import SchoolComparisonFormatter

        result = self.create_mock_school_comparison_result()
        message = SchoolComparisonFormatter.format(result)

        assert "## 유파별 해석 비교" in message
        assert "### 자평명리" in message
        assert "**용신**: 목" in message
        assert "**격국**: 정인격" in message
        assert "### 적천수" in message
        assert "### 합의점" in message
        assert "- 일간이 약함에 동의" in message
        assert "### 종합 권장" in message
        assert "목 오행을 강화" in message


class TestSuggestedQuestionsGenerator:
    """추천 질문 생성기 테스트"""

    def test_get_suggested_questions_by_analysis_type(self):
        """분석 유형별 추천 질문 조회"""
        from api.formatters import SuggestedQuestionsGenerator
        from api.schemas import AnalysisType

        questions = SuggestedQuestionsGenerator.for_analysis_type(AnalysisType.FORTUNE_GENERAL)
        assert len(questions) > 0
        assert any("운세" in q or "주의" in q for q in questions)

        questions = SuggestedQuestionsGenerator.for_analysis_type(AnalysisType.YONGSIN)
        assert len(questions) > 0
        assert any("용신" in q for q in questions)

    def test_generate_from_context(self):
        """질문/응답 컨텍스트 기반 추천 질문 생성"""
        from api.formatters import SuggestedQuestionsGenerator

        questions = SuggestedQuestionsGenerator.from_context(
            user_question="제 성격이 어떤가요?",
            ai_response="당신은 목 성향이 강합니다..."
        )

        assert len(questions) == 3
        assert any("성격" in q for q in questions)

    def test_generate_from_context_career(self):
        """직업 관련 질문에 대한 추천 질문"""
        from api.formatters import SuggestedQuestionsGenerator

        questions = SuggestedQuestionsGenerator.from_context(
            user_question="직업운이 어떤가요?",
            ai_response="재물운이 좋습니다..."
        )

        assert len(questions) == 3
        assert any("재물" in q or "사업" in q or "투자" in q for q in questions)

    def test_generate_from_context_default(self):
        """키워드가 없는 질문에 대한 기본 추천 질문"""
        from api.formatters import SuggestedQuestionsGenerator

        questions = SuggestedQuestionsGenerator.from_context(
            user_question="안녕하세요",
            ai_response="안녕하세요."
        )

        assert len(questions) == 3
