"""Problem routes - practice problems and solution submission."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import Problem, ProblemAttempt, RoadmapTopic, LearningStats, ProblemStatus
from schemas import ProblemResponse, ProblemAttemptCreate, ProblemAttemptResponse
from agents import review_solution, get_progressive_hint, solve_problem_with_ai
from leetcode_descriptions import LOCAL_DESCRIPTIONS, fetch_leetcode_description

router = APIRouter()


def _is_placeholder(desc: str) -> bool:
    """Check if description is a placeholder."""
    return not desc or desc.startswith("Solve:") or len(desc) < 30


@router.get("/topic/{topic_id}", response_model=list[ProblemResponse])
async def get_problems_for_topic(topic_id: int, db: AsyncSession = Depends(get_db)):
    """Get all problems for a specific topic, enriching descriptions if missing."""
    result = await db.execute(
        select(Problem).where(Problem.topic_id == topic_id)
    )
    problems = list(result.scalars().all())

    # Enrich any placeholder descriptions
    updated = False
    for problem in problems:
        if _is_placeholder(problem.description):
            desc = LOCAL_DESCRIPTIONS.get(problem.leetcode_number) or LOCAL_DESCRIPTIONS.get(problem.title)
            if not desc:
                desc = await fetch_leetcode_description(problem.title, problem.leetcode_number)
            if desc:
                problem.description = desc
                updated = True
    if updated:
        await db.commit()

    return problems


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific problem by ID, enriching description if missing."""
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Enrich placeholder description
    if _is_placeholder(problem.description):
        desc = LOCAL_DESCRIPTIONS.get(problem.leetcode_number) or LOCAL_DESCRIPTIONS.get(problem.title)
        if not desc:
            desc = await fetch_leetcode_description(problem.title, problem.leetcode_number)
        if desc:
            problem.description = desc
            await db.commit()

    return problem


@router.post("/{problem_id}/submit")
async def submit_solution(
    problem_id: int,
    attempt: ProblemAttemptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit a solution for code review and feedback."""
    # Get the problem
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Get AI review if code is provided
    ai_feedback = None
    if attempt.code:
        review = await review_solution(
            problem_title=problem.title,
            code=attempt.code,
            language=attempt.language,
            time_taken=attempt.time_taken_minutes
        )
        ai_feedback = review.get("summary", "")
        if review.get("improvements"):
            ai_feedback += "\n\nImprovements:\n" + "\n".join(f"• {imp}" for imp in review["improvements"])
        if review.get("edge_cases"):
            ai_feedback += "\n\nEdge cases to consider:\n" + "\n".join(f"• {ec}" for ec in review["edge_cases"])

    # Save the attempt
    db_attempt = ProblemAttempt(
        user_id=attempt.user_id,
        problem_id=problem_id,
        status=ProblemStatus(attempt.status),
        code=attempt.code,
        language=attempt.language,
        time_taken_minutes=attempt.time_taken_minutes,
        used_hint=attempt.used_hint,
        self_rating=attempt.self_rating,
        ai_feedback=ai_feedback,
    )
    db.add(db_attempt)

    # Update learning stats
    stats_result = await db.execute(
        select(LearningStats).where(LearningStats.user_id == attempt.user_id)
    )
    stats = stats_result.scalar_one_or_none()
    if stats and attempt.status == "solved":
        stats.total_problems_solved += 1
        if problem.difficulty.value == "easy":
            stats.easy_solved += 1
        elif problem.difficulty.value == "medium":
            stats.medium_solved += 1
        elif problem.difficulty.value == "hard":
            stats.hard_solved += 1

        # Update XP
        xp_map = {"easy": 10, "medium": 25, "hard": 50}
        stats.xp_points += xp_map.get(problem.difficulty.value, 10)
        stats.level = stats.xp_points // 100 + 1

        # Update streak
        stats.current_streak += 1
        stats.max_streak = max(stats.max_streak, stats.current_streak)

    await db.commit()
    await db.refresh(db_attempt)

    return {
        "attempt_id": db_attempt.id,
        "ai_feedback": ai_feedback,
        "review": review if attempt.code else None
    }


@router.get("/{user_id}/attempts/{problem_id}", response_model=list[ProblemAttemptResponse])
async def get_attempts(user_id: int, problem_id: int, db: AsyncSession = Depends(get_db)):
    """Get all attempts for a specific problem by a user."""
    result = await db.execute(
        select(ProblemAttempt)
        .where(
            ProblemAttempt.user_id == user_id,
            ProblemAttempt.problem_id == problem_id,
        )
        .order_by(ProblemAttempt.attempted_at.desc())
    )
    return result.scalars().all()


@router.post("/{problem_id}/hint")
async def get_hint(problem_id: int, hint_level: int = 1, db: AsyncSession = Depends(get_db)):
    """Get a progressive hint for a problem."""
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    hint = await get_progressive_hint(
        problem_title=problem.title,
        problem_description=problem.description or problem.title,
        hint_level=min(3, max(1, hint_level))
    )
    return hint


@router.post("/{problem_id}/ai-solve")
async def ai_solve(problem_id: int, db: AsyncSession = Depends(get_db)):
    """Get a complete AI walkthrough for solving a problem."""
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    solution = await solve_problem_with_ai(
        problem_title=problem.title,
        problem_description=problem.description or problem.title,
        difficulty=problem.difficulty.value if hasattr(problem.difficulty, 'value') else problem.difficulty,
        patterns=problem.patterns or [],
    )
    return solution
