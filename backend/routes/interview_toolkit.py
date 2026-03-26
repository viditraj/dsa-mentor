"""Interview Day Toolkit API routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import UserProfile, LearningStats, ProblemAttempt, Problem
from agents import (
    generate_pattern_quiz,
    generate_cheat_sheet,
    generate_warmup_session,
    generate_company_focus,
)

router = APIRouter()


@router.get("/{user_id}/quiz")
async def get_pattern_quiz(
    user_id: int,
    num_questions: int = 10,
    time_per_question: int = 30,
    db: AsyncSession = Depends(get_db),
):
    """Generate a quick-fire pattern recognition quiz."""
    user = await db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stats = await db.execute(select(LearningStats).where(LearningStats.user_id == user_id))
    stats = stats.scalar_one_or_none()

    quiz = await generate_pattern_quiz(
        experience_level=user.experience_level,
        weak_areas=stats.weak_areas if stats else [],
        num_questions=num_questions,
        time_per_question=time_per_question,
    )
    return quiz


class QuizAnswerRequest(BaseModel):
    answers: list[dict]  # [{question_index, selected_pattern, time_taken_seconds}]


@router.post("/{user_id}/quiz/score")
async def score_quiz(user_id: int, req: QuizAnswerRequest, db: AsyncSession = Depends(get_db)):
    """Score a pattern recognition quiz."""
    correct = 0
    results = []
    for ans in req.answers:
        is_correct = ans.get("selected_pattern", "").lower() == ans.get("correct_pattern", "").lower()
        if is_correct:
            correct += 1
        results.append({
            "question_index": ans.get("question_index", 0),
            "selected": ans.get("selected_pattern"),
            "correct": ans.get("correct_pattern"),
            "is_correct": is_correct,
            "time_taken": ans.get("time_taken_seconds", 0),
        })

    total = len(req.answers)
    return {
        "total": total,
        "correct": correct,
        "score_percent": round(correct / total * 100, 1) if total > 0 else 0,
        "results": results,
        "speed_avg": round(sum(r["time_taken"] for r in results) / total, 1) if total > 0 else 0,
    }


@router.get("/{user_id}/cheat-sheet")
async def get_cheat_sheet(
    user_id: int,
    focus: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Generate a condensed 1-page cheat sheet of weak areas."""
    user = await db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stats = await db.execute(select(LearningStats).where(LearningStats.user_id == user_id))
    stats = stats.scalar_one_or_none()

    cheat_sheet = await generate_cheat_sheet(
        experience_level=user.experience_level,
        weak_areas=stats.weak_areas if stats else [],
        strong_areas=stats.strong_areas if stats else [],
        focus=focus,
    )
    return cheat_sheet


@router.get("/{user_id}/warmup")
async def get_warmup(user_id: int, db: AsyncSession = Depends(get_db)):
    """Generate a quick warm-up session (2 easy problems to get in flow state)."""
    user = await db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    warmup = await generate_warmup_session(
        experience_level=user.experience_level,
        language=user.preferred_language,
    )
    return warmup


@router.get("/{user_id}/company-focus")
async def get_company_focus(
    user_id: int,
    company: str = "google",
    db: AsyncSession = Depends(get_db),
):
    """Get company-specific interview focus areas and tips."""
    user = await db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stats = await db.execute(select(LearningStats).where(LearningStats.user_id == user_id))
    stats = stats.scalar_one_or_none()

    focus = await generate_company_focus(
        company=company,
        experience_level=user.experience_level,
        weak_areas=stats.weak_areas if stats else [],
        strong_areas=stats.strong_areas if stats else [],
    )
    return focus
