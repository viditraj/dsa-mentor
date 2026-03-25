"""FAANG Prep routes — crash course API endpoints."""
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import FAANGProgress, PatternMastery, UserProfile
from schemas import FAANGQuestionSubmit
from agents import teach_pattern_story, get_faang_question_walkthrough
from faang_questions import (
    FAANG_PATTERNS, FAANG_QUESTIONS, FAANG_PHASES, MILESTONES, MOTIVATION_QUOTES,
    get_questions_by_pattern, get_questions_by_phase, get_question_by_id,
    get_pattern_info, get_readiness_score,
)

router = APIRouter()


# ── Overview ──────────────────────────────

@router.get("/faang-prep/overview")
async def get_overview():
    """Get the full FAANG 75 curriculum overview (patterns, phases, questions)."""
    phases = {}
    for phase_num, phase_info in FAANG_PHASES.items():
        patterns_in_phase = []
        for pk in phase_info["patterns"]:
            p = FAANG_PATTERNS[pk]
            qs = get_questions_by_pattern(pk)
            patterns_in_phase.append({
                "key": pk,
                "name": p["name"],
                "emoji": p["emoji"],
                "difficulty": p["difficulty"],
                "estimated_hours": p["estimated_hours"],
                "story_preview": p["story"][:120] + "...",
                "intuition": p["intuition"],
                "complexity": p["complexity"],
                "question_count": len(qs),
            })
        phases[phase_num] = {
            **phase_info,
            "patterns_detail": patterns_in_phase,
            "total_questions": len(get_questions_by_phase(phase_num)),
        }

    return {
        "total_questions": len(FAANG_QUESTIONS),
        "total_patterns": len(FAANG_PATTERNS),
        "total_phases": len(FAANG_PHASES),
        "phases": phases,
        "milestones": MILESTONES,
    }


# ── User Progress ────────────────────────

