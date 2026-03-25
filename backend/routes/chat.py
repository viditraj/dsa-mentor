"""Chat routes - AI mentor interaction."""
from fastapi import APIRouter
from schemas import ChatMessage, ChatResponse
from agents import chat_with_mentor

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the DSA mentor AI."""
    result = await chat_with_mentor(message.message, message.context)
    return ChatResponse(**result)
