"""Multi-provider LLM Client for DSA Mentor.

Supported providers (set via LLM_PROVIDER env var):
  - "nvidia" : NVIDIA NIM API (OpenAI-compatible, e.g. DeepSeek on NVIDIA)
  - "ollama" : Local Ollama instance (OpenAI-compatible API)
"""
import json
import os
import random
import re
import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APITimeoutError, RateLimitError

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=False)

# Reasoning models that use max_completion_tokens, ignore temperature,
# and don't support response_format JSON mode.
_REASONING_MODELS = {"o1", "o1-mini", "o3", "o3-mini", "o4-mini"}


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() == "true"


# ═══════════════════════════════════════
#  BASE LLM CLIENT
# ═══════════════════════════════════════

class BaseLLMClient(ABC):
    """Common interface for all LLM providers."""

    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 16000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_api_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
        self.retry_backoff_sec = float(os.getenv("LLM_BACKOFF_SEC", "1.0"))

    @abstractmethod
    def _create_client(self) -> OpenAI:
        """Create the OpenAI-compatible client."""

    def chat(self, messages: list[dict[str, str]]) -> str:
        """Send a chat completion request and return the response content."""
        kwargs = self._build_request_kwargs(messages)
        response = self._execute_with_retry(kwargs)
        return self._extract_content(response)

    def chat_json(self, messages: list[dict[str, str]]) -> str:
        """Send a chat completion request expecting JSON output."""
        augmented = list(messages)
        if augmented:
            last = augmented[-1].copy()
            last["content"] = (
                last["content"]
                + "\n\nIMPORTANT: You MUST respond with valid JSON only. "
                "No markdown, no explanation, no code fences. Just the JSON object."
            )
            augmented[-1] = last

        kwargs = self._build_request_kwargs(augmented)
        try:
            kwargs["response_format"] = {"type": "json_object"}
            response = self._execute_with_retry(kwargs)
            return self._extract_content(response)
        except Exception as exc:
            err_msg = str(exc).lower()
            if "response_format" in err_msg or "json" in err_msg:
                # Model doesn't support JSON mode; fall back to regular chat
                kwargs.pop("response_format", None)
                response = self._execute_with_retry(kwargs)
                raw = self._extract_content(response)
                return self._extract_json_from_text(raw)
            raise

    def _build_request_kwargs(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        return kwargs

    def _execute_with_retry(self, kwargs: dict[str, Any]):
        attempt = 0
        while True:
            try:
                return self.client.chat.completions.create(**kwargs)
            except (RateLimitError, APIConnectionError, APITimeoutError) as exc:
                if attempt >= self.max_api_retries:
                    print(f"[LLM] Request failed after {attempt + 1} attempts: {exc}")
                    raise RuntimeError(
                        f"LLM request failed after {attempt + 1} retries: {exc}"
                    ) from exc
                delay = self.retry_backoff_sec * (2 ** attempt) + random.uniform(0, 0.25)
                print(f"[LLM] Retry {attempt + 1}/{self.max_api_retries} "
                      f"after {delay:.1f}s ({type(exc).__name__})")
                time.sleep(delay)
                attempt += 1

    def _extract_content(self, response) -> str:
        choice = response.choices[0]
        msg = choice.message

        content = (getattr(msg, "content", None) or "").strip()
        reasoning = (
            getattr(msg, "reasoning_content", None)
            or getattr(msg, "reasoning", None)
            or ""
        ).strip()

        if content:
            return content
        if reasoning:
            return reasoning
        if choice.finish_reason == "length":
            print("[LLM] Warning: Model hit token limit with no content.")
        return content

    @staticmethod
    def _extract_json_from_text(text: str) -> str:
        """Extract JSON object from text that may contain reasoning/markdown."""
        stripped = text.strip()

        if stripped.startswith('{') and stripped.endswith('}'):
            return stripped

        fence_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', stripped, re.DOTALL)
        if fence_match:
            return fence_match.group(1)

        # Find the last JSON object in the text
        json_blocks = []
        depth = 0
        start = -1
        in_string = False
        escape_next = False
        for i, ch in enumerate(stripped):
            if escape_next:
                escape_next = False
                continue
            if ch == '\\' and in_string:
                escape_next = True
                continue
            if ch == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0 and start >= 0:
                    json_blocks.append(stripped[start:i+1])
                    start = -1

        if json_blocks:
            return max(json_blocks, key=len)
        return stripped

    @property
    def provider_name(self) -> str:
        return self.__class__.__name__


# ═══════════════════════════════════════
#  NVIDIA NIM CLIENT
# ═══════════════════════════════════════

class _StreamedMessage:
    """Synthetic message object assembled from streamed chunks."""
    def __init__(self, content: str, reasoning_content: str):
        self.content = content
        self.reasoning_content = reasoning_content

class _StreamedChoice:
    def __init__(self, message: _StreamedMessage, finish_reason: str):
        self.message = message
        self.finish_reason = finish_reason

class _StreamedResponse:
    """Synthetic response object that matches the OpenAI non-streamed format."""
    def __init__(self, content: str, reasoning_content: str, finish_reason: str):
        self.choices = [
            _StreamedChoice(
                message=_StreamedMessage(content=content, reasoning_content=reasoning_content),
                finish_reason=finish_reason,
            )
        ]


class NvidiaLLMClient(BaseLLMClient):
    """NVIDIA NIM API client (OpenAI-compatible, supports thinking/reasoning)."""

    def __init__(
        self,
        model: str = None,
        base_url: str = None,
        api_key: str = None,
        temperature: float = 1.0,
        max_tokens: int = 8192,
        enable_thinking: bool = None,
    ):
        model = model or os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

        self.base_url = base_url or os.getenv(
            "NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"
        )
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY", "")
        if enable_thinking is None:
            self.enable_thinking = _bool_env("NVIDIA_ENABLE_THINKING", default=True)
        else:
            self.enable_thinking = enable_thinking

        print(f"[NVIDIA LLM] Initializing: model={self.model}, "
              f"base_url={self.base_url}, thinking={self.enable_thinking}")

        self.client = self._create_client()
        print(f"[NVIDIA LLM] Client ready. Model: {self.model}")

    def _create_client(self) -> OpenAI:
        return OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=httpx.Timeout(connect=10.0, read=300.0, write=10.0, pool=10.0),
        )

    def _build_request_kwargs(self, messages, response_format=None):
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": 0.95,
            "max_tokens": self.max_tokens,
            "stream": self.enable_thinking,  # stream only when thinking is enabled (DeepSeek)
        }
        if self.enable_thinking:
            kwargs["extra_body"] = {"chat_template_kwargs": {"thinking": True}}
        if response_format:
            kwargs["response_format"] = response_format
        return kwargs

    def _execute_with_retry(self, kwargs):
        """Override to handle both streaming and non-streaming NVIDIA responses."""
        is_streaming = kwargs.get("stream", False)
        attempt = 0
        while True:
            try:
                response = self.client.chat.completions.create(**kwargs)

                if not is_streaming:
                    # Non-streaming: response is already a complete object
                    return response

                # Streaming: consume chunks and assemble a synthetic response
                content_parts = []
                reasoning_parts = []
                finish_reason = None
                for chunk in response:
                    if not getattr(chunk, "choices", None):
                        continue
                    delta = chunk.choices[0].delta
                    if getattr(delta, "reasoning_content", None):
                        reasoning_parts.append(delta.reasoning_content)
                    if getattr(delta, "content", None):
                        content_parts.append(delta.content)
                    if chunk.choices[0].finish_reason:
                        finish_reason = chunk.choices[0].finish_reason

                return _StreamedResponse(
                    content="".join(content_parts),
                    reasoning_content="".join(reasoning_parts),
                    finish_reason=finish_reason or "stop",
                )
            except (RateLimitError, APIConnectionError, APITimeoutError) as exc:
                if attempt >= self.max_api_retries:
                    print(f"[NVIDIA LLM] Request failed after {attempt + 1} attempts: {exc}")
                    raise RuntimeError(
                        f"NVIDIA LLM request failed after {attempt + 1} retries: {exc}"
                    ) from exc
                delay = self.retry_backoff_sec * (2 ** attempt) + random.uniform(0, 0.25)
                print(f"[NVIDIA LLM] Retry {attempt + 1}/{self.max_api_retries} "
                      f"after {delay:.1f}s ({type(exc).__name__})")
                time.sleep(delay)
                attempt += 1

    def _extract_content(self, response) -> str:
        """Extract content from NVIDIA response, handling reasoning_content."""
        choice = response.choices[0]
        msg = choice.message

        content = (getattr(msg, "content", None) or "").strip()
        reasoning = (
            getattr(msg, "reasoning_content", None)
            or getattr(msg, "reasoning", None)
            or ""
        ).strip()

        print(f"[NVIDIA LLM] Extract: content={len(content)} chars, reasoning={len(reasoning)} chars")

        # For NVIDIA, prefer the final content (reasoning is the "thinking" trace)
        if content:
            return content
        if reasoning:
            return reasoning
        return content


