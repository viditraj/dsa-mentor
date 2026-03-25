"""Learning statistics routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import LearningStats, ProblemAttempt, RoadmapTopic, Roadmap, TopicStatus
from schemas import StatsResponse

router = APIRouter()


@router.get("/{user_id}", response_model=StatsResponse)
async def get_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get comprehensive learning statistics for a user."""
    result = await db.execute(
        select(LearningStats).where(LearningStats.user_id == user_id)
    )
    stats = result.scalar_one_or_none()
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


@router.get("/{user_id}/progress")
async def get_progress(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get detailed progress including topic completion and problem stats."""
    # Get stats
    stats_result = await db.execute(
        select(LearningStats).where(LearningStats.user_id == user_id)
    )
    stats = stats_result.scalar_one_or_none()

    # Get roadmap progress
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == user_id)
    )
    roadmap = roadmap_result.scalar_one_or_none()

    topic_progress = []
    if roadmap:
        topics_result = await db.execute(
            select(RoadmapTopic)
            .where(RoadmapTopic.roadmap_id == roadmap.id)
            .order_by(RoadmapTopic.order)
        )
        topics = topics_result.scalars().all()
        for topic in topics:
            topic_progress.append({
                "id": topic.id,
                "name": topic.name,
                "category": topic.category,
                "status": topic.status.value,
                "mastery_score": topic.mastery_score,
                "order": topic.order,
            })

    # Calculate overall progress
    total_topics = len(topic_progress)
    completed_topics = sum(1 for t in topic_progress if t["status"] in ("completed", "mastered"))
    mastered_topics = sum(1 for t in topic_progress if t["status"] == "mastered")

    return {
        "stats": {
            "total_problems_solved": stats.total_problems_solved if stats else 0,
            "easy_solved": stats.easy_solved if stats else 0,
            "medium_solved": stats.medium_solved if stats else 0,
            "hard_solved": stats.hard_solved if stats else 0,
            "current_streak": stats.current_streak if stats else 0,
            "max_streak": stats.max_streak if stats else 0,
            "xp_points": stats.xp_points if stats else 0,
            "level": stats.level if stats else 1,
            "learning_pace": stats.learning_pace if stats else "normal",
        },
        "roadmap_progress": {
            "current_day": roadmap.current_day if roadmap else 0,
            "total_days": roadmap.total_days if roadmap else 0,
            "completion_percentage": round((completed_topics / total_topics * 100) if total_topics > 0 else 0, 1),
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "mastered_topics": mastered_topics,
        },
        "topic_progress": topic_progress,
    }
