"""Spaced Repetition & Review Queue routes."""
import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import ReviewCard, RoadmapTopic, Roadmap
from spaced_repetition import (
    sm2_update,
    get_review_queue,
    get_upcoming_reviews,
    create_review_cards_for_topic,
    apply_mastery_decay,
    calculate_mastery_decay,
)
from agents import generate_review_question

router = APIRouter(prefix="/review", tags=["review"])


class ReviewSubmission(BaseModel):
    quality: int  # 0-5 recall quality


class CreateCardsRequest(BaseModel):
    topic_id: int


@router.get("/{user_id}/queue")
async def get_review_queue_endpoint(
    user_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Get cards due for review right now (the review queue)."""
    cards = await get_review_queue(db, user_id, limit)

    return {
        "due_count": len(cards),
        "cards": [_card_to_dict(c) for c in cards],
    }


@router.get("/{user_id}/upcoming")
async def get_upcoming_reviews_endpoint(
    user_id: int,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """Get cards coming up for review in the next N days."""
    cards = await get_upcoming_reviews(db, user_id, days)

    # Group by day
    by_day = {}
    now = datetime.datetime.utcnow()
    for card in cards:
        if card.next_review <= now:
            day_key = "today"
        else:
            delta = (card.next_review - now).days
            if delta == 0:
                day_key = "today"
            elif delta == 1:
                day_key = "tomorrow"
            else:
                day_key = card.next_review.strftime("%A, %b %d")

        if day_key not in by_day:
            by_day[day_key] = []
        by_day[day_key].append(_card_to_dict(card))

    return {
        "total": len(cards),
        "by_day": by_day,
    }


@router.get("/{user_id}/stats")
async def get_review_stats(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get spaced repetition statistics for the user."""
    now = datetime.datetime.utcnow()

    # Total cards
    total_result = await db.execute(
        select(func.count(ReviewCard.id))
        .where(ReviewCard.user_id == user_id)
    )
    total_cards = total_result.scalar() or 0

    # Due now
    due_result = await db.execute(
        select(func.count(ReviewCard.id))
        .where(and_(ReviewCard.user_id == user_id, ReviewCard.next_review <= now))
    )
    due_now = due_result.scalar() or 0

    # Reviewed today
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    reviewed_result = await db.execute(
        select(func.count(ReviewCard.id))
        .where(and_(
            ReviewCard.user_id == user_id,
            ReviewCard.last_reviewed >= today_start,
        ))
    )
    reviewed_today = reviewed_result.scalar() or 0

    # Average easiness factor (higher = easier retention)
    ef_result = await db.execute(
        select(func.avg(ReviewCard.easiness_factor))
        .where(and_(ReviewCard.user_id == user_id, ReviewCard.total_reviews > 0))
    )
    avg_ef = round(ef_result.scalar() or 2.5, 2)

    # Mastered cards (high EF + long interval)
    mastered_result = await db.execute(
        select(func.count(ReviewCard.id))
        .where(and_(
            ReviewCard.user_id == user_id,
            ReviewCard.easiness_factor >= 2.5,
            ReviewCard.interval_days >= 14,
        ))
    )
    mastered_cards = mastered_result.scalar() or 0

    # Struggling cards (low EF)
    struggling_result = await db.execute(
        select(func.count(ReviewCard.id))
        .where(and_(
            ReviewCard.user_id == user_id,
            ReviewCard.easiness_factor < 1.8,
            ReviewCard.total_reviews > 0,
        ))
    )
    struggling_cards = struggling_result.scalar() or 0

    return {
        "total_cards": total_cards,
        "due_now": due_now,
        "reviewed_today": reviewed_today,
        "avg_easiness_factor": avg_ef,
        "mastered_cards": mastered_cards,
        "struggling_cards": struggling_cards,
        "retention_rate": round((mastered_cards / max(total_cards, 1)) * 100, 1),
    }


@router.post("/{user_id}/cards/create")
async def create_cards_for_topic(
    user_id: int,
    req: CreateCardsRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create review cards when starting a new topic."""
    # Check if cards already exist for this topic
    existing = await db.execute(
        select(ReviewCard)
        .where(and_(
            ReviewCard.user_id == user_id,
            ReviewCard.topic_id == req.topic_id,
        ))
    )
    if list(existing.scalars().all()):
        return {"message": "Review cards already exist for this topic", "created": 0}

    # Get the topic
    topic_result = await db.execute(
        select(RoadmapTopic).where(RoadmapTopic.id == req.topic_id)
    )
    topic = topic_result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    cards = await create_review_cards_for_topic(db, user_id, topic)
    await db.commit()

    return {
        "message": f"Created {len(cards)} review cards for {topic.name}",
        "created": len(cards),
        "cards": [_card_to_dict(c) for c in cards],
    }


@router.post("/{user_id}/cards/{card_id}/review")
async def submit_review(
    user_id: int,
    card_id: int,
    submission: ReviewSubmission,
    db: AsyncSession = Depends(get_db),
):
    """Submit a review result for a card (SM-2 quality 0-5)."""
    result = await db.execute(
        select(ReviewCard)
        .where(and_(ReviewCard.id == card_id, ReviewCard.user_id == user_id))
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    old_interval = card.interval_days
    old_ef = card.easiness_factor

    card = sm2_update(card, submission.quality)
    await db.commit()

    return {
        "card": _card_to_dict(card),
        "changes": {
            "interval": {"old": old_interval, "new": card.interval_days},
            "easiness_factor": {"old": round(old_ef, 2), "new": round(card.easiness_factor, 2)},
            "next_review": card.next_review.isoformat(),
            "quality_submitted": submission.quality,
        },
    }


@router.get("/{user_id}/cards/{card_id}/question")
async def get_review_question(
    user_id: int,
    card_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get an AI-generated review question for a card."""
    result = await db.execute(
        select(ReviewCard)
        .where(and_(ReviewCard.id == card_id, ReviewCard.user_id == user_id))
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    question = await generate_review_question(card.title, card.content or {})
    return {
        "card": _card_to_dict(card),
        "question": question,
    }


@router.post("/{user_id}/decay")
async def trigger_mastery_decay(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Apply mastery decay to topics that haven't been reviewed."""
    decayed = await apply_mastery_decay(db, user_id)
    return {
        "decayed_topics": decayed,
        "count": len(decayed),
    }


def _card_to_dict(card: ReviewCard) -> dict:
    """Convert a ReviewCard to a JSON-serializable dict."""
    now = datetime.datetime.utcnow()
    is_overdue = card.next_review <= now
    days_until = max(0, (card.next_review - now).days) if not is_overdue else 0
    days_overdue = max(0, (now - card.next_review).days) if is_overdue else 0

    return {
        "id": card.id,
        "topic_id": card.topic_id,
        "card_type": card.card_type,
        "title": card.title,
        "content": card.content,
        "easiness_factor": round(card.easiness_factor, 2),
        "interval_days": card.interval_days,
        "repetitions": card.repetitions,
        "next_review": card.next_review.isoformat() if card.next_review else None,
        "last_reviewed": card.last_reviewed.isoformat() if card.last_reviewed else None,
        "total_reviews": card.total_reviews,
        "avg_quality": round(card.avg_quality, 1),
        "is_overdue": is_overdue,
        "days_until_review": days_until,
        "days_overdue": days_overdue,
        "strength": _card_strength(card),
    }


def _card_strength(card: ReviewCard) -> str:
    """Classify card retention strength."""
    if card.total_reviews == 0:
        return "new"
    if card.easiness_factor >= 2.5 and card.interval_days >= 14:
        return "strong"
    if card.easiness_factor >= 2.0 and card.interval_days >= 7:
        return "good"
    if card.easiness_factor >= 1.5:
        return "moderate"
    return "weak"
