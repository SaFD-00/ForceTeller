"""
설정 모듈 테스트
"""

import pytest
from unittest.mock import patch
import os


class TestSettings:
    """Settings 클래스 테스트"""

    def test_settings_has_conversation_history_limit(self):
        """대화 히스토리 제한 설정이 있는지 확인"""
        from config.settings import settings

        assert hasattr(settings, "CONVERSATION_HISTORY_LIMIT")
        assert isinstance(settings.CONVERSATION_HISTORY_LIMIT, int)
        assert settings.CONVERSATION_HISTORY_LIMIT > 0

    def test_settings_has_session_cleanup_percentage(self):
        """세션 정리 비율 설정이 있는지 확인"""
        from config.settings import settings

        assert hasattr(settings, "SESSION_CLEANUP_PERCENTAGE")
        assert isinstance(settings.SESSION_CLEANUP_PERCENTAGE, float)
        assert 0 < settings.SESSION_CLEANUP_PERCENTAGE <= 1.0

    def test_settings_has_openrouter_config(self):
        """OpenRouter 설정이 있는지 확인"""
        from config.settings import settings

        assert hasattr(settings, "OPENROUTER_BASE_URL")
        assert settings.OPENROUTER_BASE_URL.startswith("https://openrouter.ai")
        assert hasattr(settings, "OPENROUTER_MODEL")
        assert ":free" in settings.OPENROUTER_MODEL or "/" in settings.OPENROUTER_MODEL
        assert settings.OPENROUTER_REASONING_EFFORT in ["low", "medium", "high"]

    def test_allowed_models_parsing(self):
        """허용 모델 목록 파싱 확인"""
        from config.settings import get_allowed_models

        models = get_allowed_models()
        assert len(models) == 6
        assert "openai/gpt-oss-120b:free" in models
        assert "deepseek/deepseek-v4-pro" in models

    def test_settings_has_log_level(self):
        """로그 레벨 설정이 있는지 확인"""
        from config.settings import settings

        assert hasattr(settings, "LOG_LEVEL")
        assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_settings_has_max_sessions(self):
        """최대 세션 수 설정이 있는지 확인"""
        from config.settings import settings

        assert hasattr(settings, "MAX_SESSIONS")
        assert isinstance(settings.MAX_SESSIONS, int)
        assert settings.MAX_SESSIONS > 0

    def test_settings_default_values(self):
        """설정 기본값 확인"""
        from config.settings import Settings

        # 환경변수 없이 기본값 사용
        with patch.dict(os.environ, {}, clear=False):
            test_settings = Settings()

            assert test_settings.CONVERSATION_HISTORY_LIMIT == 10
            assert test_settings.SESSION_CLEANUP_PERCENTAGE == 0.2
            assert test_settings.LOG_LEVEL == "INFO"
            assert test_settings.MAX_SESSIONS == 100

    def test_settings_env_override(self):
        """환경변수로 설정 오버라이드 확인"""
        from config.settings import Settings

        with patch.dict(os.environ, {
            "CONVERSATION_HISTORY_LIMIT": "20",
            "LOG_LEVEL": "DEBUG",
            "MAX_SESSIONS": "50",
        }):
            test_settings = Settings()

            assert test_settings.CONVERSATION_HISTORY_LIMIT == 20
            assert test_settings.LOG_LEVEL == "DEBUG"
            assert test_settings.MAX_SESSIONS == 50


class TestLoggingConfig:
    """로깅 설정 테스트"""

    def test_get_logger_returns_logger(self):
        """get_logger가 로거를 반환하는지 확인"""
        from config.logging_config import get_logger

        logger = get_logger("test")
        assert logger is not None
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_get_logger_with_module_name(self):
        """모듈 이름으로 로거 생성"""
        from config.logging_config import get_logger

        logger = get_logger(__name__)
        assert logger.name == __name__

    def test_logger_has_handlers(self):
        """로거에 핸들러가 설정되어 있는지 확인"""
        from config.logging_config import setup_logging, get_logger

        setup_logging()
        logger = get_logger("test_handlers")

        # 루트 로거 또는 현재 로거에 핸들러가 있어야 함
        import logging
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0 or len(logger.handlers) > 0
