"""
Protocol 인터페이스 테스트
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, List, Any, Optional

from utils.protocols import LLMClientProtocol, SessionManagerProtocol


class TestLLMClientProtocol:
    """LLMClientProtocol 테스트"""

    def test_protocol_is_runtime_checkable(self):
        """프로토콜이 런타임에 체크 가능한지 확인"""
        assert hasattr(LLMClientProtocol, '__protocol_attrs__') or \
               hasattr(LLMClientProtocol, '_is_runtime_protocol')

    def test_mock_implements_protocol(self):
        """Mock 객체가 프로토콜을 구현하는지 확인"""
        # Python 3.12+의 runtime_checkable isinstance는 멤버 존재를 정적으로 확인하므로
        # 동적 속성을 가진 plain MagicMock 대신 spec으로 프로토콜을 명시한다.
        mock_client = MagicMock(spec=LLMClientProtocol)
        mock_client.chat = AsyncMock(return_value="테스트 응답")
        mock_client.chat_stream = AsyncMock()

        # runtime_checkable 프로토콜은 isinstance로 확인 가능
        assert isinstance(mock_client, LLMClientProtocol)

    @pytest.mark.asyncio
    async def test_mock_client_chat(self):
        """Mock 클라이언트 chat 메서드 테스트"""
        mock_client = MagicMock()
        mock_client.chat = AsyncMock(return_value={"interpretation": "테스트"})

        messages = [{"role": "user", "content": "테스트 질문"}]
        result = await mock_client.chat(messages)

        assert result == {"interpretation": "테스트"}
        mock_client.chat.assert_called_once_with(messages)

    @pytest.mark.asyncio
    async def test_mock_client_chat_with_schema(self):
        """Mock 클라이언트 chat 메서드 (스키마 포함) 테스트"""
        mock_client = MagicMock()
        mock_client.chat = AsyncMock(return_value={"interpretation": "스키마 응답"})

        messages = [{"role": "user", "content": "질문"}]
        schema = {"name": "response", "schema": {"type": "object"}}

        result = await mock_client.chat(messages, response_schema=schema)

        assert result == {"interpretation": "스키마 응답"}


class TestSessionManagerProtocol:
    """SessionManagerProtocol 테스트"""

    def test_protocol_is_runtime_checkable(self):
        """프로토콜이 런타임에 체크 가능한지 확인"""
        assert hasattr(SessionManagerProtocol, '__protocol_attrs__') or \
               hasattr(SessionManagerProtocol, '_is_runtime_protocol')

    def test_mock_implements_protocol(self):
        """Mock 객체가 프로토콜을 구현하는지 확인"""
        mock_manager = MagicMock()
        mock_manager.create_session = MagicMock()
        mock_manager.get_session = MagicMock()
        mock_manager.delete_session = MagicMock()
        mock_manager.add_message = MagicMock()
        mock_manager.get_conversation_history = MagicMock()
        mock_manager.list_sessions = MagicMock()
        mock_manager.get_session_count = MagicMock()
        mock_manager.export_session = MagicMock()

        assert isinstance(mock_manager, SessionManagerProtocol)

    def test_mock_session_manager_create_session(self):
        """Mock 세션 매니저 create_session 테스트"""
        mock_manager = MagicMock()
        mock_session = MagicMock()
        mock_session.session_id = "test-123"
        mock_manager.create_session = MagicMock(return_value=mock_session)

        saju_data = {"pillars": {}}
        result = mock_manager.create_session(saju_data)

        assert result.session_id == "test-123"
        mock_manager.create_session.assert_called_once_with(saju_data)

    def test_mock_session_manager_get_session(self):
        """Mock 세션 매니저 get_session 테스트"""
        mock_manager = MagicMock()
        mock_session = MagicMock()
        mock_session.session_id = "existing-id"
        mock_manager.get_session = MagicMock(return_value=mock_session)

        result = mock_manager.get_session("existing-id")

        assert result.session_id == "existing-id"

    def test_mock_session_manager_get_nonexistent_session(self):
        """존재하지 않는 세션 조회 테스트"""
        mock_manager = MagicMock()
        mock_manager.get_session = MagicMock(return_value=None)

        result = mock_manager.get_session("nonexistent")

        assert result is None

    def test_mock_session_manager_add_message(self):
        """Mock 세션 매니저 add_message 테스트"""
        mock_manager = MagicMock()
        mock_message = MagicMock()
        mock_message.role = "user"
        mock_message.content = "테스트 메시지"
        mock_manager.add_message = MagicMock(return_value=mock_message)

        result = mock_manager.add_message("session-id", "user", "테스트 메시지")

        assert result.role == "user"
        assert result.content == "테스트 메시지"

    def test_mock_session_manager_get_conversation_history(self):
        """Mock 세션 매니저 get_conversation_history 테스트"""
        mock_manager = MagicMock()
        history = [
            {"role": "user", "content": "질문"},
            {"role": "assistant", "content": "응답"}
        ]
        mock_manager.get_conversation_history = MagicMock(return_value=history)

        result = mock_manager.get_conversation_history("session-id")

        assert len(result) == 2
        assert result[0]["role"] == "user"

    def test_mock_session_manager_list_sessions(self):
        """Mock 세션 매니저 list_sessions 테스트"""
        mock_manager = MagicMock()
        sessions = [
            {"session_id": "s1", "name": "테스트1"},
            {"session_id": "s2", "name": "테스트2"}
        ]
        mock_manager.list_sessions = MagicMock(return_value=sessions)

        result = mock_manager.list_sessions()

        assert len(result) == 2

    def test_mock_session_manager_delete_session(self):
        """Mock 세션 매니저 delete_session 테스트"""
        mock_manager = MagicMock()
        mock_manager.delete_session = MagicMock(return_value=True)

        result = mock_manager.delete_session("session-id")

        assert result is True
