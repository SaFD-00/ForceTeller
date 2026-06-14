"""
ForceTeller 설정 모듈
환경 변수 및 전역 설정 관리
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 프로젝트 경로
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # ===================
    # LLM (OpenRouter 단일 게이트웨이)
    # ===================
    # OpenRouter는 OpenAI 호환 API이므로 모든 모델을 하나의 클라이언트로 호출한다.
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, alias="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # 기본 해석 모델 / 라우팅(경량) 모델 / 폴백 모델
    OPENROUTER_MODEL: str = "openai/gpt-oss-120b:free"
    OPENROUTER_ROUTING_MODEL: str = "openai/gpt-oss-20b:free"
    OPENROUTER_FALLBACK_MODEL: str = "google/gemma-4-31b-it:free"

    # 호출 파라미터
    OPENROUTER_MAX_TOKENS: int = 4096
    OPENROUTER_REASONING_EFFORT: str = "medium"  # "low" | "medium" | "high"
    OPENROUTER_TEMPERATURE: float = 0.7

    # OpenRouter 랭킹용 헤더 (선택)
    OPENROUTER_SITE_URL: str = "https://forceteller.app"
    OPENROUTER_APP_NAME: str = "ForceTeller"

    # 서버에서 허용할 모델 화이트리스트 (콤마 구분)
    OPENROUTER_ALLOWED_MODELS: str = (
        "openai/gpt-oss-120b:free,"
        "openai/gpt-oss-20b:free,"
        "google/gemma-4-26b-a4b-it:free,"
        "google/gemma-4-31b-it:free,"
        "deepseek/deepseek-v4-flash,"
        "deepseek/deepseek-v4-pro"
    )

    # 서버 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: str = "*"  # 콤마로 구분된 도메인 목록 (예: "https://example.com,https://app.example.com")

    # 세션 설정
    SESSION_MAX_HISTORY: int = 20
    SESSION_TIMEOUT_MINUTES: int = 60
    MAX_SESSIONS: int = 100  # 최대 세션 수
    SESSION_CLEANUP_PERCENTAGE: float = 0.2  # 세션 정리 시 삭제 비율

    # 대화 설정
    CONVERSATION_HISTORY_LIMIT: int = 10  # LLM에 전달할 대화 히스토리 최대 개수

    # 로깅 설정
    LOG_LEVEL: str = "INFO"  # "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 만세력 설정
    DEFAULT_CITY: str = "Seoul"
    USE_TRUE_SOLAR_TIME: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# 전역 설정 인스턴스
settings = Settings()


def get_openrouter_api_key() -> str:
    """OpenRouter API 키 반환"""
    if settings.OPENROUTER_API_KEY:
        return settings.OPENROUTER_API_KEY
    raise ValueError("OPENROUTER_API_KEY not set in environment")


def get_allowed_models() -> list[str]:
    """허용된 모델 ID 목록 반환"""
    return [m.strip() for m in settings.OPENROUTER_ALLOWED_MODELS.split(",") if m.strip()]
