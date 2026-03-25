"""Multi-provider LLM Client for DSA Mentor.

Supported providers (set via LLM_PROVIDER env var):
  - "dell"   : Dell AIA Gateway with SSO/OAuth authentication
  - "nvidia" : NVIDIA NIM API (OpenAI-compatible, e.g. DeepSeek on NVIDIA)
  - "ollama" : Local Ollama instance (OpenAI-compatible API)

Dell authentication flow (when provider="dell"):
  1. USE_SSO=true (default) → triggers Dell SSO browser login via aia-auth-client
  2. CLIENT_ID + CLIENT_SECRET set → uses OAuth client_credentials flow
  3. ENABLE_TOKEN_REFRESH_AT_SERVER_SIDE=true → uses Basic auth with server-side refresh
"""
import io
import json
import os
import random
import re
import sys
import uuid
import zipfile
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

import certifi
import httpx
import requests
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APITimeoutError, RateLimitError

# Load .env into actual OS environment so authentication_provider can read USE_SSO, CLIENT_ID, etc.
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=False)

# Reasoning models that use max_completion_tokens, ignore temperature,
# and don't support response_format JSON mode.
_REASONING_MODELS = {"gpt-oss-120b", "o1", "o1-mini", "o3", "o3-mini", "o4-mini"}

_certifi_updated = False


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
        self.max_api_retries = int(os.getenv("LLM_MAX_RETRIES", os.getenv("DELL_LLM_MAX_RETRIES", "3")))
        self.retry_backoff_sec = float(os.getenv("LLM_BACKOFF_SEC", os.getenv("DELL_LLM_BACKOFF_SEC", "1.0")))

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
#  DELL LLM CLIENT (original)
# ═══════════════════════════════════════

def _update_certifi_bundle() -> None:
    """Download Dell PKI certificates and append to certifi bundle (once)."""
    global _certifi_updated
    if _certifi_updated:
        return
    try:
        url = "https://pki.dell.com//Dell%20Technologies%20PKI%202018%20B64_PEM.zip"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        cert_path = certifi.where()
        dell_root_cert_name = "Dell Technologies Root Certificate Authority 2018.pem"
        dell_issuing_cert_name = "Dell Technologies Issuing CA 101_new.pem"

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            root_cert_content = z.read(dell_root_cert_name).decode("utf-8")
            issuing_cert_content = z.read(dell_issuing_cert_name).decode("utf-8")

            with open(cert_path, "a", encoding="utf-8") as bundle:
                bundle.write("\n")
                bundle.write(root_cert_content)
                bundle.write("\n")
                bundle.write(issuing_cert_content)
                bundle.write("\n")
        _certifi_updated = True
        print("[Dell LLM] PKI certificates updated successfully.")
    except Exception as e:
        print(f"[Dell LLM] Warning: Could not update certifi bundle: {e}")
        _certifi_updated = True  # Don't retry on failure


def _resolve_auth_mode() -> str:
    """Determine which authentication mode to use.
    
    Priority:
      1. USE_SSO=true → SSO (Dell browser login)
      2. CLIENT_ID + CLIENT_SECRET present → OAuth client_credentials
      3. ENABLE_TOKEN_REFRESH_AT_SERVER_SIDE=true → Basic auth (server refresh)
      4. Fall back to client-side token refresh (needs CLIENT_ID + CLIENT_SECRET)
      5. Default to SSO if nothing is configured
    """
    if _bool_env("USE_SSO", default=True):
        return "sso"
    if os.getenv("CLIENT_ID") and os.getenv("CLIENT_SECRET"):
        if _bool_env("ENABLE_TOKEN_REFRESH_AT_SERVER_SIDE"):
            return "basic"
        return "oauth"
    return "sso"  # Default to SSO


def _get_default_headers(auth_mode: str) -> dict[str, str]:
    """Get authentication headers for Dell AIA Gateway."""
    # Import local authentication_provider (copied from headless-code-fix-agent)
    import authentication_provider

    default_headers = {
        "x-correlation-id": str(uuid.uuid4()),
        "accept": "*/*",
        "Content-Type": "application/json",
    }

    if auth_mode == "sso":
        print("[Dell LLM] Authenticating via SSO (Dell browser login)...")
        auth = authentication_provider.AuthenticationProvider()
        auth.use_sso = True
        token = auth.generate_auth_token()
        default_headers["Authorization"] = "Bearer " + token
        print("[Dell LLM] SSO authentication successful.")
    elif auth_mode == "basic":
        print("[Dell LLM] Authenticating via Basic auth (server-side token refresh)...")
        auth = authentication_provider.AuthenticationProvider()
        default_headers["Authorization"] = "Basic " + auth.get_basic_credentials()
        print("[Dell LLM] Basic auth credentials set.")
    elif auth_mode == "oauth":
        print("[Dell LLM] Authenticating via OAuth client_credentials...")
        auth = authentication_provider.AuthenticationProvider()
        auth.use_sso = False
        token = auth.generate_auth_token()
        default_headers["Authorization"] = "Bearer " + token
        print("[Dell LLM] OAuth authentication successful.")

    return default_headers


