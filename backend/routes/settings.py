"""Settings API routes — LLM provider management."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from llm_client import (
    get_available_providers,
    get_current_provider,
    switch_provider,
    get_llm_client,
)

router = APIRouter()


class SwitchProviderRequest(BaseModel):
    provider: str


@router.get("/providers")
async def list_providers():
    """List all available LLM providers and which one is active."""
    providers = get_available_providers()
    current = get_current_provider()
    return {
        "providers": providers,
        "active": current,
    }


@router.post("/provider")
async def set_provider(req: SwitchProviderRequest):
    """Switch the active LLM provider at runtime."""
    valid_ids = {p["id"] for p in get_available_providers()}
    if req.provider not in valid_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider '{req.provider}'. Valid: {sorted(valid_ids)}",
        )
    try:
        client = switch_provider(req.provider)
        return {
            "status": "ok",
            "active": req.provider,
            "model": client.model,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/provider/test")
async def test_provider():
    """Quick test: send a trivial prompt to the active LLM and return the response."""
    import asyncio

    try:
        client = get_llm_client()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."},
        ]
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, client.chat, messages)
        return {
            "status": "ok",
            "provider": get_current_provider(),
            "model": client.model,
            "response": result[:500],
        }
    except Exception as e:
        return {
            "status": "error",
            "provider": get_current_provider(),
            "error": str(e),
        }
