"""
LangChain 기반 LLM 추상화 (OpenRouter 단일 게이트웨이)

OpenRouter는 OpenAI 호환 API이므로 ChatOpenAI 하나로 모든 모델을 호출한다.
캐싱, 모델 폴백, 구조화된 출력, 재시도를 지원한다.
"""

import json
from functools import lru_cache
from typing import Any, TypeVar

from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from config.settings import settings

T = TypeVar("T", bound=BaseModel)


def _openrouter_headers() -> dict[str, str]:
    """OpenRouter 랭킹/식별용 헤더"""
    return {
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
    }


@lru_cache(maxsize=16)
def create_llm(
    model: str | None = None,
    temperature: float = 0.7,
) -> BaseChatModel:
    """OpenRouter LLM 인스턴스 생성 (캐시됨)

    Args:
        model: OpenRouter 모델 ID (None이면 기본 모델)
        temperature: 온도 (0.0 ~ 2.0)

    Returns:
        OpenRouter를 가리키는 ChatOpenAI 인스턴스

    Note:
        lru_cache 키는 (model, temperature). ChatOpenAI는 상태 없는 경량
        객체이므로 모델별로 캐시해도 안전하다.
    """
    return ChatOpenAI(
        model=model or settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=temperature,
        max_tokens=settings.OPENROUTER_MAX_TOKENS,
        default_headers=_openrouter_headers(),
    )


def create_structured_llm(
    schema: type[T],
    model: str | None = None,
    temperature: float = 0.0,
) -> BaseChatModel:
    """구조화된 출력을 위한 LLM 생성

    Pydantic 스키마를 사용하여 LLM이 항상 해당 형식으로 응답하도록 한다.
    무료/오픈 모델의 스키마 준수율을 높이기 위해 기본 temperature는 0.0.

    Args:
        schema: Pydantic 스키마 클래스
        model: OpenRouter 모델 ID
        temperature: 온도 (구조화 출력은 0 권장)

    Returns:
        with_structured_output이 적용된 LLM
    """
    llm = create_llm(model=model, temperature=temperature)
    return llm.with_structured_output(schema, method="json_schema")


def create_llm_with_fallback(
    model: str | None = None,
    fallback_model: str | None = None,
) -> BaseChatModel:
    """모델 폴백 체인이 있는 LLM 생성

    Primary 모델이 실패하면 자동으로 fallback 모델을 시도한다.

    Args:
        model: 기본 모델 ID (None이면 설정 기본값)
        fallback_model: 폴백 모델 ID (None이면 설정 폴백값)

    Returns:
        폴백 체인이 적용된 LLM
    """
    primary = create_llm(model=model or settings.OPENROUTER_MODEL)
    fallback = create_llm(model=fallback_model or settings.OPENROUTER_FALLBACK_MODEL)
    return primary.with_fallbacks([fallback])


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((ValidationError, OutputParserException, json.JSONDecodeError)),
    reraise=True,
)
async def ainvoke_structured(chain: Any, payload: dict) -> Any:
    """구조화 출력 체인을 재시도와 함께 호출

    무료/오픈 모델은 JSON 스키마 준수가 불안정할 수 있어
    검증 실패 시 지수 백오프로 재시도한다.

    Args:
        chain: prompt | structured_llm 형태의 Runnable
        payload: chain.ainvoke에 전달할 입력

    Returns:
        검증된 Pydantic 결과
    """
    return await chain.ainvoke(payload)


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
    """LLM 캐시 초기화 (테스트나 설정 변경 시 사용)"""
    create_llm.cache_clear()