def _get_dell_http_client(auth_mode: str) -> httpx.Client:
    """Get HTTP client with Dell certificate verification."""
    import authentication_provider

    _update_certifi_bundle()

    if auth_mode in ("sso", "basic", "oauth"):
        return httpx.Client(verify=certifi.where())
    else:
        auth = authentication_provider.AuthenticationProviderWithClientSideTokenRefresh()
        return httpx.Client(auth=auth, verify=certifi.where())


class DellLLMClient(BaseLLMClient):
    """Dell AIA Gateway LLM client with SSO/OAuth authentication."""

    def __init__(
        self,
        model: str = None,
        base_url: str = None,
        temperature: float = 0.7,
        max_tokens: int = 16000,
    ):
        model = model or os.getenv("DELL_LLM_MODEL", "gpt-oss-120b")
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)

        self.base_url = base_url or os.getenv(
            "DELL_LLM_BASE_URL", "https://aia.gateway.dell.com/genai/dev/v1"
        )
        self.is_reasoning_model = any(
            r in self.model.lower() for r in _REASONING_MODELS
        )
        self._json_mode_supported = not self.is_reasoning_model

        auth_mode = _resolve_auth_mode()
        print(f"[Dell LLM] Initializing: model={self.model}, "
              f"base_url={self.base_url}, auth_mode={auth_mode}")

        self.client = self._create_client(auth_mode)
        print(f"[Dell LLM] Client ready. Model: {self.model}")

    def _create_client(self, auth_mode: str = None) -> OpenAI:
        if auth_mode is None:
            auth_mode = _resolve_auth_mode()
        default_headers = _get_default_headers(auth_mode)
        http_client = _get_dell_http_client(auth_mode)
        return OpenAI(
            base_url=self.base_url,
            http_client=http_client,
            api_key="",
            default_headers=default_headers,
        )

    def _build_request_kwargs(self, messages, response_format=None):
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        if self.is_reasoning_model:
            kwargs["max_tokens"] = self.max_tokens
        else:
            kwargs["max_tokens"] = self.max_tokens
            kwargs["temperature"] = self.temperature
            if response_format:
                kwargs["response_format"] = response_format
        return kwargs

    def chat(self, messages):
        kwargs = self._build_request_kwargs(messages)
        response = self._execute_with_retry(kwargs)
        return self._extract_content(response, prefer_reasoning=self.is_reasoning_model)

    def chat_json(self, messages):
        if not self._json_mode_supported or self.is_reasoning_model:
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
            if self.is_reasoning_model and raw:
                raw = self._extract_json_from_text(raw)
            return raw

        kwargs = self._build_request_kwargs(
            messages, response_format={"type": "json_object"}
        )
        try:
            response = self._execute_with_retry(kwargs)
            return self._extract_content(response)
        except Exception as exc:
            err_msg = str(exc).lower()
            if "response_format" in err_msg or "json" in err_msg:
                self._json_mode_supported = False
                return self.chat(messages)
            raise

    def _extract_content(self, response, prefer_reasoning: bool = False) -> str:
        choice = response.choices[0]
        msg = choice.message

        content = (getattr(msg, "content", None) or "").strip()
        reasoning = (
            getattr(msg, "reasoning_content", None)
            or getattr(msg, "reasoning", None)
            or ""
        ).strip()

        print(f"[Dell LLM] Extract: content={len(content)} chars, reasoning={len(reasoning)} chars")

        if prefer_reasoning and reasoning and content:
            if len(reasoning) > len(content) * 1.5 and len(reasoning) > 200:
                return reasoning
            return content

        if not content and reasoning:
            return reasoning
        if not content and choice.finish_reason == "length":
            print("[Dell LLM] Warning: Model hit token limit with no content.")
        return content


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
    provider = (provider or os.getenv("LLM_PROVIDER", "dell")).lower().strip()
    print(f"[LLM] Creating client for provider: {provider}")

    if provider == "nvidia":
        return NvidiaLLMClient()
    elif provider == "ollama":
        return OllamaLLMClient()
    elif provider == "dell":
        return DellLLMClient()
    else:
        print(f"[LLM] Unknown provider '{provider}', falling back to dell")
        return DellLLMClient()


def get_llm_client() -> BaseLLMClient:
    """Get or create the singleton LLM client.

    On first call, this initializes the client for the configured provider.
    Subsequent calls reuse the same client unless switch_provider() is called.
    """
    global _client_instance, _current_provider
    desired = (os.getenv("LLM_PROVIDER") or "dell").lower().strip()

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
    return _current_provider or os.getenv("LLM_PROVIDER", "dell").lower().strip()


def get_available_providers() -> list[dict[str, str]]:
    """Return metadata about all available LLM providers."""
    return [
        {
            "id": "dell",
            "name": "Dell AIA Gateway",
            "description": "Dell enterprise LLM (gpt-oss-120b) via SSO/OAuth",
            "model": os.getenv("DELL_LLM_MODEL", "gpt-oss-120b"),
        },
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
