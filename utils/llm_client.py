"""
LLM API 클라이언트 (OpenRouter 단일 게이트웨이)

OpenRouter는 OpenAI 호환 Chat Completions API를 제공하므로
AsyncOpenAI 클라이언트를 base_url만 바꿔 사용한다.
스트리밍 시 reasoning 토큰은 delta.reasoning 필드로 전달된다.
"""

from collections.abc import AsyncIterator
from typing import Any

from config.logging_config import get_logger
from config.settings import settings

logger = get_logger(__name__)


class OpenRouterClient:
    """OpenRouter 통합 LLM 클라이언트"""

    def __init__(
        self,
        model: str | None = None,
        max_tokens: int | None = None,
        reasoning_effort: str | None = None,
    ):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": settings.OPENROUTER_SITE_URL,
                "X-Title": settings.OPENROUTER_APP_NAME,
            },
        )
        self.model = model or settings.OPENROUTER_MODEL
        self.max_tokens = max_tokens or settings.OPENROUTER_MAX_TOKENS
        self.reasoning_effort = reasoning_effort or settings.OPENROUTER_REASONING_EFFORT
        # 모델 폴백 체인 (primary 실패 시 OpenRouter가 서버측에서 전환)
        self.fallback_model = settings.OPENROUTER_FALLBACK_MODEL

    def _models_chain(self, model: str) -> list[str]:
        """OpenRouter 네이티브 폴백용 모델 배열"""
        chain = [model]
        if self.fallback_model and self.fallback_model != model:
            chain.append(self.fallback_model)
        return chain

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> str:
        """채팅 완료 (비스트리밍)"""
        model = kwargs.get("model", self.model)
        try:
            resp = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                extra_body={"models": self._models_chain(model)},
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenRouter chat 오류: {type(e).__name__}: {e}")
            raise

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> AsyncIterator[str]:
        """스트리밍 채팅 (텍스트만)"""
        model = kwargs.get("model", self.model)
        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            stream=True,
            extra_body={"models": self._models_chain(model)},
        )
        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                yield delta.content

    async def chat_stream_with_reasoning(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> AsyncIterator[dict[str, Any]]:
        """reasoning과 output을 분리하여 스트리밍

        이벤트 계약 (프론트엔드 SSE 소비자와 동일):
        - {"type": "reasoning", "content": str}
        - {"type": "reasoning_done", "content": ""}
        - {"type": "output", "content": str}
        - {"type": "done", "content": ""}
        """
        model = kwargs.get("model", self.model)
        reasoning_effort = kwargs.get("reasoning_effort", self.reasoning_effort)

        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                stream=True,
                extra_body={
                    "models": self._models_chain(model),
                    "reasoning": {"effort": reasoning_effort},
                },
            )

            reasoning_active = False
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta is None:
                    continue

                # OpenRouter reasoning 토큰 (typed schema에 없으므로 getattr)
                reasoning = getattr(delta, "reasoning", None)
                if reasoning:
                    reasoning_active = True
                    yield {"type": "reasoning", "content": reasoning}

                content = getattr(delta, "content", None)
                if content:
                    if reasoning_active:
                        yield {"type": "reasoning_done", "content": ""}
                        reasoning_active = False
                    yield {"type": "output", "content": content}

            yield {"type": "done", "content": ""}

        except Exception as e:
            logger.error(f"OpenRouter 스트리밍 오류: {type(e).__name__}: {e}")
            yield {"type": "error", "content": str(e)}
            yield {"type": "done", "content": ""}


def get_llm_client(model: str | None = None, **kwargs) -> OpenRouterClient:
    """LLM 클라이언트 팩토리 함수"""
    return OpenRouterClient(model=model, **kwargs)
