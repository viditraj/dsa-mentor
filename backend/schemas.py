"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── User Schemas ──
class UserCreate(BaseModel):
    name: str
    email: str
    experience_level: str = "beginner"
    target_company: Optional[str] = None
    target_date: Optional[datetime] = None
    daily_hours: float = 2.0
    preferred_language: str = "python"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    experience_level: str
    target_company: Optional[str]
    target_date: Optional[datetime]
    daily_hours: float
    preferred_language: str
    strengths: list
    weaknesses: list

    class Config:
        from_attributes = True


# ── Roadmap Schemas ──
class TopicResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]
    difficulty: str
    status: str
    order: int
    estimated_days: int
    day_start: Optional[int]
    day_end: Optional[int]
    mastery_score: float
    key_concepts: list
    common_patterns: list
    prerequisites: list

    class Config:
        from_attributes = True


class RoadmapResponse(BaseModel):
    id: int
    user_id: int
    total_days: int
    current_day: int
    topics: List[TopicResponse]

    class Config:
        from_attributes = True


# ── Problem Schemas ──
class ProblemResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    leetcode_number: Optional[int]
    leetcode_url: Optional[str]
    difficulty: str
    description: Optional[str]
    hints: list
    solution_approach: Optional[str]
    time_complexity: Optional[str]
    space_complexity: Optional[str]
    patterns: list

    class Config:
        from_attributes = True


class ProblemAttemptCreate(BaseModel):
    user_id: int
    problem_id: Optional[int] = None
    status: str = "attempted"
    code: Optional[str] = None
    language: str = "python"
    time_taken_minutes: Optional[int] = None
    used_hint: bool = False
    self_rating: Optional[int] = None


class ProblemAttemptResponse(BaseModel):
    id: int
    problem_id: int
    status: str
    code: Optional[str]
    time_taken_minutes: Optional[int]
    used_hint: bool
    self_rating: Optional[int]
    ai_feedback: Optional[str]
    attempted_at: datetime

    class Config:
        from_attributes = True


# ── Daily Plan Schemas ──
class DailyPlanResponse(BaseModel):
    id: int
    day_number: int
    date: datetime
    concept_lesson: Optional[dict]
    problems_assigned: list
    review_problems: list
    completed: bool
    notes: Optional[str]
    ai_summary: Optional[str]

    class Config:
        from_attributes = True


# ── Learning Stats Schemas ──
class StatsResponse(BaseModel):
    total_problems_solved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    current_streak: int
    max_streak: int
    avg_time_easy: float
    avg_time_medium: float
    avg_time_hard: float
    topics_completed: int
    topics_mastered: int
    weak_areas: list
    strong_areas: list
    learning_pace: str
    xp_points: int
    level: int

    class Config:
        from_attributes = True


# ── Chat/AI Schemas ──
class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None  # current topic or problem context


class ChatResponse(BaseModel):
    response: str
    visualization: Optional[dict] = None
    code_example: Optional[str] = None
    follow_up_questions: list = []


class VisualizationRequest(BaseModel):
    topic: str
    algorithm: Optional[str] = None
    data: Optional[list] = None
    step_by_step: bool = True


# ── FAANG Prep Schemas ──
class FAANGQuestionSubmit(BaseModel):
    user_id: int
    question_id: int
    status: str = "solved"  # attempted, solved
    code: Optional[str] = None
    language: str = "python"
    time_taken_minutes: Optional[int] = None
    confidence: int = 3  # 1-5


class FAANGProgressResponse(BaseModel):
    question_id: int
    pattern_key: str
    status: str
    confidence: int
    time_taken_minutes: Optional[int]
    solved_at: Optional[datetime]

    class Config:
        from_attributes = True


class PatternMasteryResponse(BaseModel):
    pattern_key: str
    problems_solved: int
    problems_total: int
    avg_confidence: float
    avg_time_minutes: float
    mastery_level: str
    story_read: bool
    template_practiced: bool

    class Config:
        from_attributes = True