# ═══════════════════════════════════════
#  OLLAMA CLIENT (local)
# ═══════════════════════════════════════

class OllamaLLMClient(BaseLLMClient):
    """Ollama local LLM client (OpenAI-compatible API at /v1)."""

    def __init__(
        self,
        model: str = None,
        base_url: str = None,
        temperature: float = 0.7,
        max_tokens: int = 16000,
    ):
        model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434/v1"
        )

        print(f"[Ollama LLM] Initializing: model={self.model}, base_url={self.base_url}")
        self.client = self._create_client()
        print(f"[Ollama LLM] Client ready. Model: {self.model}")

    def _create_client(self) -> OpenAI:
        return OpenAI(
            base_url=self.base_url,
            api_key="ollama",  # Ollama ignores the key but OpenAI client requires one
        )

    def chat_json(self, messages):
        """Ollama may not support response_format; always use prompt-based JSON."""
        augmented = list(messages)
        if augmented:
            last = augmented[-1].copy()
            last["content"] = (
                last["content"]
                + "\n\nIMPORTANT: You MUST respond with valid JSON only. "
                "No markdown, no explanation, no code fences. Just the JSON object."
            )
            augmented[-1] = last
        kwargs = self._build_request_kwargs(augmented)
        response = self._execute_with_retry(kwargs)
        raw = self._extract_content(response)
        return self._extract_json_from_text(raw)


