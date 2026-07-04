"""
테스트 공통 fixtures
"""

from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

# ============================================================================
# Sample Data Fixtures
# ============================================================================


@pytest.fixture
def sample_saju_data() -> dict[str, Any]:
    """샘플 사주 계산 결과 데이터"""
    return {
        "input": {
            "name": "테스트",
            "birth_date": "1990-05-15",
            "birth_time": "14:30",
            "gender": "male",
            "calendar": "solar",
            "city": "Seoul",
        },
        "pillars": {
            "year": {"stem": "경", "branch": "오", "element": "금", "polarity": "양"},
            "month": {"stem": "신", "branch": "사", "element": "금", "polarity": "음"},
            "day": {"stem": "갑", "branch": "자", "element": "목", "polarity": "양"},
            "hour": {"stem": "임", "branch": "신", "element": "수", "polarity": "양"},
        },
        "elements": {"wood": 2, "fire": 1, "earth": 1, "metal": 3, "water": 1},
        "ten_gods": {"year_stem": "편관", "month_stem": "정관", "hour_stem": "편인"},
        "day_master_strength": {"strength": "약함", "score": 35},
        "yongsin": {"yongsin": "수", "heesin": "목", "geesin": "화"},
    }


@pytest.fixture
def sample_saju_data_display_format() -> dict[str, Any]:
    """프론트엔드 display 형식의 사주 데이터"""
    return {
        "birth_info": {
            "name": "테스트",
            "birth_date": "1990-05-15",
            "birth_time": "14:30",
            "gender": "male",
        },
        "four_pillars": {
            "year": {"천간": "경", "지지": "오"},
            "month": {"천간": "신", "지지": "사"},
            "day": {"천간": "갑", "지지": "자"},
            "hour": {"천간": "임", "지지": "신"},
        },
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
# DB 영속화 Fixtures (DBSessionManager / SessionRepository 테스트용)
# ============================================================================


@pytest_asyncio.fixture
async def db_url(tmp_path):
    """테스트용 임시 SQLite DB URL (테스트마다 격리)"""
    return f"sqlite+aiosqlite:///{tmp_path}/test_forceteller.db"


@pytest_asyncio.fixture
async def db_session_manager(db_url):
    """임시 DB에 스키마를 만들고 DBSessionManager를 제공 (teardown에서 엔진 정리)"""
    from conversation.db_session_manager import DBSessionManager
    from db.base import configure_engine, dispose_engine, init_models

    configure_engine(db_url)
    await init_models()
    try:
        yield DBSessionManager(session_ttl_hours=24, max_sessions=100)
    finally:
        await dispose_engine()


# ============================================================================
# Mock LLM Client Fixtures
# ============================================================================


@pytest.fixture
def mock_llm_response() -> dict[str, Any]:
    """LLM 응답 모킹 데이터"""
    return {
        "interpretation": "테스트 해석 결과입니다. 사주팔자를 분석한 결과...",
        "suggested_questions": ["직업운은 어떤가요?", "올해 운세는 어떤가요?", "궁합을 봐주세요"],
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

    fixed_time = datetime(2026, 1, 5, 12, 0, 0)

    with patch("conversation.session_manager.datetime") as mock_datetime:
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
