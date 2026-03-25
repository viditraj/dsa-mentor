"""Skill Tree & Bridge Lessons routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import UserProfile, Roadmap, RoadmapTopic
from agents import generate_bridge_lesson
from topic_dependencies import (
    TOPIC_DEPENDENCIES,
    DEPENDENCY_EXPLANATIONS,
    SKILL_TREE_LAYOUT,
    CATEGORY_COLORS,
)

router = APIRouter(prefix="/skill-tree", tags=["skill-tree"])


@router.get("/{user_id}")
async def get_skill_tree(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get the full skill tree graph with user progress overlaid."""
    # Get user's roadmap topics for status
    result = await db.execute(
        select(RoadmapTopic)
        .join(Roadmap)
        .where(Roadmap.user_id == user_id)
    )
    topics = list(result.scalars().all())
    
    # Build topic status lookup
    topic_status = {}
    for t in topics:
        topic_status[t.name] = {
            "id": t.id,
            "status": t.status.value if hasattr(t.status, 'value') else t.status,
            "mastery_score": t.mastery_score,
            "category": t.category,
            "difficulty": t.difficulty.value if hasattr(t.difficulty, 'value') else t.difficulty,
            "key_concepts": t.key_concepts or [],
        }

    # Build nodes
    nodes = []
    for topic_name, layout in SKILL_TREE_LAYOUT.items():
        status_info = topic_status.get(topic_name, {})
        category = status_info.get("category", "foundations")
        
        nodes.append({
            "id": topic_name,
            "name": topic_name,
            "topic_id": status_info.get("id"),
            "x": layout["x"],
            "y": layout["y"],
            "tier": layout["tier"],
            "status": status_info.get("status", "locked"),
            "mastery": status_info.get("mastery_score", 0),
            "category": category,
            "color": CATEGORY_COLORS.get(category, "#6366f1"),
            "difficulty": status_info.get("difficulty", "easy"),
            "key_concepts": status_info.get("key_concepts", []),
            "prerequisites": TOPIC_DEPENDENCIES.get(topic_name, []),
            "unlocks": [t for t, deps in TOPIC_DEPENDENCIES.items() if topic_name in deps],
        })

    # Build edges
    edges = []
    for topic_name, prerequisites in TOPIC_DEPENDENCIES.items():
        for prereq in prerequisites:
            if prereq in SKILL_TREE_LAYOUT and topic_name in SKILL_TREE_LAYOUT:
                # Both prereq and current topic must be completed/in-progress for "active" edge
                prereq_status = topic_status.get(prereq, {}).get("status", "locked")
                topic_st = topic_status.get(topic_name, {}).get("status", "locked")
                
                active = prereq_status in ("completed", "mastered", "in_progress")
                
                edges.append({
                    "from": prereq,
                    "to": topic_name,
                    "active": active,
                    "explanation": DEPENDENCY_EXPLANATIONS.get(
                        (prereq, topic_name), 
                        f"{prereq} is a prerequisite for {topic_name}"
                    ),
                })

    return {
        "nodes": nodes,
        "edges": edges,
        "category_colors": CATEGORY_COLORS,
        "total_topics": len(nodes),
        "completed_topics": sum(1 for n in nodes if n["status"] in ("completed", "mastered")),
        "in_progress_topics": sum(1 for n in nodes if n["status"] == "in_progress"),
        "available_topics": sum(1 for n in nodes if n["status"] == "available"),
    }


@router.get("/{user_id}/node/{topic_name}")
async def get_node_details(
    user_id: int,
    topic_name: str,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed info about a skill tree node including prerequisites and what it unlocks."""
    prerequisites = TOPIC_DEPENDENCIES.get(topic_name, [])
    unlocks = [t for t, deps in TOPIC_DEPENDENCIES.items() if topic_name in deps]

    # Get prerequisite explanations
    prereq_details = []
    for prereq in prerequisites:
        explanation = DEPENDENCY_EXPLANATIONS.get(
            (prereq, topic_name),
            f"Understanding {prereq} is needed for {topic_name}."
        )
        prereq_status = "locked"
        # Try to get actual status from DB
        result = await db.execute(
            select(RoadmapTopic)
            .join(Roadmap)
            .where(Roadmap.user_id == user_id, RoadmapTopic.name == prereq)
        )
        prereq_topic = result.scalar_one_or_none()
        if prereq_topic:
            prereq_status = prereq_topic.status.value if hasattr(prereq_topic.status, 'value') else prereq_topic.status

        prereq_details.append({
            "name": prereq,
            "status": prereq_status,
            "explanation": explanation,
        })

    return {
        "topic_name": topic_name,
        "prerequisites": prereq_details,
        "unlocks": unlocks,
        "layout": SKILL_TREE_LAYOUT.get(topic_name, {}),
    }


@router.post("/{user_id}/bridge-lesson")
async def get_bridge_lesson(
    user_id: int,
    from_topic: str,
    to_topic: str,
    db: AsyncSession = Depends(get_db),
):
    """Generate an AI bridge lesson connecting two related topics."""
    # Get user level
    user_result = await db.execute(
        select(UserProfile).where(UserProfile.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    user_level = user.experience_level if user else "beginner"

    # Get dependency explanation if it exists  
    explanation = DEPENDENCY_EXPLANATIONS.get(
        (from_topic, to_topic),
        None,
    )

    lesson = await generate_bridge_lesson(
        from_topic=from_topic,
        to_topic=to_topic,
        dependency_explanation=explanation,
        user_level=user_level,
    )
    return lesson