# ═══════════════════════════════════════
#  FACTORY + SINGLETON
# ═══════════════════════════════════════

_client_instance: Optional[BaseLLMClient] = None
_client_lock = threading.Lock()
_current_provider: Optional[str] = None


def _create_llm_client(provider: str = None) -> BaseLLMClient:
    """Create an LLM client for the given provider."""
    provider = (provider or os.getenv("LLM_PROVIDER", "nvidia")).lower().strip()
    print(f"[LLM] Creating client for provider: {provider}")

    if provider == "nvidia":
        return NvidiaLLMClient()
    elif provider == "ollama":
        return OllamaLLMClient()
    else:
        print(f"[LLM] Unknown provider '{provider}', falling back to nvidia")
        return NvidiaLLMClient()


def get_llm_client() -> BaseLLMClient:
    """Get or create the singleton LLM client.

    On first call, this initializes the client for the configured provider.
    Subsequent calls reuse the same client unless switch_provider() is called.
    """
    global _client_instance, _current_provider
    desired = (os.getenv("LLM_PROVIDER") or "nvidia").lower().strip()

    if _client_instance is None or _current_provider != desired:
        with _client_lock:
            if _client_instance is None or _current_provider != desired:
                print(f"[LLM] Creating new client (provider={desired})...")
                _client_instance = _create_llm_client(desired)
                _current_provider = desired
    return _client_instance


def switch_provider(provider: str) -> BaseLLMClient:
    """Switch the LLM provider at runtime. Returns the new client."""
    global _client_instance, _current_provider
    provider = provider.lower().strip()
    with _client_lock:
        print(f"[LLM] Switching provider to: {provider}")
        os.environ["LLM_PROVIDER"] = provider
        _client_instance = _create_llm_client(provider)
        _current_provider = provider
    return _client_instance


def get_current_provider() -> str:
    """Return the name of the currently active provider."""
    return _current_provider or os.getenv("LLM_PROVIDER", "nvidia").lower().strip()


def get_available_providers() -> list[dict[str, str]]:
    """Return metadata about all available LLM providers."""
    return [
        {
            "id": "nvidia",
            "name": "NVIDIA NIM",
            "description": "NVIDIA cloud API (DeepSeek, Llama, etc.)",
            "model": os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct"),
        },
        {
            "id": "ollama",
            "name": "Ollama (Local)",
            "description": "Run models locally via Ollama",
            "model": os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
        },
    ]
