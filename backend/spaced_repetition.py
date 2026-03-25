"""Spaced Repetition Engine using the SM-2 algorithm.

SM-2 (SuperMemo 2) adjusts review intervals based on recall quality:
  Quality 0-2: Reset (failed recall — restart from beginning)
  Quality 3: Correct but difficult — shorter interval
  Quality 4: Correct with some effort — normal interval
  Quality 5: Perfect recall — longer interval

Mastery decay: Topics lose mastery if not reviewed within their interval.
"""
import datetime
import math
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models import ReviewCard, RoadmapTopic


def sm2_update(card: ReviewCard, quality: int) -> ReviewCard:
    """Apply SM-2 algorithm to update review card scheduling.
    
    Args:
        card: The review card to update
        quality: User's recall quality (0-5)
            0 = Complete blackout
            1 = Wrong, but recognized after seeing answer
            2 = Wrong, but answer felt familiar
            3 = Correct, but required significant effort
            4 = Correct, with some hesitation
            5 = Perfect recall
    
    Returns:
        Updated card with new interval, EF, and next_review date
    """
    quality = max(0, min(5, quality))  # clamp to 0-5
    now = datetime.datetime.utcnow()

    # Update tracking
    card.total_reviews += 1
    card.last_reviewed = now
    card.avg_quality = (
        (card.avg_quality * (card.total_reviews - 1) + quality) / card.total_reviews
    )

    if quality < 3:
        # Failed recall — reset repetitions, short interval
        card.repetitions = 0
        card.interval_days = 1
    else:
        # Successful recall — increase interval
        if card.repetitions == 0:
            card.interval_days = 1
        elif card.repetitions == 1:
            card.interval_days = 3
        else:
            card.interval_days = round(card.interval_days * card.easiness_factor)

        card.repetitions += 1

    # Update easiness factor (EF)
    # EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
    card.easiness_factor = max(
        1.3,
        card.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )

    # Schedule next review
    card.next_review = now + datetime.timedelta(days=card.interval_days)

    return card


def calculate_mastery_decay(
    current_mastery: float,
    last_reviewed: Optional[datetime.datetime],
    interval_days: int,
) -> float:
    """Calculate decayed mastery score based on time since last review.
    
    Uses exponential decay: mastery drops when overdue for review.
    
    Args:
        current_mastery: Current mastery score (0-100)
        last_reviewed: When the topic was last reviewed
        interval_days: Expected review interval in days
    
    Returns:
        Decayed mastery score (0-100)
    """
    if last_reviewed is None or current_mastery <= 0:
        return current_mastery

    now = datetime.datetime.utcnow()
    days_since = (now - last_reviewed).total_seconds() / 86400

    if days_since <= interval_days:
        # Within review window — no decay
        return current_mastery

    # Overdue: decay proportional to how overdue
    overdue_ratio = (days_since - interval_days) / max(interval_days, 1)
    decay_factor = math.exp(-0.3 * overdue_ratio)  # gentle exponential decay

    return round(max(0, current_mastery * decay_factor), 1)


async def get_review_queue(
    db: AsyncSession,
    user_id: int,
    limit: int = 20,
) -> list[ReviewCard]:
    """Get cards due for review, ordered by urgency.
    
    Priority: most overdue first, then by lowest easiness factor.
    """
    now = datetime.datetime.utcnow()
    result = await db.execute(
        select(ReviewCard)
        .where(
            and_(
                ReviewCard.user_id == user_id,
                ReviewCard.next_review <= now,
            )
        )
        .order_by(ReviewCard.next_review.asc(), ReviewCard.easiness_factor.asc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_upcoming_reviews(
    db: AsyncSession,
    user_id: int,
    days_ahead: int = 7,
    limit: int = 50,
) -> list[ReviewCard]:
    """Get cards due within the next N days."""
    now = datetime.datetime.utcnow()
    cutoff = now + datetime.timedelta(days=days_ahead)
    result = await db.execute(
        select(ReviewCard)
        .where(
            and_(
                ReviewCard.user_id == user_id,
                ReviewCard.next_review <= cutoff,
            )
        )
        .order_by(ReviewCard.next_review.asc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_review_cards_for_topic(
    db: AsyncSession,
    user_id: int,
    topic: RoadmapTopic,
) -> list[ReviewCard]:
    """Auto-create review cards when a user starts learning a topic.
    
    Creates cards for:
    - The topic concept itself
    - Each key concept within the topic
    - Each common pattern
    """
    cards = []

    # Card for the main topic concept
    cards.append(ReviewCard(
        user_id=user_id,
        topic_id=topic.id,
        card_type="concept",
        title=topic.name,
        content={
            "category": topic.category,
            "description": topic.description or f"Core concepts of {topic.name}",
            "key_concepts": topic.key_concepts or [],
        },
    ))

    # Card for each key concept
    for concept in (topic.key_concepts or []):
        cards.append(ReviewCard(
            user_id=user_id,
            topic_id=topic.id,
            card_type="concept",
            title=f"{topic.name}: {concept}",
            content={
                "parent_topic": topic.name,
                "concept": concept,
                "category": topic.category,
            },
        ))

    # Card for each pattern
    for pattern in (topic.common_patterns or []):
        cards.append(ReviewCard(
            user_id=user_id,
            topic_id=topic.id,
            card_type="pattern",
            title=f"Pattern: {pattern}",
            content={
                "parent_topic": topic.name,
                "pattern": pattern,
                "category": topic.category,
            },
        ))

    for card in cards:
        db.add(card)
    await db.flush()
    return cards


async def apply_mastery_decay(
    db: AsyncSession,
    user_id: int,
) -> list[dict]:
    """Apply mastery decay to all topics based on review status.
    
    Returns list of topics whose mastery dropped.
    """
    # Get all topics with review cards
    result = await db.execute(
        select(ReviewCard)
        .where(ReviewCard.user_id == user_id)
        .where(ReviewCard.card_type == "concept")
    )
    cards = list(result.scalars().all())

    decayed_topics = []
    topic_ids_seen = set()

    for card in cards:
        if card.topic_id and card.topic_id not in topic_ids_seen and card.title == (card.content or {}).get("parent_topic", card.title):
            topic_ids_seen.add(card.topic_id)
            topic_result = await db.execute(
                select(RoadmapTopic).where(RoadmapTopic.id == card.topic_id)
            )
            topic = topic_result.scalar_one_or_none()
            if topic and topic.mastery_score > 0:
                old_mastery = topic.mastery_score
                new_mastery = calculate_mastery_decay(
                    old_mastery,
                    card.last_reviewed,
                    card.interval_days,
                )
                if new_mastery < old_mastery:
                    topic.mastery_score = new_mastery
                    decayed_topics.append({
                        "topic_id": topic.id,
                        "name": topic.name,
                        "old_mastery": old_mastery,
                        "new_mastery": new_mastery,
                        "drop": round(old_mastery - new_mastery, 1),
                    })

    if decayed_topics:
        await db.commit()

    return decayed_topics
