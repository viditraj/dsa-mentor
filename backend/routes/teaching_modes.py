"""ELI5 + Socratic Teaching Modes API routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from agents import teach_eli5, teach_socratic

router = APIRouter()


class ELI5Request(BaseModel):
    topic: str
    subtopic: Optional[str] = None
    context: Optional[str] = None  # what the user already knows


class SocraticRequest(BaseModel):
    topic: str
    current_understanding: Optional[str] = None  # what user thinks they know
    previous_answers: list[dict] = []  # [{question, answer}] conversation so far


@router.post("/eli5")
async def explain_like_five(req: ELI5Request):
    """Explain a DSA concept with zero jargon, using everyday analogies."""
    result = await teach_eli5(
        topic=req.topic,
        subtopic=req.subtopic,
        context=req.context,
    )
    return result


@router.post("/socratic")
async def socratic_method(req: SocraticRequest):
    """Guide learning through questions instead of answers."""
    result = await teach_socratic(
        topic=req.topic,
        current_understanding=req.current_understanding,
        previous_answers=req.previous_answers,
    )
    return result
