"""Behavioral Interview Prep API routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import UserProfile
from agents import (
    generate_behavioral_questions,
    review_behavioral_answer,
    generate_star_coaching,
)

router = APIRouter()


COMPANY_FRAMEWORKS = {
    "amazon": {
        "name": "Amazon Leadership Principles",
        "principles": [
            "Customer Obsession", "Ownership", "Invent and Simplify",
            "Are Right, A Lot", "Learn and Be Curious", "Hire and Develop the Best",
            "Insist on the Highest Standards", "Think Big", "Bias for Action",
            "Frugality", "Earn Trust", "Dive Deep",
            "Have Backbone; Disagree and Commit", "Deliver Results",
            "Strive to be Earth's Best Employer", "Success and Scale Bring Broad Responsibility",
        ],
    },
    "google": {
        "name": "Googleyness & Leadership",
        "principles": [
            "Googleyness", "General Cognitive Ability", "Role-Related Knowledge",
            "Leadership", "Collaboration", "Navigating Ambiguity",
        ],
    },
    "meta": {
        "name": "Meta Core Values",
        "principles": [
            "Move Fast", "Be Bold", "Focus on Impact",
            "Be Open", "Build Social Value", "Meta-specific leadership",
        ],
    },
    "microsoft": {
        "name": "Microsoft Growth Mindset",
        "principles": [
            "Growth Mindset", "Customer Obsession", "Diversity and Inclusion",
            "One Microsoft", "Making a Difference",
        ],
    },
    "apple": {
        "name": "Apple Culture",
        "principles": [
            "Innovation", "Attention to Detail", "Collaboration",
            "Passion for Products", "Excellence",
        ],
    },
}


class GenerateQuestionsRequest(BaseModel):
    user_id: int
    company: Optional[str] = None
    role: str = "software_engineer"
    num_questions: int = 5
    experience_summary: Optional[str] = None


class ReviewAnswerRequest(BaseModel):
    question: str
    answer: str
    company: Optional[str] = None
    principle: Optional[str] = None


class STARCoachingRequest(BaseModel):
    experience: str  # raw description of a project/experience
    target_question_type: Optional[str] = None  # e.g. "leadership", "conflict", "failure"


@router.get("/frameworks")
async def get_company_frameworks():
    """Get all company-specific behavioral frameworks."""
    return {"frameworks": COMPANY_FRAMEWORKS}


@router.get("/frameworks/{company}")
async def get_company_framework(company: str):
    """Get behavioral framework for a specific company."""
    company = company.lower()
    if company not in COMPANY_FRAMEWORKS:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{company}' not found. Available: {list(COMPANY_FRAMEWORKS.keys())}",
        )
    return COMPANY_FRAMEWORKS[company]


@router.post("/questions")
async def generate_questions(req: GenerateQuestionsRequest, db: AsyncSession = Depends(get_db)):
    """Generate behavioral interview questions."""
    user = await db.get(UserProfile, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    framework = COMPANY_FRAMEWORKS.get(req.company.lower()) if req.company else None

    questions = await generate_behavioral_questions(
        company=req.company,
        role=req.role,
        framework=framework,
        num_questions=req.num_questions,
        experience_summary=req.experience_summary,
        experience_level=user.experience_level,
    )
    return questions


@router.post("/review-answer")
async def review_answer(req: ReviewAnswerRequest):
    """Review a behavioral answer using STAR method."""
    result = await review_behavioral_answer(
        question=req.question,
        answer=req.answer,
        company=req.company,
        principle=req.principle,
    )
    return result


@router.post("/star-coaching")
async def star_coaching(req: STARCoachingRequest):
    """Transform a raw experience into a polished STAR response."""
    result = await generate_star_coaching(
        experience=req.experience,
        target_question_type=req.target_question_type,
    )
    return result
