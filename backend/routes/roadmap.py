"""Roadmap generation and management routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import (
    UserProfile, Roadmap, RoadmapTopic, Problem, LearningStats,
    TopicStatus, Difficulty
)
from leetcode_descriptions import LOCAL_DESCRIPTIONS
from schemas import RoadmapResponse, TopicResponse
from agents import generate_adaptive_roadmap
from dsa_knowledge import DSA_CURRICULUM

router = APIRouter()


@router.post("/{user_id}/generate", response_model=RoadmapResponse)
async def generate_roadmap(user_id: int, db: AsyncSession = Depends(get_db)):
    """Generate a personalized DSA roadmap for the user."""
    # Get user profile
    result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get stats for adaptive roadmap
    stats_result = await db.execute(
        select(LearningStats).where(LearningStats.user_id == user_id)
    )
    stats = stats_result.scalar_one_or_none()
    stats_dict = {
        "total_problems_solved": stats.total_problems_solved if stats else 0,
        "weak_areas": stats.weak_areas if stats else [],
        "strong_areas": stats.strong_areas if stats else [],
        "learning_pace": stats.learning_pace if stats else "normal",
        "topics_completed": stats.topics_completed if stats else 0,
    }

    # Get AI recommendations
    user_dict = {
        "name": user.name,
        "experience_level": user.experience_level,
        "daily_hours": user.daily_hours,
        "target_company": user.target_company,
        "target_date": str(user.target_date) if user.target_date else None,
        "preferred_language": user.preferred_language,
    }
    ai_recommendations = await generate_adaptive_roadmap(user_dict, stats_dict)

    # Delete existing roadmap if any
    existing = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user_id).options(selectinload(Roadmap.topics))
    )
    existing_roadmap = existing.scalar_one_or_none()
    if existing_roadmap:
        await db.delete(existing_roadmap)
        await db.flush()

    # Create roadmap from curriculum
    total_days = ai_recommendations.get("total_days", 90)
    roadmap = Roadmap(user_id=user_id, total_days=total_days)
    db.add(roadmap)
    await db.flush()

    # Populate topics from DSA_CURRICULUM
    topic_order = 0
    current_day = 1
    focus_areas = ai_recommendations.get("focus_areas", [])
    skip_suggestions = ai_recommendations.get("skip_suggestions", [])

    for category_key, category_data in sorted(DSA_CURRICULUM.items(), key=lambda x: x[1]["order"]):
        for topic_data in category_data["topics"]:
            topic_order += 1
            estimated_days = topic_data["estimated_days"]

            # Adjust based on AI recommendations
            if topic_data["category"] in skip_suggestions:
                estimated_days = max(1, estimated_days - 1)
            if topic_data["category"] in focus_areas:
                estimated_days += 1

            # Adjust based on experience level
            if user.experience_level == "advanced" and topic_data["difficulty"] == "easy":
                estimated_days = max(1, estimated_days - 1)
            elif user.experience_level == "beginner" and topic_data["difficulty"] == "hard":
                estimated_days += 1

            # Set status based on order
            if topic_order == 1:
                status = TopicStatus.AVAILABLE
            elif topic_order <= 3 and user.experience_level in ("intermediate", "advanced"):
                status = TopicStatus.AVAILABLE
            else:
                status = TopicStatus.LOCKED

            topic = RoadmapTopic(
                roadmap_id=roadmap.id,
                name=topic_data["name"],
                category=topic_data["category"],
                description=f"Master {topic_data['name']} with hands-on practice",
                difficulty=Difficulty(topic_data["difficulty"]),
                status=status,
                order=topic_order,
                estimated_days=estimated_days,
                day_start=current_day,
                day_end=current_day + estimated_days - 1,
                key_concepts=topic_data.get("key_concepts", []),
                common_patterns=topic_data.get("common_patterns", []),
            )
            db.add(topic)
            await db.flush()

            # Add problems for this topic
            for prob_data in topic_data.get("problems", []):
                lc_num = prob_data.get("leetcode_number")
                desc = LOCAL_DESCRIPTIONS.get(lc_num) or LOCAL_DESCRIPTIONS.get(prob_data["title"]) or f"Solve: {prob_data['title']}"
                problem = Problem(
                    topic_id=topic.id,
                    title=prob_data["title"],
                    leetcode_number=lc_num,
                    leetcode_url=f"https://leetcode.com/problems/{prob_data['title'].lower().replace(' ', '-').replace('(', '').replace(')', '')}/",
                    difficulty=Difficulty(prob_data["difficulty"]),
                    description=desc,
                    patterns=topic_data.get("common_patterns", []),
                )
                db.add(problem)

            current_day += estimated_days

    await db.commit()

    # Reload with relationships
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.id == roadmap.id)
        .options(selectinload(Roadmap.topics))
    )
    roadmap = result.scalar_one()
    return roadmap


@router.get("/{user_id}", response_model=RoadmapResponse)
async def get_roadmap(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get the user's current roadmap."""
    result = await db.execute(
        select(Roadmap)
        .where(Roadmap.user_id == user_id)
        .options(selectinload(Roadmap.topics))
    )
    roadmap = result.scalar_one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found. Generate one first.")
    return roadmap


@router.put("/topic/{topic_id}/status")
async def update_topic_status(topic_id: int, status: str, db: AsyncSession = Depends(get_db)):
    """Update the status of a roadmap topic."""
    result = await db.execute(select(RoadmapTopic).where(RoadmapTopic.id == topic_id))
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.status = TopicStatus(status)

    # If completed, unlock next topic
    if status in ("completed", "mastered"):
        next_result = await db.execute(
            select(RoadmapTopic)
            .where(
                RoadmapTopic.roadmap_id == topic.roadmap_id,
                RoadmapTopic.order == topic.order + 1
            )
        )
        next_topic = next_result.scalar_one_or_none()
        if next_topic and next_topic.status == TopicStatus.LOCKED:
            next_topic.status = TopicStatus.AVAILABLE

    await db.commit()
    return {"status": "updated", "topic_id": topic_id, "new_status": status}


@router.put("/topic/{topic_id}/mastery")
async def update_mastery_score(topic_id: int, score: float, db: AsyncSession = Depends(get_db)):
    """Update the mastery score for a topic (0-100)."""
    result = await db.execute(select(RoadmapTopic).where(RoadmapTopic.id == topic_id))
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.mastery_score = min(100.0, max(0.0, score))

    # Auto-update status based on mastery
    if topic.mastery_score >= 90:
        topic.status = TopicStatus.MASTERED
    elif topic.mastery_score >= 70:
        topic.status = TopicStatus.COMPLETED

    await db.commit()
    return {"topic_id": topic_id, "mastery_score": topic.mastery_score, "status": topic.status.value}
