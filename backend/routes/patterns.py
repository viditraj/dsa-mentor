"""Pattern recognition & code execution routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Problem
from pattern_engine import (
    get_all_patterns, get_pattern_for_problem,
    match_patterns_to_problem, PATTERNS
)
from agents import analyze_code_pattern, generate_test_cases

router = APIRouter(prefix="/patterns", tags=["patterns"])


class CodeAnalysisRequest(BaseModel):
    problem_title: str
    code: str
    language: str = "python"


class TestCaseRequest(BaseModel):
    problem_title: str
    problem_description: str = ""
    difficulty: str = "medium"


# ── Pattern Catalog ──

@router.get("/catalog")
async def get_pattern_catalog():
    """Get the full pattern catalog with templates and recognition cues."""
    return {"patterns": get_all_patterns()}


@router.get("/catalog/{pattern_key}")
async def get_pattern_detail(pattern_key: str):
    """Get details for a specific pattern."""
    pattern = PATTERNS.get(pattern_key)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return {"key": pattern_key, **pattern}


@router.get("/for-problem/{problem_id}")
async def get_problem_patterns(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get pattern tags for a specific problem."""
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Try exact match first
    pattern_info = get_pattern_for_problem(problem.title)

    # Fall back to heuristic matching
    if not pattern_info.get("primary") or pattern_info["primary"] is None:
        matches = match_patterns_to_problem(
            problem.title,
            problem.description or ""
        )
        if matches:
            primary = matches[0]
            secondary = matches[1:] if len(matches) > 1 else []
            pattern_info = {"primary": primary, "secondary": secondary}

    return {
        "problem_id": problem_id,
        "problem_title": problem.title,
        **pattern_info,
    }


@router.get("/match")
async def match_pattern(
    title: str = Query(...),
    description: str = Query(""),
):
    """Heuristic pattern matching from problem title/description."""
    matches = match_patterns_to_problem(title, description)
    return {"matches": matches}


# ── AI Code Analysis ──

@router.post("/analyze-code")
async def analyze_code(req: CodeAnalysisRequest):
    """AI analyzes submitted code to identify which pattern was used vs. optimal."""
    # Get known pattern for this problem
    known = get_pattern_for_problem(req.problem_title)

    result = await analyze_code_pattern(
        problem_title=req.problem_title,
        code=req.code,
        language=req.language,
        known_optimal_pattern=known.get("primary", {}).get("key") if known.get("primary") else None,
    )

    return {
        "analysis": result,
        "known_patterns": known,
    }


# ── Test Case Generation ──

@router.post("/test-cases")
async def generate_test_cases_endpoint(req: TestCaseRequest):
    """AI generates test cases for a problem."""
    result = await generate_test_cases(
        problem_title=req.problem_title,
        problem_description=req.problem_description,
        difficulty=req.difficulty,
    )
    return result
