"""Daily plan routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import UserProfile, DailyPlan, Roadmap, RoadmapTopic, LearningStats, TopicStatus
from schemas import DailyPlanResponse
from agents import generate_daily_plan, teach_concept

router = APIRouter()


@router.get("/{user_id}/today", response_model=DailyPlanResponse)
async def get_today_plan(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get or generate today's learning plan."""
    # Get user
    user_result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get roadmap
    roadmap_result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user_id)
        .options(selectinload(Roadmap.topics))
    )
    roadmap = roadmap_result.scalar_one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="No roadmap found. Generate one first.")

    day_number = roadmap.current_day

    # Check if plan already exists for today
    existing = await db.execute(
        select(DailyPlan).where(
            DailyPlan.user_id == user_id,
            DailyPlan.day_number == day_number
        )
    )
    existing_plan = existing.scalar_one_or_none()
    if existing_plan:
        return existing_plan

    # Find current topic
    current_topic = None
    for topic in roadmap.topics:
        if topic.status in (TopicStatus.AVAILABLE, TopicStatus.IN_PROGRESS):
            current_topic = topic
            break

    if not current_topic:
        # All topics done or none available - use last topic
        current_topic = roadmap.topics[-1] if roadmap.topics else None

    # Get stats
    stats_result = await db.execute(
        select(LearningStats).where(LearningStats.user_id == user_id)
    )
    stats = stats_result.scalar_one_or_none()

    # Generate daily plan with AI
    topic_dict = {
        "name": current_topic.name if current_topic else "DSA Fundamentals",
        "category": current_topic.category if current_topic else "foundations",
        "key_concepts": current_topic.key_concepts if current_topic else [],
        "common_patterns": current_topic.common_patterns if current_topic else [],
    }
    user_dict = {
        "name": user.name,
        "experience_level": user.experience_level,
        "daily_hours": user.daily_hours,
    }
    stats_dict = {
        "learning_pace": stats.learning_pace if stats else "normal",
        "weak_areas": stats.weak_areas if stats else [],
    } if stats else None

    plan_data = await generate_daily_plan(user_dict, day_number, topic_dict, stats_dict)

    # Mark current topic as in-progress
    if current_topic and current_topic.status == TopicStatus.AVAILABLE:
        current_topic.status = TopicStatus.IN_PROGRESS

    # Save the plan
    daily_plan = DailyPlan(
        user_id=user_id,
        day_number=day_number,
        concept_lesson=plan_data.get("concept_lesson"),
        problems_assigned=[],
        review_problems=[],
        ai_summary=plan_data.get("motivation", ""),
    )
    db.add(daily_plan)
    await db.commit()
    await db.refresh(daily_plan)
    return daily_plan


@router.post("/{user_id}/complete-day")
async def complete_day(user_id: int, db: AsyncSession = Depends(get_db)):
    """Mark today's plan as complete and advance to next day."""
    # Get roadmap
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user_id)
    )
    roadmap = roadmap_result.scalar_one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="No roadmap found")

    # Mark current day plan as complete
    plan_result = await db.execute(
        select(DailyPlan).where(
            DailyPlan.user_id == user_id,
            DailyPlan.day_number == roadmap.current_day
        )
    )
    plan = plan_result.scalar_one_or_none()
    if plan:
        plan.completed = True

    # Advance the day
    roadmap.current_day += 1

    await db.commit()
    return {"message": f"Day {roadmap.current_day - 1} completed! Moving to Day {roadmap.current_day}."}


@router.get("/{user_id}/teach/{topic}")
async def get_lesson(user_id: int, topic: str, subtopic: str = None,
                     db: AsyncSession = Depends(get_db)):
    """Get an AI-generated lesson for a specific topic."""
    # Get user's preferred language
    user_result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = user_result.scalar_one_or_none()
    language = user.preferred_language if user else "python"

    lesson = await teach_concept(topic, subtopic, language)
    return lesson
