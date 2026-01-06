"""
LLM API 클라이언트
OpenAI (gpt-5-nano) + Google Gemini (gemini-3-flash-preview) 통합
"""

import os
import json
from typing import List, Dict, Any, Optional, Literal, AsyncIterator, Union
from abc import ABC, abstractmethod
import asyncio

from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)


class BaseLLMClient(ABC):
    """LLM 클라이언트 기본 클래스"""

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """채팅 완료 API 호출"""
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 채팅"""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API 클라이언트 (Responses API 사용)"""

    def __init__(
        self,
        model: str = None,
        reasoning_effort: str = None,
        text_verbosity: str = None,
        max_tokens: int = None,
    ):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or settings.OPENAI_MODEL
        self.reasoning_effort = reasoning_effort or settings.OPENAI_REASONING_EFFORT
        self.text_verbosity = text_verbosity or settings.OPENAI_TEXT_VERBOSITY
        self.max_tokens = max_tokens or settings.OPENAI_MAX_TOKENS

    async def chat(
        self,
        messages: List[Dict[str, str]],
        instructions: str = None,
        response_schema: Dict = None,
        **kwargs
    ) -> Union[str, Dict]:
        """
        OpenAI Responses API 호출

        참고: openai_guide.md
        - instructions: 시스템 프롬프트 (developer 권한)
        - input: 메시지 배열 직접 전달
        - reasoning.effort: "none" | "low" | "medium" | "high" | "xhigh"
        - text.verbosity: "low" | "medium" | "high"
        - response_schema: Structured Outputs용 JSON 스키마 (선택적)
          예: {"name": "response", "schema": {...}}
        """
        reasoning_effort = kwargs.get("reasoning_effort", self.reasoning_effort)
        text_verbosity = kwargs.get("text_verbosity", self.text_verbosity)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        # 메시지에서 system 역할 분리 (하위 호환성)
        system_prompt = None
        input_messages = []

        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            else:
                input_messages.append(msg)

        # instructions 파라미터 우선, 없으면 system 메시지 사용
        final_instructions = instructions or system_prompt

        # text 설정: Structured Outputs 또는 일반 verbosity
        if response_schema:
            text_config = {
                "format": {
                    "type": "json_schema",
                    "name": response_schema.get("name", "response"),
                    "strict": True,
                    "schema": response_schema.get("schema")
                }
            }
        else:
            text_config = {"verbosity": text_verbosity}

        try:
            # Responses API 사용 (GPT-5.2 가이드 기준)
            response = await self.client.responses.create(
                model=self.model,
                instructions=final_instructions,
                input=input_messages,
                reasoning={"effort": reasoning_effort},
                text=text_config,
                max_output_tokens=max_tokens,
            )

            output_text = response.output_text

            # 디버깅: 응답 확인
            logger.debug(f"output_text 길이: {len(output_text) if output_text else 0}")
            if output_text:
                logger.debug(f"output_text 앞 200자: {output_text[:200]}")

            # Structured Outputs인 경우 JSON 파싱하여 반환
            if response_schema:
                if not output_text or not output_text.strip():
                    # 빈 응답인 경우 기본값 반환
                    logger.debug("빈 응답 - 기본값 반환")
                    return {
                        "interpretation": "응답을 생성할 수 없습니다. 다시 시도해주세요.",
                        "suggested_questions": ["다시 질문해 주세요", "다른 주제로 질문해 주세요", "더 구체적으로 질문해 주세요"]
                    }

                # 1. 마크다운 코드블록 제거
                text_to_parse = output_text.strip()
                if text_to_parse.startswith("```"):
                    lines = text_to_parse.split("\n")
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    text_to_parse = "\n".join(lines)

                # 2. BOM 제거
                text_to_parse = text_to_parse.lstrip('\ufeff')

                try:
                    return json.loads(text_to_parse)
                except json.JSONDecodeError as e:
                    logger.debug(f"JSON 파싱 실패: {e}")
                    logger.debug(f"원본 응답: {text_to_parse[:500] if text_to_parse else 'None'}")

                    # JSON처럼 보이면 raw JSON을 표시하지 않고 에러 메시지 반환
                    if text_to_parse.strip().startswith("{"):
                        return {
                            "interpretation": "응답 처리 중 오류가 발생했습니다. 다시 시도해 주세요.",
                            "suggested_questions": ["다시 질문해 주세요"]
                        }

                    # 일반 텍스트면 그대로 사용
                    return {
                        "interpretation": text_to_parse,
                        "suggested_questions": []
                    }

            return output_text

        except AttributeError:
            # Responses API가 없는 경우 Chat Completions API fallback
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API 호출 오류: {type(e).__name__}: {e}")
            raise

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        instructions: str = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 응답"""
        reasoning_effort = kwargs.get("reasoning_effort", self.reasoning_effort)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        # 메시지에서 system 역할 분리 (하위 호환성)
        system_prompt = None
        input_messages = []

        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            else:
                input_messages.append(msg)

        final_instructions = instructions or system_prompt

        try:
            stream = await self.client.responses.create(
                model=self.model,
                instructions=final_instructions,
                input=input_messages,
                reasoning={"effort": reasoning_effort},
                max_output_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if hasattr(chunk, 'output_text') and chunk.output_text:
                    yield chunk.output_text
        except AttributeError:
            # Chat Completions API fallback
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    async def chat_stream_with_reasoning(
        self,
        messages: List[Dict[str, str]],
        instructions: str = None,
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """reasoning summary와 output을 분리하여 스트리밍"""
        reasoning_effort = kwargs.get("reasoning_effort", self.reasoning_effort)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        # 메시지에서 system 역할 분리
        system_prompt = None
        input_messages = []

        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            else:
                input_messages.append(msg)

        final_instructions = instructions or system_prompt

        try:
            stream = await self.client.responses.create(
                model=self.model,
                instructions=final_instructions,
                input=input_messages,
                reasoning={
                    "effort": reasoning_effort,
                    "summary": "auto"  # reasoning summary 활성화
                },
                max_output_tokens=max_tokens,
                stream=True,
            )

            async for event in stream:
                # 이벤트 타입에 따라 분류
                event_type = getattr(event, 'type', None)

                if event_type == "response.reasoning_summary_text.delta":
                    # reasoning summary 텍스트 스트리밍
                    delta = getattr(event, 'delta', '')
                    if delta:
                        yield {"type": "reasoning", "content": delta}
                elif event_type == "response.output_text.delta":
                    # 최종 응답 텍스트 스트리밍
                    delta = getattr(event, 'delta', '')
                    if delta:
                        yield {"type": "output", "content": delta}
                elif event_type == "response.reasoning_summary_part.done":
                    # reasoning 파트 완료
                    yield {"type": "reasoning_done", "content": ""}
                elif event_type == "response.completed":
                    # 전체 응답 완료
                    yield {"type": "done", "content": ""}

        except AttributeError as e:
            # Responses API가 없는 경우 일반 스트리밍으로 폴백
            logger.debug(f"Responses API not available, falling back: {e}")
            async for chunk in self.chat_stream(messages, instructions, **kwargs):
                yield {"type": "output", "content": chunk}
            yield {"type": "done", "content": ""}


class GeminiClient(BaseLLMClient):
    """Google Gemini API 클라이언트"""

    def __init__(
        self,
        model: str = None,
        thinking_level: str = None,
        max_tokens: int = None,
    ):
        from google import genai
        from google.genai import types

        self.genai = genai
        self.types = types
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model = model or settings.GEMINI_MODEL
        self.thinking_level = thinking_level or settings.GEMINI_THINKING_LEVEL
        self.max_tokens = max_tokens or settings.GEMINI_MAX_TOKENS

    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Gemini API 호출

        참고: gemini_guide.md
        - thinking_level: "minimal" | "low" | "medium" | "high"
        """
        thinking_level = kwargs.get("thinking_level", self.thinking_level)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        # 메시지를 Gemini 형식으로 변환
        contents = self._messages_to_contents(messages)

        # 동기 API를 비동기로 래핑
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self.types.GenerateContentConfig(
                    thinking_config=self.types.ThinkingConfig(
                        thinking_level=thinking_level
                    ),
                    max_output_tokens=max_tokens,
                ),
            )
        )

        return response.text

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 응답 (Gemini는 동기 스트리밍만 지원)"""
        thinking_level = kwargs.get("thinking_level", self.thinking_level)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        contents = self._messages_to_contents(messages)

        # Gemini 스트리밍은 동기식이므로 별도 처리
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=self.types.GenerateContentConfig(
                thinking_config=self.types.ThinkingConfig(
                    thinking_level=thinking_level
                ),
                max_output_tokens=max_tokens,
            ),
            stream=True,
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    def _messages_to_contents(self, messages: List[Dict[str, str]]) -> List:
        """메시지를 Gemini contents 형식으로 변환"""
        contents = []
        system_prompt = None

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                # 시스템 프롬프트는 첫 user 메시지에 포함
                system_prompt = content
            elif role == "assistant":
                contents.append(
                    self.types.Content(
                        role="model",
                        parts=[self.types.Part(text=content)]
                    )
                )
            else:
                # user 메시지
                if system_prompt and not contents:
                    # 첫 user 메시지에 시스템 프롬프트 포함
                    content = f"{system_prompt}\n\n{content}"
                    system_prompt = None
                contents.append(
                    self.types.Content(
                        role="user",
                        parts=[self.types.Part(text=content)]
                    )
                )

        return contents


class LLMClient:
    """통합 LLM 클라이언트"""

    def __init__(
        self,
        provider: Literal["openai", "gemini"] = None,
        **kwargs
    ):
        self.provider = provider or settings.DEFAULT_LLM_PROVIDER

        if self.provider == "openai":
            self._client = OpenAIClient(**kwargs)
        elif self.provider == "gemini":
            self._client = GeminiClient(**kwargs)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        response_schema: Dict = None,
        **kwargs
    ) -> Union[str, Dict]:
        """채팅 완료"""
        return await self._client.chat(messages, response_schema=response_schema, **kwargs)

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 채팅"""
        async for chunk in self._client.chat_stream(messages, **kwargs):
            yield chunk

    async def chat_stream_with_reasoning(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """reasoning summary와 output을 분리하여 스트리밍 (OpenAI 전용)"""
        if hasattr(self._client, 'chat_stream_with_reasoning'):
            async for chunk in self._client.chat_stream_with_reasoning(messages, **kwargs):
                yield chunk
        else:
            # Gemini 등 지원하지 않는 클라이언트는 일반 스트리밍으로 폴백
            async for chunk in self._client.chat_stream(messages, **kwargs):
                yield {"type": "output", "content": chunk}
            yield {"type": "done", "content": ""}

    def chat_sync(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """동기 채팅 (CLI용)"""
        return asyncio.run(self.chat(messages, **kwargs))


def get_llm_client(
    provider: Literal["openai", "gemini"] = None,
    **kwargs
) -> LLMClient:
    """LLM 클라이언트 팩토리 함수"""
    return LLMClient(provider=provider, **kwargs)
