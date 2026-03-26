"""Mock Interview Simulator API routes."""
import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import UserProfile, ProblemAttempt, LearningStats, MockInterviewSession
from agents import (
    start_mock_interview,
    interview_respond,
    score_mock_interview,
)

router = APIRouter()


class StartInterviewRequest(BaseModel):
    user_id: int
    difficulty: str = "medium"  # easy, medium, hard, mixed
    focus_area: Optional[str] = None  # e.g. "arrays", "trees", "dp"
    duration_minutes: int = 45
    company_style: Optional[str] = None  # google, meta, amazon, etc.


class InterviewMessageRequest(BaseModel):
    session_id: int
    message: str
    code: Optional[str] = None


@router.post("/start")
async def start_interview(req: StartInterviewRequest, db: AsyncSession = Depends(get_db)):
    """Start a new mock interview session."""
    user = await db.get(UserProfile, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user's weak areas for targeted questions
    stats = await db.execute(select(LearningStats).where(LearningStats.user_id == req.user_id))
    stats = stats.scalar_one_or_none()
    weak_areas = stats.weak_areas if stats else []

    interview_data = await start_mock_interview(
        experience_level=user.experience_level,
        difficulty=req.difficulty,
        focus_area=req.focus_area,
        weak_areas=weak_areas,
        company_style=req.company_style,
        language=user.preferred_language,
        duration_minutes=req.duration_minutes,
    )

    # Save session
    session = MockInterviewSession(
        user_id=req.user_id,
        difficulty=req.difficulty,
        focus_area=req.focus_area,
        company_style=req.company_style,
        duration_minutes=req.duration_minutes,
        problem_title=interview_data.get("problem_title", "Mock Problem"),
        problem_description=interview_data.get("problem_description", ""),
        conversation=[ {"role": "interviewer", "content": interview_data.get("opening_message", "")} ],
        status="in_progress",
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "session_id": session.id,
        "problem_title": interview_data.get("problem_title"),
        "problem_description": interview_data.get("problem_description"),
        "opening_message": interview_data.get("opening_message"),
        "hints_available": interview_data.get("hints_available", 3),
        "expected_patterns": interview_data.get("expected_patterns", []),
        "difficulty": req.difficulty,
        "duration_minutes": req.duration_minutes,
        "started_at": session.started_at.isoformat() if session.started_at else None,
    }


@router.post("/respond")
async def respond_to_interview(req: InterviewMessageRequest, db: AsyncSession = Depends(get_db)):
    """Send a message/code in the mock interview and get interviewer response."""
    session = await db.get(MockInterviewSession, req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail="Interview is not in progress")

    # Add user message to conversation
    conversation = session.conversation or []
    user_msg = {"role": "candidate", "content": req.message}
    if req.code:
        user_msg["code"] = req.code
    conversation.append(user_msg)

    # Get interviewer response
    response = await interview_respond(
        conversation=conversation,
        problem_title=session.problem_title,
        problem_description=session.problem_description,
        candidate_code=req.code,
    )

    # Add interviewer response to conversation
    conversation.append({"role": "interviewer", "content": response.get("message", "")})
    session.conversation = conversation
    await db.commit()

    return {
        "message": response.get("message"),
        "hint": response.get("hint"),
        "follow_up": response.get("follow_up"),
        "assessment_so_far": response.get("assessment_so_far"),
        "phase": response.get("phase", "discussion"),
    }


@router.post("/{session_id}/end")
async def end_interview(session_id: int, db: AsyncSession = Depends(get_db)):
    """End the interview and get final scoring."""
    session = await db.get(MockInterviewSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    # Score the interview
    scoring = await score_mock_interview(
        conversation=session.conversation or [],
        problem_title=session.problem_title,
        problem_description=session.problem_description,
        difficulty=session.difficulty,
    )

    session.status = "completed"
    session.ended_at = datetime.datetime.utcnow()
    session.score = scoring.get("overall_score", 0)
    session.feedback = scoring
    await db.commit()

    return {
        "session_id": session.id,
        "overall_score": scoring.get("overall_score"),
        "communication_score": scoring.get("communication_score"),
        "problem_solving_score": scoring.get("problem_solving_score"),
        "code_quality_score": scoring.get("code_quality_score"),
        "time_management_score": scoring.get("time_management_score"),
        "strengths": scoring.get("strengths", []),
        "improvements": scoring.get("improvements", []),
        "detailed_feedback": scoring.get("detailed_feedback"),
        "hire_recommendation": scoring.get("hire_recommendation"),
    }


@router.get("/{user_id}/history")
async def get_interview_history(user_id: int, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Get user's mock interview history."""
    result = await db.execute(
        select(MockInterviewSession)
        .where(MockInterviewSession.user_id == user_id)
        .order_by(MockInterviewSession.started_at.desc())
        .limit(limit)
    )
    sessions = result.scalars().all()

    return {
        "sessions": [
            {
                "id": s.id,
                "difficulty": s.difficulty,
                "focus_area": s.focus_area,
                "company_style": s.company_style,
                "problem_title": s.problem_title,
                "status": s.status,
                "score": s.score,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            }
            for s in sessions
        ],
        "total": len(sessions),
    }
