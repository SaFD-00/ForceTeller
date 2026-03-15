"""
LangChain 기반 LLM 추상화

Provider 독립적인 LLM 래퍼를 제공합니다.
캐싱, 폴백 체인, 구조화된 출력 등을 지원합니다.
"""

import os
from functools import lru_cache
from typing import TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential


T = TypeVar("T", bound=BaseModel)


@lru_cache(maxsize=8)
def create_llm(
    provider: str = "openai",
    model: str | None = None,
    temperature: float = 0.7,
) -> BaseChatModel:
    """LLM 인스턴스 생성 (캐시됨)

    Args:
        provider: LLM 제공자 ("openai" | "google")
        model: 모델명 (None이면 기본값 사용)
        temperature: 온도 (0.0 ~ 2.0)

    Returns:
        BaseChatModel 인스턴스

    Raises:
        ValueError: 알 수 없는 provider인 경우
    """
    if provider == "openai":
        return ChatOpenAI(
            model=model or os.getenv("OPENAI_MODEL", "gpt-4o"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
        )
    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model=model or os.getenv("GOOGLE_MODEL", "gemini-2.0-flash"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=temperature,
        )
    else:
        raise ValueError(
            f"Unknown provider: '{provider}'. Available: openai, google"
        )


def create_structured_llm(
    schema: type[T],
    provider: str = "openai",
    model: str | None = None,
    temperature: float = 0.7,
) -> BaseChatModel:
    """구조화된 출력을 위한 LLM 생성

    Pydantic 스키마를 사용하여 LLM이 항상 해당 형식으로 응답하도록 합니다.

    Args:
        schema: Pydantic 스키마 클래스
        provider: LLM 제공자
        model: 모델명
        temperature: 온도

    Returns:
        with_structured_output이 적용된 LLM

    Example:
        >>> from agents.schemas import InterpretationResult
        >>> llm = create_structured_llm(InterpretationResult)
        >>> result = await llm.ainvoke(messages)
        >>> print(result.interpretation)
    """
    llm = create_llm(provider=provider, model=model, temperature=temperature)
    return llm.with_structured_output(schema)


def create_llm_with_fallback(
    primary_provider: str = "openai",
    fallback_provider: str = "google",
    model: str | None = None,
) -> BaseChatModel:
    """폴백 체인이 있는 LLM 생성

    Primary LLM이 실패하면 자동으로 fallback LLM을 시도합니다.

    Args:
        primary_provider: 기본 LLM 제공자
        fallback_provider: 폴백 LLM 제공자
        model: 모델명 (None이면 각 provider 기본값)

    Returns:
        폴백 체인이 적용된 LLM

    Example:
        >>> llm = create_llm_with_fallback("openai", "google")
        >>> # OpenAI 실패 시 자동으로 Google 시도
        >>> result = await llm.ainvoke(messages)
    """
    primary = create_llm(provider=primary_provider, model=model)
    fallback = create_llm(provider=fallback_provider)
    return primary.with_fallbacks([fallback])


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def invoke_with_retry(
    llm: BaseChatModel,
    messages: list,
) -> str:
    """재시도 로직이 있는 LLM 호출

    Args:
        llm: LLM 인스턴스
        messages: 메시지 리스트

    Returns:
        LLM 응답 내용
    """
    response = await llm.ainvoke(messages)
    return response.content


def clear_llm_cache() -> None:
    """LLM 캐시 초기화

    테스트나 설정 변경 시 사용합니다.
    """
    create_llm.cache_clear()
