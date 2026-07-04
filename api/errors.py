"""API 오류 응답 헬퍼.

내부 예외 상세(str(exc), 스택트레이스)는 서버 로그에만 남기고, 클라이언트에는
일반화된 메시지만 반환한다. settings.DEBUG=True일 때만 상세를 응답에 포함한다.
"""

import logging

from fastapi import HTTPException

from config.settings import settings


def http_500(logger: logging.Logger, context: str, exc: Exception) -> HTTPException:
    """500 응답용 HTTPException을 만들고 서버 로그에 스택트레이스를 남긴다.

    반드시 except 블록 안에서 호출할 것(logger.exception이 현재 예외의
    트레이스백을 sys.exc_info로 잡는다). 클라이언트에는 DEBUG=True일 때만
    원본 예외 문자열을 노출한다.

    Args:
        logger: 호출 모듈의 로거
        context: 사용자에게 보일 일반화된 상황 설명(내부 정보 없음)
        exc: 원본 예외

    Returns:
        호출부에서 raise할 HTTPException
    """
    logger.exception("%s: %s", context, exc)
    detail = f"{context}: {exc}" if settings.DEBUG else context
    return HTTPException(status_code=500, detail=detail)


def safe_error_content(context: str, exc: Exception) -> str:
    """스트리밍(SSE) 등 HTTPException을 못 쓰는 경로용 일반화 메시지.

    DEBUG=True일 때만 원본 예외를 덧붙인다. 로깅은 호출부 책임.
    """
    return f"{context}: {exc}" if settings.DEBUG else context
