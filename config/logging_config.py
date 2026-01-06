"""
로깅 설정 모듈

애플리케이션 전체의 로깅을 중앙에서 관리합니다.
"""

import logging
import sys
from typing import Optional

from config.settings import settings


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> None:
    """
    로깅 설정 초기화

    Args:
        level: 로그 레벨 (기본값: settings.LOG_LEVEL)
        format_string: 로그 포맷 (기본값: settings.LOG_FORMAT)
    """
    log_level = level or settings.LOG_LEVEL
    log_format = format_string or settings.LOG_FORMAT

    # 숫자 레벨로 변환
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # 기존 핸들러 제거 (중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)

    # 외부 라이브러리 로그 레벨 조정
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    모듈용 로거 반환

    Args:
        name: 로거 이름 (보통 __name__ 사용)

    Returns:
        설정된 로거 인스턴스
    """
    return logging.getLogger(name)


# 모듈 로드 시 자동 설정
setup_logging()
