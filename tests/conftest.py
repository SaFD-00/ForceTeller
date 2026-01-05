"""
테스트 공통 fixtures
"""

import pytest
import asyncio
from typing import Dict, Any, List, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_saju_data() -> Dict[str, Any]:
    """샘플 사주 계산 결과 데이터"""
    return {
        "input": {
            "name": "테스트",
            "birth_date": "1990-05-15",
            "birth_time": "14:30",
            "gender": "male",
            "calendar": "solar",
            "city": "Seoul"
        },
        "pillars": {
            "year": {"stem": "경", "branch": "오", "element": "금", "polarity": "양"},
            "month": {"stem": "신", "branch": "사", "element": "금", "polarity": "음"},
            "day": {"stem": "갑", "branch": "자", "element": "목", "polarity": "양"},
            "hour": {"stem": "임", "branch": "신", "element": "수", "polarity": "양"}
        },
        "elements": {
            "wood": 2,
            "fire": 1,
            "earth": 1,
            "metal": 3,
            "water": 1
        },
        "ten_gods": {
            "year_stem": "편관",
            "month_stem": "정관",
            "hour_stem": "편인"
        },
        "day_master_strength": {
            "strength": "약함",
            "score": 35
        },
        "yongsin": {
            "yongsin": "수",
            "heesin": "목",
            "geesin": "화"
        }
    }


@pytest.fixture
def sample_saju_data_display_format() -> Dict[str, Any]:
    """프론트엔드 display 형식의 사주 데이터"""
    return {
        "birth_info": {
            "name": "테스트",
            "birth_date": "1990-05-15",
            "birth_time": "14:30",
            "gender": "male"
        },
        "four_pillars": {
            "year": {"천간": "경", "지지": "오"},
            "month": {"천간": "신", "지지": "사"},
            "day": {"천간": "갑", "지지": "자"},
            "hour": {"천간": "임", "지지": "신"}
        }
    }


# ============================================================================
# Session Fixtures
# ============================================================================

@pytest.fixture
def session_manager():
    """SessionManager 인스턴스"""
    from conversation.session_manager import SessionManager
    return SessionManager(max_sessions=100, session_ttl_hours=24)


@pytest.fixture
def sample_session(session_manager, sample_saju_data):
    """샘플 세션"""
    return session_manager.create_session(sample_saju_data)


# ============================================================================
# Mock LLM Client Fixtures
# ============================================================================

@pytest.fixture
def mock_llm_response() -> Dict[str, Any]:
    """LLM 응답 모킹 데이터"""
    return {
        "interpretation": "테스트 해석 결과입니다. 사주팔자를 분석한 결과...",
        "suggested_questions": [
            "직업운은 어떤가요?",
            "올해 운세는 어떤가요?",
            "궁합을 봐주세요"
        ]
    }


@pytest.fixture
def mock_llm_client(mock_llm_response):
    """LLMClient 모킹"""
    mock_client = MagicMock()

    # chat 메서드 모킹 (async)
    async def mock_chat(*args, **kwargs):
        return mock_llm_response

    mock_client.chat = AsyncMock(side_effect=mock_chat)

    # chat_stream 메서드 모킹 (async generator)
    async def mock_chat_stream(*args, **kwargs):
        for chunk in ["테스트 ", "해석 ", "결과"]:
            yield chunk

    mock_client.chat_stream = mock_chat_stream

    return mock_client


@pytest.fixture
def mock_llm_client_error():
    """LLM 호출 실패 모킹"""
    mock_client = MagicMock()

    async def mock_chat_error(*args, **kwargs):
        raise Exception("API 호출 실패")

    mock_client.chat = AsyncMock(side_effect=mock_chat_error)

    return mock_client


# ============================================================================
# Agent Fixtures
# ============================================================================

@pytest.fixture
def mock_agent_response():
    """AgentResponse 모킹 데이터"""
    from agents.base_agent import AgentResponse
    return AgentResponse(
        agent_name="personality",
        interpretation="성격 분석 결과입니다.",
        confidence=1.0,
        metadata={"provider": "openai", "model": "gpt-4"},
        suggested_questions=["직업운은?", "연애운은?"]
    )


# ============================================================================
# API Test Fixtures
# ============================================================================

@pytest.fixture
def test_client():
    """FastAPI TestClient"""
    from fastapi.testclient import TestClient
    from api.server import create_app

    app = create_app()
    return TestClient(app)


@pytest.fixture
def async_test_client():
    """비동기 테스트 클라이언트"""
    import httpx
    from api.server import create_app

    app = create_app()
    return httpx.AsyncClient(app=app, base_url="http://test")


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def freeze_time():
    """시간 고정 fixture (테스트용)"""
    from unittest.mock import patch
    from datetime import datetime

    fixed_time = datetime(2026, 1, 5, 12, 0, 0)

    with patch('conversation.session_manager.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.fromisoformat = datetime.fromisoformat
        yield fixed_time


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """pytest 마커 등록"""
    config.addinivalue_line("markers", "unit: 단위 테스트")
    config.addinivalue_line("markers", "integration: 통합 테스트")
    config.addinivalue_line("markers", "e2e: End-to-End 테스트")
    config.addinivalue_line("markers", "slow: 느린 테스트")
