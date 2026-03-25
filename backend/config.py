"""Application configuration."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "DSA Mentor"
    DATABASE_URL: str = "sqlite+aiosqlite:///./dsa_mentor.db"
    DAILY_PROBLEMS_COUNT: int = 3
    MAX_DAILY_CONCEPTS: int = 2

    # LLM provider: "dell", "nvidia", or "ollama"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "dell")

    # Dell
    DELL_LLM_MODEL: str = os.getenv("DELL_LLM_MODEL", "gpt-oss-120b")
    DELL_LLM_BASE_URL: str = os.getenv("DELL_LLM_BASE_URL", "https://aia.gateway.dell.com/genai/dev/v1")

    # NVIDIA NIM
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "deepseek-ai/deepseek-v3.2")
    NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    NVIDIA_ENABLE_THINKING: bool = os.getenv("NVIDIA_ENABLE_THINKING", "true").lower() == "true"

    # Ollama (local)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
