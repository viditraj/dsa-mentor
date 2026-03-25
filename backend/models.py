"""SQLAlchemy models for DSA Mentor."""
import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import relationship
import enum

from database import Base


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ProblemStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    ATTEMPTED = "attempted"
    SOLVED = "solved"
    NEEDS_REVIEW = "needs_review"


class TopicStatus(str, enum.Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    experience_level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    target_company = Column(String(100), nullable=True)
    target_date = Column(DateTime, nullable=True)
    daily_hours = Column(Float, default=2.0)
    preferred_language = Column(String(30), default="python")
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    roadmap = relationship("Roadmap", back_populates="user", uselist=False, cascade="all, delete-orphan")
    daily_plans = relationship("DailyPlan", back_populates="user", cascade="all, delete-orphan")
    problem_attempts = relationship("ProblemAttempt", back_populates="user", cascade="all, delete-orphan")
    learning_stats = relationship("LearningStats", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    total_days = Column(Integer, default=90)
    current_day = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("UserProfile", back_populates="roadmap")
    topics = relationship("RoadmapTopic", back_populates="roadmap", cascade="all, delete-orphan",
                          order_by="RoadmapTopic.order")


class RoadmapTopic(Base):
    __tablename__ = "roadmap_topics"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # arrays, linked_lists, trees, graphs, dp, etc.
    description = Column(Text, nullable=True)
    difficulty = Column(SAEnum(Difficulty), default=Difficulty.EASY)
    status = Column(SAEnum(TopicStatus), default=TopicStatus.LOCKED)
    order = Column(Integer, nullable=False)
    estimated_days = Column(Integer, default=3)
    day_start = Column(Integer, nullable=True)
    day_end = Column(Integer, nullable=True)
    prerequisites = Column(JSON, default=list)  # list of topic IDs
    mastery_score = Column(Float, default=0.0)  # 0.0 to 100.0
    key_concepts = Column(JSON, default=list)
    common_patterns = Column(JSON, default=list)

    roadmap = relationship("Roadmap", back_populates="topics")
    problems = relationship("Problem", back_populates="topic", cascade="all, delete-orphan")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("roadmap_topics.id"), nullable=False)
    title = Column(String(300), nullable=False)
    leetcode_number = Column(Integer, nullable=True)
    leetcode_url = Column(String(500), nullable=True)
    difficulty = Column(SAEnum(Difficulty), default=Difficulty.EASY)
    description = Column(Text, nullable=True)
    hints = Column(JSON, default=list)
    solution_approach = Column(Text, nullable=True)
    time_complexity = Column(String(50), nullable=True)
    space_complexity = Column(String(50), nullable=True)
    patterns = Column(JSON, default=list)  # two pointers, sliding window, etc.
    is_daily = Column(Boolean, default=False)
    assigned_date = Column(DateTime, nullable=True)

    topic = relationship("RoadmapTopic", back_populates="problems")
    attempts = relationship("ProblemAttempt", back_populates="problem", cascade="all, delete-orphan")


class ProblemAttempt(Base):
    __tablename__ = "problem_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    status = Column(SAEnum(ProblemStatus), default=ProblemStatus.NOT_STARTED)
    code = Column(Text, nullable=True)
    language = Column(String(30), default="python")
    time_taken_minutes = Column(Integer, nullable=True)
    used_hint = Column(Boolean, default=False)
    self_rating = Column(Integer, nullable=True)  # 1-5
    ai_feedback = Column(Text, nullable=True)
    attempted_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserProfile", back_populates="problem_attempts")
    problem = relationship("Problem", back_populates="attempts")


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    concept_lesson = Column(JSON, nullable=True)  # {title, content, visualizations, examples}
    problems_assigned = Column(JSON, default=list)  # list of problem IDs
    review_problems = Column(JSON, default=list)  # spaced repetition review
    completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)

    user = relationship("UserProfile", back_populates="daily_plans")


class LearningStats(Base):
    __tablename__ = "learning_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    total_problems_solved = Column(Integer, default=0)
    easy_solved = Column(Integer, default=0)
    medium_solved = Column(Integer, default=0)
    hard_solved = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    avg_time_easy = Column(Float, default=0.0)
    avg_time_medium = Column(Float, default=0.0)
    avg_time_hard = Column(Float, default=0.0)
    topics_completed = Column(Integer, default=0)
    topics_mastered = Column(Integer, default=0)
    weak_areas = Column(JSON, default=list)
    strong_areas = Column(JSON, default=list)
    learning_pace = Column(String(20), default="normal")  # slow, normal, fast
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    xp_points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    user = relationship("UserProfile", back_populates="learning_stats")


class ReviewCard(Base):
    """Spaced Repetition review card (SM-2 algorithm)."""
    __tablename__ = "review_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("roadmap_topics.id"), nullable=True)
    # What's being reviewed
    card_type = Column(String(50), nullable=False)  # concept, problem, pattern
    title = Column(String(300), nullable=False)
    content = Column(JSON, default=dict)  # flexible content for the card
    # SM-2 algorithm fields
    easiness_factor = Column(Float, default=2.5)  # EF >= 1.3
    interval_days = Column(Integer, default=1)     # days until next review
    repetitions = Column(Integer, default=0)       # successful consecutive reviews
    next_review = Column(DateTime, default=datetime.datetime.utcnow)  # when to review next
    last_reviewed = Column(DateTime, nullable=True)
    # Quality tracking
    total_reviews = Column(Integer, default=0)
    avg_quality = Column(Float, default=0.0)  # average quality score (0-5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserProfile", backref="review_cards")
    topic = relationship("RoadmapTopic", backref="review_cards")


class FAANGProgress(Base):
    """Tracks a user's progress through the FAANG 75 crash course."""
    __tablename__ = "faang_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    question_id = Column(Integer, nullable=False)  # FAANG_QUESTIONS id (1-75)
    pattern_key = Column(String(50), nullable=False)  # e.g. "two_pointers"
    status = Column(String(20), default="not_started")  # not_started, attempted, solved
    code = Column(Text, nullable=True)
    language = Column(String(30), default="python")
    time_taken_minutes = Column(Integer, nullable=True)
    confidence = Column(Integer, default=0)  # 1-5 self-rated confidence
    notes = Column(Text, nullable=True)
    solved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserProfile", backref="faang_progress")


class PatternMastery(Base):
    """Tracks mastery of each FAANG pattern for a user."""
    __tablename__ = "pattern_mastery"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    pattern_key = Column(String(50), nullable=False)  # e.g. "two_pointers"
    problems_solved = Column(Integer, default=0)
    problems_total = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)
    avg_time_minutes = Column(Float, default=0.0)
    mastery_level = Column(String(20), default="locked")  # locked, learning, practiced, mastered
    last_practiced = Column(DateTime, nullable=True)
    story_read = Column(Boolean, default=False)
    template_practiced = Column(Boolean, default=False)

    user = relationship("UserProfile", backref="pattern_mastery")
