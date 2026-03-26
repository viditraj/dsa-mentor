"""Complexity Analyzer API routes."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from agents import analyze_complexity

router = APIRouter()


class AnalyzeComplexityRequest(BaseModel):
    code: str
    language: str = "python"
    problem_title: Optional[str] = None
    known_optimal: Optional[str] = None  # e.g. "O(n log n)"


@router.post("/analyze")
async def analyze(req: AnalyzeComplexityRequest):
    """Analyze code complexity with detailed Big-O breakdown."""
    result = await analyze_complexity(
        code=req.code,
        language=req.language,
        problem_title=req.problem_title,
        known_optimal=req.known_optimal,
    )
    return result
