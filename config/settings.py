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

    # API 키
    OPENAI_API_KEY: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")

    # LLM 설정
    DEFAULT_LLM_PROVIDER: str = "openai"  # "openai" | "gemini"
    OPENAI_MODEL: str = "gpt-5-nano"
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    # OpenAI 설정
    OPENAI_REASONING_EFFORT: str = "none"  # "none" | "low" | "medium" | "high" | "xhigh"
    OPENAI_TEXT_VERBOSITY: str = "medium"  # "low" | "medium" | "high"
    OPENAI_MAX_TOKENS: int = 4096

    # Gemini 설정
    GEMINI_THINKING_LEVEL: str = "low"  # "minimal" | "low" | "medium" | "high"
    GEMINI_MAX_TOKENS: int = 4096

    # 서버 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: str = "*"  # 콤마로 구분된 도메인 목록 (예: "https://example.com,https://app.example.com")

    # 세션 설정
    SESSION_MAX_HISTORY: int = 20
    SESSION_TIMEOUT_MINUTES: int = 60

    # 만세력 설정
    DEFAULT_CITY: str = "Seoul"
    USE_TRUE_SOLAR_TIME: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# 전역 설정 인스턴스
settings = Settings()


def get_openai_api_key() -> str:
    """OpenAI API 키 반환"""
    if settings.OPENAI_API_KEY:
        return settings.OPENAI_API_KEY
    raise ValueError("OPENAI_API_KEY not set in environment")


def get_google_api_key() -> str:
    """Google API 키 반환"""
    if settings.GOOGLE_API_KEY:
        return settings.GOOGLE_API_KEY
    raise ValueError("GOOGLE_API_KEY not set in environment")
