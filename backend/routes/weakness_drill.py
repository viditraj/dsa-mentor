"""Weakness-Targeted Problem Generator API routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import UserProfile, ProblemAttempt, Problem, LearningStats, RoadmapTopic
from agents import generate_weakness_drill

router = APIRouter()


@router.get("/{user_id}/analyze")
async def analyze_weaknesses(user_id: int, db: AsyncSession = Depends(get_db)):
    """Analyze user's attempt history to identify weak areas."""
    user = await db.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all attempts with problem info
    result = await db.execute(
        select(ProblemAttempt, Problem)
        .join(Problem, ProblemAttempt.problem_id == Problem.id)
        .where(ProblemAttempt.user_id == user_id)
        .order_by(ProblemAttempt.attempted_at.desc())
    )
    rows = result.all()

    # Analyze patterns
    pattern_stats = {}
    difficulty_stats = {"easy": {"solved": 0, "failed": 0, "avg_time": 0, "times": []},
                        "medium": {"solved": 0, "failed": 0, "avg_time": 0, "times": []},
                        "hard": {"solved": 0, "failed": 0, "avg_time": 0, "times": []}}
    topic_stats = {}

    for attempt, problem in rows:
        # Track by pattern
        for pattern in (problem.patterns or []):
            if pattern not in pattern_stats:
                pattern_stats[pattern] = {"solved": 0, "failed": 0, "hint_used": 0, "avg_time": 0, "times": [], "avg_rating": 0, "ratings": []}
            ps = pattern_stats[pattern]
            if attempt.status and attempt.status.value == "solved":
                ps["solved"] += 1
            else:
                ps["failed"] += 1
            if attempt.used_hint:
                ps["hint_used"] += 1
            if attempt.time_taken_minutes:
                ps["times"].append(attempt.time_taken_minutes)
            if attempt.self_rating:
                ps["ratings"].append(attempt.self_rating)

        # Track by difficulty
        diff = problem.difficulty.value if problem.difficulty else "medium"
        if diff in difficulty_stats:
            ds = difficulty_stats[diff]
            if attempt.status and attempt.status.value == "solved":
                ds["solved"] += 1
            else:
                ds["failed"] += 1
            if attempt.time_taken_minutes:
                ds["times"].append(attempt.time_taken_minutes)

        # Track by topic
        topic_id = problem.topic_id
        if topic_id not in topic_stats:
            topic_stats[topic_id] = {"solved": 0, "failed": 0, "topic_id": topic_id}
        ts = topic_stats[topic_id]
        if attempt.status and attempt.status.value == "solved":
            ts["solved"] += 1
        else:
            ts["failed"] += 1

    # Compute averages and weakness scores
    weak_patterns = []
    for pattern, stats in pattern_stats.items():
        total = stats["solved"] + stats["failed"]
        if total == 0:
            continue
        stats["avg_time"] = round(sum(stats["times"]) / len(stats["times"]), 1) if stats["times"] else 0
        stats["avg_rating"] = round(sum(stats["ratings"]) / len(stats["ratings"]), 1) if stats["ratings"] else 0
        success_rate = stats["solved"] / total if total > 0 else 0
        hint_rate = stats["hint_used"] / total if total > 0 else 0
        # Weakness score: lower success + higher hint usage + lower self-rating = weaker
        weakness_score = round((1 - success_rate) * 40 + hint_rate * 30 + (5 - stats["avg_rating"]) / 5 * 30, 1)
        weak_patterns.append({
            "pattern": pattern,
            "weakness_score": weakness_score,
            "success_rate": round(success_rate * 100, 1),
            "total_attempts": total,
            "hint_usage_rate": round(hint_rate * 100, 1),
            "avg_time_minutes": stats["avg_time"],
            "avg_self_rating": stats["avg_rating"],
        })

    # Sort by weakness score (highest = weakest)
    weak_patterns.sort(key=lambda x: x["weakness_score"], reverse=True)

    for diff, stats in difficulty_stats.items():
        stats["avg_time"] = round(sum(stats["times"]) / len(stats["times"]), 1) if stats["times"] else 0
        del stats["times"]

    return {
        "user_id": user_id,
        "weak_patterns": weak_patterns[:10],
        "difficulty_breakdown": difficulty_stats,
        "total_attempts": len(rows),
        "overall_solve_rate": round(sum(1 for a, _ in rows if a.status and a.status.value == "solved") / len(rows) * 100, 1) if rows else 0,
    }


class DrillRequest(BaseModel):
    user_id: int
    focus_pattern: Optional[str] = None
    difficulty: Optional[str] = None
    num_problems: int = 5


@router.post("/generate")
async def generate_drill(req: DrillRequest, db: AsyncSession = Depends(get_db)):
    """Generate a targeted drill session based on weaknesses."""
    user = await db.get(UserProfile, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get weakness analysis
    result = await db.execute(
        select(ProblemAttempt, Problem)
        .join(Problem, ProblemAttempt.problem_id == Problem.id)
        .where(ProblemAttempt.user_id == req.user_id)
    )
    rows = result.all()

    # Summarize attempt history for the AI
    attempt_summary = []
    for attempt, problem in rows[-50:]:  # Last 50 attempts
        attempt_summary.append({
            "problem": problem.title,
            "difficulty": problem.difficulty.value if problem.difficulty else "medium",
            "patterns": problem.patterns or [],
            "status": attempt.status.value if attempt.status else "attempted",
            "time_minutes": attempt.time_taken_minutes,
            "used_hint": attempt.used_hint,
            "rating": attempt.self_rating,
        })

    stats = await db.execute(select(LearningStats).where(LearningStats.user_id == req.user_id))
    stats_row = stats.scalar_one_or_none()

    drill = await generate_weakness_drill(
        experience_level=user.experience_level,
        attempt_history=attempt_summary,
        weak_areas=stats_row.weak_areas if stats_row else [],
        strong_areas=stats_row.strong_areas if stats_row else [],
        focus_pattern=req.focus_pattern,
        difficulty=req.difficulty,
        num_problems=req.num_problems,
        language=user.preferred_language,
    )

    return drill