@router.get("/faang-prep/{user_id}/progress")
async def get_user_progress(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a user's full FAANG 75 progress with readiness score."""
    # Get all progress records
    result = await db.execute(
        select(FAANGProgress).where(FAANGProgress.user_id == user_id)
    )
    progress_records = result.scalars().all()

    solved_ids = [p.question_id for p in progress_records if p.status == "solved"]
    attempted_ids = [p.question_id for p in progress_records if p.status == "attempted"]

    readiness = get_readiness_score(solved_ids)

    # Get pattern mastery records
    mastery_result = await db.execute(
        select(PatternMastery).where(PatternMastery.user_id == user_id)
    )
    mastery_records = {m.pattern_key: m for m in mastery_result.scalars().all()}

    # Build per-question progress map
    question_progress = {}
    for p in progress_records:
        question_progress[p.question_id] = {
            "status": p.status,
            "confidence": p.confidence,
            "time_taken_minutes": p.time_taken_minutes,
            "solved_at": p.solved_at.isoformat() if p.solved_at else None,
        }

    # Build per-pattern mastery
    pattern_mastery = {}
    for pk in FAANG_PATTERNS:
        if pk in mastery_records:
            m = mastery_records[pk]
            pattern_mastery[pk] = {
                "problems_solved": m.problems_solved,
                "problems_total": m.problems_total,
                "avg_confidence": m.avg_confidence,
                "mastery_level": m.mastery_level,
                "story_read": m.story_read,
                "template_practiced": m.template_practiced,
            }
        else:
            qs = get_questions_by_pattern(pk)
            pattern_mastery[pk] = {
                "problems_solved": 0,
                "problems_total": len(qs),
                "avg_confidence": 0,
                "mastery_level": "locked",
                "story_read": False,
                "template_practiced": False,
            }

    # Pick a motivational quote
    import random
    if len(solved_ids) == 0:
        ctx = "starting"
    elif len(solved_ids) < 10:
        ctx = "practice"
    elif len(solved_ids) < 38:
        ctx = "progress"
    else:
        ctx = "faang"
    context_quotes = [q for q in MOTIVATION_QUOTES if q["context"] == ctx]
    quote = random.choice(context_quotes) if context_quotes else random.choice(MOTIVATION_QUOTES)

    return {
        **readiness,
        "solved_ids": solved_ids,
        "attempted_ids": attempted_ids,
        "question_progress": question_progress,
        "pattern_mastery": pattern_mastery,
        "motivation_quote": quote,
    }


# ── Questions ────────────────────────────

@router.get("/faang-prep/questions")
async def get_all_questions():
    """Get all 75 FAANG questions."""
    return {"questions": FAANG_QUESTIONS, "total": len(FAANG_QUESTIONS)}


@router.get("/faang-prep/questions/pattern/{pattern_key}")
async def get_pattern_questions(pattern_key: str):
    """Get questions for a specific pattern."""
    if pattern_key not in FAANG_PATTERNS:
        raise HTTPException(status_code=404, detail="Pattern not found")
    questions = get_questions_by_pattern(pattern_key)
    pattern = FAANG_PATTERNS[pattern_key]
    return {
        "pattern": pattern,
        "questions": questions,
    }


@router.get("/faang-prep/questions/phase/{phase}")
async def get_phase_questions(phase: int):
    """Get questions for a specific phase."""
    if phase not in FAANG_PHASES:
        raise HTTPException(status_code=404, detail="Phase not found")
    questions = get_questions_by_phase(phase)
    return {
        "phase": FAANG_PHASES[phase],
        "questions": questions,
    }


@router.get("/faang-prep/question/{question_id}")
async def get_question_detail(question_id: int):
    """Get a specific question with its pattern info."""
    question = get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    pattern = FAANG_PATTERNS.get(question["pattern"], {})
    return {
        "question": question,
        "pattern": pattern,
    }


# ── Pattern Teaching ─────────────────────

@router.get("/faang-prep/pattern/{pattern_key}")
async def get_pattern_detail(pattern_key: str):
    """Get full pattern info (story, template, when-to-use)."""
    if pattern_key not in FAANG_PATTERNS:
        raise HTTPException(status_code=404, detail="Pattern not found")
    pattern = FAANG_PATTERNS[pattern_key]
    questions = get_questions_by_pattern(pattern_key)
    return {
        "pattern": pattern,
        "questions": questions,
    }


@router.get("/faang-prep/pattern/{pattern_key}/story")
async def get_pattern_story(pattern_key: str, language: str = "python"):
    """Get an AI-generated story-based lesson for a pattern."""
    if pattern_key not in FAANG_PATTERNS:
        raise HTTPException(status_code=404, detail="Pattern not found")
    pattern = FAANG_PATTERNS[pattern_key]
    story = await teach_pattern_story(pattern_key, pattern, language)
    return story


@router.get("/faang-prep/question/{question_id}/walkthrough")
async def get_question_walkthrough(question_id: int, language: str = "python"):
    """Get an AI-generated interview-style walkthrough for a question."""
    question = get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    walkthrough = await get_faang_question_walkthrough(question, language)
    return walkthrough


# ── Submit / Track Progress ──────────────

@router.post("/faang-prep/submit")
async def submit_question(data: FAANGQuestionSubmit, db: AsyncSession = Depends(get_db)):
    """Mark a FAANG 75 question as solved/attempted."""
    question = get_question_by_id(data.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check for existing progress record
    result = await db.execute(
        select(FAANGProgress).where(
            FAANGProgress.user_id == data.user_id,
            FAANGProgress.question_id == data.question_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.status = data.status
        existing.code = data.code
        existing.language = data.language
        existing.time_taken_minutes = data.time_taken_minutes
        existing.confidence = data.confidence
        if data.status == "solved":
            existing.solved_at = datetime.datetime.utcnow()
    else:
        progress = FAANGProgress(
            user_id=data.user_id,
            question_id=data.question_id,
            pattern_key=question["pattern"],
            status=data.status,
            code=data.code,
            language=data.language,
            time_taken_minutes=data.time_taken_minutes,
            confidence=data.confidence,
            solved_at=datetime.datetime.utcnow() if data.status == "solved" else None,
        )
        db.add(progress)

    # Update pattern mastery
    pattern_key = question["pattern"]
    mastery_result = await db.execute(
        select(PatternMastery).where(
            PatternMastery.user_id == data.user_id,
            PatternMastery.pattern_key == pattern_key,
        )
    )
    mastery = mastery_result.scalar_one_or_none()

    pattern_qs = get_questions_by_pattern(pattern_key)
    total_in_pattern = len(pattern_qs)

    if not mastery:
        mastery = PatternMastery(
            user_id=data.user_id,
            pattern_key=pattern_key,
            problems_total=total_in_pattern,
        )
        db.add(mastery)

    # Recalculate mastery stats
    all_progress = await db.execute(
        select(FAANGProgress).where(
            FAANGProgress.user_id == data.user_id,
            FAANGProgress.pattern_key == pattern_key,
            FAANGProgress.status == "solved",
        )
    )
    solved_in_pattern = all_progress.scalars().all()
    mastery.problems_solved = len(solved_in_pattern)
    mastery.problems_total = total_in_pattern

    if solved_in_pattern:
        confidences = [p.confidence for p in solved_in_pattern if p.confidence]
        times = [p.time_taken_minutes for p in solved_in_pattern if p.time_taken_minutes]
        mastery.avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        mastery.avg_time_minutes = sum(times) / len(times) if times else 0

    mastery.last_practiced = datetime.datetime.utcnow()

    # Determine mastery level
    pct = mastery.problems_solved / mastery.problems_total if mastery.problems_total else 0
    if pct >= 1.0 and mastery.avg_confidence >= 4:
        mastery.mastery_level = "mastered"
    elif pct >= 0.6:
        mastery.mastery_level = "practiced"
    elif pct > 0:
        mastery.mastery_level = "learning"
    else:
        mastery.mastery_level = "locked"

    await db.commit()

    # Return updated readiness
    all_solved = await db.execute(
        select(FAANGProgress.question_id).where(
            FAANGProgress.user_id == data.user_id,
            FAANGProgress.status == "solved",
        )
    )
    solved_ids = [r[0] for r in all_solved.all()]
    readiness = get_readiness_score(solved_ids)

    return {
        "success": True,
        "question_id": data.question_id,
        "status": data.status,
        **readiness,
    }


@router.post("/faang-prep/{user_id}/pattern/{pattern_key}/mark-story-read")
async def mark_story_read(user_id: int, pattern_key: str, db: AsyncSession = Depends(get_db)):
    """Mark a pattern story as read."""
    if pattern_key not in FAANG_PATTERNS:
        raise HTTPException(status_code=404, detail="Pattern not found")

    result = await db.execute(
        select(PatternMastery).where(
            PatternMastery.user_id == user_id,
            PatternMastery.pattern_key == pattern_key,
        )
    )
    mastery = result.scalar_one_or_none()

    if not mastery:
        mastery = PatternMastery(
            user_id=user_id,
            pattern_key=pattern_key,
            problems_total=len(get_questions_by_pattern(pattern_key)),
            story_read=True,
            mastery_level="learning",
        )
        db.add(mastery)
    else:
        mastery.story_read = True
        if mastery.mastery_level == "locked":
            mastery.mastery_level = "learning"

    await db.commit()
    return {"success": True, "pattern_key": pattern_key, "story_read": True}


@router.post("/faang-prep/{user_id}/pattern/{pattern_key}/mark-template-practiced")
async def mark_template_practiced(user_id: int, pattern_key: str, db: AsyncSession = Depends(get_db)):
    """Mark a pattern template as practiced."""
    if pattern_key not in FAANG_PATTERNS:
        raise HTTPException(status_code=404, detail="Pattern not found")

    result = await db.execute(
        select(PatternMastery).where(
            PatternMastery.user_id == user_id,
            PatternMastery.pattern_key == pattern_key,
        )
    )
    mastery = result.scalar_one_or_none()

    if not mastery:
        mastery = PatternMastery(
            user_id=user_id,
            pattern_key=pattern_key,
            problems_total=len(get_questions_by_pattern(pattern_key)),
            template_practiced=True,
            mastery_level="learning",
        )
        db.add(mastery)
    else:
        mastery.template_practiced = True
        if mastery.mastery_level == "locked":
            mastery.mastery_level = "learning"

    await db.commit()
    return {"success": True, "pattern_key": pattern_key, "template_practiced": True}


# ── Motivation & Milestones ──────────────

@router.get("/faang-prep/{user_id}/milestones")
async def get_milestones(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all milestones with earned status for a user."""
    result = await db.execute(
        select(FAANGProgress.question_id).where(
            FAANGProgress.user_id == user_id,
            FAANGProgress.status == "solved",
        )
    )
    solved_ids = [r[0] for r in result.all()]
    readiness = get_readiness_score(solved_ids)

    return {
        "milestones": MILESTONES,
        "earned": readiness["milestones_earned"],
        "total_solved": len(solved_ids),
    }


@router.get("/faang-prep/motivation")
async def get_motivation(context: str = "progress"):
    """Get a motivational quote for the user's current context."""
    import random
    context_quotes = [q for q in MOTIVATION_QUOTES if q["context"] == context]
    if context_quotes:
        return random.choice(context_quotes)
    return random.choice(MOTIVATION_QUOTES)
