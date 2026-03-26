"""Problem Similarity Engine API routes."""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Problem, ProblemAttempt
from agents import find_similar_problems, generate_pattern_evolution
from pattern_engine import PATTERN_CATALOG

router = APIRouter()


@router.get("/similar/{problem_id}")
async def get_similar_problems(
    problem_id: int,
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
):
    """Find problems similar to the given problem based on patterns."""
    problem = await db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Get all other problems
    result = await db.execute(select(Problem).where(Problem.id != problem_id))
    all_problems = result.scalars().all()

    # Score similarity based on shared patterns and difficulty proximity
    scored = []
    target_patterns = set(problem.patterns or [])
    diff_order = {"easy": 1, "medium": 2, "hard": 3}
    target_diff = diff_order.get(problem.difficulty.value if problem.difficulty else "medium", 2)

    for p in all_problems:
        p_patterns = set(p.patterns or [])
        shared = target_patterns & p_patterns
        if not shared:
            continue
        pattern_score = len(shared) / max(len(target_patterns | p_patterns), 1)
        p_diff = diff_order.get(p.difficulty.value if p.difficulty else "medium", 2)
        diff_score = 1.0 - abs(target_diff - p_diff) / 3.0
        similarity = round(pattern_score * 0.7 + diff_score * 0.3, 3)
        scored.append({
            "problem_id": p.id,
            "title": p.title,
            "leetcode_number": p.leetcode_number,
            "difficulty": p.difficulty.value if p.difficulty else "medium",
            "patterns": p.patterns or [],
            "shared_patterns": list(shared),
            "similarity_score": similarity,
        })

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {
        "source_problem": {
            "id": problem.id,
            "title": problem.title,
            "patterns": problem.patterns or [],
            "difficulty": problem.difficulty.value if problem.difficulty else "medium",
        },
        "similar_problems": scored[:limit],
    }


@router.get("/pattern-family/{pattern_key}")
async def get_pattern_family(
    pattern_key: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all problems in a pattern family, ordered by difficulty progression."""
    pattern = PATTERN_CATALOG.get(pattern_key)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_key}' not found")

    result = await db.execute(select(Problem))
    all_problems = result.scalars().all()

    family = []
    for p in all_problems:
        if pattern_key in (p.patterns or []):
            family.append({
                "id": p.id,
                "title": p.title,
                "leetcode_number": p.leetcode_number,
                "difficulty": p.difficulty.value if p.difficulty else "medium",
                "patterns": p.patterns or [],
            })

    diff_order = {"easy": 0, "medium": 1, "hard": 2}
    family.sort(key=lambda x: diff_order.get(x["difficulty"], 1))

    return {
        "pattern_key": pattern_key,
        "pattern_name": pattern.get("name", pattern_key),
        "description": pattern.get("description", ""),
        "problems": family,
        "total": len(family),
        "difficulty_distribution": {
            "easy": sum(1 for p in family if p["difficulty"] == "easy"),
            "medium": sum(1 for p in family if p["difficulty"] == "medium"),
            "hard": sum(1 for p in family if p["difficulty"] == "hard"),
        },
    }


@router.get("/evolution/{problem_id}")
async def get_pattern_evolution(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the pattern evolution chain - how this problem relates to easier/harder variants."""
    problem = await db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    evolution = await generate_pattern_evolution(
        problem_title=problem.title,
        problem_patterns=problem.patterns or [],
        difficulty=problem.difficulty.value if problem.difficulty else "medium",
    )
    return evolution


@router.get("/{user_id}/recommendations")
async def get_recommendations(
    user_id: int,
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
):
    """Get 'If you liked this, try these' recommendations based on solved problems."""
    # Get user's recently solved problems
    result = await db.execute(
        select(ProblemAttempt, Problem)
        .join(Problem, ProblemAttempt.problem_id == Problem.id)
        .where(ProblemAttempt.user_id == user_id)
        .where(ProblemAttempt.status == "solved")
        .order_by(ProblemAttempt.attempted_at.desc())
        .limit(10)
    )
    recent_solved = result.all()

    if not recent_solved:
        return {"recommendations": [], "message": "Solve some problems first to get recommendations!"}

    # Collect patterns from solved problems
    solved_ids = set()
    pattern_freq = {}
    for attempt, problem in recent_solved:
        solved_ids.add(problem.id)
        for p in (problem.patterns or []):
            pattern_freq[p] = pattern_freq.get(p, 0) + 1

    # Find unsolved problems that match frequent patterns
    all_result = await db.execute(select(Problem))
    all_problems = all_result.scalars().all()

    recommendations = []
    for p in all_problems:
        if p.id in solved_ids:
            continue
        score = sum(pattern_freq.get(pat, 0) for pat in (p.patterns or []))
        if score > 0:
            recommendations.append({
                "problem_id": p.id,
                "title": p.title,
                "leetcode_number": p.leetcode_number,
                "difficulty": p.difficulty.value if p.difficulty else "medium",
                "patterns": p.patterns or [],
                "relevance_score": score,
                "reason": f"Uses patterns you've been practicing: {', '.join(pat for pat in (p.patterns or []) if pat in pattern_freq)}",
            })

    recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)

    return {
        "recommendations": recommendations[:limit],
        "based_on_patterns": sorted(pattern_freq.keys(), key=lambda k: pattern_freq[k], reverse=True)[:5],
    }
